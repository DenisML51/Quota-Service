from app import app 
from flask import render_template, request, session 
import numpy as np

from utils import get_db_connection
from models.index_model import get_ovz
from models.candid_model import get_vacancy
from models.vacancy_model import get_vac_comp, add_new_vacancy, add_new_comp_vac

@app.route('/vacancy', methods=['get'])
def vacancy():
    conn = get_db_connection()
    search = session['search']
    company = session['company']

    vac_df = get_vac_comp(conn, company)

    if request.values.get('Добавить') == '1':
        name = request.values.get('name')
        descr = request.values.get('descr')
        spec = request.values.get('spec')
        exp = request.values.get('exp')

        id_vac = add_new_vacancy(conn, name, descr)
        id_vac = int(id_vac.loc[0, 'id_vacancy'])
        add_new_comp_vac(conn, id_vac, company, spec, exp)
        vac_df = get_vac_comp(conn, company)

    return render_template(
        'vacancy.html', 
        search = search,
        company = company,
        len = len,
        vac_df = vac_df
    )