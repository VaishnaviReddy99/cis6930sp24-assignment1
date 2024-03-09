# cis6930sp24 -- Assignment0 

Name: Sree Vaishnavi Madireddy

UFID: 87626790

# Assignment Description 
The objective of this project is to extract predominantly tabular data from PDF files and store it in a database. Additionally, the project seeks to derive exploratory insights from the created database.

# How to install
pipenv install

## How to run
pipenv run python assignment0/main.py --incidents sample_url

It can be run as follows:
![](https://github.com/VaishnaviReddy99/cis6930sp24-assignment0/blob/test/output.gif)



## Functions
#### main.py \
parseUrl() -- This method takes each incident url and performs all the requires actions including extracting and printing results

connectAndTestDB() -- This method is responsible for connecting to the in memory database and return the connection object

parseAndFetchResults() -- Responsible for quering the remote url and extracting each page from the pdf

parseEachPage() -- Parses each page and returns the extract text

insertResultSet() -- Responsible for Inserting extracted data into the database

natureTypeState() -- Responsible for printing each nature and the number of times the nature appears

## Database Development
The Database file is in the location 'resources' and the database file is normanpd.db
This file gets created during application runtime if not present.

## Assumptions
a. The provided data parsing algorithm assumes a minimum of four spaces or more between each column. 

b. This code has the assumption that, in the incidents data, if Location is null then Nature is also null. Both the values would     be empty

c. Date/Time, Incident Number, Incident ORI cannot be null/empty


## Bugs
If the incident's nature is present but the location is not, or vice versa, the script would encounter a failure, preventing it from parsing the entire data file.

The result set always prints NULL Nature values wrt their count at the very last.
