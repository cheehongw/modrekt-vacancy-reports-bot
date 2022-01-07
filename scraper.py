from numpy import NaN
import pandas, os, tabula

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
    df = df.replace({'\r' : ''}, regex=True) #clean up \r in 
    df = df.replace({'×':pandas.NA, 'x':pandas.NA, '-':pandas.NA}) 
    df = df.apply(pandas.to_numeric, errors='ignore')

    #add columns for year, semester and round
    df = df.assign(**get_round_info(filepath))

    df = df.convert_dtypes()
    print('year: {year}, sem: {semester}, round: {round}'.format(**get_round_info(filepath)))
    print(df.dtypes)
    return df