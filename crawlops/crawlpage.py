# Importing Libraries
from bs4 import BeautifulSoup
from lxml import etree
import requests
import dateutil.parser as dp
  
# Solana StackExchange URL
URL = "https://solana.stackexchange.com/questions/1554/keypair-pubkey-mismatch-when-partial-signing-python"

# Headers
HEADERS = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',\
            'Accept-Language': 'en-US, en;q=0.5'})
  
# Getting the webpage HTML
webpage = requests.get(URL, headers=HEADERS)

# Creating a soup object
soup = BeautifulSoup(webpage.content, "html.parser")
dom = etree.HTML(str(soup))

# Extracting Question Title
print("Question Title -",dom.xpath('//*[@id="question-header"]/h1/a')[0].text)

# Extracting Question Upvote Count
questionUpvoteCount = dom.xpath('(//*[@itemprop="upvoteCount"])[1]')[0].text.strip()
print("Question Upvotes -",int(questionUpvoteCount))

# Extracting Number of answers to question
numAnswers = int(dom.xpath('//*[@id="answers-header"]/div/div[1]/h2/span')[0].text.strip())
print("Number Of Answers -", numAnswers)

# If the answer is accepted - Only fetch the accepted answer's upvotes and author
if(len(dom.xpath('//*[@itemprop="acceptedAnswer"]'))>0):
    print("Up votes on answer -",dom.xpath('//*[@itemprop="acceptedAnswer"]//*[@itemprop="upvoteCount"]')[0].text.strip())
    print("Author of answer - ",dom.xpath('//*[@itemprop="acceptedAnswer"]//*[@itemprop="author"]/a')[0].text.strip())
# If no answer is accepted - Fetch all the upvotes with their authors
else:
    for x in range(numAnswers):
        print("Up votes on answer -",dom.xpath('(//*[@itemprop="upvoteCount"])['+str(x+2)+']')[0].text.strip())
        print("Author of answer - ",dom.xpath('(//*[@itemprop="author"]/a)['+str(x+2)+']')[0].text.strip())

# Extracting Date Created
qelem = soup.find(attrs={"itemprop" : "dateCreated"})
print("Question Created on (UNIX timestamp)-",int(dp.parse(qelem['datetime']).timestamp()))


