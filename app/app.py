from flask import (
    Flask,
    jsonify,
    render_template,
    request,
    redirect,
    session,
    url_for,
    flash,
)
import os
import psycopg2
from functools import wraps

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "alterar")

DATABASE_URL = os.environ.get("DATABASE_URL")


def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "funcionario_id" not in session:
            flash("Você precisa estar logado para acessar esta página.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)

    return decorated_function


@app.route("/pacientes")
@login_required
def get_pacientes():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Pacientes")
    pacientes = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(pacientes)


@app.route("/funcionarios")
@login_required
def get_funcionarios():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Funcionarios")
    funcionarios = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(funcionarios)


@app.route("/agendamento")
@login_required
def get_funcionarios_page():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Funcionarios")
    funcionarios = cur.fetchall()
    cur.close()
    conn.close()

    return render_template("index.html", funcionarios=funcionarios)


@app.route("/search_funcionarios")
@login_required
def search_funcionarios():
    query = request.args.get("search_funcionarios", None)
    if len(query) < 2:
        return ""

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Funcionarios WHERE nome ILIKE %s", ("%" + query + "%",))
    funcionarios = cur.fetchall()
    cur.close()
    conn.close()

    return render_template("partials/funcionarios_list.html", funcionarios=funcionarios)


@app.route("/search_pacientes")
@login_required
def search_pacientes():
    query = request.args.get("search_pacientes", None)
    if len(query) < 2:
        return ""

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Pacientes WHERE nome ILIKE %s", ("%" + query + "%",))
    funcionarios = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("partials/pacientes_list.html", funcionarios=funcionarios)


@app.route("/editar_paciente/<int:id>", methods=["POST"])
@login_required
def editar_paciente(id):
    nome = request.form["nome"]
    endereco = request.form.get("endereco")
    telefone = request.form.get("telefone")
    data_nascimento = request.form.get("data_nascimento")
    cartao_sus = request.form.get("cartao_sus")

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE Pacientes
        SET nome = %s,
            endereco = %s,
            telefone = %s,
            data_nascimento = %s,
            cartao_sus = %s
        WHERE id = %s
        """,
        (nome, endereco, telefone, data_nascimento, cartao_sus, id),
    )
    conn.commit()
    cur.close()
    conn.close()

    return render_template(
        "partials/success.html", mensagem="Paciente atualizado com sucesso!"
    )


@app.route("/paciente/<int:id>", methods=["GET"])
@login_required
def buscar_paciente(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Pacientes WHERE id = %s", (id,))
    paciente = cur.fetchone()

    if paciente is None:
        flash("Paciente não encontrado!")
        return redirect(
            url_for("index")
        )  # Redirecionar para uma página de lista ou inicial
    paciente = {
        "nome": paciente[1],
        "endereco": paciente[2],
        "telefone": paciente[3],
        "data_nascimento": paciente[4],
        "cartao_sus": paciente[5],
    }
    return render_template("buscar_paciente.html", id=id, paciente=paciente)


@app.route("/agendar_consulta", methods=["POST"])
@login_required
def agendar_consulta():
    try:
        funcionario_id = request.form["funcionario_id"]
        paciente_id = request.form["paciente_id"]
        date = request.form["date"]
        time = request.form["time"]

        conn = get_db_connection()
        cur = conn.cursor()

        insert_query = """
        INSERT INTO Consultas (data, horario, status, funcionario_id, paciente_id) 
        VALUES (%s, %s, %s, %s, %s)
        """
        cur.execute(insert_query, (date, time, "pendente", funcionario_id, paciente_id))

        conn.commit()
        cur.close()
        conn.close()

        return render_template(
            "partials/success.html", mensagem="A consulta foi agendada com successo!"
        )
    except Exception as e:
        return render_template("partials/erro.html", erro=e)


@app.route("/")
@login_required
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Consultas")
    consultas = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("dashboard.html", consultas=consultas)


@app.route("/listar_consultas", methods=["GET"])
@login_required
def listar_consultas():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT c.id, c.data, c.horario, c.status, f.nome AS funcionario_nome, p.nome AS paciente_nome
        FROM Consultas c
        JOIN Funcionarios f ON c.funcionario_id = f.id
        JOIN Pacientes p ON c.paciente_id = p.id
        """
    )
    consultas = cur.fetchall()

    return render_template("partials/listar_consultas.html", consultas=consultas)


@app.route("/paciente/cadastro", methods=["GET"])
@login_required
def cadastro_paciente():
    return render_template("cadastro_paciente.html")


@app.route("/paciente/inserir", methods=["POST"])
@login_required
def insere_paciente():
    nome = request.form["nome"]
    endereco = request.form.get("endereco")
    telefone = request.form.get("telefone")
    data_nascimento = request.form.get("data_nascimento")
    cartao_sus = request.form.get("cartao_sus")

    # Adicione o paciente ao banco de dados
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO Pacientes (nome, endereco, telefone, data_nascimento, cartao_sus)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (nome, endereco, telefone, data_nascimento, cartao_sus),
    )
    conn.commit()
    cur.close()
    conn.close()

    return render_template(
        "partials/success.html", mensagem="Paciente cadastrado com sucesso!"
    )


@app.route("/funcionario/inserir", methods=["POST"])
@login_required
def inserir_funcionario():
    nome = request.form["nome"]
    especialidade = request.form.get("especialidade")
    email = request.form["email"]
    senha = request.form["senha"]
    conn = get_db_connection()
    cur = conn.cursor()

    # Adicione o funcionário ao banco de dados
    cur.execute(
        """
        INSERT INTO Funcionarios (nome, especialidade, email, senha)
        VALUES (%s, %s, %s, %s)
        """,
        (nome, especialidade, email, senha),
    )
    conn.commit()
    cur.close()
    conn.close()

    return render_template(
        "partials/success.html", mensagem="Funcionário cadastrado com sucesso!"
    )


@app.route("/funcionario/cadastro", methods=["GET"])
@login_required
def cadastro_funcionario():
    return render_template("cadastro_funcionario.html")


@app.route("/paciente/atualizar/<int:id>", methods=["POST"])
@login_required
def atualizar_paciente(id):
    nome = request.form["nome"]
    cartao_sus = request.form["cartao_sus"]
    endereco = request.form["endereco"]
    telefone = request.form["telefone"]
    data_nascimento = request.form["data_nascimento"]

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE Pacientes
        SET nome = %s, cartao_sus = %s, endereco = %s, telefone = %s, data_nascimento = %s
        WHERE id = %s
    """,
        (nome, cartao_sus, endereco, telefone, data_nascimento, id),
    )
    conn.commit()
    cur.close()
    conn.close()
    return render_template(
        "partials/success.html", mensagem="Paciente alterado com sucesso!"
    )


@app.route("/funcionario/atualizar/<int:id>", methods=["POST"])
@login_required
def atualizar_funcionario(id):
    nome = request.form.get("nome")
    email = request.form.get("email")
    senha = request.form.get("senha")
    especialidade = request.form.get("especialidade")

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE Funcionarios
        SET nome = %s, email = %s, senha = %s, especialidade = %s
        WHERE id = %s
    """,
        (nome, email, senha, especialidade, id),
    )
    conn.commit()
    cur.close()
    conn.close()

    return render_template(
        "partials/success.html", mensagem="Funcionário atualizado com sucesso!"
    )


@app.route("/paciente/novo", methods=["POST"])
@login_required
def novo_paciente():
    return render_template("partials/form_paciente.html", paciente=None)


@app.route("/funcionario/novo", methods=["POST"])
@login_required
def novo_funcionario():
    return render_template("partials/form_funcionario.html", paciente=None)


@app.route("/funcionario/<int:id>", methods=["GET"])
@login_required
def buscar_funcionario(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Funcionarios WHERE id = %s", (id,))
    funcionario = cur.fetchone()

    if funcionario is None:
        flash("Funcionário não encontrado!")
        return redirect(
            url_for("index")
        )  # Redirecionar para uma página de lista ou inicial

    funcionario = {
        "nome": funcionario[1],
        "email": funcionario[2],
        "senha": funcionario[3],
        "especialidade": funcionario[4],
    }

    return render_template("buscar_funcionario.html", id=id, funcionario=funcionario)


@app.route("/funcionario/deletar/<int:id>", methods=["DELETE"])
@login_required
def deletar_funcionario(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Funcionarios WHERE id = %s", (id,))
    conn.commit()
    cur.close()
    conn.close()

    return render_template(
        "partials/success.html", mensagem="Funcionário deletado com sucesso!"
    )


@app.route("/paciente/deletar/<int:id>", methods=["DELETE"])
@login_required
def deletar_paciente(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Pacientes WHERE id = %s", (id,))
    conn.commit()
    cur.close()
    conn.close()

    return render_template(
        "partials/success.html", mensagem="Paciente deletado com sucesso!"
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Funcionarios WHERE email = %s", (email,))
        funcionario = cur.fetchone()
        cur.close()
        conn.close()

        if funcionario and funcionario[3] == senha:
            session["funcionario_id"] = funcionario[0]
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for("index"))
        else:
            flash("Email ou senha incorretos!", "danger")

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    session.pop("funcionario_id", None)
    flash("Você saiu da sua conta.", "info")
    return redirect(url_for("login"))


# if __name__ == "__main__":
#     app.config["TEMPLATES_AUTO_RELOAD"] = True
#     app.run(host="0.0.0.0", debug=True)
