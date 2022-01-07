from configparser import ConfigParser

section_to_use = "elephantsql" #change this accordingly

def config(filename="db.ini", section=section_to_use):
    parser = ConfigParser()
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section{0} is not found in the {1} file.'.format(section, filename))

    #parser.clear()
    return db
    
def sqlalchemy_engine_str(filename="db.ini", dialect="postgresql"):
    config_dict = config(filename=filename, section=section_to_use)
    config_dict['dialect'] = dialect
    
    output = '{dialect}://{user}:{password}@{host}:5432/{database}'.format(**config_dict)

    return output