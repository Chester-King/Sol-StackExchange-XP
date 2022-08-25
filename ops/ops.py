# Importing Libraries
from urllib import response
from dotenv import dotenv_values
from airtable import airtable
from bs4 import BeautifulSoup
from lxml import etree
import requests
import dateutil.parser as dp

# Getting .env file config
config = dotenv_values(".env")

# Setting necessary keys and IDs
API_KEY = config["API_KEY"]
BASE_ID = config["BASE_ID"]
TABLE_ID = config["TABLE_ID"]
HEADERS = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',\
            'Accept-Language': 'en-US, en;q=0.5'})

# Function which returns information about the URL
def crawl(URL):
    # Getting the webpage HTML
    webpage = requests.get(URL, headers=HEADERS)

    # Creating a soup object
    soup = BeautifulSoup(webpage.content, "html.parser")
    dom = etree.HTML(str(soup))

    resp = {}
    resp["QuestionTitle"] = dom.xpath('//*[@id="question-header"]/h1/a')[0].text
    resp["QuestionUpvoteCount"] = int(dom.xpath('(//*[@itemprop="upvoteCount"])[1]')[0].text.strip())
    resp["NumberOfAnswers"] = int(dom.xpath('//*[@id="answers-header"]/div/div[1]/h2/span')[0].text.strip())
    if(len(dom.xpath('//*[@itemprop="acceptedAnswer"]'))>0):
        resp["Accepted"] = True
        resp["Upvotes"] = int(dom.xpath('//*[@itemprop="acceptedAnswer"]//*[@itemprop="upvoteCount"]')[0].text.strip())
        resp["Author"] = dom.xpath('//*[@itemprop="acceptedAnswer"]//*[@itemprop="author"]/a')[0].text.strip()
        resp["Reason"] = "Accepted Answer"
        resp["XP"] = "+10"
    else:
        resp["Accepted"] = False
        if(resp["NumberOfAnswers"]>0):
            mint = 0
            muser = None
            for x in range(resp["NumberOfAnswers"]):
                if(int(dom.xpath('(//*[@itemprop="upvoteCount"])['+str(x+2)+']')[0].text.strip())>mint):
                    mint = int(dom.xpath('(//*[@itemprop="upvoteCount"])['+str(x+2)+']')[0].text.strip())
                    muser = dom.xpath('(//*[@itemprop="author"]/a)['+str(x+2)+']')[0].text.strip()
            if(muser==None):
                resp["Upvotes"] = None
                resp["Author"] = None
                resp["Reason"] = "Answer with 0 upvotes"
                resp["XP"] = "0"
            else:
                resp["Upvotes"] = mint
                resp["Author"] = muser
                resp["Reason"] = "Upvotes but no accepted answer"
                resp["XP"] = "+5"
        else:
            resp["Upvotes"] = None
            resp["Author"] = None
            resp["Reason"] = "No one has answered this question"
            resp["XP"] = "0"
    return(resp)



# Makes an airtable object which takes baseID and API_KEY
at = airtable.Airtable(BASE_ID, API_KEY)

# Returns an iterable with data
data_tab = at.iterate(TABLE_ID)

for x in data_tab:
    # In each iteration x consist of a OrderedDict with record ID, createdTime and the table Data
    # Right now we printing the data in the 'Name' field in the table
    # print(x['fields']['QuestionURL'])
    # print(x['fields']['username'])
    # print(x['fields']['discord'])
    if(x['fields'].get('Done')==True):
        continue
    crawldata = crawl(x['fields']['QuestionURL'])
    fields = {}
    if(crawldata["NumberOfAnswers"]==0):
        print("No answers")
    elif(x['fields']['username']==crawldata["Author"]):
        print("Correct Author - Grant XP")
        fields['Legit'] = True
    else:
        print("Illegal")
        crawldata["Reason"] = "Wrong Username"
        crawldata["XP"] = "0"
    fields['Done'] = True
    fields['Reason'] = crawldata["Reason"]
    fields['XP'] = crawldata["XP"]
    print(x["id"])
    at.update(TABLE_ID,x["id"],fields)