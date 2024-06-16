from app import app 
from flask import render_template, request, session 
import numpy as np

from utils import get_db_connection
from models.candid_model import get_ovz_search, get_spec, get_city, get_vacancy, get_exp, get_group, get_obraz, add_vac, get_employee

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

@app.route('/lichkab', methods=['get'])
def lichkab():
    conn = get_db_connection()
    search = session['search']
    company = session['company']
    if session['id_ovz'] != '':
        session['id_ovz'] = session['id_ovz']
    else:
        session['id_ovz'] = ''

    if session['id_comp_vacancy'] != '':
        session['id_comp_vacancy'] = session['id_comp_vacancy']
    else:
        session['id_comp_vacancy'] = ''


    city_db = get_city(conn)
    exp_db = get_exp(conn)
    group_db = get_group(conn)
    obraz_db = get_obraz(conn)
    df_vacancy = get_vacancy(conn, session['company'])
    df_employee = get_employee(conn, session['company'])

    spec = ()
    list_city = ()
    list_exp = ()
    list_group = ()
    list_obraz = ()

    if request.values.get('ovz'):
        session['id_ovz'] = request.values.get('ovz')

    if request.values.get('vacan'):
        session['id_comp_vacancy'] = request.values.get('vacan')

        if session['id_ovz'] != '' and session['id_comp_vacancy'] != '':
            add_vac(conn, session['id_ovz'], session['id_comp_vacancy'], session['company'])
            session['id_ovz'] = ''
            session['id_comp_vacancy'] = ''

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
            
            if request.values.get('group[]') and list_exp != ():
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
        'lichkab.html',
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
        id_ovz = session['id_ovz'],
        id_vac = session['id_comp_vacancy'],
        company = session['company'],
        str = str,
        employee = df_employee
    )

if __name__ == "__main__":
    app.run(debug=True)