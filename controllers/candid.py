from app import app 
from flask import render_template, request, session 
import numpy as np

from utils import get_db_connection
from models.index_model import get_aunt
from models.candid_model import get_ovz_search, get_spec, get_city, get_vacancy, get_exp, get_group, get_obraz

def to_tuple(list_char):
    if len(list_char) != 0:
        tup = tuple(np.array(list_char + ['-1'], int))
    else:
        tup = '-9'

    return tup

def to_tuple_2(list_char):
    if len(list_char) != 0:
        tup = tuple(np.array(list_char + ['-1'], str))
    else:
        tup = '-9'

    return tup


@app.route('/candid', methods=['get'])

def candid():
    conn = get_db_connection()
    search = session['search']
    company = session['company']
    city_db = get_city(conn)
    exp_db = get_exp(conn)
    group_db = get_group(conn)
    obraz_db = get_obraz(conn)
    df_vacancy = get_vacancy(conn, session['company'])

    spec = ()
    list_city = ()
    list_exp = ()
    list_group = ()
    list_obraz = ()
    test = 0

    if request.values.get('Войти1') == '1':
        login = str(request.values.get('login'))
        passw = str(request.values.get('password'))

        aunt_df = get_aunt(conn, login, passw)

        company = aunt_df.loc[0, 'id_comp']
        session['company'] = int(company)
        session['search'] = search

    if session['company'] != '':

        spec_ser = []
        spec = get_spec(conn, session['search'])

        for i in spec['id_spec']:
            spec_ser.append(i)
        ovz_db = get_ovz_search(conn, to_tuple(spec_ser), list_city, list_exp, list_obraz, list_group)
        df_vacancy = get_vacancy(conn, session['company'])
        

    if session['search'] != '' :

        if request.values.get('search_bar'):
            searchs = str(request.values.get('search_bar'))
            session['search'] = searchs

        if request.values.get('city[]'):
            list_city = to_tuple(request.values.getlist('city[]'))

        if request.values.get('group[]'):
            list_group = to_tuple_2(request.values.getlist('group[]'))
        
        if request.values.get('exp[]'):
            list_exp = to_tuple_2(request.values.getlist('exp[]'))

        if request.values.get('obraz[]'):
            list_obraz = to_tuple_2(request.values.getlist('obraz[]'))

        if request.values.get('Очистить'):
            list_city = ()
            list_exp = ()
            list_group = ()
            list_obraz = ()

        spec_ser = []
        spec = ''
        spec = get_spec(conn, session['search'])

        for i in spec['id_spec']:
            spec_ser.append(i)

        ovz_db = get_ovz_search(conn, to_tuple(spec_ser), list_city, list_exp, list_obraz, list_group)

    elif request.values.get('search_bar'):
            
            if request.values.get('city[]'):
                list_city = to_tuple(request.values.getlist('city[]')) 
            
            if request.values.get('group[]'):
                list_group = to_tuple_2(request.values.getlist('group[]'))
            if request.values.get('exp[]'):
                list_exp = to_tuple_2(request.values.getlist('exp[]'))

            if request.values.get('obraz[]'):
                list_obraz = to_tuple_2(request.values.getlist('obraz[]'))
            if request.values.get('Очистить'):
                list_city = ()
                list_exp = ()
                list_group = ()
                list_obraz = ()

            searchs = str(request.values.get('search_bar'))
            session['search'] = searchs
            spec_ser = []
            spec = ''
            spec = get_spec(conn, session['search'])

            for i in spec['id_spec']:
                spec_ser.append(i)
            ovz_db = get_ovz_search(conn, to_tuple(spec_ser), list_city, list_exp, list_obraz, list_group)



    else:
        if request.values.get('city[]'):
            list_city = to_tuple(request.values.getlist('city[]')) 

        if request.values.get('group[]'):
            list_group = to_tuple_2(request.values.getlist('group[]'))
        if request.values.get('exp[]'):
            list_exp = to_tuple_2(request.values.getlist('exp[]'))

        if request.values.get('obraz[]'):
            list_obraz = to_tuple_2(request.values.getlist('obraz[]'))
        if request.values.get('Очистить'):
            list_city = ()
            list_exp = ()
            list_group = ()
            list_obraz = ()

        elif session['search'] == '':

            session['search'] = ''


        ovz_db = get_ovz_search(conn, search, list_city, list_exp, list_obraz, list_group) 

    return render_template(
        'candid.html',
        ovz_db=ovz_db,
        search = session['search'],
        spec = list,
        city=list_city,
        exp = list_exp,
        obraz = list_obraz,
        group = list_group,
        city_db = city_db,
        exp_db = exp_db,
        group_db = group_db,
        obraz_db = obraz_db,
        df_vacancy = df_vacancy,
        len=len,
        company = session['company'],
        str = str
    )

if __name__ == "__main__":
    app.run(debug=True)

