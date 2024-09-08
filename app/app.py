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

        return render_template("partials/success.html", mensagem="A consulta foi agendada com successo!")
    except Exception as e:
        return render_template("partials/erro.html", erro=e)


@app.route('/dashboard')
def dashboard():        
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Consultas")
    consultas = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('dashboard.html', consultas=consultas)

@app.route('/listar_consultas', methods=['GET'])
def listar_consultas():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        '''
        SELECT c.id, c.data, c.horario, c.status, f.nome AS funcionario_nome, p.nome AS paciente_nome
        FROM Consultas c
        JOIN Funcionarios f ON c.funcionario_id = f.id
        JOIN Pacientes p ON c.paciente_id = p.id
        '''
    )
    consultas = cur.fetchall()
    
    return render_template('partials/listar_consultas.html', consultas=consultas)


@app.route('/paciente/cadastro', methods=['GET'])
def cadastro_paciente():
    return render_template('cadastro_paciente.html')

@app.route('/paciente/inserir', methods=['POST'])
def insere_paciente():
    nome = request.form['nome']
    endereco = request.form.get('endereco')
    telefone = request.form.get('telefone')
    data_nascimento = request.form.get('data_nascimento')
    cartao_sus = request.form.get('cartao_sus')

    # Adicione o paciente ao banco de dados
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        '''
        INSERT INTO Pacientes (nome, endereco, telefone, data_nascimento, cartao_sus)
        VALUES (%s, %s, %s, %s, %s)
        ''', (
            nome, endereco, telefone, data_nascimento, cartao_sus
        )
    )
    conn.commit()
    cur.close()
    conn.close()


    return render_template('partials/success.html', mensagem="Paciente cadastrado com sucesso!")

@app.route('/funcionario/inserir', methods=['POST'])
def inserir_funcionario():
    nome = request.form['nome']
    especialidade = request.form.get('especialidade')
    email = request.form['email']
    senha = request.form['senha']
    conn = get_db_connection()
    cur = conn.cursor()

    # Adicione o funcionário ao banco de dados
    cur.execute(
        '''
        INSERT INTO Funcionarios (nome, especialidade, email, senha)
        VALUES (%s, %s, %s, %s)
        ''', (
            nome, especialidade, email, senha
        )
    )
    conn.commit()
    cur.close()
    conn.close()

    return render_template('partials/success.html', mensagem="Funcionário cadastrado com sucesso!")

@app.route('/funcionario/cadastro', methods=['GET'])
def cadastro_funcionario():
    return render_template('cadastro_funcionario.html')

if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host='0.0.0.0', debug=True)
