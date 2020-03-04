import requests
from datetime import datetime

def DateToTimestampStr(dateStr):
    '''Converts string dates to ms timestamp'''
    return str(int( datetime.timestamp( datetime.strptime(dateStr, '%Y-%m-%d') )*1000) )

def GetDictResponse(URL):
        return requests.get(URL).json()




class LOL_API_Connection():
    '''
    Sending requests to the LOL API
    '''
    def __init__(self, api_key, region = 'eun1'):
        self.api_key = api_key
        self.region = region
    
    def api_key_to_url(self, filters = ''):
        if filters == '':
            return '?api_key={}'.format(self.api_key )
        else:
            return 'api_key={}'.format(self.api_key )

    @property
    def url_league_detail(self):
        return 'https://' + self.region + '.api.riotgames.com/lol/league/v4/entries/'

    @property
    def url_summoner_by_name(self):
        return 'https://' + self.region + '.api.riotgames.com/lol/summoner/v4/summoners/by-name/'
    
    @property
    def url_summoner_matchlist(self):
        return 'https://' + self.region + '.api.riotgames.com/lol/match/v4/matchlists/by-account/'

    @property
    def url_match_details(self):
        return 'https://' + self.region + '.api.riotgames.com/lol/match/v4/matches/'
    
    
    def GetSummonerNames(self, division, tier, queue = 'RANKED_SOLO_5x5'):
        URL = self.url_league_detail + '/'.join((queue, tier, division)) + self.api_key_to_url()
        return GetDictResponse(URL)
    
    def GetSummonerID(self, summoner_name):
        URL = self.url_summoner_by_name + summoner_name + self.api_key_to_url()
        response = requests.get(URL)
        return response.json()

    def GetMatchHist_full(self, SummonerID, **FilterItems):
        '''Returns list of matches as a list. Filters:
            - queue: ID for the kind of match
            - season: ID for the season
            - beginTime date format as string: %Y-%m-%d'''
        filters = ''
        for filterType, value in FilterItems.items():
            if filterType == 'beginTime':
                filters += filterType + '=' + DateToTimestampStr(value) + '&'
            else:
                filters += filterType + '=' + str(value) + '&'
        if filters != '':
            filters = '?' + filters
            
        URL = self.url_summoner_matchlist + SummonerID + filters +  self.api_key_to_url(filters = filters)
        response = requests.get(URL)        
        try:
            if 'matches' in response.json().keys():
                return response.json()['matches']
            else:
                return response.json()
        except: 
            return {'status': {'status_code' :  response.status_code} }

    def GetMatchHist_gameid(self, SummonerID = None, **FilterItems):
        '''Returns the gameIDs for the given summoner name in the class'''
        matchlist = self.GetMatchHist_full(SummonerID, **FilterItems)
        return [matchlist[i]['gameId'] for i in range(len(matchlist))]
        
    def GetMatchDetails(self, gameID):
        URL = self.url_match_details + str(gameID) + self.api_key_to_url(filters = '')
        response = requests.get(URL)
        return response.json()



class GetRiotMapping():
    ''' Get the mapping tables from Riot
    SeasonsMapping()
    QueueMapping()
    ChampMapping()
    '''
    def __init__(self):
        self.season = 'http://static.developer.riotgames.com/docs/lol/seasons.json'
        self.queue = 'http://static.developer.riotgames.com/docs/lol/queues.json'
        self.champions = 'http://ddragon.leagueoflegends.com/cdn/9.22.1/data/en_US/champion.json'
        self.itemURL = 'http://ddragon.leagueoflegends.com/cdn/9.22.1/data/en_US/item.json'    
    
    def Seasons(self):
        SeasonMap = {}
        seasons = GetDictResponse(self.season)
        for item in seasons:
            SeasonMap[ int(item['id']) ] = item['season']
        return SeasonMap
    
    def Queue(self):
        QueueMap = {}
        queues = GetDictResponse(self.queue)
        for item in queues:
            QueueMap[ int(item['queueId']) ] = str(item['map']) + ' | ' + str(item['description'])
        return QueueMap
    
    def Champions(self):
        ChampMap = {}
        champs = GetDictResponse(self.champions)['data']
        for key in champs:
            ChampMap[ int( champs[key]['key'] ) ] = key
        return ChampMap

    def Champs(self):
        ChampMap = {}
        champs = GetDictResponse(self.champions)['data']
        for key in champs:
            ChampMap[ int( champs[key]['key'] ) ] = key
        return ChampMap

    def Items(self):
        ItemMap = {}
        items = GetDictResponse(self.itemURL)['data']
        for key, value in items.items():
            ItemMap[ int(key) ] = value['name']
        return ItemMap






     
'''      
API_key = 'RGAPI-ca357b56-e07a-400e-a9b1-859cceb5ae84'
name = "Stabbinback Hz"
region = 'eun1'

obj = GetSummoner_GameDetails(API_key, region, name)

print(obj.GetMatchHist_gameid(season = 13, beginTime = '2019-01-01') )

'''





























    

