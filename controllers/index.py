from app import app 
from flask import render_template, request, session 

from models.index_model import get_spec, get_aunt
from utils import get_db_connection

@app.route('/', methods=['GET'])
def index():

    conn = get_db_connection()
    company = ''
    session['id_ovz'] = ''
    session['id_comp_vacancy'] = ''
    session['empl'] = ''
    session['vacancy_id'] = ''


    if request.values.get('search_bar'):
        searchs = str(request.values.get('search_bar'))
        session['search'] = searchs

    elif request.values.get('Войти1') == '1':
        login = str(request.values.get('login'))
        passw = str(request.values.get('password'))

        aunt_df = get_aunt(conn, login, passw)

        company = aunt_df.loc[0, 'id_comp']
        session['company'] = int(company)
        
    else:
        session['search'] = ''
        session['company'] = ''
        
        company = ''



    return render_template(
        'index.html',
        search=session['search'],
        company = session['company'],
        len=len,
    )

if __name__ == "__main__":
    app.run(debug=True)