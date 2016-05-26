from WordLevel import WordLevel
#from TopicModelingPreprocessing import TopicModelingPreprocessing
from TopicModeling import TopicModeling
from SentimentAnalysis import SentimentAnalysis

text = '"A\\xc2\\xa0majority of Canadians can and has been wrong before now and will be again.\\n\\nUnless you\'re fucking supportive of the idea. "' 
#that nothing is full proof or perfect so you take your chances and if we should inadvertently kill your son or daughter then them\'s the breaks and we can always regard you as collateral damage like in wartime - and sorry, but\\xc2\\xa0the cheques in the mail. "'
myWordLevel = WordLevel(text, 'upperCount, quoteRemove, decoding, repetitionCount, repetitionRemove, spellCorrector, cleaning, wordCount, charCount, negWordCount, posWordCount, badWordCount')

myTopicModeling = TopicModeling()
mySentimentAnalysis = SentimentAnalysis()
#myTopicModelingPreprocessing = TopicModelingPreprocessing()
# import lda
# X = lda.datasets.load_reuters()
# model = lda.LDA(n_topics=20, n_iter=1500, random_state=1)
# model.fit(X)  # model.fit_transform(X) is also available
