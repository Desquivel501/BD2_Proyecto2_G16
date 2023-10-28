from requests import post
import os
from dotenv import load_dotenv
import time
import pymongo
from datetime import datetime

load_dotenv()

myclient = pymongo.MongoClient(os.getenv('MONGO_HOST'))
mydb = myclient["bd2-proyecto2"]
mycol = mydb["platforms"]


regions = ["Europe", "North America", "Australia", "New Zealand",
           "Japan", "China", "Asia", "Worldwide", "Korea", "Brazil"]

category = ["console", "arcade", "platform",
            "operating_system", "portable_console", "computer"]

fields = 'fields name, alternative_name, abbreviation, category, generation, platform_family.name, summary, versions.name, versions.main_manufacturer.company, versions.platform_version_release_dates.human, versions.platform_version_release_dates.region;'


offset = 0
start = time.time()
while True:
    response = post('https://api.igdb.com/v4/platforms', **{'headers': {'Client-ID': os.getenv('CLIENT_ID'),
                                                                        'Authorization': os.getenv('AUTORIZATION')}, 'data': fields + 'limit 500; offset ' + str(offset) + ';'})

    if (response.status_code != 200):
        print("Code: ", str(response.status_code))
        print("Error: ", response.text)
        break

    res = response.json()

    if res == []:
        break

    offset += 500

    platforms = []

    for i in res:

        try:

            platform = {}
            platform["id"] = i["id"]
            platform["name"] = i["name"]

            if "alternative_name" in i:
                platform["alternative_name"] = i["alternative_name"]

            if "abbreviation" in i:
                platform["abbreviation"] = i["abbreviation"]

            if "category" in i:
                platform["category"] = category[i["category"] - 1]

            if "generation" in i:
                platform["generation"] = i["generation"]

            if "platform_family" in i:
                platform["platform_family"] = i["platform_family"]["name"]

            if "summary" in i:
                platform["summary"] = i["summary"]

            if "versions" in i:
                platform["versions"] = []
                for j in i["versions"]:
                    version = {}
                    version["name"] = j["name"]

                    if "main_manufacturer" in j:
                        version["manufacturer"] = j["main_manufacturer"]["company"]

                    if "platform_version_release_dates" in j:
                        version["release_dates"] = []
                        for k in j["platform_version_release_dates"]:
                            release_date = {}
                            release_date["human"] = k["human"]
                            release_date["region"] = regions[k["region"] - 1]
                            version["release_dates"].append(release_date)

                    platform["versions"].append(version)

            games = []

            offset2 = 0
            while True:

                response_games = post('https://api.igdb.com/v4/games', **{'headers': {'Client-ID': os.getenv('CLIENT_ID'),
                                                                                      'Authorization': os.getenv('AUTORIZATION')}, 'data': 'fields name; where platforms = ' + str(i["id"]) + ';' + 'limit 500; offset ' + str(offset2) + ';'})

                if (response_games.status_code != 200):
                    print("Code: ", str(response_games.status_code))
                    print("Error: ", response_games.text)
                    break

                res_games = response_games.json()

                if res_games == []:
                    break

                offset2 += 500

                for j in res_games:
                    games.append(j["name"])

                print("-", end="")

            platform["games"] = games
            print(".", end="")

        except Exception as e:
            print("Error: ", e)
            continue

        platforms.append(platform)

    mycol.insert_many(platforms, ordered=False)
    print("")


print("")

end = time.time()
print('Elapsed Time: ' + str(end - start) + 's')
print("-----------------------------------")
