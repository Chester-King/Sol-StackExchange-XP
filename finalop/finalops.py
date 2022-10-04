# Importing Libraries
from urllib import response
from dotenv import dotenv_values
from airtable import airtable
from bs4 import BeautifulSoup
from lxml import etree
import urllib
import requests
import dateutil.parser as dp

# Getting .env file config
config = dotenv_values(".env")

# Setting necessary keys and IDs
API_KEY = config["API_KEY"]
BASE_ID = config["BASE_ID"]
USER_TABLE_ID = config["USER_TABLE_ID"]
QUESTION_TABLE_ID = config["QUESTION_TABLE_ID"]
HEADERS = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',\
            'Accept-Language': 'en-US, en;q=0.5'})

# Function which returns information about the URL
def getqdata(questionID):
    print(questionID)
    apiurl = "https://api.stackexchange.com/2.3/questions/"+str(questionID)+"/answers?site=solana"
    response = requests.get(apiurl)
    resp = {}
    presp = response.json()
    resp["NumberOfAnswers"] = len(presp["items"])
    if(resp["NumberOfAnswers"]==0):
        resp["Upvotes"] = None
        resp["Author"] = None
        resp["Reason"] = "No one has answered this question"
        resp["XP"] = "0"
    else:
        mint = 0
        muser = None
        for x in presp["items"]:
            if(x["is_accepted"]):
                resp["Accepted"] = True
                resp["Upvotes"] = x["score"]
                resp["Author"] = x["owner"]["display_name"]
                resp["Reason"] = "Accepted Answer"
                resp["XP"] = "+10"
                return(resp)
            if(x["score"]>mint):
                mint = x["score"]
                muser = x["owner"]["display_name"]
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

    return(resp)



# Makes an airtable object which takes baseID and API_KEY
at = airtable.Airtable(BASE_ID, API_KEY)

# Returns an iterable with data
user_tab = at.iterate(USER_TABLE_ID)
data_tab = at.iterate(QUESTION_TABLE_ID)

userdb = {}

for x in user_tab:
    userdb[x['fields']['Name (from membername)'][0]] = x['fields']['stackusername']

print(userdb)

pros = {}

for x in data_tab:
    print(x)
    # In each iteration x consist of a OrderedDict with record ID, createdTime and the table Data
    # Right now we printing the data in the 'Name' field in the table
    print(x['fields']['QuestionURL'])
    print(x['fields']['Name (from membername) (from stackuser)'][0])
    superid = x['fields']['Name (from membername) (from stackuser)'][0]
    print("username - ",userdb[superid])
    username = userdb[superid]
    # print(x['fields']['discord'])
    if(pros.get(x['fields']['QuestionURL'],False)):
        at.delete(QUESTION_TABLE_ID,x['id'])
        continue


    
    crawldata = getqdata(x['fields']['QuestionURL'])
    fields = {}
    if(crawldata["NumberOfAnswers"]==0):
        print("No answers")
    elif(username==crawldata["Author"]):
        print("Correct Author - Grant XP")
        fields['Legit'] = True
    else:
        print("Illegal")
        crawldata["Reason"] = "Wrong Username"
        crawldata["XP"] = "0"
    fields['Done'] = True
    fields['Reason'] = crawldata["Reason"]
    fields['XP'] = crawldata["XP"]



    if(fields['Done']==True and fields.get('Legit',False)==True):
        pros[x['fields']['QuestionURL']] = True
        at.update(QUESTION_TABLE_ID,x["id"],fields)
    else:
        at.delete(QUESTION_TABLE_ID,x['id'])