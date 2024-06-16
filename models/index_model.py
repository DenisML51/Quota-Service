import pandas as pd 

def get_new_company(conn):
    return pd.read_sql('''
''')

def get_company(conn):
    return pd.read_sql(
        '''SELECT * FROM company''', conn
    )

def get_ovz(conn):
    return pd.read_sql(
        '''SELECT * FROM ovz''', conn
    )

def get_comp_vac(conn):
    return pd.read_sql(
        ''''''
    )

def get_spec(conn, search):
    return pd.read_sql(
        '''
SELECT id_spec
FROM specialization
WHERE specialization == :p''',conn, params={':p': search}
    )

def get_aunt(conn, login, password):
    return pd.read_sql(
        '''
SELECT id_comp
FROM company
WHERE company.comp_login = :p1 AND company.comp_pass = :p2''', conn, params={'p1':login, 'p2':password}
    )