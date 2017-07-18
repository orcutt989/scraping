import requests
from bs4 import BeautifulSoup
from collections import Counter
from nltk.corpus import stopwords
from nltk.corpus import brown
from itertools import chain

main_url="https://weworkremotely.com"
stopwords = set(stopwords.words('english'))
words = set(brown.words())
stopwords = stopwords.union(words)
stopwords.add(" ")
punctuation = "!\"$%&'()*+,-./:;<=>?@[\]^_`{|}~"
links = []
i=0
text = chain()

# put all urls into an array
r = requests.get(main_url)
soup = BeautifulSoup(r.content, 'lxml')
for link in soup.findAll('a'):
    if link.get('href').startswith('/jobs/'):
        links.append(link.get('href'))


# iterate over links in array and add them to generator
for i in range(len(links)):
    url=main_url+links[i]
    r = requests.get(url)
    print(r)
    print(url)
    soup = BeautifulSoup(r.content, 'lxml')
    text = chain((''.join(s.findAll(text=True))for s in soup.findAll(class_='listing-container')),text)

#  can loop this
'''url="https://weworkremotely.com/jobs/5051-ruby-on-rails-developer"
r = requests.get(url)
soup = BeautifulSoup(r.content, 'lxml')
text = chain((''.join(s.findAll(text=True))for s in soup.findAll(class_='listing-container')),text)'''

# turn generator into counter with values and counts
# gets rid of punctuation and separates values
c = Counter((x.rstrip(punctuation).lower() for y in text for x in y.split()))

# print (c.most_common()) # prints most common words staring at most common.

# words appearing more than 5 times
# print ([x for x in c if c.get(x) > 0 and x not in stopwords])

# print values and counts descending by most common
for value, count in c.most_common():
    # make sure its not in stopwords and occurs at least 5 times
    if(value not in stopwords and count > 20):
        print(value, count)