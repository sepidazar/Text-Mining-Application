import re, math, collections, itertools
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.metrics import BigramAssocMeasures, precision, recall
from nltk.probability import FreqDist, ConditionalFreqDist

class SentimentAnalysis:
    
    def __init__(self):
        #finds word scores
        self.word_scores = self.create_word_scores()
        numbers_to_test = [10, 100, 1000, 10000, 15000]
    #tries the best_word_features mechanism with each of the numbers_to_test of features
        for num in numbers_to_test:
            print 'evaluating best %d word features' % (num)
            self.best_words = self.find_best_words(self.word_scores, num)
            self.evaluate_features(self.best_word_features)
        
     
    def evaluate_features(self, feature_select):
        #reading pre-labeled input and splitting into lines
        posSentences = open('rt-polarity-pos.txt', 'r')
        negSentences = open('rt-polarity-neg.txt', 'r')
        posSentences = re.split(r'\n', posSentences.read())
        negSentences = re.split(r'\n', negSentences.read())
      
        posFeatures = []
        negFeatures = []
        #breaks up the sentences into lists of individual words (as selected by the input mechanism) and appends 'pos' or 'neg' after each list
        for i in posSentences:
            posWords = re.findall(r"[\w']+|[.,!?;]", i)
            posWords = [feature_select(posWords), 'pos']
            posFeatures.append(posWords)
        for i in negSentences:
            negWords = re.findall(r"[\w']+|[.,!?;]", i)
            negWords = [feature_select(negWords), 'neg']
            negFeatures.append(negWords)
         
        #selects 3/4 of the features to be used for training and 1/4 to be used for testing
        posCutoff = int(math.floor(len(posFeatures)*3/4))
        negCutoff = int(math.floor(len(negFeatures)*3/4))
        trainFeatures = posFeatures[:posCutoff] + negFeatures[:negCutoff]
        testFeatures = posFeatures[posCutoff:] + negFeatures[negCutoff:]
        #Training Phase: 
        classifier = NaiveBayesClassifier.train(trainFeatures)
         
        referenceSets = collections.defaultdict(set)
        testSets = collections.defaultdict(set)    
         
        #Testing Phase:
        for i, (features, label) in enumerate(testFeatures):
            referenceSets[label].add(i)
            predicted = classifier.classify(features)
            testSets[predicted].add(i)
             
        print 'Trained on %d instances, Tested on %d instances' % (len(trainFeatures), len(testFeatures))
        print 'Accuracy:', nltk.classify.util.accuracy(classifier, testFeatures)
        print 'Positive Precision:', precision(referenceSets['pos'], testSets['pos'])
        print 'Positive Recall:', recall(referenceSets['pos'], testSets['pos'])
        print 'Negative Precision:', precision(referenceSets['neg'], testSets['neg'])
        print 'Negative Recall:', recall(referenceSets['neg'], testSets['neg'])
    #     classifier.show_most_informative_features(10)
         
    # def make_full_dict(words):
    #     return dict([(word, True) for word in words])
    #  
    # #tries using all words as the feature selection mechanism
    # print 'using all words as features'
    # evaluate_features(make_full_dict)
         
         
    def create_word_scores(self):
            #splits sentences into lines
        posSentences = open('rt-polarity-pos.txt', 'r')
        negSentences = open('rt-polarity-neg.txt', 'r')
        posSentences = re.split(r'\n', posSentences.read())
        negSentences = re.split(r'\n', negSentences.read())
          
        #creates lists of all positive and negative words
        posWords = []
        negWords = []
        for i in posSentences:
            posWord = re.findall(r"[\w']+|[.,!?;]", i)
            posWords.append(posWord)
        for i in negSentences:
            negWord = re.findall(r"[\w']+|[.,!?;]", i)
            negWords.append(negWord)
        posWords = list(itertools.chain(*posWords))
        negWords = list(itertools.chain(*negWords))
         
        word_fd = FreqDist()
        cond_word_fd = ConditionalFreqDist()
         
        for word in posWords:
            word_fd[word.lower()] += 1
            cond_word_fd['pos'][word.lower()] += 1
        for word in negWords:
            word_fd[word.lower()] += 1
            cond_word_fd['neg'][word.lower()] += 1
         
        pos_word_count = cond_word_fd['pos'].N()
        neg_word_count = cond_word_fd['neg'].N()
        total_word_count = pos_word_count + neg_word_count
         
        word_scores = {}
        for word, freq in word_fd.iteritems():
            pos_score = BigramAssocMeasures.chi_sq(cond_word_fd['pos'][word], (freq, pos_word_count), total_word_count)
            neg_score = BigramAssocMeasures.chi_sq(cond_word_fd['neg'][word], (freq, neg_word_count), total_word_count)
            word_scores[word] = pos_score + neg_score
        return word_scores
         
    def find_best_words(self, word_scores, number):
        best_vals = sorted(word_scores.iteritems(), key=lambda (w, s): s, reverse=True)[:number]
        best_words = set([w for w, s in best_vals])
        return best_words
         
    def best_word_features(self, words):
        return dict([(word, True) for word in words if word in self.best_words])