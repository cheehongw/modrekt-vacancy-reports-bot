# Initial setup:

1. Clone this repo
2. Create a `.env` file in the root of the project directory
3. For each default section seen in the `db.ini` file, there are placeholders for certain key-value pairs. Example from the current `db.ini` file:

```
[elephantsql]  #default
host=satao.db.elephantsql.com
database=${ELEPHANTUSER}
user=${ELEPHANTUSER}
password=${ELEPHANTSQL}
```
The values `${ELEPHANTUSER}` and `${ELEPHANTSQL}` are placeholders for username and password to access the elephantDB. These secret values are stored as key-value pairs in the `.env` file, or as `config vars` in heroku deployment:

```
#elephantsql
ELEPHANTSQL=hunter2
ELEPHANTUSER=admin
```

Otherwise, you can directly replace these placeholder values in the `db.ini` with the corresponding secret, but you will have to include `db.ini` in your `.gitignore` file.

There are 3 default sections in the `db.ini` file. They are default sections because these sections are used in line #10 and #12 of `main.py` and line #4 of `config.py`. You can specify alternative sections to use by changing the values at said lines.

The `[postgresql]` and `[telebot_public]` sections in the repo's `db.ini` file are examples of alternative sections.

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