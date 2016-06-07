#---import---
import csv, sys, re, spell, itertools, codecs

class Preprocess_Test:
	
	def __init__(self):
		badword_file = open('badwords_all.txt', "r")
		self.badwords = []
		for line in badword_file:
			self.badwords.append(''.join(filter(lambda x: ord(x)<128,line.strip())))
		badword_file.close()
	
	#---open negative & positive word files---
		self.negword_list, self.posword_list = [], []
		with open('negative-words.txt', "r") as negword_file:
			for negword in negword_file:
				self.negword_list.append(negword.strip())
		with open('positive-words.txt', "r") as posword_file:
			for posword in posword_file:
				self.posword_list.append(posword.strip())
	
	
		doc_file = open('dev.txt', "r")
		line_count = 0
		with open('testMegam.csv', 'wb') as fp:
			a = csv.writer(fp, delimiter=',')
			#write header row
			a.writerow(["insult","badword_count", "rep_count", "negword_count", "posword_count", "comment", "caps_count"])
	
			for row in doc_file:
				print "\r"+str(line_count),
				sys.stdout.flush()
				line_count+=1
				myOut = self.get_stats(row, self.badwords, self.negword_list, self.posword_list)
				#write processed line and stats to file
				a.writerow(myOut)
				
#---customized handler for encode---
	def handler(self, e):
		return (u' ',e.start + 1)
			
	#---preprocess---
	def get_stats(self, line, badwords, negword_list, posword_list):
		#register error handler
		codecs.register_error('replace_with_space', self.handler) 
			
		#count uppercase letters
		caps_count = sum(x.isupper() for x in line)
	
		#remove garbage, lowercase & strip
		line = ''.join(filter(lambda x: ord(x)<128,line.lower().strip()))
	
		#decode to ascii
		line = line.decode('string-escape').decode('utf-8','replace_with_space').encode('ascii','ignore').decode('unicode-escape').encode('iso-8859-1','replace_with_space')
	
		#remove @name
		line = re.sub(r'^@\w{2,}', r'NameOfPerson', line)
	
		#count words with unwanted repetitions
		rep_count = len(re.findall(r'(.)\1\1+',line))
	
		#remove unwanted repetitions
		line = re.sub(r'(.)\1\1+', r'\1', line)
	
		#replace badwords
		for badword in badwords:
			line = re.sub(r"\b"+re.escape(badword)+r"\b|[!@#$%^&*+?~`]{3,}", r'xxbdWrdxx', line)
	
		#replace 'u' with 'you' & 'ur' with 'you are'
		line = re.sub(r"\bu\b", r'you', line)
		line = re.sub(r"\bu\s*r\b", r'you are', line)
			
		#correct spelling
		tmp_line = []
		for word in re.split(r"[^\w\,\'\.\-\?\!]+", line):
			tmp_line.append(spell.correct(word))
		line = ' '.join(tmp_line)
	
		#count negative words
		negword_count = 0
		for negword in negword_list:
			negword_count += line.count(negword.strip())
	
		#count positive words
		posword_count = 0
		for posword in posword_list:
			posword_count += line.count(posword.strip())
			
		#---categorize counts---
		#categorize badword_count
		badword_count = line.count("xxbdWrdxx")
		if badword_count >=3:
			badword_count = 3
		#categorize rep_count
		if rep_count == 2:
			rep_count = 1
		elif rep_count >=3:
			rep_count = 2
		#categorize negword_count
		if negword_count == 2:
			negword_count = 1
		elif negword_count >= 3 and negword_count <= 7:
			negword_count = 2
		elif negword_count >= 8:
			negword_count = 3
		#categorize posword_count
		if posword_count == 2:
			posword_count = 1
		elif posword_count >= 3 and posword_count <= 6:
			posword_count = 2
		elif posword_count >= 7:
			posword_count = 3
		#categorize caps_count
		if caps_count == 2:
			caps_count = 1
		elif caps_count >=3 and caps_count <=5:
			caps_count = 2
		elif caps_count >=6:
			caps_count = 3
	
		#write processed line and stats to file
		return ["dummy_label", str(badword_count), str(rep_count), str(negword_count), str(posword_count), line, str(caps_count)]
