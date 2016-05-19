import re, spell
class WordLevel:
    def __init__(self, text, module):
        self.line = text
        self.modules = module.split(', ');
        for m in self.modules:
            if(m == 'quoteRemove'):
                print('Double quotes removed: ')
                self.line = self.quoteRemove(self.line)
                print(self.line)
            if(m == 'decoding'):
                print('decode to ascii: ')
                self.line = self.decoding(self.line)
                print(self.line)
            if(m == 'upperCount'):
                print('Number of capital characters in the input texts are: ')
                print(self.upperCount(self.line))
            if(m == 'repetitionCount'):
                print('count words with unwanted repetitions: ')
                print(self.repetitionCount(self.line))
            if(m == 'repetitionRemove'):
                print('remove unwanted repetitions: ')
                self.line = self.repetitionRemove(self.line)
                print(self.line)
            if(m == 'spellCorrector'):
                print('correct spelling using Peter Norvig spelling corrector algorithm: ')
                self.line = self.spellCorrector(self.line)
                print(self.line)
            if(m == 'cleaning'):
                print('Garbage removed, lowercased & strip: ')
                self.line = self.cleaning(self.line)
                print(self.line)
            if(m == 'wordCount'):
                print('Number of words in the input texts are: ')
                print(self.wordCount(self.line))
            if(m == 'charCount'):
                print('Number of Characters in the input texts are: ')
                print(self.charCount(self.line))
            if(m == 'negWordCount'):
                print('Number of negative words: ')
                print(self.negWordCount(self.line))
            if(m == 'posWordCount'):
                print('Number of positive words: ')
                print(self.posWordCount(self.line))
            if(m == 'badWordCount'):
                print('Number of bad words: ')
                print(self.badWordCount(self.line))
 
    #count uppercase letters
    def upperCount(self, text):
        caps_count = sum(x.isupper() for x in text)
        return caps_count 
    
    #remove garbage, lowercase & strip
    def cleaning(self, text):
        line = ''.join(filter(lambda x: ord(x)<128,text.lower().strip()))
        return line
    
    #remove double quotes
    def quoteRemove(self, text):
        if text.startswith('"') and text.endswith('"'):
            line = text[1:-1]
        else:
            line = text
        return line
    
    #decode to ascii
    def decoding(self, text):
        line = text.decode('string-escape').decode('utf-8','replace_with_space').encode('ascii','ignore').decode('unicode-escape').encode('iso-8859-1','replace_with_space')
        return line
    #count words with unwanted repetitions
    def repetitionCount(self, text):
        rep_count = len(re.findall(r'(.)\1\1+',text))
        return rep_count
    
    #remove unwanted repetitions
    def repetitionRemove(self, text):
        line = re.sub(r'(.)\1\1+', r'\1', text)
        return line
    
    #correct spelling using Peter Norvig spelling corrector algorithm in the spell.py file. 
    #spell.correct is the function that takes care of spell correction!
    def spellCorrector(self, text):
        tmp_line = []
        for word in re.split(r"[^\w\,\'\.\-\?\!]+", text):
            tmp_line.append(spell.correct(word))
        line = ' '.join(tmp_line)
        return line
    
    #count number of words
    def wordCount(self, text):
        word_count = len(text.split())
        return word_count

    #Count number of Characters
    def charCount(self, text):
        temp_line = text.replace(',', '')
        temp_line = temp_line.replace('.', '')
        temp_line = temp_line.replace('?', '')
        temp_line = temp_line.replace('!', '')

        char_count = sum(c != ' ' for c in temp_line)
        return char_count
    
    #count negative words
    def negWordCount(self, text):
        negword_list = []
        negword_count = 0
        with open('negative-words.txt', "r") as negword_file:
            for negword in negword_file:
                negword_list.append(negword.strip())
        for negword in negword_list:
            negword_count += text.count(negword.strip())
        return negword_count
    
    #count positive words
    def posWordCount(self, text):
        posword_list = []
        posword_count = 0
        with open('positive-words.txt', "r") as posword_file:
            for posword in posword_file:
                posword_list.append(posword.strip())
        for posword in posword_list:
            posword_count += text.count(posword.strip())
        return posword_count
    
    #count bad words
    def badWordCount(self, text):
        badword_file = open('badwords_all.txt', "r")
        badwords = []
        for line in badword_file:
            badwords.append(''.join(filter(lambda x: ord(x)<128,line.strip())))
        badword_file.close()
        myText = text
        for badword in badwords:
            myText = re.sub(r"\b"+re.escape(badword)+r"\b|[!@#$%^&*+?~`]{3,}", r'xxbdWrdxx', myText)
        badword_count = myText.count("xxbdWrdxx")
        return badword_count