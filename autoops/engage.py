# Importing Libraries
from urllib import response
from dotenv import dotenv_values
from airtable import airtable
import urllib
import requests
import dateutil.parser as dp

# Getting .env file config
config = dotenv_values(".env")

# Setting necessary keys and IDs
API_KEY = config["API_KEY"]
XP_BASE_ID = config["XP_BASE_ID"]
XP_PQ_ID = config["XP_PQ_ID"]
XP_USER_ID = config["XP_USER_ID"]

# Makes an airtable object which takes baseID and API_KEY
at = airtable.Airtable(XP_BASE_ID, API_KEY)

# Returns an iterable with data
question_tab = at.iterate(XP_PQ_ID)
user_tab = at.iterate(XP_USER_ID)

question_dict = {}
local_question_dict = {}

# Function which returns the XP accumulated
def calcUserXP(userID):
    print("Processing user - ",userID)
    apiurl = "https://api.stackexchange.com/2.3/users/"+str(userID)+"/answers?site=solana"
    response = requests.get(apiurl)
    resp = {}
    presp = response.json()
    ansdata = presp["items"]
    resp["AccXP"] = 0
    if(len(ansdata)==0):
        pass
    else:
        for x in ansdata:
            qid = x["question_id"]
            acceptance = x["is_accepted"]
            if(acceptance and question_dict.get(qid,None)==None and local_question_dict.get(qid,None)==None):
                resp["AccXP"] += 5
                local_question_dict[qid] = userID
    return(resp)

for x in question_tab:
    question_dict[x['fields']['QuestionID']] = x['fields']['AcceptedUser']

# Prints the processed questions
print(question_dict)

for x in user_tab:
    sid = x['fields']['Stack Exchange Id']
    xpresp = calcUserXP(sid)
    currentXP = x['fields']['XPAccumilated']
    cumulativeXP = x['fields']['CumulativeXP']
    currentXP += xpresp["AccXP"]
    cumulativeXP += xpresp["AccXP"]
    print(sid , currentXP, cumulativeXP)
    print("Record ID -",x["id"])
    fields = {}
    fields['XPAccumilated'] = currentXP
    fields['CumulativeXP'] = cumulativeXP
    at.update(XP_USER_ID,x["id"],fields)

usedQuestionAdd = []
ct = 0
for x in local_question_dict:
    print(x, local_question_dict[x])
    fields = {}
    fields['QuestionID'] = x
    fields['AcceptedUser'] = local_question_dict[x]
    usedQuestionAdd.append(fields)
    at.create(XP_PQ_ID,usedQuestionAdd[ct])
    ct+=1