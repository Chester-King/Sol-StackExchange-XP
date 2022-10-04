# Importing Libraries
from tkinter.tix import Tree
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
USER_TABLE_ID = config["USER_TABLE_ID"]
QUESTION_TABLE_ID = config["QUESTION_TABLE_ID"]

# Makes an airtable object which takes baseID and API_KEY
at = airtable.Airtable(BASE_ID, API_KEY)

data_tab = at.iterate(QUESTION_TABLE_ID)

def checklink(URL):
    trurl = URL.strip()
    qid = int(trurl)
    apiurl = "https://api.stackexchange.com/2.3/questions/"+str(qid)+"?site=solana"
    response = requests.get(apiurl)
    resp = {}
    presp = response.json()
    if(len(presp["items"])==0):
        return(False,trurl)
    else:
        return(True,trurl)


checklink("143141341")
# for x in data_tab:
