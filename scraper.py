import re
import requests
import string
from bs4 import BeautifulSoup
import csv

#removes squar-boxed citation numbers
def removecitation(words): #takes in a list of unpunctuated words
    word_list = list()
    for word in words:
        if re.search(".+\[[0-9]+\]$",word):
            word = word[:-3]
            word_list.append(word)
        else:
            word_list.append(word)
    return word_list #returns a list of uncited words
    
    
#removes punctuations from paragraph text
def removepunctuation(words): #takes in a list of words
    word_list = list()
    for word in words:
        if len(word) > 1:
            if word[0] in string.punctuation:
                word = word[1:]
                if word[-1] in string.punctuation:
                    word = word[:-1]
                    word_list.append(word)
                else:
                    word_list.append(word)
            else:
                if word[-1] in string.punctuation:
                    word = word[:-1]
                    word_list.append(word)
                else:
                    word_list.append(word)
        else:
            word_list.append(word)                
    return word_list #returns a list of words
    
    
#Tabulate a word frequency histogram
def uniquewordcount(words, word_hist): #takes in a word list and target count dictionary
    for word in words:
        word = word.lower()
        if word not in word_hist:
            word_hist[word] = 1
        else:
            word_hist[word] = word_hist[word] + 1
    return word_hist #returns an updated dictionary word count
    
    
#Generate word count froma wiki page
def wikiwordcount(url,word_freq):
    wiki = requests.get(url).text
    #print("The page can be scraped:", wiki.ok, "| The status code is:", wiki.status_code)

    #Filter all paragraph elements
    soup = BeautifulSoup(wiki, "html")
    wiki_text = soup.find_all("p")

    #Extract paragraph text from all paragraph elements
    for paragraph in wiki_text:
        wiki_paragraph = str(paragraph.text)
        
        #extract words from paragraph text
        not_altered_words = wiki_paragraph.split()
        not_cited_words = removecitation(not_altered_words) #remove citations
        words = removepunctuation(not_cited_words)#removes punctuations
        
        #make/update word frequency count
        uniquewordcount(words, word_freq)
        
    return word_freq   
    
#Generate word count from a given url num times 
def getwordfrequency(url, num):
    #Create a Word Frequency Histogram
    word_freq = dict()
    url = "https://en.wikipedia.org/wiki/Special:Random"

    for i in range(num):
        wikiwordcount(url, word_freq)
        
    return word_freq
  
#store a list of tuples into a csv  
def storeintocsv(filename, sortedwords):
    with open(filename, mode='w') as csv_file:
        fieldnames = ['word', 'count']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for word in sortedwords:
          writer.writerow({'word': word[0], 'count': word[1]})  
  
def main():
    url = "https://en.wikipedia.org/wiki/Special:Random"
    numArticles = 10000 

    sortedwords = getwordfrequency(url, num)
    
    filename = "words.csv"
    storeintocsv(filename, sortedwords)
    
    
if __name__ == '__main__':
    main()
    
