# Importing Libraries
from dotenv import dotenv_values
from airtable import airtable

# Getting .env file config
config = dotenv_values(".env")

# Setting necessary keys and IDs
API_KEY = config["API_KEY"]
BASE_ID = config["BASE_ID"]
TABLE_ID = config["READ_TABLE_ID"]

# Makes an airtable object which takes baseID and API_KEY
at = airtable.Airtable(BASE_ID, API_KEY)

# Returns an iterable with data
data_tab = at.iterate(TABLE_ID)

for x in data_tab:
    # In each iteration x consist of a OrderedDict with record ID, createdTime and the table Data
    # Right now we printing the data in the 'Name' field in the table
    print(x['fields']['Name'])