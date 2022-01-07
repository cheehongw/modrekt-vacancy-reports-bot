Initial setup:

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