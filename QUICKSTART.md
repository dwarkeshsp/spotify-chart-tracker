# 🚀 Quick Start Guide

## For GitHub Actions (5 minutes)

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Spotify podcast tracker"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/spotify-chart-tracker.git
   git push -u origin main
   ```

2. **Get Anthropic API Key**
   - Visit: https://console.anthropic.com/
   - Sign up/Login → API Keys → Create Key
   - Copy the key (starts with `sk-ant-`)

3. **Add to GitHub Secrets**
   - Go to: `Settings` → `Secrets and variables` → `Actions`
   - Click: `New repository secret`
   - Name: `ANTHROPIC_API_KEY`
   - Value: Paste your key
   - Save

4. **Test it!**
   - Go to `Actions` tab
   - Click `Daily Podcast Ranking Tracker`
   - Click `Run workflow` → `Run workflow`
   - Wait ~1 minute
   - Refresh the repo to see `RANKING_REPORT.md`!

✅ **Done!** It will now run automatically every day at 10 AM UTC.

---

## For Local Testing (5 minutes)

1. **Setup**
   ```bash
   ./setup.sh
   ```

2. **Set API Key**
   ```bash
   export ANTHROPIC_API_KEY="your_key_here"
   ```

3. **Run**
   ```bash
   source venv/bin/activate
   python track_ranking.py
   ```

4. **Check Results**
   - `RANKING_REPORT.md` - Your ranking report
   - `rankings.csv` - Historical data
   - `screenshots/` - Chart screenshots

---

## What Happens Daily?

1. 🌐 Opens Spotify podcast charts
2. 📸 Takes a full-page screenshot
3. 🤖 Analyzes with Claude AI to find your ranking
4. 💾 Saves to `rankings.csv`
5. 📊 Generates `RANKING_REPORT.md`
6. 🚀 Commits results back to GitHub

---

## Viewing Your Stats

**On GitHub:**
- Click `RANKING_REPORT.md` to see your latest ranking and trends

**Locally:**
- Open `RANKING_REPORT.md` in any markdown viewer
- Or: `cat RANKING_REPORT.md`

---

## Need Help?

Check the full `README.md` for troubleshooting and advanced options!

