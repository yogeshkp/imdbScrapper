import pandas as pd
import requests
from bs4 import BeautifulSoup

url = 'https://www.imdb.com/search/title/?count=100&groups=top_1000&sort=user_rating' # name of the site we are scrapping
response = requests.get(url)
soup = BeautifulSoup(response.content,'html.parser')

movie_name = []
year = []
runTime = []
rating = []
metascore = []
votes = []
gross = []

movie_data = soup.findAll('div',attrs = {'class':
'lister-item mode-advanced'})

for store in movie_data:
  name = store.h3.a.text
  movie_name.append(name)

  year_of_release = store.h3.find('span',class_ = 'lister-item-year text-muted unbold').text.replace('(','').replace(')','')
  year.append(year_of_release)

  runtime = store.p.find('span',class_ = 'runtime').text
  runTime.append(runtime)

  rate = store.find('div',class_ ="inline-block ratings-imdb-rating").text.replace('\n','')
  rating.append(rate)

  meta = store.find('span', class_ = 'metascore').text.replace(' ','') if store.find('span', class_ = 'metascore') else 'none'
  metascore.append(meta)

  value = store.find_all('span',attrs = { 'name': 'nv'})

  vote = value[0].text
  votes.append(vote)

  grosses = value[1].text if len(value) > 1 else 'none'
  gross.append(grosses)

movie_DF = pd.DataFrame({'Name of the Movie': movie_name, 'Year of Release': year, 'Runtime of the Movie': runTime, 'Rating of the Movie':rating, 'Metascore': metascore, 'Total Votes': votes, 'Total Grossed': gross})

movie_DF.index += 1

print(movie_DF.head(30))
#showing the first 30 in the list
