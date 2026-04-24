import requests

USERNAME = "just-aldrin"

try:
    url = f"https://github-contributions-api.jogruber.de/v4/{USERNAME}"
    data = requests.get(url, timeout=10).json()

    weeks = data["contributions"]

    days = []
    for week in weeks:
        days.extend(week["contributionDays"])

    total = sum(day["contributionCount"] for day in days)

    # fallback simple values (prevents crashes)
    current_streak = 0
    longest_streak = 0

except Exception as e:
    print("Error fetching data:", e)
    total = 0
    current_streak = 0
    longest_streak = 0

content = f"""
<div align="center">

### 📈 Contribution Highlights

<img src="https://img.shields.io/badge/Total%20Contributions-{total}-ff69b4?style=for-the-badge&labelColor=0d1117" />
<img src="https://img.shields.io/badge/Current%20Streak-{current_streak}%20days-ff1493?style=for-the-badge&labelColor=0d1117" />
<img src="https://img.shields.io/badge/Longest%20Streak-{longest_streak}%20days-ff69b4?style=for-the-badge&labelColor=0d1117" />

</div>
"""

with open("README.md", "r") as f:
    readme = f.read()

start = "<!--START_SECTION:stats-->"
end = "<!--END_SECTION:stats-->"

if start in readme and end in readme:
    new_readme = readme.split(start)[0] + start + content + end + readme.split(end)[1]

    with open("README.md", "w") as f:
        f.write(new_readme)
else:
    print("Markers not found in README")