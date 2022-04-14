#AUTHOR: SHIVAM SHANDILYA 2020A7PS2094H

import os
import re


from nltk.stem import WordNetLemmatizer

#Stopwords
#can use nltk.corpus import stopwords for
# but find it better

stopwords = []
with open('Stopwords.txt') as f:
    for line in f:
        sw = line.split("\n")
        stopwords.append(sw)

#ENDP stopwords

lem = WordNetLemmatizer()

 #Inverted Index with lemmatization 
 #because it takes into consideration the context of the word to determine which is the intended meaning the user is looking for.
 # This process allows to decrease noise and speed up the user’s task.
 #Lemmatization is computationally expensive since it involves look-up tables and what not. 
 # If I have large dataset and performance is an issue, I will go with Stemming. 
 # But If accuracy is paramount and dataset isn't humongous,I have to go with Lemmatization.
 #tokens :=  storing inverted index
 #BiGramInvertedIndex := storing bigram indexes
tokens = {}
BiGramInvertedIndex = {}
documentID = 0
#path for the documents
path = r"D:\Search ENgine\Wildcard-Query-Search-Engine-master\Part 1\dataset"
#documentCount
documentCount = 0
#For all files,roots,dirs from the path
for roots,dirs,files in os.walk(path):
    #For all file among the files
    for file in files:
        #incrementing documentCount for each file
        documentCount+=1
        #reading file
        with open(os.path.join(path, file)) as f:
            #giving identity to file
                documentID += 1
                #for storing words
                line_tokens = []
                #from line from files
                for line in f:
                    #splitting line to word
                    line_tokens = re.split(r"[\. \\\,\/\?\!\@\#\$\%\^\&\*\(\)\:\{\[\]\}\<\>\t\r\`\~\n\=\:\-\"\'\;\d]", line)
                    #for each word do lemmatization and lowerCasing and preparing for bigram index
                    for each in line_tokens:
                        lemmatizedWord = lem.lemmatize(each)
                        lemmatizedWord = lemmatizedWord.lower()
                        #If not present in stopword then only will store 
                        if each not in stopwords:
                            biwordinput = '$' + lemmatizedWord + '$'
                            if biwordinput == '$$':
                                continue 
                            #for each word storing 2 letters across from each iteration
                            for i in range(len(biwordinput) - 1):
                                biword = biwordinput[i:i+2]
                                if biword in BiGramInvertedIndex:
                                    BiGramInvertedIndex[biword].append(lemmatizedWord)
                                else:
                                    BiGramInvertedIndex[biword] = [lemmatizedWord]
                            if lemmatizedWord not in tokens:
                                tokens[lemmatizedWord] = [documentID]
                            else:
                                if(documentID not in tokens[lemmatizedWord]): tokens[lemmatizedWord].append(documentID)
                        
#Writing to InvertedIndex.txt
file = open("InvertedIndex.txt", "w")
for key in sorted(tokens):
    file.write(key)
    file.write(" ")
    value = ','.join(str(v) for v in tokens[key])
    file.write(value)
    file.write("\n")
file.close()
#ENDP Inverted Index


#Writing to BiGramInvertedIndex.txt
file = open("BiGramInvertedIndex.txt","w")
for key in sorted(BiGramInvertedIndex):
  file.write(key)
  file.write(" ")
  value = ','.join(str(v)for v in BiGramInvertedIndex[key])
  file.write(value)
  file.write("\n")
file.close()
#ENDP

''' 
Function to calculate the LevenshteinDistance or the mininum edit distance;
used for spell check
takes two strings as input, 
    str1 --> first word
    str2 --> second word;
returns the levenshtein distance between str1 and str2
'''

#EditDistance
def LevenshteinDistance(str1, str2):
    str1Length = len(str1)
    str2Length = len(str2)

    LevenshteinArray = [[0 for i in range(str2Length+1)] for j in range(str1Length + 1)]
    for i in range(1,str1Length+1):
        LevenshteinArray[i][0] = i
    for i in range(1,str2Length+1):
        LevenshteinArray[0][i] = i

    for i in range(1,str1Length+1):
        for j in range(1,str2Length+1):
            LevenshteinArray[i][j] = min(LevenshteinArray[i-1][j-1] + (0 if str1[i-1] == str2[j-1] else 1), (LevenshteinArray[i-1][j] +1), (LevenshteinArray[i][j-1] +1))

    return LevenshteinArray[str1Length][str2Length]
#ENDP EditDistance

# AND,OR and NOT
def AND(p1, p2):
    """
    input parameters:
    p1(list): positing list 1
    p2(list): posting list 2
    Performs intersection on input lists and returns common documents
    Returns list
    """
    len_p1, len_p2 = len(p1), len(p2)
    answer = []
    i, j = 0, 0
    while i != len_p1 and j != len_p2:
        if p1[i] == p2[j]:
            answer.append(p1[i])
            i += 1
            j += 1
        elif p1[i] < p2[j]:
            i += 1
        else:
            j += 1
    return answer


def OR(p1, p2):
    """
    input parameters:
    p1(list): positing list 1
    p2(list): posting list 2
    Performs union on input lists and returns all documents present in both lists
    Returns list
    """
    len_p1, len_p2 = len(p1), len(p2)
    answer = []
    i, j = 0, 0
    while i != len_p1 and j != len_p2:
        if p1[i] == p2[j]:
            answer.append(p1[i])
            i += 1
            j += 1
        elif p1[i] < p2[j]:
            answer.append(p1[i])
            i += 1
        else:
            answer.append(p2[j])
            j += 1

    while i < len_p1:
        answer.append(p1[i])
        i += 1
    while j < len_p2:
        answer.append(p2[j])
        j += 1
    return answer


def NOT(p):
    """
    input parameter:
    p(list): posting list
    Performs not operation and return posting list of documents not present in input list
    Returns list
    """
    len_p = len(p)
    answer = [x for x in range(1, documentCount+1)]
    i, j = 0, 0
    while j != len_p:
        if answer[i] == p[j]:
            answer.pop(i)
            j += 1
            continue
        elif answer[i] < p[j]:
            i += 1
        else:
            j += 1
    return answer

#making the invertedIndexTable of the docs in the corpus
InvertedIndex1 = tokens

def BigramQuery(word):
    '''Converting input wildcard query for Bi-Gram Query search'''
    word = '$' + word + '$'
    
    # splits on '*' for wildcard query searches
    wordList = word.split('*')
    
    # empty list
    bigrams = []
    
    # making bigrams from the input wildcardQuery
    for elem in wordList:
        for i in range(len(elem)-1):
            bigrams.append(elem[i:i+2])
    
    # starts with first bi-gram word 
    result = BiGramInvertedIndex[bigrams[0]]
    
    # updates(takes intersection) of the result for all the possible bi-grams of the query
    for i in range(1, len(bigrams)):
        # set to remove duplicates
        result = set(result)
        
        # temp set to store words satisfying the next bi-gram query 
        temp = set(BiGramInvertedIndex[bigrams[i]])
        
        # taking intersection of bi-grams
        result = result.intersection(temp)
        result = list(result)

    # returns bi-grams 
    return result

def BigramSearch(words):
    '''Bi-gram search function'''
    
    result = InvertedIndex1[words[0]]
    for i in range(1, len(words)):
        # set to remove duplicates
        result = set(result)
        
        # temp set to store words satisfying the next bi-gram query 
        temp = set(InvertedIndex1[words[i]])
        
        # taking union of all the queries which satisifed
        result = result.union(temp)
        result = list(result)
    
    # returns list containing biGram matches
    return result




'''
Function to pre-process the query.
Input is the raw.
Query is processed the same way as the words from the doc corpus
Query goes thru spell check using the levenshtein distance between the query word and words present in the inverted index table
Return the querywords as a list after spell correction and removing the stop words, bit operation words 
'''
def normalQuery(raw):
    # Spaces, special chars and numbers removed from the query (as they were removed when making the inverted index table)
    words = re.split(r"[\. \\\,\/\?\!\@\#\$\%\^\&\(\)\:\{\[\]\}\<\>\t\r\`\~\n\=\:\-\"\'\;\d]", raw)
    ind = 0
    
    stoplessWords = []

    # # lemmatizing the words in query
    for word in words:
        lemmatizedWord = lem.lemmatize(word)
        lemmatizedWord = lemmatizedWord.lower()
        if word not in stopwords:
            stoplessWords.append(word)
    
    words = stoplessWords
    for word in words:
        # bit operation as words in the query are ignored
        if (word in ('and', 'or', 'not')) or ('*' in word) :
            # index increased as bit operation remain the same after spell check of the queries
            ind += 1
            continue

        # ans stores the updated queryWord with it's levenshtein distance with the orginial queryWord
        ans = (None, None)
        
        for dictword in InvertedIndex1:
            
            # calculating the levenshtein distance of query word and word in the inverted index table
            dist = LevenshteinDistance(word,dictword)
            
            # updates the queryWord with word in inverted index table with minimun levenshtein distance 
            if (ans[1] == None) or (dist <= ans[1]):
                ans = (dictword, dist)
        
        # stores the updated queryWord after spell correction(min levenshtein distance)
        words[ind] = ans[0]
        ind += 1
    
    # list for the final query after skipping stop words and the bit operation words
    # contains the main queryWords after spell correction
    finalWordList = []
    for word in words:
        if (word not in stopwords) or (word in ('and','or','not')):
            finalWordList.append(word)
            
    # final queryWords to be searched in the corpus
    resultStr = ''
    for word in finalWordList:
        resultStr += word + ' '
        
    # removes the extra space after the last word
    resultStr.strip()
    
    return resultStr
        

'''
Function for booleanQuery search
Input is Pre-processed query string and inverted index table
Returns 
'''
def ParseBoolean(PreprocessedQueryString, invertedIndexTable):
    # stack
    stack = []
    
    for query in PreprocessedQueryString.split():
        stack.append(query)
    
    intermediateResult = invertedIndexTable[stack.pop()]

    # while stack is not empty
    while(stack):
        # top element in the stack
        popped_elem = stack.pop()
        
        if(popped_elem == "not"):
            intermediateResult = NOT(intermediateResult)
            continue
        
        elif(popped_elem == "or"):
            temporaryResult = invertedIndexTable[stack.pop()]
            intermediateResult = OR(intermediateResult, temporaryResult)
            continue
        
        elif(popped_elem == "and"):
            temporaryResult = invertedIndexTable[stack.pop()]
            intermediateResult = AND(intermediateResult, temporaryResult)
            continue
        
    ResultDocumentSet = intermediateResult

    return ResultDocumentSet

    # Driver code

print("\nInfront of you, Presenting Google's Little Bro:\nPOODLE Search Engine:\n")
# get query input
choice = input("1) Enter Query\n2) Exit\n\n")
while(True):
    if(choice=='1'):
        query = input("Enter a query: ")

        # preprocessing the query
        preProcessedQuery = normalQuery(query)

        print("The query being run is: ", preProcessedQuery)
        
        for word in preProcessedQuery.split():
            # determing if any wildcard requests in the query
            if '*' in word:
                wordSet = BigramQuery(word)
                bigramDocList = list(set(BigramSearch(wordSet)))
                InvertedIndex1[word] = bigramDocList

        #Contains the outputfiles
        finalDocList = ParseBoolean(preProcessedQuery, InvertedIndex1)

        #saving filename into RetrievedDocuments.txt
        documentID = 0
        outputfile = open("RetrievedDocuments.txt","w")
        path = r"D:\Search ENgine\Wildcard-Query-Search-Engine-master\Part 1\dataset"
        for root, dirs, files in os.walk(path):
            for file in files:
                documentID = documentID + 1
                with open(os.path.join(path, file)) as f:
                    if documentID in finalDocList:
                            outputfile.write(file + "\n")
                f.close()
        outputfile.close()

        #writing to cmd lines
        with open("retrievedDocuments.txt","r") as f:
            for line in f:
                line_tokens = re.split(r"\n", line)
                    #for each word do lemmatization and lowerCasing and preparing for bigram index
                for each in line_tokens:
                    print(each)    

        print("Results have been stored in the RetrievedDocument.txt showing name of the document\n")
    elif choice =='2':
        print("Come Back Soon.")
        break
    else:
        print("\nInvalid Input.Please Try again.")
    choice = input("1) Enter Query\n2) Exit\n\n")
