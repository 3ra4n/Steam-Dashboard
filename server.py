from flask import Flask, jsonify
import requests

app = Flask(__name__)
API_KEY = "793CA27CC1CFCB2898B7EC8686C5AED7"

@app.route("/api/stats/<steam_id>")
def get_stats(steam_id):
    games_url = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/"
    games_params = {
        "key": API_KEY,
        "steamid": steam_id,
        "include_appinfo": True,
        "format": "json",
    }
    games_response = requests.get(games_url, params=games_params)
    games_data = games_response.json()
    games_raw = games_data.get("response", {}).get("games", [])

    games = []
    for g in games_raw:
        minutes = g.get("playtime_forever", 0)
        hours = round(minutes / 60, 1)
        games.append({
            "appid": g.get("appid"),
            "name": g.get("name", "Unknown Game"),
            "playtime_hours": hours,
        })
    games.sort(key=lambda x: x["playtime_hours"], reverse=True)

    # Player summary
    summary_url =  "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/"
    summary_params = {
        "key": API_KEY,
        "steamids": steam_id,
        "format": "json",
    }
    summary_response = requests.get(summary_url, params=summary_params)
    summary_data = summary_response.json()
    players = summary_data["response"].get("players", [])

    if not players:
        return jsonify({"error": "Player not found"}), 404

    player = players[0]

    #response data
    result = {
        "player": {
            "name": player.get("personaname", "Unknown"),
            "avatar": player.get("avatarfull", ""),
        },
        "top_games": games[:10],  # Return top 10 games
    }
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, port=5000)