from collections import deque
from preprocess import Match

import json
import pickle

def betterthanciz(target = 'C!Z'):
    plists = pickle.load(open('plists.pkl','r'))
    
    bfs = deque([target])
    ans = dict({target:[]})
    
    while bfs:
        player = bfs.popleft()
        for loss in plists[player]['losses']:
            if loss.winner not in ans:
                ans[loss.winner] = [loss._asdict()] + ans[player]
                bfs.append(loss.winner)

    pickle.dump(ans, open('betterthanciz.pkl','w'))
    json.dump(ans, open('betterthanciz.json','w'))

if __name__ == '__main__':
    betterthanciz()