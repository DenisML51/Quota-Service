from app import app 
from flask import render_template, request, session 
import numpy as np

from utils import get_db_connection
from models.candid_model import get_employee, get_vacancy
from models.vacancy_model import get_vac_comp
from models.kabinet_model import get_vacancy2, get_employee2, add_status1, add_status3, add_status2, get_status, get_ovz_emp, add_worker

@app.route('/kabinet', methods=['get'])
def kabinet():
    conn = get_db_connection()
    df_vacancy = ()

    status4 = 0
    id_ovz = ''
    df_vacancy = get_vacancy(conn, session['company'])
    vacancy = get_vacancy2(conn, session['company'], 1)
    df_employee = ()
    vacancy_id = session['vacancy_id']


    if session['empl'] != '':
        session['empl'] = session['empl']
        empl = session['empl']
    else:
        session['empl'] = ''
        empl = session['empl']


    if request.values.get('1'):
        add_status1(conn, session['empl'])
        status1 = get_status(conn, session['empl']).loc[0, 'status1']

    if request.values.get('2'):
        add_status2(conn, session['empl'])
        status2 = get_status(conn, session['empl']).loc[0, 'status2']

    if request.values.get('3'):
        add_status3(conn, session['empl'])
        status3 = get_status(conn, session['empl']).loc[0, 'status3']
        id_ovz = get_ovz_emp(conn, session['empl'], vacancy_id).loc[0, 'id_ovz']
        add_worker(conn, session['company'], vacancy_id, id_ovz)


    if request.values.get('4'):
        status4 = request.values.get('4')

    if request.values.get('ovz'):
        empl = request.values.get('ovz')
        session['empl'] = empl


    if request.values.get('gender'):
        session['vacancy_id'] = request.values.get('gender')
        vacancy_id = session['vacancy_id']

    if vacancy_id != '':    
        vacancy = get_vacancy2(conn, session['company'], vacancy_id)
        df_employee = get_employee2(conn, session['company'], vacancy_id)
    else:
        vacancy_id = ''


    df_status = get_status(conn, session['empl'])
    if session['empl'] != '':
        status1 = df_status.loc[0, 'status1']
        status2 = df_status.loc[0, 'status2']
        status3 = df_status.loc[0, 'status3']
    else:
        status1 = 0
        status2 = 0
        status3 = 0


    session['empl'] = empl

    return render_template(
        'kabinet.html',
        df_employee = df_employee,
        df_vacancy = df_vacancy,
        vacancy_id = vacancy_id,
        vacancy = vacancy,
        len = len,
        status1 = status1,
        status2 = status2,
        status3 = status3,
        status4 = status4,
        empl = empl,
        id_ovz = id_ovz
    )

if __name__ == "__main__":
    app.run(debug=True)