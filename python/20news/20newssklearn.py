from sklearn.datasets import fetch_20newsgroups
from pprint import pprint
import logging

logging.basicConfig()

categories = ['comp.graphics',
              'comp.os.ms-windows.misc',
              'comp.sys.ibm.pc.hardware',
              'comp.sys.mac.hardware',
              'comp.windows.x']
# categories = ['comp.graphics',
#               'comp.os.ms-windows.misc',
#               'comp.sys.ibm.pc.hardware',
#               'comp.sys.mac.hardware',
#               'comp.windows.x']

newsgroup_train = fetch_20newsgroups(subset='train', categories=categories)

pprint(list(newsgroup_train.target_names))
