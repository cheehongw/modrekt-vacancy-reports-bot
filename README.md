# Initial setup:

1. Clone this repo
2. Create a `db.ini` file in the root of the project directory
3. Inside the file, include the following sections with key-value pairs:
```
[postgresql]
host=<specify host url here>
database=<specify db name>
user=<specify user account>
password=<your password>

[telebot]
token=<your token>
parse_mode=None
```
example:
```
[postgresql]
host=localhost
database=master
user=postgres
password=123456

[telebot]
token=abcdgaksf:23641273uehwbdeh
parse_mode=None
````
The database port is 5432 by default.

To include other database hosts, just add the same 5 lines with a different section header like so:

```
[postgresql]
host=<specify host url here>
database=<specify db name>
user=<specify user account>
password=<your password>

[hostnumber2]
host=<specify host url here>
database=<specify db name>
user=<specify user account>
password=<your password>
```

# Vacancy Reports Folder

This folder contains all the vacancy reports from previous rounds.
The naming convention is: `{year} Sem {semester} Round {round}.pdf`
Example: `2020 Sem 2 Round 1.pdf`

For the `year` variable, if the academic year is `AY19/20`, then year will be `2019`. 
Always take the lower year in an academic year.

## Inspiration
 During modreg, we wanted some way of quickly looking up old vacancy reports to gauge the trend in the number of vacancies left for a particular mod. 

There was hardly any archive of past year vacancy reports (except for 1 reddit thread)  and hence the idea for a vacancy report scraper/database and a python bot to query the database

## What it does
The frontend is a bot that queries the postgresql database.
On the back, pdfs of old vacancy reports are fed through a scraper to generate the relevant tables and stored into the database.

## How we built it
1. scrape pdfs using tabula
2. perform data cleaning on the scraped data
3. insert clean data into postgresql database
4. write some functions to query the database
5. have a python bot invoke these functions

## Challenges we ran into
dealing with panda dataframes

## Accomplishments that we're proud of
- hosting a postgresql db
- good workflow implemented into the scraper so more vacancy reports can be added into the database as they come.

## What we learned
python-telegram-bot, postgresql, data cleaning

## What's next for modrekt vacancy reports bot (mvrb)
- we are missing vacancy reports for sem 1!!!
- expand the different ways data can be queried
- move away from text-based to image-based data visualisation for better viewing experience
- perform normalization on the database