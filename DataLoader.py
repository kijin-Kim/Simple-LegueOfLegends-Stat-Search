import requests

class DataLoader:
    def __init__(self):
        self.api_key = API_KEY
        self.region = "kr"
        self.url_substr = "https://" + self.region +".api.riotgames.com"
        self.api_substr = "?api_key=" + self.api_key

    def get_summoner_data(self, summoner_name):
        return self.response_data("/lol/summoner/v4/summoners/by-name/", summoner_name)

    def get_summoner_league(self, encrypted_id):
        return self.response_data("/lol/league/v4/entries/by-summoner/", encrypted_id)

    def get_summoner_match(self, encrypted_accountId):
        return self.response_data("/lol/match/v4/matchlists/by-account/", encrypted_accountId)

    def get_match_information(self, matchId):
        return self.response_data("/lol/match/v4/matches/", matchId)

    def get_champion_rotation(self):
        return self.response_data("/lol/platform/v3/champion-rotations", "")

    def get_current_game_information(self, encrypted_id):
        return self.response_data("/lol/spectator/v4/active-games/by-summoner/", encrypted_id)

    def response_data(self, url_string, input_parameter):
        url = self.url_substr + url_string + input_parameter + self.api_substr
        response = requests.get(url)
        return response.json()

