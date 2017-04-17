from __future__ import print_function

import sys
from operator import add
from pyspark import SparkContext
from csv import reader

if __name__ == "__main__":
	sc = SparkContext()
	lines = sc.textFile('crime.csv')
	header = lines.first()
	lines = lines.filter(lambda row: row != header)
	lines = lines.mapPartitions(lambda x: reader(x))
	counts = lines.map(lambda x: (int(x[6]), 1))
	counts = counts.reduceByKey(lambda a, b: a + b)
	count1 = counts.map(lambda x: (x[1], x[0]))
	count1 = count1.sortByKey(False)
	
	df = count1.map(lambda r: str(r[1]) + "\t" + str(r[0]))
	df.saveAsTextFile("taskwc.out")
