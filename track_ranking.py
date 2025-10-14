#!/usr/bin/env python3
"""
Spotify Podcast Chart Tracker
Captures daily screenshots and tracks podcast rankings using AI vision analysis.
"""

import os
import csv
import json
from datetime import datetime
from pathlib import Path
import base64
import anthropic
from playwright.sync_api import sync_playwright
from PIL import Image


# Configuration
SPOTIFY_CHARTS_URL = "https://podcastcharts.byspotify.com/"
PODCAST_NAME = "Dwarkesh Podcast"
SCREENSHOTS_DIR = Path("screenshots")
RANKINGS_FILE = Path("rankings.csv")
REPORT_FILE = Path("RANKING_REPORT.md")


def ensure_directories():
    """Create necessary directories if they don't exist."""
    SCREENSHOTS_DIR.mkdir(exist_ok=True)


def capture_chart_screenshot():
    """
    Capture a full screenshot of the Spotify podcast charts page.
    Scrolls down to ensure podcasts ranked below 10 are visible.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = SCREENSHOTS_DIR / f"chart_{timestamp}.png"
    
    print(f"🌐 Opening {SPOTIFY_CHARTS_URL}...")
    
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=True)
        # Use a taller viewport to capture more content without needing full_page
        context = browser.new_context(
            viewport={'width': 1920, 'height': 4000},  # Tall viewport to capture more rankings
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        )
        page = context.new_page()
        
        # Navigate to the page
        page.goto(SPOTIFY_CHARTS_URL, wait_until="networkidle", timeout=60000)
        
        # Wait for content to load
        page.wait_for_selector('img[alt*="Experience"], img[alt*="podcast"], img[alt*="Podcast"]', timeout=30000)
        
        # Close any cookie banners or popups
        try:
            # Try to close the banner that appears
            close_btn = page.locator('.close-btn, button[aria-label*="close" i], button[aria-label*="Close" i]').first
            if close_btn.is_visible(timeout=2000):
                close_btn.click()
                page.wait_for_timeout(1000)
        except:
            pass
        
        # Scroll to top first to include header
        print("📜 Positioning for screenshot...")
        page.evaluate("window.scrollTo(0, 0)")
        page.wait_for_timeout(1500)
        
        # Scroll down just a tiny bit to get more podcasts while keeping "United States" and "Top Podcasts" header visible
        page.evaluate("window.scrollTo(0, 150)")
        page.wait_for_timeout(1000)
        
        # Move mouse to hover over Dwarkesh Podcast (rank 16)
        # This creates a nice highlight effect for your podcast
        try:
            print("🎯 Highlighting your podcast...")
            # Find the Dwarkesh Podcast element and hover over it
            dwarkesh_element = page.locator('text="Dwarkesh Podcast"').first
            if dwarkesh_element.is_visible(timeout=2000):
                dwarkesh_element.hover()
                page.wait_for_timeout(500)
        except:
            # If we can't find it, move mouse far away to avoid any hover effects
            page.mouse.move(0, 0)
        
        # Take viewport screenshot (not full page - this will be higher quality)
        print(f"📸 Capturing screenshot...")
        page.screenshot(path=str(screenshot_path), full_page=False)
        
        browser.close()
    
    print(f"✅ Screenshot saved: {screenshot_path}")
    return screenshot_path


def resize_image_if_needed(image_path, max_dimension=7000):
    """
    Resize image if any dimension exceeds max_dimension while maintaining aspect ratio.
    Claude has a limit of 8000px per dimension, so we use 7000 to be safe.
    """
    img = Image.open(image_path)
    width, height = img.size
    
    # Check if resizing is needed
    if width <= max_dimension and height <= max_dimension:
        return image_path
    
    # Calculate new dimensions
    if width > height:
        new_width = max_dimension
        new_height = int((max_dimension / width) * height)
    else:
        new_height = max_dimension
        new_width = int((max_dimension / height) * width)
    
    # Resize image
    resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    # Save resized image (overwrite the original)
    resized_img.save(image_path, optimize=True, quality=95)
    print(f"📐 Resized image from {width}x{height} to {new_width}x{new_height}")
    
    return image_path


def analyze_ranking_with_claude(screenshot_path):
    """
    Use Claude Vision API to analyze the screenshot and extract the podcast ranking.
    """
    print(f"🤖 Analyzing screenshot with Claude Vision API...")
    
    # Get API key from environment
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set!")
    
    # Resize image if needed (Claude has 8000px limit per dimension)
    screenshot_path = resize_image_if_needed(screenshot_path)
    
    # Read and encode the screenshot
    with open(screenshot_path, "rb") as image_file:
        image_data = base64.standard_b64encode(image_file.read()).decode("utf-8")
    
    # Create Claude client
    client = anthropic.Anthropic(api_key=api_key)
    
    # Construct the prompt
    prompt = f"""Look at this Spotify podcast chart screenshot and find the ranking for "{PODCAST_NAME}".

IMPORTANT: The podcast name might appear as variations like:
- "Dwarkesh Podcast"
- "Dwarkesh Patel"  
- "The Dwarkesh Podcast"
- Or just "Dwarkesh" in the title

Please analyze the image and respond with ONLY a JSON object in this exact format:
{{
    "ranking": <number or null if not found>,
    "found": <true or false>,
    "podcast_title": "<exact name as shown on chart>",
    "notes": "<brief note about the ranking or why it wasn't found>"
}}

Search carefully through all visible podcast names. Look at BOTH the podcast title and the author/host name. The podcast might be anywhere from rank 1 to 100 or beyond."""

    # Call Claude Vision API
    message = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": image_data,
                        },
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ],
            }
        ],
    )
    
    # Parse the response
    response_text = message.content[0].text.strip()
    print(f"📊 Claude response: {response_text}")
    
    # Extract JSON from response (handle potential markdown code blocks)
    if "```json" in response_text:
        response_text = response_text.split("```json")[1].split("```")[0].strip()
    elif "```" in response_text:
        response_text = response_text.split("```")[1].split("```")[0].strip()
    
    result = json.loads(response_text)
    
    return result


def save_ranking(ranking_data, screenshot_path):
    """
    Save the ranking data to CSV file.
    """
    timestamp = datetime.now()
    
    # Check if file exists to determine if we need headers
    file_exists = RANKINGS_FILE.exists()
    
    # Prepare the row
    row = {
        'date': timestamp.strftime("%Y-%m-%d"),
        'timestamp': timestamp.isoformat(),
        'ranking': ranking_data.get('ranking', 'N/A'),
        'found': ranking_data.get('found', False),
        'notes': ranking_data.get('notes', ''),
        'screenshot': str(screenshot_path)
    }
    
    # Write to CSV
    with open(RANKINGS_FILE, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['date', 'timestamp', 'ranking', 'found', 'notes', 'screenshot'])
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)
    
    print(f"💾 Ranking saved to {RANKINGS_FILE}")


def generate_report():
    """
    Generate a markdown report with ranking trends.
    """
    if not RANKINGS_FILE.exists():
        print("⚠️  No rankings data found yet.")
        return
    
    # Read all rankings
    rankings = []
    with open(RANKINGS_FILE, 'r') as f:
        reader = csv.DictReader(f)
        rankings = list(reader)
    
    if not rankings:
        return
    
    # Get latest ranking
    latest = rankings[-1]
    
    # Calculate trend
    trend_emoji = "📊"
    trend_text = "First recording"
    
    if len(rankings) >= 2:
        previous = rankings[-2]
        try:
            current_rank = int(latest['ranking']) if latest['ranking'] != 'N/A' else None
            prev_rank = int(previous['ranking']) if previous['ranking'] != 'N/A' else None
            
            if current_rank and prev_rank:
                diff = prev_rank - current_rank
                if diff > 0:
                    trend_emoji = "🚀"
                    trend_text = f"Up {diff} position{'s' if diff > 1 else ''}"
                elif diff < 0:
                    trend_emoji = "📉"
                    trend_text = f"Down {abs(diff)} position{'s' if abs(diff) > 1 else ''}"
                else:
                    trend_emoji = "➡️"
                    trend_text = "No change"
        except (ValueError, TypeError):
            pass
    
    # Generate report
    report = f"""# 🎙️ Dwarkesh Podcast - Spotify Chart Rankings

## Latest Update
- **Date**: {latest['date']}
- **Ranking**: #{latest['ranking']} {trend_emoji}
- **Trend**: {trend_text}
- **Status**: {"✅ Found on charts" if latest['found'] == 'True' else "❌ Not found on charts"}

## Recent History (Last 10 Days)

| Date | Ranking | Change | Notes |
|------|---------|--------|-------|
"""
    
    # Add last 10 entries
    recent = rankings[-10:] if len(rankings) >= 10 else rankings
    recent.reverse()
    
    for i, entry in enumerate(recent):
        rank_display = f"#{entry['ranking']}" if entry['ranking'] != 'N/A' else "Not Found"
        
        # Calculate change from previous
        change = "-"
        if i < len(recent) - 1:
            try:
                curr = int(entry['ranking']) if entry['ranking'] != 'N/A' else None
                prev = int(recent[i+1]['ranking']) if recent[i+1]['ranking'] != 'N/A' else None
                if curr and prev:
                    diff = prev - curr
                    if diff > 0:
                        change = f"🚀 +{diff}"
                    elif diff < 0:
                        change = f"📉 {diff}"
                    else:
                        change = "➡️ 0"
            except (ValueError, TypeError):
                pass
        
        report += f"| {entry['date']} | {rank_display} | {change} | {entry['notes'][:50]} |\n"
    
    # Add statistics
    found_rankings = [int(r['ranking']) for r in rankings if r['ranking'] != 'N/A' and r['found'] == 'True']
    
    if found_rankings:
        report += f"""
## 📈 Statistics
- **Best Ranking**: #{min(found_rankings)}
- **Current Ranking**: #{latest['ranking']}
- **Average Ranking**: #{sum(found_rankings) / len(found_rankings):.1f}
- **Total Tracking Days**: {len(rankings)}
- **Days on Charts**: {len(found_rankings)}

## 📸 Latest Screenshot
![Latest Chart]({latest['screenshot']})
"""
    
    report += f"""
---
*Last updated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")}*
*Tracking powered by Claude Vision API & Playwright*
"""
    
    # Write report
    with open(REPORT_FILE, 'w') as f:
        f.write(report)
    
    print(f"📋 Report generated: {REPORT_FILE}")
    
    # Also print to console
    print("\n" + "="*60)
    print(report)
    print("="*60 + "\n")


def main():
    """Main execution function."""
    print("🎙️  Spotify Podcast Chart Tracker")
    print("="*60)
    
    try:
        # Ensure directories exist
        ensure_directories()
        
        # Capture screenshot
        screenshot_path = capture_chart_screenshot()
        
        # Analyze with Claude
        ranking_data = analyze_ranking_with_claude(screenshot_path)
        
        # Display result
        if ranking_data['found']:
            print(f"\n🎉 SUCCESS! {PODCAST_NAME} is ranked #{ranking_data['ranking']}")
            print(f"📝 Notes: {ranking_data['notes']}")
        else:
            print(f"\n❌ {PODCAST_NAME} was not found in the charts")
            print(f"📝 Notes: {ranking_data['notes']}")
        
        # Save to CSV
        save_ranking(ranking_data, screenshot_path)
        
        # Generate report
        generate_report()
        
        print("\n✅ Tracking complete!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        raise


if __name__ == "__main__":
    main()

