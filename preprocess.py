from collections import namedtuple

import json
import scrape_challonge

Match = namedtuple('Match', ['winner', 'loser', 'event'])

def load_aliases():
    f = open('aliases.json', 'r')
    players = json.load(f)
    
    lookup = dict()
    for player in players:
        for alias in player['aliases']:
            lookup[alias] = player['tag']

    return lookup
        

def preprocess():
    alias = load_aliases()
    
    f = open('events.json', 'r')
    events = json.load(f)
    matches = []
    for event in events:
        ematches = scrape_challonge.scrape_url(event['url'])
        matches += [Match(alias.get(winner,winner), alias.get(loser,loser), event['name']) for winner, loser in ematches]
    
    players = set()
    for match in matches:
        players.add(match.winner)
        players.add(match.loser)
        
    print sorted(list(players), key = lambda s:s.lower())
        
    
if __name__ == '__main__':
    preprocess()