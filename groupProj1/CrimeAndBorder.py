import os
import csv
import urllib.request
import urllib
import matplotlib
import scipy
from bs4 import BeautifulSoup
from matplotlib import pyplot
import re
import geopy.distance


BaseURL = "https://en.wikipedia.org/wiki/List_of_United_States_cities_by_crime_rate"
CityCrimes = {}
CityLinks={}
CityCords={}
CheckedCities={}
CityCoeff = {}


def getDocument(url): # Tries to open a file locally, if it cannot it will download and keep the file in the /data/
   i = url.rsplit('/', 1)
   i = 'data/' + i[1] + '.html'
   if not os.path.exists("data"):
       os.mkdir("data")
   if not os.path.exists(i):
       print("Downloading:" + i)
       urllib.request.urlretrieve(url, i)
       html = urllib.request.urlopen(url).read()
       soup = BeautifulSoup(html, 'html.parser')
       return soup
   if os.path.exists(i):
       with open(i, encoding='utf8') as file:
           contents = BeautifulSoup(file, "lxml")
           return contents


def GetCityCrimes(): # extracts the crimerates, citynames, and direct city links
       soup = getDocument(BaseURL)
       ListOfCities = []
       ListOfLinks = []
       TempList = []
       ListOfCrimeRates = []
       for row in soup.table.findAll('a'): # gets links + names for each city removes
           A = row.get('href')
           A = "https://en.wikipedia.org" + A
           B = row.get('title')
           if CheckIfCity(A) and B not in ListOfCities and B != "District of Columbia":
               ListOfLinks.append(A)
               ListOfCities.append(B)
           else:
               None
       for row in soup.table.tbody.findAll("tr"): # Gets the violent crime rate for each city
           A = row.findAll('td')
           if A != []:
               TempList.append(A)
       i = 0
       while i < len(TempList):   # Removes irrelevant values
           test = str(TempList[i][3])
           test = cleanhtml(test)
           try:
               test = float(test)
               ListOfCrimeRates.append(test)
           except:
               del ListOfCities[i]
               del ListOfLinks[i]
           i+=1
       print("Finished Pass - populating CityLinks")
       populatedict(ListOfCities, ListOfLinks, CityLinks)
       print("Finished Pass - populating CityCrimes")
       populatedict(ListOfCities, ListOfCrimeRates, CityCrimes)

def CheckIfCity(Var): # Given a url it will check the category returns true if not a state
   Soup = getDocument(Var)
   Type = Soup.find(class_="category").get_text()

   try:
       if Type.lower() == "state":
           return False
       Test = Soup.find(class_="fn org").get_text()
   except:
       return False
   return True

def populatedict(ListKeys, ListValues, Dict): # Takes 3 arguments: Key and Value along with dictionary to populate
   i = 0
   while i != len(ListKeys):
      try:
       Dict[ListKeys[i]] = ListValues[i]
       i+=1
      except:
        print("failed to populate")
        i+=1

def cleanhtml(raw_html):  # This code block was retrieved from stackoverflow, its a regex function to strip tags
 cleanr = re.compile('<.*?>')
 cleantext = re.sub(cleanr, '', raw_html)
 return cleantext

def GetCoords(): # Will use the coordinates and links to cities dictionary to extract the coordinates
       Keys = list(CityLinks.keys())
       Values = list(CityLinks.values())
       Distances = []
       i = 0
       while i < len(Values):
           CityDesc = urllib.request.urlopen(Values[i])
           html = CityDesc.read()
           soup = BeautifulSoup(html, "html.parser")
           text = soup.find(class_="geo").get_text()
           SplitText = text.split("; ")
           lat = abs(float(SplitText[0]))
           long = abs(float(SplitText[1]))
           ShortestDistance = (calcDistance(lat, long))
           Distances.append(ShortestDistance)
           i+=1
       populatedict(Keys, Distances, CityCords)

def calcDistance(lat, long): # Calculates distance based on lat and long
   r1 = geopy.distance.geodesic((lat, long), (32.5556, 117.0470)).km  # San Ysidro
   r2 = geopy.distance.geodesic((lat, long), (32.6927, 114.6277)).km  # Yuma
   r3 = geopy.distance.geodesic((lat, long), (32.2226, 110.9747)).km  # Tucson
   r4 = geopy.distance.geodesic((lat, long), (31.7619, 106.4850)).km  # El Paso
   r5 = geopy.distance.geodesic((lat, long), (27.5036, 99.5076)).km  # Laredo
   r6 = geopy.distance.geodesic((lat, long), (29.3709, 100.8959)).km  # Del Rio
   r7 = geopy.distance.geodesic((lat, long), (25.9017, 97.4975)).km  # Brownsville
   results = [r1, r2, r3, r4, r5, r6, r7]
   return min(results)



def CalcCorr(): # Calculates the corr between distance and crime.
   CrimeRate = list(CityCrimes.values())
   Distance = list(CityCords.values())
   temp = scipy.corrcoef(Distance, CrimeRate)
   with open("Correlation.txt", "w") as file:
       print(temp)
       temp = str(temp)
       print(temp)
       file.write(temp)

def BuildCSVprintTable(): # Creates a CSV from the created dictionaries and creates a scatterplot
   Cities = list(CityCrimes.keys())
   CityDistances = list(CityCords.values())
   CrimeLevel = list(CityCrimes.values())
   CityData = []
   i = 0
   while i < len(Cities):
       CityData.append([Cities[i], CityDistances[i], CrimeLevel[i]])
       i+=1
   with open('CitiesandCrime.csv', 'w', newline='') as file:
       writer = csv.writer(file)
       writer.writerow(['City', 'Distance to border', 'Crime Rate'])
       writer.writerows(CityData)
   matplotlib.pyplot.scatter(CityDistances, CrimeLevel, c='red', marker="4", label='Crime vs Distance')
   matplotlib.pyplot.xlabel("Distance to closest border city")
   matplotlib.pyplot.ylabel("Crime per 100,000 people")
   matplotlib.pyplot.legend(loc='upper left')
   matplotlib.pyplot.show()

GetCityCrimes()
GetCoords()
CalcCorr()
BuildCSVprintTable()
