from __future__ import print_function

import numpy as np

class DocMining:
    
#     def __init__(self):
#         self.title = title
        # create a temp variable with doc-term info, first row has the vocabulary 
        # and the remaining rows have the document-term matrix
#         self.myList = titleList
    
    # Add the documents to term-document matrix    
    def addToTDM(self, doc, tdm):
        tdm.add_doc(doc)
    
    # get the vocab from first row of temp variable
    def getVocab(self, temp):
        return tuple(temp[0])
    
    # get document-term matrix from temp variable
    def getDTM(self, temp):
        return np.array(temp[1:])
    # get titles for documents  
#     def getTitle(self):
#         self.myList.append(self.title)
#         return self.myList
    
        
    