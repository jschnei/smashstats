from collections import deque
from preprocess import Match
import pickle

def betterthanciz(target = 'C!Z'):
    plists = pickle.load(open('plists.pkl','r'))
    
    bfs = deque([(target, 0)])
    ans = dict({target:(None, 0)})
    
    while bfs:
        player, score = bfs.popleft()
        for loss in plists[player]['losses']:
            if loss.winner not in ans:
                ans[loss.winner] = (loss, score+1)
                bfs.append((loss.winner, score+1))

    pickle.dump(ans, open('betterthanciz.pkl','w'))

if __name__ == '__main__':
    betterthanciz()