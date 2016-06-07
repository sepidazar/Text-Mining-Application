import sys, subprocess, csv, itertools, re, os

cnt = 0
positive_words = []
negative_words = []
temp = []

if(len(sys.argv)<3):
    print "Inout Format: python createFeatureFile.py <input_file> <output_feature_file>" 
    sys.exit(0)

trainInput = open(sys.argv[2] , 'w+')


with open('positive-words.txt','r') as f1:
    for line in f1:
        positive_words.append(line.strip())

#print(positive_words)
            
with open('negative-words.txt','r') as f2:
    for line in f2:
        negative_words.append(line.strip())

#print(negative_words)



# read CSV file and save paragraph of comment in temp.txt
cr = csv.reader(open(sys.argv[1],"rb"))
line_number = 1
for row in itertools.islice(cr,1,None):
    print "\r"+str(line_number), 
    sys.stdout.flush()
    line_number+=1
    content = row[5]
#     if(line_number == 70):
#         print content
    tmp = open('temp.txt','w+')
    tmp.write(content)
    tmp.flush()
    tmp.close()
    
    content = []
    content.append(row[0])
    content.append("BWC:"+row[1])
    content.append("RC:"+row[2])
    content.append("NC:"+row[3])
    content.append("PC:"+row[4])
    content.append("CC:"+row[6])
    
    # Set up the sh command and direct the output to a pipe
    p1 = subprocess.Popen(['sh', 'lexparser.sh',
                            'temp.txt'], stdout=subprocess.PIPE, stderr = subprocess.PIPE)
    # Run the command
    output, err = p1.communicate()
    output = re.sub(r"\(ROOT\n(.+?\n)+", "", output)
#     print output
    out = open('out.txt', 'w+')
    out.write(output)
    out.flush()
    
    errr = open('errorFile.txt', 'w+')
    errr.write(err)
    errr.flush()
    
    # Getting only head and dependant in this format: HEAD DEPENDANT
    with open('out.txt', 'r') as f:
        feature = open('feature.txt', 'w+')
        for line in f:
            line = line[line.find("(")+1:line.find(")")]
            for token in line.split(', '):
                token = token [:token.rfind("-")]
                feature.write(token + " ")
            feature.write("\n")
    feature.flush()
    
    # Replacing all the positive adjectives with "posWrd" and all the negative adjectives with "negWrd"
    with open('feature.txt', 'r') as f:
        medium = open('med-file.txt', 'w+')
        for line in f:
            for token in line.split():
                if token in positive_words:
                    token = "posWrd"
                elif token in negative_words:
                    token = "negWrd"
                medium.write(token + " ")
            medium.write('\n')
    medium.flush()

    #Checking for "you", "your", "this", "xxbdWrdxx", "not" and "negWrd" and extract those to a file as H:HEADD:DEPENDANT
    with open('med-file.txt', 'r') as f:
        finalFeature = ""
        for line in f:
            token = line.split()
            if token != []:
                if (token[0] == "you"): 
                    finalFeature += "H:"
                    cnt = 0
                    finalFeature +=token[0]
                    finalFeature +="D:"
                    finalFeature +=token[1]
                    #final.write(' ')
                     
                elif (token[1] == "you"): 
                    finalFeature +="H:"
                    cnt = 0
                    finalFeature +=token[0]
                    finalFeature +="D:"
                    finalFeature +=token[1]
                    #finalFeature +=' ')
                     
                elif (token[0] == "your"): 
                    finalFeature +="H:"
                    cnt = 0
                    finalFeature +=token[0]
                    finalFeature +="D:"
                    finalFeature +=token[1]
                #finalFeature +=' ')
                 
                elif (token[1] == "your"):
                    finalFeature +="H:"
                    cnt = 0
                    finalFeature +=token[0]
                    finalFeature +="D:"
                    finalFeature +=token[1]
                #inal.write(' ')
                 
                elif (token[0] == "this"): 
                    finalFeature +="H:"
                    cnt = 0
                    finalFeature +=token[0]
                    finalFeature +="D:"
                    finalFeature +=token[1]
                #finalFeature +=' ')
                 
                elif (token[1] == "this"): 
                    finalFeature +="H:"
                    cnt = 0
                    finalFeature +=token[0]
                    finalFeature +="D:"
                    finalFeature +=token[1]
                #finalFeature +=' ')
                 
                elif (token[0] == "xxbdWrdxx"): 
                    finalFeature +="H:"
                    cnt = 0
                    finalFeature +=token[0]
                    finalFeature +="D:"
                    finalFeature +=token[1]
                #finalFeature +=' ')
                 
                elif (token[1] == "xxbdWrdxx"): 
                    finalFeature +="H:"
                    cnt = 0
                    finalFeature +=token[0]
                    finalFeature +="D:"
                    finalFeature +=token[1]
                             
                elif (token[1] == "not"): 
                    finalFeature +="H:"
                    cnt = 0
                    finalFeature +=token[0]
                    finalFeature +="D:"
                    finalFeature +=token[1]
                     
                elif (token[1] == "n't"):
                    finalFeature +="H:"
                    cnt = 0
                    finalFeature +=token[0]
                    finalFeature +="D:"
                    finalFeature +=token[1]
                     
                elif (token[0] == "negWrd"): 
                    finalFeature +="H:"
                    cnt = 0
                    finalFeature +=token[0]
                    finalFeature +="D:"
                    finalFeature +=token[1]
                     
                elif (token[1] == "negWrd"): 
                    finalFeature +="H:"
                    cnt = 0
                    finalFeature +=token[0]
                    finalFeature +="D:"
                    finalFeature +=token[1]
                         
            if cnt == 0:
                finalFeature +=" "
                cnt = 1
    #final.flush()
    content.append(finalFeature)
    trainInput.write(" ".join(content) + '\n' )
    content = []
    trainInput.flush()

os.remove("temp.txt")
os.remove("out.txt")
os.remove("feature.txt")
os.remove("med-file.txt")