from requests import post
import os
from dotenv import load_dotenv
import time
import pymongo
from datetime import datetime

load_dotenv()

myclient = pymongo.MongoClient(os.getenv('MONGO_HOST'))
mydb = myclient["bd2-proyecto2"]
mycol = mydb["games"]

regions = ["Europe", "North America", "Australia", "New Zealand",
           "Japan", "China", "Asia", "Worldwide", "Korea", "Brazil"]

fields = 'fields name, summary, storyline, rating, rating_count, aggregated_rating, aggregated_rating_count, parent_game, release_dates, genres.name, involved_companies.company.name, involved_companies.developer, involved_companies.porting, involved_companies.publisher, involved_companies.supporting, language_supports.language.name, language_supports.language_support_type.name, themes.name, game_modes.name, player_perspectives.name, game_engines.name, franchises.name, release_dates.human, release_dates.platform.name, release_dates.region, platforms.name;'

offset = 59000
start = time.time()
while True:
    response = post('https://api.igdb.com/v4/games', **{'headers': {'Client-ID': os.getenv('CLIENT_ID'),
                                                                    'Authorization': os.getenv('AUTORIZATION')}, 'data': fields + 'limit 500; offset ' + str(offset) + ';'})

    if (response.status_code != 200):
        print("Code: ", str(response.status_code))
        print("Error: ", response.text)
        break

    res = response.json()

    if res == []:
        break

    offset += 500

    games = []

    for i in res:

        try:

            game = {}
            game["id"] = i["id"]
            game["name"] = i["name"]
            if "summary" in i:
                game["summary"] = i["summary"]
            if "storyline" in i:
                game["storyline"] = i["storyline"]
            if "rating" in i:
                game["rating"] = i["rating"]
            if "rating_count" in i:
                game["rating_count"] = i["rating_count"]
            if "aggregated_rating" in i:
                game["aggregated_rating"] = i["aggregated_rating"]
            if "aggregated_rating_count" in i:
                game["aggregated_rating_count"] = i["aggregated_rating_count"]

            if "release_dates" in i:
                releases = []
                for release_date in i["release_dates"]:
                    val = {}
                    val["human"] = release_date["human"]
                    val["region"] = regions[release_date["region"] - 1]

                    if "platform" in release_date:
                        val["platform"] = release_date["platform"]["name"]

                    releases.append(val)
                game["release_dates"] = releases

            if "genres" in i:
                game["genres"] = [j["name"] for j in i["genres"]]

            if "involved_companies" in i:
                companies = []
                for company in i["involved_companies"]:
                    val = {
                        "company": company["company"]["name"],
                        "developer": company["developer"],
                        "porting": company["porting"],
                        "publisher": company["publisher"],
                        "supporting": company["supporting"]
                    }
                    companies.append(val)
                game["involved_companies"] = companies

            if "language_supports" in i:
                language_supports = []
                for language_support in i["language_supports"]:
                    val = {
                        "language": language_support["language"]["name"],
                        "language_support_type": language_support["language_support_type"]["name"]
                    }
                    language_supports.append(val)
                game["language_supports"] = language_supports

            if "themes" in i:
                game["themes"] = [j["name"] for j in i["themes"]]

            if "game_modes" in i:
                game["game_modes"] = [j["name"] for j in i["game_modes"]]

            if "player_perspectives" in i:
                game["player_perspectives"] = [j["name"]
                                               for j in i["player_perspectives"]]

            if "game_engines" in i:
                game["game_engines"] = [j["name"] for j in i["game_engines"]]

            if "franchises" in i:
                game["franchises"] = [j["name"] for j in i["franchises"]]

            if "platforms" in i:
                game["platforms"] = [j["name"] for j in i["platforms"]]

        except Exception as e:
            print("Error: ", e)
            continue

        games.append(game)

    mycol.insert_many(games, ordered=False)

    print(".", end="")

print("")

end = time.time()
print('Elapsed Time: ' + str(end - start) + 's')
print("-----------------------------------")
