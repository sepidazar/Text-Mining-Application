from __future__ import print_function

from DocMining import DocMining
from TitleMining import TitleMining

from nltk.corpus import stopwords

import textmining

class TopicModelingPreprocessing:
    
    def __init__(self):
        self.tdm = textmining.TermDocumentMatrix()
        self.myDM = DocMining()
        self.cachedStopWords = stopwords.words("english")
        self.doc_file = open('documents.txt', "r")
        for line in self.doc_file:
            text = ' '.join([word for word in line.split() if word not in self.cachedStopWords])
            self.myDM.addToTDM(text, self.tdm)
        self.doc_file.close()
        self.temp = list(self.tdm.rows(cutoff=1))
        
#         X = self.documentTermMatrix()
#         print("The 'document-term' matrix")
#         #print("type(X): {}".format(type(X)))
#         #print("shape: {}".format(X.shape))
#         print("X:", X, sep='\n')
#         
#         vocab = self.vocabulary()
#         print("The 'vocabulary':")
#         #print("type(vocab): {}".format(type(vocab)))
#         #print("len(vocab): {}".format(len(vocab)))
#         print("vocab:", vocab, sep='\n')
#         
#         titles = self.documentTitles()   
#         print("The 'titles' for this 'corpus':")
#         print(titles) 
                
    def documentTermMatrix(self):
        return self.myDM.getDTM(self.temp)
    
    def vocabulary(self):
        return self.myDM.getVocab(self.temp)
        
    def documentTitles(self):
        myTM = TitleMining()
        myList = []
        title_file = open('titles.txt', "r")
        for line2 in title_file:
            line2 = line2.strip('\n')
            text = ' '.join([word for word in line2.split() if word not in self.cachedStopWords])
            myTM.getTitle(text, myList)
        
        return tuple(myList)