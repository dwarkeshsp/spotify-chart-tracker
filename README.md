# 🎙️ Spotify Podcast Chart Tracker

Automated daily tracking of the **Dwarkesh Podcast** ranking on [Spotify Podcast Charts](https://podcastcharts.byspotify.com/) using AI-powered screenshot analysis.

## 🌟 Features

- 📸 **Daily Screenshots**: Automatically captures full-page screenshots of Spotify podcast charts
- 🤖 **AI-Powered Analysis**: Uses Claude Vision API to intelligently extract your podcast's ranking
- 📊 **Trend Tracking**: Maintains historical data in CSV format with automatic trend analysis
- 📈 **Beautiful Reports**: Generates markdown reports showing ranking trends, statistics, and changes
- ☁️ **GitHub Actions**: Runs automatically in the cloud every day (no need to keep your computer on!)
- 🎯 **Smart Scrolling**: Captures rankings beyond the top 10 by automatically scrolling

## 🚀 Quick Start

### Option 1: GitHub Actions (Recommended)

**Best for:** Set-it-and-forget-it automated tracking

1. **Fork/Clone this repository**
   ```bash
   git clone https://github.com/yourusername/spotify-chart-tracker.git
   cd spotify-chart-tracker
   ```

2. **Get your Anthropic API Key**
   - Go to [https://console.anthropic.com/](https://console.anthropic.com/)
   - Sign up or log in
   - Create a new API key
   - Copy the key (starts with `sk-ant-...`)

3. **Add API Key to GitHub Secrets**
   - Go to your repository on GitHub
   - Click **Settings** → **Secrets and variables** → **Actions**
   - Click **New repository secret**
   - Name: `ANTHROPIC_API_KEY`
   - Value: Your API key
   - Click **Add secret**

4. **Enable GitHub Actions**
   - Go to **Actions** tab in your repository
   - If prompted, enable workflows
   - The tracker will run automatically every day at 10:00 AM UTC

5. **Run Manually (Optional)**
   - Go to **Actions** tab
   - Click **Daily Podcast Ranking Tracker**
   - Click **Run workflow** → **Run workflow**
   - Wait ~1 minute for completion
   - Check the `RANKING_REPORT.md` file in your repo!

### Option 2: Local Testing

**Best for:** Testing before deploying or occasional manual checks

1. **Clone and setup**
   ```bash
   git clone https://github.com/yourusername/spotify-chart-tracker.git
   cd spotify-chart-tracker
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```

4. **Set up environment variable**
   ```bash
   export ANTHROPIC_API_KEY="your_api_key_here"
   ```

5. **Run the tracker**
   ```bash
   python track_ranking.py
   ```

6. **View results**
   - Check `RANKING_REPORT.md` for your ranking report
   - Check `rankings.csv` for historical data
   - Check `screenshots/` folder for captured images

## 📂 Project Structure

```
spotify-chart-tracker/
├── track_ranking.py           # Main tracking script
├── requirements.txt           # Python dependencies
├── rankings.csv              # Historical ranking data (auto-generated)
├── RANKING_REPORT.md         # Latest report (auto-generated)
├── screenshots/              # Screenshot archive (auto-generated)
│   └── chart_YYYYMMDD_HHMMSS.png
├── .github/
│   └── workflows/
│       └── daily-tracker.yml # GitHub Actions workflow
└── README.md                 # This file
```

## 📊 Understanding the Output

### rankings.csv
Tracks every check with the following columns:
- `date`: Date of the check (YYYY-MM-DD)
- `timestamp`: Full timestamp (ISO format)
- `ranking`: Your podcast's ranking number (or N/A if not found)
- `found`: Whether the podcast was found on the charts
- `notes`: AI's notes about the ranking
- `screenshot`: Path to the screenshot file

### RANKING_REPORT.md
Beautiful markdown report showing:
- 🎯 **Latest ranking** and trend direction
- 📈 **Recent history** (last 10 days) with change indicators
- 📊 **Statistics** (best ranking, average, days on charts)
- 📸 **Screenshot** of the latest chart

Example:
```markdown
# 🎙️ Dwarkesh Podcast - Spotify Chart Rankings

## Latest Update
- **Date**: 2025-10-14
- **Ranking**: #16 🚀
- **Trend**: Up 2 positions
- **Status**: ✅ Found on charts
```

## ⚙️ Configuration

### Change Tracking Time
Edit `.github/workflows/daily-tracker.yml`:
```yaml
schedule:
  - cron: '0 10 * * *'  # 10:00 AM UTC
  # Change to '0 14 * * *' for 2:00 PM UTC, etc.
```

### Change Podcast Name
Edit `track_ranking.py`:
```python
PODCAST_NAME = "Dwarkesh Podcast"  # Change to your podcast name
```

### Change Screenshot Settings
Edit the viewport size or scrolling in `track_ranking.py`:
```python
viewport={'width': 1920, 'height': 1080}  # Adjust resolution
page.evaluate("window.scrollTo(0, 1200)")  # Adjust scroll depth
```

## 🔧 Troubleshooting

### "ANTHROPIC_API_KEY not set"
- **GitHub Actions**: Ensure you added the secret correctly in repository settings
- **Local**: Run `export ANTHROPIC_API_KEY="your_key"` before running the script

### "Podcast not found"
- Your podcast might not be in the top 20 on that day
- Try adjusting the scroll depth in `track_ranking.py` to capture more rankings
- Check the screenshot in `screenshots/` to verify what was captured

### GitHub Actions failing
- Check the **Actions** tab for error logs
- Ensure your API key is valid and has credits
- Try running manually first using **Run workflow** button

### Screenshots too small
Increase the scroll depth:
```python
page.evaluate("window.scrollTo(0, 2000)")  # Scroll more
```

## 💰 Cost Estimation

### Anthropic API Costs
- Claude 3.5 Sonnet: ~$0.003 per image analysis
- **Daily**: $0.003/day = $0.09/month
- **Yearly**: ~$1.10/year

### GitHub Actions
- **FREE** (2000 minutes/month free tier)
- This workflow uses ~2-3 minutes/day = 60-90 minutes/month
- Well within free tier limits!

**Total Cost**: ~$0.09/month or ~$1/year 🎉

## 🎯 Advanced Usage

### Run multiple times per day
Modify the cron schedule to run multiple times:
```yaml
schedule:
  - cron: '0 10 * * *'  # 10 AM UTC
  - cron: '0 18 * * *'  # 6 PM UTC
```

### Track multiple podcasts
Create separate tracking scripts or modify the main script to loop through multiple podcast names.

### Export to Google Sheets / Airtable
Add a step in the GitHub Action to push data to external services using their APIs.

### Visualize with Python
Create a plotting script:
```python
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('rankings.csv')
df['ranking'] = pd.to_numeric(df['ranking'], errors='coerce')
plt.plot(df['date'], df['ranking'])
plt.gca().invert_yaxis()  # Lower ranking = better
plt.savefig('trend.png')
```

## 🤝 Contributing

Found a bug or have an improvement? Feel free to:
1. Open an issue
2. Submit a pull request
3. Share your feedback

## 📝 License

MIT License - feel free to use and modify for your own podcast tracking!

## 🙏 Acknowledgments

- **Playwright** for browser automation
- **Claude AI** by Anthropic for intelligent image analysis
- **GitHub Actions** for free cloud automation
- **Spotify Charts** for podcast rankings data

---

## 📞 Support

If you have questions or need help:
1. Check the **Troubleshooting** section above
2. Review the **Actions** tab logs on GitHub
3. Open an issue in this repository

**Happy Tracking! 🎉**

---

*Made with ❤️ for podcast creators who want to track their growth*

