# Importing Libraries
from dotenv import dotenv_values
from airtable import airtable

# Getting .env file config
config = dotenv_values(".env")

# Setting necessary keys and IDs
API_KEY = config["API_KEY"]
BASE_ID = config["BASE_ID"]
TABLE_ID = config["WRITE_TABLE_ID"]

# Makes an airtable object which takes baseID and API_KEY
at = airtable.Airtable(BASE_ID, API_KEY)

# Data object - A record in the airtable will be added - with "Dummy" as data under the "Name" field
dummydata = { "Name" : "Dummy"}

# Creating a new record in the airtable
data_tab = at.create(TABLE_ID,dummydata)