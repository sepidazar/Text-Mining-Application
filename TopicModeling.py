from __future__ import division, print_function

from TopicModelingPreprocessing import TopicModelingPreprocessing

import numpy as np
import lda

class TopicModeling:
    
    def __init__(self):
        self.mypreproc = TopicModelingPreprocessing()
        self.topicModelingResults() 
    
    def topicModelingResults(self):
        X = self.mypreproc.documentTermMatrix()
        print("The 'document-term' matrix")
        print("X:", X, sep='\n')
         
        vocab = self.mypreproc.vocabulary()
        print("The 'vocabulary':")
        print("vocab:", vocab, sep='\n')
         
        titles = self.mypreproc.documentTitles()   
        print("The 'titles' for this 'corpus':")
        print(titles) 
        
        model = lda.LDA(n_topics=3, n_iter=500, random_state=1)
        model.fit(X)
        
        topic_word = model.topic_word_ 
        print("type(topic_word): {}".format(type(topic_word)))
        print("shape: {}".format(topic_word.shape))
        
        topic_word = model.topic_word_ 
        print("type(topic_word): {}".format(type(topic_word)))
        print("shape: {}".format(topic_word.shape))
        
        for n in range(3):
            sum_pr = sum(topic_word[n,:])
            print("topic: {} sum: {}".format(n, sum_pr))
            
        n = 5
        for i, topic_dist in enumerate(topic_word):
            topic_words = np.array(vocab)[np.argsort(topic_dist)][:-(n+1):-1]
            print('*Topic {}\n- {}'.format(i, ' '.join(topic_words)))
            
        doc_topic = model.doc_topic_
        print("type(doc_topic): {}".format(type(doc_topic)))
        print("shape: {}".format(doc_topic.shape))
        
        for n in range(3):
            sum_pr = sum(doc_topic[n,:])
            print("document: {} sum: {}".format(n, sum_pr))
        
        for n in range(3):
            topic_most_pr = doc_topic[n].argmax()
            print("doc: {} topic: {}\n{}...".format(n,
                                            topic_most_pr,
                                            titles[n][:50]))