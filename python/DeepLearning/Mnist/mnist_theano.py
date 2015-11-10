__author__ = 'zhangyi'

import cPickle, gzip, numpy
import theano.tensor as T

f = gzip.open('mnist.pkl.gz', 'rb')
train_set, valid_set, test_set = cPickle.load(f)
f.close()








