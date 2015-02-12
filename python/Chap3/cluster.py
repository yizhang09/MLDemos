# coding:utf-8

def readfile(filename):
	lines = [line for line in file(filename)]

	#表
	colnames = lines[0].strip().split('\t')[1:]
	print(colnames)
	rownames = []
	data = []
	for line in lines[1:]:
		p = line.strip().split('\t')

		rownames.append(p[0])
		print(p[0])

		data.append([float(x) for x in p[1:]])
	return rownames,colnames,data

rownames = readfile('blogdata.txt')
print(rownames)


