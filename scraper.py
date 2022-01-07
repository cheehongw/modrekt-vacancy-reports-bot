from numpy import NaN
import pandas
import os
import tabula
from db import connect
from config import sqlalchemy_engine_str
from sqlalchemy import create_engine

conv_dict = {
    'Faculty/School' : 'faculty_school',
    'Department' : 'department',
    'Module Code': 'module_code',
    'Module Title': 'module_title',
    'Module Class': 'module_class',
    'UG' : 'ug', 'GD' : 'gd', 'DK' : 'dk', 'NG' : 'ng', 'CPE' : 'cpe'
}

def get_round_info(filepath):
    filename = os.path.basename(filepath)
    args = filename.split()
    roundinfo = {
        'year' : int(args[0]), 
        'semester': int(args[2]),
        'round': int(args[4].split('.')[0])
    }

    return roundinfo

def pdf_to_dataframe(filepath):
    #convert pdf to dataframe
    df = df = tabula.read_pdf(filepath, output_format='dataframe', 
        encoding='mbcs', pages='all', pandas_options={'encoding' : 'mbcs', 'engine' : 'python'})[0]

    #keep rows where Module Code != 'Module Code' 
    df = df[df['Module Code'] != 'Module Code']
    df = df.reset_index().drop(columns='index')

    #merge rows that are broken due to formatting
    group = df['Module Code'].notna().cumsum()
    df['Department'] = df.groupby(group)['Department'].transform('sum')
    df['Faculty/School'] = df.groupby(group)['Faculty/School'].transform('sum')
    df['Module Title'] = df.groupby(group)['Module Title'].transform('sum')
    df['Module Class'] = df.groupby(group)['Module Class'].transform('sum')
    df = df.dropna(subset=['Module Code'])
    df = df.reset_index().drop(columns='index')

    #fix nullish values and other formatting mistakes
    df = df.rename(columns=conv_dict)
    df = df.replace({'×':pandas.NA, '\r' : ''}, regex=True)   
    df = df.apply(pandas.to_numeric, errors='ignore')

    #add columns for year, semester and round
    df = df.assign(**get_round_info(filepath))

    df = df.convert_dtypes()
    #print(df.dtypes)
    return df

def upload_to_SQL_table(df, table_name):
    engine = create_engine(sqlalchemy_engine_str())
    df.to_sql(table_name, engine, if_exists='append', index=False)


def create_SQL_table(table_name):
    create_table = """CREATE TABLE IF NOT EXISTS {0} (
        faculty_school varchar(256) NOT NULL,
        department varchar(256) NOT NULL,
        module_code varchar(20) NOT NULL,
        module_title varchar(256) NOT NULL,
        module_class varchar(128) NOT NULL,
        year INTEGER NOT NULL,
        semester INTEGER NOT NULL,
        round INTEGER NOT NULL,
        ug INTEGER,
        gd INTEGER,
        dk INTEGER,
        ng INTEGER,
        cpe INTEGER);
        """.format(table_name)
    connection = connect()
    cursor = connection.cursor()
    cursor.execute(create_table)
    connection.commit()