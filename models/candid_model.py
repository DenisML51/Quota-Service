import pandas as pd 


def get_ovz_search(conn, search, city, exp, obraz, group):
    if search != '':
        search_str = '''WHERE  id_descript = 3 AND '''
        if len(search) != 0:
            search_str += f'''id_spec IN {tuple(search)} AND '''

        if len(city) != 0 and city[0] != -1:
            search_str += f'''id_city IN {tuple(city)} AND '''

        if len(exp) != 0 and exp[0] != '-1':
            search_str += f'''ovz_descr.descr IN {tuple(exp)} AND '''
        
        if len(obraz) != 0 and obraz[0] != '-1':
            search_str += f'''ovz_descr.descr IN {tuple(obraz)} AND '''

        if len(group) != 0 and group[0] != '-1':
            search_str += f'''ovz_descr.descr IN {tuple(group)} AND '''



        search_str += '''1=1'''

        df = pd.read_sql(
                f'''
                SELECT id_ovz, ovz.id as ID, city_name as Город, specialization.specialization as Специальность, descr as Описание
                FROM ovz_descr
                JOIN ovz USING (id_ovz)
                JOIN city USING (id_city)
                JOIN descript USING (id_descript)
                JOIN specialization USING (id_spec) {search_str}
                ''', conn
            )
        return df
    else:
        search_str = '''WHERE  id_descript = 3 AND '''

        if len(city) != 0 and city[0] != -1:
            search_str += f'''id_city IN {tuple(city)} AND '''


        if len(exp) != 0 and exp[0] != '-1':
            search_str += f'''ovz_descr.descr IN {tuple(exp)} AND '''
        
        if len(obraz) != 0 and obraz[0] != '-1':
            search_str += f'''ovz_descr.descr IN {tuple(obraz)} AND '''

        if len(group) != 0 and group[0] != '-1':
            search_str += f'''ovz_descr.descr IN {tuple(group)} AND '''



        search_str += '''1=1'''

        df = pd.read_sql(
        f'''
        SELECT id_ovz, ovz.id as ID, city_name as Город, specialization.specialization as Специальность, descr as Описание
        FROM ovz_descr
        JOIN ovz USING (id_ovz)
        JOIN city USING (id_city)
        JOIN descript USING (id_descript)
        JOIN specialization USING (id_spec)  {search_str}

        ''', conn
    )
        return df


def get_spec(conn, search):
    return pd.read_sql(
            '''
    SELECT id_spec
    FROM specialization
    WHERE specialization = :l
    ''',conn, params={'l': str(search)}
        
    )

def get_city(conn):
    return pd.read_sql(
        '''
SELECT * FROM city''', conn
    )

def get_exp(conn):
    return pd.read_sql(
        '''
SELECT DISTINCT descr
FROM ovz_descr
WHERE id_descript = 3''' , conn
    )

def get_group(conn):
    return pd.read_sql(
        '''
SELECT DISTINCT(descr)
FROM ovz_descr
WHERE id_descript = 1''' , conn
    )


def get_obraz(conn):
    return pd.read_sql(
        '''
SELECT DISTINCT(descr)
FROM ovz_descr
WHERE id_descript = 2''' , conn
    )


def get_vacancy(conn, company):
    return pd.read_sql(
        '''
SELECT id_comp_vacancy, vac_name, cv_need_spec, cv_need_exp
FROM comp_vacancy
JOIN vacancy USING (id_vacancy)
WHERE id_company = :p''', conn, params={'p': company}
    )

def add_vac(conn, ovz, vac, comp):
    cur = conn.cursor()
    cur.execute(
        '''insert into employee(id_company, id_ovz, id_comp_vacancy, job_start) 
        VALUES (:p_comp, :p_ovz, :p_vac, DATE('now'))''', {"p_comp": comp, "p_ovz": ovz, "p_vac": vac}
    )
    conn.commit()
    return cur.lastrowid

def get_employee(conn, comp):
    return pd.read_sql(
        '''
SELECT id, specialization, city_name, descr, id_comp_vacancy
FROM employee
JOIN ovz USiNG (id_ovz)
JOIN specialization USING (id_spec)
JOIN ovz_descr USING (id_ovz)
JOIN city USING (id_city)
WHERE id_descript = 3 AND id_company = :p''', conn, params={'p': comp}
    )