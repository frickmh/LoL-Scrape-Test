#Match numbers starting at: 2536802224
#Matches go to at least: 2541354219

#Test URL: https://na1.api.riotgames.com/lol/match/v3/matches/2536802224?api_key=RGAPI-adfe4a14-d491-4f12-a50f-833c09b1c138

#Production Key:  55b49f8b-52e1-4cbc-b7cf-d30a054b7833

#Rate Limit: 3k/10s, 180k/600s

#Test 2 URL: https://na1.api.riotgames.com/lol/match/v3/matches/2536802224?api_key=55b49f8b-52e1-4cbc-b7cf-d30a054b7833

import scrapy
import json

class QuotesSpider(scrapy.Spider):
    name = "getMatches"

    print("INSTANTIATED!")

    def start_requests(self):
        match = 2536802224 + 150000

        print("STARTED!")

        #200 games = 400 kB, .5 min
		#1000 games = 2 mB, 1.25 min
        for i in range(0, 100000):
            url = "https://na1.api.riotgames.com/lol/match/v3/matches/" + str(match + i) + "?api_key=55b49f8b-52e1-4cbc-b7cf-d30a054b7833"

            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        print("PARSING!")
        #page = response.url.split("/")[-2]


        body = json.loads(response.body)
        queueId = body["queueId"] #Has to be 420

        if int(queueId) == 420:

            platCount = 0

            for j in range(0, 9):
                tier = body["participants"][j]["highestAchievedSeasonTier"]
                if tier == "PLATINUM" or tier == "DIAMOND" or tier == "MASTER" or tier == "CHALLENGER":
                    platCount += 1

            if platCount <= 3:
                return

            gameId = body["gameId"]

            filename = 'match-%s.json' % gameId
            with open(filename, 'wb') as f:
                f.write(response.body)
                f.flush()
                f.close()
                self.log('Saved file %s' % filename)