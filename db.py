import psycopg2, pandas, os, scraper, sqlalchemy, config
from config import sqlalchemy_engine_str

#import config function that returns a config dictionary
from config import config

def connect():
    params = config()
    connection = psycopg2.connect(**params)
    connection.autocommit = True
    return connection

def upload_to_SQL_table(df, table_name, hard_reset=False):
    engine = sqlalchemy.create_engine(sqlalchemy_engine_str())
    if hard_reset:
        df.to_sql(table_name, engine, if_exists='replace', index=False)
    else:
        df.to_sql(table_name, engine, if_exists='append', index=False)


def insert_vacancy_reports(table_name='raw', hard_reset=False):
    directory_str = 'Vacancy Reports'
    directory = os.fsencode(directory_str)
    df_xs = []

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        df_xs.append(scraper.pdf_to_dataframe('{0}/{1}'.format(directory_str, filename)))
    
    df = pandas.concat(df_xs).drop_duplicates().reset_index(drop=True)
    upload_to_SQL_table(df, table_name, hard_reset=hard_reset)
    cursor = connect().cursor()
    f = open('queries/delete_dupes.sql', mode='r')
    q = f.read()
    f.close()
    cursor.execute(q)



#---------testing purposes--------

#insert_vacancy_reports(table_name='test', hard_reset=True)

#---------------------------------

# def create_SQL_table(table_name):
#     create_table = """CREATE TABLE IF NOT EXISTS {0} (
#         faculty_school varchar(256) NOT NULL,
#         department varchar(256) NOT NULL,
#         module_code varchar(20) NOT NULL,
#         module_title varchar(256) NOT NULL,
#         module_class varchar(128) NOT NULL,
#         year INTEGER NOT NULL,
#         semester INTEGER NOT NULL,
#         round INTEGER NOT NULL,
#         ug INTEGER,
#         gd INTEGER,
#         dk INTEGER,
#         ng INTEGER,
#         cpe INTEGER);
#         """.format(table_name)
#     connection = connect()
#     cursor = connection.cursor()
#     cursor.execute(create_table)
#     connection.commit()