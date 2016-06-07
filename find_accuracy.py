import os,sys

if len(sys.argv) != 3:
    sys.exit('Input format filename.py <INPUT ground_truthFile> <INPUT PredictionFile.txt>')

ground_file = sys.argv[1]
prediction_file = sys.argv[2]
accu = []

from itertools import izip

with  open(ground_file,'r') as ip1, open(prediction_file,'r') as ip2:
    for x, y in zip(ip1, ip2):
        first = x.split()[0]
        second = y.split()[0]
        if len(first) != len(second):
            sys.exit("not equal length of lines!! ")

        if first == second:
            accu.append(1)
        else:
            accu.append(0)
            # print x
            # print y
                # print '::'+first[index] + '::'+second[index]+'::'

print 'accuracy ' + str(sum(accu)/float(len(accu)))
print len(accu)
