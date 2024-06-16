import pandas as pd 

def get_vacancy2(conn, company, id):
    return pd.read_sql(
        '''
SELECT id_comp_vacancy, vac_name, vac_desc, cv_need_spec
FROM comp_vacancy
JOIN vacancy USING (id_vacancy)
WHERE id_company = :p AND id_comp_vacancy = :p2''', conn, params={'p': company, 'p2': id}
    )

def get_employee2(conn, comp, id):
    return pd.read_sql(
        '''
SELECT id_employee, id, specialization, city_name, descr, id_comp_vacancy
FROM employee
JOIN ovz USiNG (id_ovz)
JOIN specialization USING (id_spec)
JOIN ovz_descr USING (id_ovz)
JOIN city USING (id_city)
WHERE id_descript = 3 AND id_company = :p AND id_comp_vacancy = :p2''', conn, params={'p': comp, 'p2': id}
    )

def add_status1(conn, empl):
    cur = conn.cursor()
    cur.execute(    
        '''UPDATE employee 
        SET status1 = '1'
        WHERE id_employee = :p_empl;''', {"p_empl": empl}
    )
    conn.commit()
    return cur.lastrowid

def add_status2(conn, empl):
    cur = conn.cursor()
    cur.execute(    
        '''UPDATE employee 
        SET status2 = '1'
        WHERE id_employee = :p_empl;''', {"p_empl": empl}
    )
    conn.commit()
    return cur.lastrowid

def add_status3(conn, empl):
    cur = conn.cursor()
    cur.execute(    
        '''UPDATE employee 
        SET status3 = '1'
        WHERE id_employee = :p_empl;''', {"p_empl": empl}
    )
    conn.commit()
    return cur.lastrowid

def get_status(conn, empl):
    return pd.read_sql(
        '''
SELECT status1, status2, status3
FROM employee
WHERE id_employee = :p''', conn, params={'p': empl}
    )

def add_worker(conn, company, vacancy, employee):
    cur = conn.cursor()
    cur.execute(    
        '''INSERT INTO worker (id_company, id_comp_vacancy, id_ovz)
        VALUES (:p1, :p2, :p3)''', {'p1': company, 'p2': vacancy, 'p3': int(employee)}
    )
    conn.commit()
    return cur.lastrowid

def get_ovz_emp(conn, employee, vacancy):
    return pd.read_sql(
        '''
SELECT id_ovz 
FROM employee 
WHERE id_employee = :p AND id_comp_vacancy = :p2''', conn, params={'p': employee, 'p2': vacancy}
    )
