
from bs4 import BeautifulSoup
from lxml import etree
import requests
import dateutil.parser as dp
  
  
URL = "https://solana.stackexchange.com/questions/2306/are-wallet-addresses-created-or-are-they-discovered"
  
HEADERS = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',\
            'Accept-Language': 'en-US, en;q=0.5'})
  
webpage = requests.get(URL, headers=HEADERS)
soup = BeautifulSoup(webpage.content, "html.parser")
dom = etree.HTML(str(soup))
print("Question Title -",dom.xpath('//*[@id="question-header"]/h1/a')[0].text)

questionUpvoteCount = dom.xpath('(//*[@itemprop="upvoteCount"])[1]')[0].text.strip()
print("Question Upvotes -",int(questionUpvoteCount))

numAnswers = int(dom.xpath('//*[@id="answers-header"]/div/div[1]/h2/span')[0].text.strip())
print("Number Of Answers -", numAnswers)

qelem = soup.find(attrs={"itemprop" : "dateCreated"})
print("Question Created on (UNIX timestamp)-",int(dp.parse(qelem['datetime']).timestamp()))


