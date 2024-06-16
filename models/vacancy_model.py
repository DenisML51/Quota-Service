import pandas as pd

def get_vac_comp(conn, company):
    return pd.read_sql(
        '''
SELECT id_comp_vacancy, vac_name, vac_desc, cv_need_spec, cv_need_exp
FROM comp_vacancy
JOIN vacancy USING (id_vacancy)
WHERE id_company = :p''', conn, params={'p': company}
    )

def add_new_vacancy(conn, name, desc):
    cur = conn.cursor()
    cur.execute(
        '''insert into vacancy(vac_name, vac_desc) 
        VALUES (:p_name, :p_desc)''', {"p_name": name, "p_desc": desc}
    )
    conn.commit()
    return pd.read_sql(
                '''
        SELECT id_vacancy 
        FROM vacancy 
        WHERE vac_name = :p1 AND vac_desc = :p2''', conn, params={'p1': name, 'p2': desc}
            )

def add_new_comp_vac(conn, id_vac, company, spec, exp):
    cur = conn.cursor()
    cur.execute(
        '''
INSERT INTO comp_vacancy (id_company, id_vacancy, cv_need_spec, cv_need_exp)
VALUES (:p1, :p2, :p3, :p4)''', {'p1': company, 'p2':id_vac, 'p3': spec, 'p4': exp}
    )

    conn.commit()
    return True