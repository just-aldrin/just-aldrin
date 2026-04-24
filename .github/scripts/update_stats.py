import requests
from datetime import datetime, timedelta

USERNAME = "YOUR_USERNAME"

# Get contribution data
url = f"https://github-contributions-api.jogruber.de/v4/{USERNAME}"
data = requests.get(url).json()

weeks = data["contributions"]

# Flatten contributions
days = []
for week in weeks:
    days.extend(week["contributionDays"])

# Sort by date
days.sort(key=lambda x: x["date"])

# Calculate total contributions
total = sum(day["contributionCount"] for day in days)

# Calculate streaks
current_streak = 0
longest_streak = 0
temp_streak = 0

today = datetime.utcnow().date()

for day in reversed(days):
    date = datetime.strptime(day["date"], "%Y-%m-%d").date()
    if day["contributionCount"] > 0:
        temp_streak += 1
        if (today - date).days <= temp_streak:
            current_streak = temp_streak
    else:
        temp_streak = 0
    longest_streak = max(longest_streak, temp_streak)

# Generate badge section
content = f"""
<div align="center">

### 📈 Contribution Highlights

<img src="https://img.shields.io/badge/Total%20Contributions-{total}-ff69b4?style=for-the-badge&labelColor=0d1117" />
<img src="https://img.shields.io/badge/Current%20Streak-{current_streak}%20days-ff1493?style=for-the-badge&labelColor=0d1117" />
<img src="https://img.shields.io/badge/Longest%20Streak-{longest_streak}%20days-ff69b4?style=for-the-badge&labelColor=0d1117" />

</div>
"""

# Replace in README
with open("README.md", "r") as f:
    readme = f.read()

start = "<!--START_SECTION:stats-->"
end = "<!--END_SECTION:stats-->"

new_readme = readme.split(start)[0] + start + content + end + readme.split(end)[1]

with open("README.md", "w") as f:
    f.write(new_readme)
