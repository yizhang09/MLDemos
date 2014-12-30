#from recommendation import critics
#from recommendation import critics
from Chap2 import pearson as p


#print p.sim_pearson(criticsdata.critics,'Lisa Rose','Gene Seymour')

#Returns
def topMatches(prefs, person, n=5, similarity=p.sim_pearson):
    scores = [(similarity(prefs, person, other), other)
                    for other in prefs if other != person]
    scores.sort()
    scores.reverse()
    return scores[0:n]


#print topMatches(criticsdata.critics,'Toby',n=3)

def getRecommendations(prefs,person,similarity=p.sim_pearson):
    totals={}
    simSums={}
    for other in prefs:
        if other == person:continue
        sim=similarity(prefs,person,other)

        if sim<=0:continue
        for item in prefs[other]:
            if item not in prefs[person] or prefs[person][item]==0:
                totals.setdefault(item,0)
                totals[item]+=prefs[other][item]*sim
                simSums.setdefault(item,0)
                simSums[item]+=sim


    rankings=[(total/simSums[item],item) for item,total in totals.items()]

    rankings.sort()
    rankings.reverse()
    return rankings





#print critics

#print critics['Jack Matthews']['Lady in the Water']



