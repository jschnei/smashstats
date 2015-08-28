from math import log, exp

import json
import numpy
import scipy.optimize as optimize

SIGMA = 50.

def cgskill():
    data = json.load(open('allmatches.json','r'))
    idmap = {player: ind for ind, player in enumerate(data['players'])}
    N = len(data['players'])
    
        
    
    def f(x):
        output = 0
        for i in xrange(N):
            output += -(x[i]**2)/(2.*SIGMA**2)
        
        for match in data['matches']:
            wid = idmap[match['winner']]
            lid = idmap[match['loser']]
            output += log(1./(1. + exp(x[lid]-x[wid])))
            
        return -output

    def fp(x):
        output = [x[i]/SIGMA for i in xrange(N)]
        
        for match in data['matches']:
            wid = idmap[match['winner']]
            lid = idmap[match['loser']]
            output[wid] -= exp(x[lid]-x[wid])/(1. + exp(x[lid]-x[wid]))
            output[lid] += exp(x[lid]-x[wid])/(1. + exp(x[lid]-x[wid]))
            
        return numpy.array(output)
        
    guess = [0. for i in xrange(N)]
    skills = optimize.fmin_cg(f, guess, fprime=fp)
    pskills = [(data['players'][i], skills[i]) for i in xrange(N)]
    pskills.sort(key = lambda x:-x[1])

    for i in xrange(N):
        print (i+1), pskills[i]
    
    nupsets = 0
    for match in data['matches']:
        wid = idmap[match['winner']]
        lid = idmap[match['loser']]
        
        if skills[lid] > skills[wid]:
            print 'Upset: {} (skill {}) beat {} (skill {}) at {}'.format(match['winner'],
                                                                         skills[wid],
                                                                         match['loser'],
                                                                         skills[lid],
                                                                         match['event'])
            nupsets+=1
    print 'Total Upsets:', nupsets
    

if __name__ == '__main__':
    cgskill()