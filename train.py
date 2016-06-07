import os,sys
if len(sys.argv) != 4:
    sys.exit('Input format train.py  <processed_train.csv> <model.dat> <number_of_iteration>')
else:
    os.system("python createFeatureFile.py "+ sys.argv[1] + " " + "megaMFeatures.txt")
    os.system("./megam -nc -maxi "+sys.argv[3]+" multitron "+ "megaMFeatures.txt" +" > "+sys.argv[2])