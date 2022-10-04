# Solana StackExchange XP System 

Goal: To develop an automated tool which will compute and distribute XP Points to Solana StackExchange contributors and community members. The macro vision can be found [here](https://www.notion.so/chester-king/Instagrant-Proposal-for-Solana-StackExchange-XP-System-574622286d524dfa89180bb41153dba2)

## Why Solana StackExchange XP?

1. In the Web 3.0 community, people with a diverse set of expertise and skillset can be found. With this, it becomes essential to know who has a track record of successful product shipping and who to put your faith & trust into. 
2. This is also the rationale behind the XP System in Superteam to encourage and drive more credibility within the community. 
3. All open source communities aid the development and expansion of an ecosystem. Particularly in the Solana ecosystem, where the majority of the components are actively being developed and tested.
4. To ensure the contributors are recognized and allowed to build their credibility in the ecosystem - I’d like to propose XP allotment automation tool for the Solana StackExchange.  [https://solana.stackexchange.com/](https://solana.stackexchange.com/)
5. This tool will allow the Solana Developer community to become more robust and result in an overall healthy Solana Developer Community.

## Path to final script

`autoops/engage.py`

## Code walk through 

The final code is written in python and here's the line by line breakdown of it

### Libraries used 

* `dotenv` - to get the data from .env file
* `airtable` - airtable wrapper used to perform read and write operations on airtable
* `requests` - used to fetch data from stackexchange API

### Config used

* API_KEY= for API key
* XP_BASE_ID= for BASE ID
* XP_PQ_ID= for processed question table ID
* XP_USER_ID= for user table ID

### Airtable Object

`at = airtable.Airtable(XP_BASE_ID, API_KEY)` this is how airtable object is defined which is used to perform read and write

### Fetching table data

```python
question_tab = at.iterate(XP_PQ_ID)
user_tab = at.iterate(XP_USER_ID)
```

The table data is fetched and stored in the variables

### Creating a hashmap of processed questions

```python
for x in question_tab:
    question_dict[x['fields']['QuestionID']] = x['fields']['AcceptedUser']
```

Hashmap of processed questions is made so that questions are not to be processed again

### Iterating through user table

`sid = x['fields']['Stack Exchange Id']`

fetches stackexchange XP user ID

### XP calculation per user

```python
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
```

Calls Stackexchange API for each user. 
This returns all the answers done by this user with are those accepted marked or not.
Responses of this API is then iterated and it is checked against the `local_question_dict` and against `question_dict` if they have already been processed. Storing and checking against `local_question_dict` helps in making sure a question is not processed in this running of stript.
If the question is accepted and not yet processed then the user receives XP+5. 


### After calculation of XP

Create a fields object that has keys similar to table columns. 
After calculation of XP of each user the airtable is data is updated for that user using the line `at.update(XP_USER_ID,x["id"],fields)`.

### After XP update

```python
for x in local_question_dict:
    print(x, local_question_dict[x])
    fields = {}
    fields['QuestionID'] = x
    fields['AcceptedUser'] = local_question_dict[x]
    usedQuestionAdd.append(fields)
    at.create(XP_PQ_ID,usedQuestionAdd[ct])
    ct+=1
```

After XP update the local processed question hashmap is appended to the airtable processed table data so that next time the script runs it does not process the processed questions this time.

Note - This repo is in active development