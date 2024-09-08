CREATE TABLE Funcionarios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    senha VARCHAR(100) NOT NULL
    especialidade VARCHAR(100)
);

CREATE TABLE Pacientes (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    endereco VARCHAR(255),
    telefone VARCHAR(20),
    data_nascimento DATE,
    cartao_sus VARCHAR(20)
);

CREATE TABLE Consultas (
    id SERIAL PRIMARY KEY,
    data DATE NOT NULL,
    horario TIME NOT NULL,
    status VARCHAR(20) NOT NULL,
    funcionario_id INT NOT NULL,
    paciente_id INT NOT NULL,
    FOREIGN KEY (funcionario_id) REFERENCES Funcionarios(id),
    FOREIGN KEY (paciente_id) REFERENCES Pacientes(id)
);
