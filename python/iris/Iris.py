from matplotlib import pyplot as plt
from sklearn.datasets import load_iris

data = load_iris()
features = data['data']
feature_names = data['feature_names']
target = data['target']
target_names = data['target_names']

#print(data)

print(feature_names)
#print(target)

for t, marker, c in zip(xrange(3), '>ox', 'rgb'):
    plt.scatter(features[target == t, 0],
                features[target == t, 1],
                marker=marker,
                c=c)

#plt.show()
plength = features[:, 2]
labels = target_names[target]
is_setosa = (labels == 'setosa')
max_setosa = plength[is_setosa].max()
min_non_setosa = plength[~is_setosa].min()

print('Maximum of setosa: {0}.'.format(max_setosa))
print('Minimum of others: {0}.'.format(min_non_setosa))