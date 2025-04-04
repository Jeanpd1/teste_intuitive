-- Cria e usa o banco de dados
CREATE DATABASE IF NOT EXISTS bd_nivelamento_intuitiveCare;
USE bd_nivelamento_intuitiveCare;

-- Cria tabelas necessárias
CREATE TABLE IF NOT EXISTS Operadoras (
    id_operadora INT AUTO_INCREMENT PRIMARY KEY,
    registro_ans VARCHAR(255) NOT NULL UNIQUE,
    cnpj VARCHAR(17) NOT NULL UNIQUE,
    razao_social VARCHAR(255) NOT NULL,
    nome_fantasia VARCHAR(255),
    modalidade VARCHAR(255),
    logradouro VARCHAR(255),
    numero VARCHAR(255),
    complemento VARCHAR(300),
    bairro VARCHAR(255),
    cidade VARCHAR(255) NOT NULL,
    uf CHAR(2) NOT NULL,
    cep VARCHAR(15),
    ddd CHAR(4),
    telefone VARCHAR(25),
    fax VARCHAR(25),
    endereco_eletronico VARCHAR(255),
    email VARCHAR(255),
    representante VARCHAR(255),
    cargo_representante VARCHAR(255),
    regiao_comercializacao VARCHAR(255),
    data_registro_ans DATE
);

CREATE TABLE IF NOT EXISTS Contas_Contabeis (
    id_conta INT AUTO_INCREMENT PRIMARY KEY,
    codigo_conta VARCHAR(255) NOT NULL UNIQUE,
    descricao VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS Demonstracoes_Contabeis (
    id_demonstracao INT AUTO_INCREMENT PRIMARY KEY,
    data DATE NOT NULL,
    registro_ans VARCHAR(255) NOT NULL,
    codigo_conta VARCHAR(255) NOT NULL,
    saldo_inicial DECIMAL(18,2) NOT NULL,
    saldo_final DECIMAL(18,2) NOT NULL,
    FOREIGN KEY (registro_ans) REFERENCES Operadoras(registro_ans),
    FOREIGN KEY (codigo_conta) REFERENCES Contas_Contabeis(codigo_conta)
);
