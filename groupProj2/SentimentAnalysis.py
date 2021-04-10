import json
from nltk.corpus import stopwords, words
from nltk.stem import WordNetLemmatizer
from collections import Counter
import nltk
import csv
import urllib

def GetJson(fileName):
      with open(fileName) as file:
          contents = json.load(file)
          return contents

def GetRawData():
  FullFile = GetJson("yelp_academic_dataset_review_small.json")
  Stars = []
  Text = []
  for Dict in FullFile:
      Values = list(Dict.values())
      [Stars.append(Values[5])]
      [Text.append(Values[-1])]
  return Stars, Text

def Main():
  Lists = GetRawData()
  Text = Lists[1]
  Stars = Lists[0]
  Text = EnglishOnly(Text)
  Text = lemmatize(Text)
  Text = StopWords(Text)
  ReviewsStars = {Text[i] : float(Stars[i]) for i in range(len(Text))}
  ReviewsRatings = GetAvg(ReviewsStars)
  BuildCSV(ReviewsRatings)
  print(ReviewsRatings)

def StopWords(list):
  Stops = set(stopwords.words('english'))
  NoStops = []
  for X in list:
      Sentence = X.split()
      Filtered = []
      [Filtered.append(X) for X in Sentence if X.lower() not in Stops and X.isalpha()]
      Filtered = " ".join(Filtered)
      NoStops.append(Filtered)
  return NoStops

def EnglishOnly(list):
 English = set(words.words())
 AllWords = []
 for X in list:
   Sentence = X.split()
   Filtered = []
   [Filtered.append(X) for X in Sentence if X.lower() in English and X.isalpha()]
   Filtered = " ".join(Filtered)
   AllWords.append(Filtered)
 return AllWords

def lemmatize(list):
  lemma = WordNetLemmatizer()
  lemmatized = []
  for X in list:
      Sentence = X.split()
      Filtered = []
      for Y in Sentence:
          Y = lemma.lemmatize(Y)
          Filtered.append(Y)
      Filtered = " ".join(Filtered)
      lemmatized.append(Filtered)
  lemmatized = StripUncommon(lemmatized)
  return lemmatized

def StripUncommon(list):
  OnlyCommon = []
  counter = Counter()
  for Sentence in list:
      counter.update(word.strip('.,?!"\'').lower() for word in Sentence.split()) # From stackoverflow
  for Sent in list:
      JustWords = Sent.split()
      [JustWords.remove(X) for X in JustWords if counter[X.lower()] < 10 or len(X) == 1]
      Filtered = " ".join(JustWords)
      OnlyCommon.append(Filtered)
  return OnlyCommon

English = set(words.words())

def GetAvg(Text):
   ListOfReviews = list(Text.keys())
   WordCounter = Counter()

   for Sentence in ListOfReviews: #Builds a dictionary containing a list of words and how often they appear
       WordCounter.update(word.strip('.,?!"\'').lower() for word in Sentence.split())

   LemmaValues = {x:0 for x in WordCounter.keys()} #Builds a new dictionary with neutral sentiment values

   for Sentence in ListOfReviews: #Gives words overall sentiments based on the reviews theyre in
       StarRating = float(Text[Sentence])
       StarRating -= 3.0 #Gives Star ratings overall values with 3 being neutral.
       WordsInReview = Sentence.split()
       for Word in WordsInReview:
           LemmaValues[Word.lower()] += StarRating

   for Word in WordCounter.keys(): #makes an average for a word based on its occurance
       LemmaValues[Word] = LemmaValues[Word] / WordCounter[Word]
   return  LemmaValues


def BuildCSV(Dict):
   Words = list(Dict.keys())
   Sentiments = list(Dict.values())

   Sentiments, Words = (list(t) for t in zip(*sorted(zip(Sentiments, Words), reverse=True)))  # sorting in descending order

   WordData = []
   i = 0
   while i < len(Words):
       WordData.append([Words[i], Sentiments[i]])
       i += 1
   MostNegative = WordData[-500:]
   MostPositive = WordData[:500]
   with open('WordsAndSentiment.csv', 'w', newline='') as file:
       writer = csv.writer(file)
       writer.writerow(['Lemma', 'Sentiment'])
       writer.writerows(MostPositive)
       writer.writerows(MostNegative)

Main()
