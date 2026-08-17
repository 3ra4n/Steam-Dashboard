import requests

API_KEY = "793CA27CC1CFCB2898B7EC8686C5AED7"
STEAM_ID = "76561198851289104"

url = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/"
params = {
    "key": API_KEY,
    "steamid": STEAM_ID,
    "include_appinfo": True,
    "format": "json",
}

response = requests.get(url, params=params)
data = response.json()

# list of games is nested inside data ["response"]["games"]
games_raw = data["response"]["games"]

games = []
for g in games_raw:
    minutes = g.get("playtime_forever", 0)
    hours = round(minutes / 60, 1)
    games.append({
        "appid": g.get("appid"),
        "name": g.get("name", "Unknown Game"),
        "playtime_hours": hours,
    })

# Sort games by playtime in descending order
games_sorted = sorted(games, key=lambda x: x["playtime_hours"], reverse=True)
top_games = games_sorted[:10]

# Print the top 10 games with their playtime
print("Top 10 Games by Playtime:")
for game in top_games:
    print(f"{game['name']}: {game['playtime_hours']} hours")

# Player summary username and avatar
url_summary = "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/"
params_summary = {
    "key": API_KEY,
    "steamids": STEAM_ID,
    "format": "json",
}
summary_response = requests.get(url_summary, params=params_summary)
summary_data = summary_response.json()
player_info = summary_data["response"]["players"][0]

# Print player summary information
print("\nPlayer Summary:")
print(f"Username: {player_info.get('personaname', 'Unknown')}")
print(f"Avatar URL: {player_info.get('avatarfull', 'No Avatar')}")

# Recently played games (last 2 weeks)
url_recent = "https://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/"
params_recent = {
    "key": API_KEY,
    "steamid": STEAM_ID,
    "format": "json",
}
recent_response = requests.get(url_recent, params=params_recent)
recent_data = recent_response.json()
recent_games_raw = recent_data.get("response", {}).get("games", [])

recent_games = []
for g in recent_games_raw:
    minutes = g.get("playtime_2weeks", 0)
    hours = round(minutes / 60, 1)
    recent_games.append({
        "appid": g.get("appid"),
        "name": g.get("name", "Unknown Game"),
        "playtime_hours": hours,
    })

# Print recently played games
print("\nRecently Played Games (Last 2 Weeks):")
if recent_games:
    for game in recent_games:
        print(f"{game['name']}: {game['playtime_hours']} hours")
else:
    print("No games played in the last 2 weeks.")

# --- Build a simple HTML file ---
html = f"""
<!DOCTYPE html>
<html>
<head>
<title>{player_info['personaname']}'s Steam Stats</title>
<link rel="stylesheet" type="text/css" href="style.css">
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{player_info['personaname']}'s Steam Dashboard</h1>
            <img src="{player_info['avatarfull']}" width="80">
        </div>

        <h2>Top 10 Games by Playtime</h2>
        <ul class="top-games">
"""

for g in top_games:
        html += f"      <li class=\"game-item\">{g['name']} — {g['playtime_hours']} hrs</li>\n"

html += """
    </ul>

    <h2>Recently Played (Last 2 Weeks)</h2>
  <ul class="recent-games">
"""

if recent_games:
    for game in recent_games:
        html+= f"<li class=\"game-item\">{game['name']} — {game['playtime_hours']} hrs</li>\n"
else:
    html+= "<li class=\"game-item\">Nothing played recently.</li>\n"

html += """
  </ul>
</body>
</html>
"""

with open("steam_dashboard.html", "w", encoding="utf-8") as f:
    f.write(html)

print("\nDashboard written to steam_dashboard.html")