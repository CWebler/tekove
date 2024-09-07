from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker('pt_BR')

NUM_FUNCIONARIOS = 50
NUM_PACIENTES = 200
NUM_CONSULTAS = 300

STATUS_OPTIONS = ['confirmada', 'cancelada', 'pendente']

def generate_funcionarios(num):
    funcionarios = []
    for _ in range(num):
        nome = fake.name()
        email = fake.unique.email()
        senha = fake.password()
        funcionarios.append((nome, email, senha))
    return funcionarios

def generate_pacientes(num):
    pacientes = []
    for _ in range(num):
        nome = fake.name()
        endereco = fake.address().replace('\n', ', ')
        telefone = fake.phone_number()
        data_nascimento = fake.date_of_birth()
        pacientes.append((nome, endereco, telefone, data_nascimento))
    return pacientes

def generate_consultas(num, num_funcionarios, num_pacientes):
    consultas = []
    for _ in range(num):
        data = fake.date_between(start_date='-1y', end_date='today')
        horario = fake.time()
        status = random.choice(STATUS_OPTIONS)
        funcionario_id = random.randint(1, num_funcionarios)
        paciente_id = random.randint(1, num_pacientes)
        consultas.append((data, horario, status, funcionario_id, paciente_id))
    return consultas

def generate_sql(funcionarios, pacientes, consultas):
    sql_statements = []

    # Create table statements
    sql_statements.append("""
    CREATE TABLE IF NOT EXISTS Funcionarios (
        id SERIAL PRIMARY KEY,
        nome VARCHAR(100) NOT NULL,
        email VARCHAR(100) NOT NULL UNIQUE,
        senha VARCHAR(100) NOT NULL
    );""")

    sql_statements.append("""
    CREATE TABLE IF NOT EXISTS Pacientes (
        id SERIAL PRIMARY KEY,
        nome VARCHAR(100) NOT NULL,
        endereco VARCHAR(255),
        telefone VARCHAR(20),
        data_nascimento DATE
    );""")

    sql_statements.append("""
    CREATE TABLE IF NOT EXISTS Consultas (
        id SERIAL PRIMARY KEY,
        data DATE NOT NULL,
        horario TIME NOT NULL,
        status VARCHAR(20) NOT NULL,
        funcionario_id INT NOT NULL,
        paciente_id INT NOT NULL,
        FOREIGN KEY (funcionario_id) REFERENCES Funcionarios(id),
        FOREIGN KEY (paciente_id) REFERENCES Pacientes(id)
    );""")

    # Insert statements for funcionarios
    for funcionario in funcionarios:
        sql_statements.append(f"""
        INSERT INTO Funcionarios (nome, email, senha) 
        VALUES ('{funcionario[0]}', '{funcionario[1]}', '{funcionario[2]}');""")

    # Insert statements for pacientes
    for paciente in pacientes:
        sql_statements.append(f"""
        INSERT INTO Pacientes (nome, endereco, telefone, data_nascimento) 
        VALUES ('{paciente[0]}', '{paciente[1]}', '{paciente[2]}', '{paciente[3]}');""")

    # Insert statements for consultas
    for consulta in consultas:
        sql_statements.append(f"""
        INSERT INTO Consultas (data, horario, status, funcionario_id, paciente_id) 
        VALUES ('{consulta[0]}', '{consulta[1]}', '{consulta[2]}', {consulta[3]}, {consulta[4]});""")

    return sql_statements

def save_to_file(sql_statements, filename):
    with open(filename, 'w') as f:
        for statement in sql_statements:
            f.write(statement + '\n')

if __name__ == "__main__":
    funcionarios = generate_funcionarios(NUM_FUNCIONARIOS)
    pacientes = generate_pacientes(NUM_PACIENTES)
    consultas = generate_consultas(NUM_CONSULTAS, NUM_FUNCIONARIOS, NUM_PACIENTES)

    sql_statements = generate_sql(funcionarios, pacientes, consultas)
    save_to_file(sql_statements, 'dados.sql')

    print("Arquivo 'dados.sql' gerado com sucesso.")
