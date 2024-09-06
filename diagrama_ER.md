## Entidades

### Funcionário

- ID (PK)
- Email
- Senha

### Paciente

- ID (PK)
- Nome
- Endereço
- Telefone
- Data de Nascimento

### Consulta

- ID (PK)
- Data
- Horário
- Status (agendada, confirmada, cancelada)
- FuncionárioID (FK)
- PacienteID (FK)

## Relacionamentos

- Um funcionário pode agendar várias consultas.
- Um paciente pode ter várias consultas agendadas.

# DER (Diagrama de Entidade-Relacionamento)

--------------------------------
|          Funcionário         |
--------------------------------
| ID (PK)                      |
| Nome                         |
| Email                        |
| Senha                        |
--------------------------------
             |
             | 1
             | N
--------------------------------
|           Consulta           |
--------------------------------
| ID (PK)                      |
| Data                         |
| Horário                      |
| Status                       |
| FuncionárioID (FK)           |
| PacienteID (FK)              |
--------------------------------
             |
             | N
             | 1
--------------------------------
|           Paciente           |
--------------------------------
| ID (PK)                      |
| Nome                         |
| Endereço                     |
| Telefone                     |
| Data de Nascimento           |
--------------------------------

## Descrição das Tabelas

### Funcionário

- ID: Identificador único do funcionário (chave primária).
- Nome: Nome do funcionário.
- Email: Email do funcionário.
- Senha: Senha do funcionário (armazenada de forma segura).

### Paciente

- ID: Identificador único do paciente (chave primária).
- Nome: Nome do paciente.
- Endereço: Endereço do paciente.
- Telefone: Telefone do paciente.
- Data de Nascimento: Data de nascimento do paciente.

### Consulta

- ID: Identificador único da consulta (chave primária).
- Data: Data da consulta.
- Horário: Horário da consulta.
- Status: Status da consulta (ex.: agendada, confirmada, cancelada).
- FuncionárioID: Referência ao ID do funcionário que agendou a consulta (chave estrangeira).
- PacienteID: Referência ao ID do paciente da consulta (chave estrangeira).