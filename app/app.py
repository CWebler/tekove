from flask import Flask, jsonify, render_template, request
import os
import psycopg2

app = Flask(__name__)

DATABASE_URL = os.environ.get('DATABASE_URL')

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

@app.route('/')
def index():
    return jsonify({"message": "Welcome to Tekove!"})

@app.route('/pacientes')
def get_pacientes():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Pacientes')
    pacientes = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(pacientes)

@app.route('/funcionarios')
def get_funcionarios():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Funcionarios')
    funcionarios = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(funcionarios)

@app.route('/agendamento')
def get_funcionarios_page():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Funcionarios')
    funcionarios = cur.fetchall()
    cur.close()
    conn.close()
 
    return render_template("index.html", funcionarios=funcionarios)

@app.route('/search_funcionarios')
def search_funcionarios():
    query = request.args.get('search_funcionarios', None)
    if len(query) < 2:
        return ""
        
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Funcionarios WHERE nome ILIKE %s", ('%' + query + '%',))
    funcionarios = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('partials/funcionarios_list.html', funcionarios=funcionarios)
    
@app.route('/search_pacientes')
def search_pacientes():
    query = request.args.get('search_pacientes', None)
    if len(query) < 2:
        return "" 
        
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Pacientes WHERE nome ILIKE %s", ('%' + query + '%',))
    funcionarios = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('partials/pacientes_list.html', funcionarios=funcionarios)
    
@app.route('/agendar_consulta', methods=['POST'])
def agendar_consulta():
    try:
        funcionario_id = request.form['funcionario_id']
        paciente_id = request.form['paciente_id']
        date = request.form['date']
        time = request.form['time']

        conn = get_db_connection()
        cur = conn.cursor()

        insert_query = """
        INSERT INTO Consultas (data, horario, status, funcionario_id, paciente_id) 
        VALUES (%s, %s, %s, %s, %s)
        """
        cur.execute(insert_query, (
            date, time, 'pendente', funcionario_id, paciente_id)
        )

        conn.commit()
        cur.close()
        conn.close()

        return render_template("partials/success.html")
    except Exception as e:
        return render_template("partials/erro.html", erro=e)
if __name__ == '__main__':
    app.run(host='0.0.0.0')
