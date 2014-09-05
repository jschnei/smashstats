from collections import namedtuple

import json
import os.path
import pickle

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
        

def preprocess(overwrite=False):
    alias = load_aliases()
    
    f = open('events.json', 'r')
    events = json.load(f)
    matches = []
    for event in events:
        print 'Processing event', event['name']
        local = 'events/{id}.json'.format(id=event['id'])
        if os.path.isfile(local) and not overwrite:
            print 'File found locally, loading from local copy'
            ematches = json.load(open(local, 'r'))['matches']
            
            # apply any new aliases
            for match in ematches:
                match['winner'] = alias.get(match['winner'], match['winner'])
                match['loser'] = alias.get(match['loser'], match['loser'])
                
        else:
            print 'Scraping file from challonge url:', event['url']
            scrape = scrape_challonge.scrape_url(event['url'])
            ematches = [Match(alias.get(winner,winner), alias.get(loser,loser), event['name'])._asdict() for winner, loser in scrape]
            
        # save local file
        f = open(local, 'w')
        json.dump({'matches': ematches, 'name': event['name']}, f)
        f.close()
        
        matches += ematches
    
    players = set()
    for match in matches:
        players.add(match['winner'])
        players.add(match['loser'])
        
    players = sorted(list(players), key = lambda s:s.lower())
    
    f = open('allmatches.json', 'w')
    json.dump({'matches': matches, 'players': players}, f)
    f.close()
    
    f = open('allmatches.pkl', 'w')
    pickle.dump({'matches': matches, 'players': players}, f)
    f.close()
    
    plists = {player: {'wins':[], 'losses':[]} for player in players}
    
    for match in matches:
        plists[match['winner']]['wins'].append(match)
        plists[match['loser']]['losses'].append(match)
   
    
    f = open('plists.json', 'w')
    json.dump(plists, f)
    f.close()
    
    f = open('plists.pkl', 'w')
    pickle.dump(plists, f)
    f.close()
    

if __name__ == '__main__':
    preprocess()