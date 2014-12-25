__author__ = 'zhangyi'

def loadMovielens(path='data/movielens/'):
    movies={}
    for line in open(path+'u.item'):
        (id,title)=line.split('|')[0:2]
        movies[id]=title


    prefs={}
    for line in open(path+'u.data'):
        (user,movieid,rating,ts)=line.split('\t')
        prefs.setdefault(user,{})
        prefs[user][movies[movieid]]=float(rating)

    return prefs


import recom
prefs = loadMovielens()
result = recom.getRecommendations(prefs,'87')[0:30]

for item in result:
    print item


