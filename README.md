# Initial setup:

1. Clone this repo
2. Create a `db.ini` file in the root of the project directory
3. Inside the file include the following section with key-value pairs:
```
[postgresql]
host=<specify host url here>
database=<specify db name>
user=<specify user account>
password=<your password>
```
example:
```
[postgresql]
host=localhost
database=master
user=postgres
password=123456
````
The port is 5432 by default.

To include other hosts, just add the same 5 lines with a different section header like so:

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