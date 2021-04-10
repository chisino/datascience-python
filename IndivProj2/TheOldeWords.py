# Artiom Dolghi

import os
import urllib.request
import urllib
import nltk
from nltk.corpus import stopwords
from nltk.corpus import words
from bs4 import BeautifulSoup
from collections import Counter

pageURL = "http://shakespeare.mit.edu/othello/full.html"
       
def main():
    soup = getDocument(pageURL)
    text = soup.text.lower()
    wordList = nltk.word_tokenize(text)
    stops = set(stopwords.words("english"))
    filteredWords = [word for word in wordList if word not in stops]
    filteredWords = [word.lower() for word in filteredWords if word.isalpha()]

    pos_translate = {"J" : "a", "V" : "v", "N" : "n", "R" : "r"}

    def pos2pos(tag):
        if tag in pos_translate: return pos_translate[tag] 
        else: return "n"
    
    lem = nltk.WordNetLemmatizer()
    lemList = [lem.lemmatize(w, pos2pos(pos[0])).lower() for w,pos in nltk.pos_tag(filteredWords)]

    wordsEn = set(words.words("en"))

    unique = [word for word in lemList if word not in wordsEn]

    counter = Counter(unique)
    top25 = counter.most_common(25)

    for result in top25:
        print(result)
        
def getDocument(url): # Caches the file
   i = 'othello.html'
   if not os.path.exists(i):
       print("Downloading:" + i)
       urllib.request.urlretrieve(url, i)
       html = urllib.request.urlopen(url).read()
       soup = BeautifulSoup(html, 'html.parser')
       return soup
   if os.path.exists(i):
       with open(i, encoding = 'utf8') as file:
           contents = BeautifulSoup(file, "html.parser")
           return contents
        
main()
