from preprocess_test import Preprocess_Test
from preprocess_train import Preprocess_Train
import os

class Insult_Detection:
    def __init__(self):
    
        self.p_train = Preprocess_Train()
        
        self.p_test = Preprocess_Test()
        
        os.system("python createFeatureFile.py testMegam.csv testFinalOutputMegam.txt")
        
        os.system("python train.py processed_train.csv myModel.dat 500")
        os.system("./megam -nc -predict myModel.dat multiclass testFinalOutputMegam.txt > myTestTags.txt")
        
        doc_file = open('myTestTags.txt', "r")
        with open('predictedLabels.txt', 'wb') as fp:
            for line in doc_file:
                fp.write(line.split(None, 1)[0])
                fp.write('\n')
        fp.close()
        doc_file.close()
        
        os.system("python find_accuracy.py dev_ground_truth.txt predictedLabels.txt")
        
        

