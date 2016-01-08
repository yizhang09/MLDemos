from datetime import datetime
from glob import glob

import numpy as np
import pandas as pd
from PIL import Image
from sklearn import ensemble, cross_validation, preprocessing


def dir_to_dataset(glob_files, loc_train_labels=""):
	"""Munging to yummy sklearn-ready data """
	print("Gonna process:\n\t %s" % glob_files)
	dataset = []
	for file_count, file_name in enumerate(sorted(glob(glob_files), key=len)):
		image = Image.open(file_name)
		img = Image.open(file_name).convert('LA')  # tograyscale
		pixels = [f[0] for f in list(img.getdata())]
		dataset.append(pixels)
		if file_count % 1000 == 0:
			print("\t %s files processed" % file_count)

	if len(loc_train_labels) > 0:
		df = pd.read_csv(loc_train_labels)
		return np.array(dataset), np.array(df["Class"])
	else:
		return np.array(dataset)


if __name__ == "__main__":
	start = datetime.now()
	# Loading the data
	X_train, y = dir_to_dataset("kaggle_julia\\trainResized\\*.BMP", "kaggle_julia\\trainLabels.csv")
	print("Train Shape:\n\t%s" % str(X_train.shape))
	print("Labels Shape:\n\t%s\n" % str(y.shape))
	X_test = dir_to_dataset("kaggle_julia\\testResized\\*.BMP")
	print("Test Shape:\n\t%s\n\n" % str(X_test.shape))

	# Label encoding
	le = preprocessing.LabelEncoder()
	le.fit(y)
	y = le.transform(y)

	# Classifier Setting
	clf = ensemble.ExtraTreesClassifier(n_estimators=160, n_jobs=-1, random_state=1)
	print("Classifier:\n\t %s" % str(clf))

	# CV
	scores = cross_validation.cross_val_score(clf, X_train, y, cv=10)
	print("\n10-fold Validation Categorization Accuracy:\n\t %0.5f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

	# Fitting
	clf.fit(X_train, y)

	# Label decoding the predictions
	preds = list(le.inverse_transform(clf.predict(X_test)))

	# Creating submission
	with open("kaggle_julia\\kaggle.julia.submission.et.csv", "wb") as outfile:
		outfile.write("ID,Class\n")
		for e, pred in enumerate(preds):
			outfile.write("%s,%s\n" % (6284 + e, pred))

	print("\n\n\t\tScript Running Time: %s" % str(datetime.now() - start))
