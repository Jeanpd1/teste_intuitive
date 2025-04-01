CREATE DATABASE IF NOT EXISTS contabilidade_ans 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE contabilidade_ans;

-- Tabela principal para contábeis

CREATE TABLE IF NOT EXISTS saldos_contabeis (
    id INT AUTO_INCREMENT PRIMARY KEY,
    data DATE NOT NULL,
    reg_ans VARCHAR(20) NOT NULL,
    cd_conta_contabil VARCHAR(50) NOT NULL,
    descricao TEXT NOT NULL,
    vl_saldo_inicial DECIMAL(15, 2),
    vl_saldo_final DECIMAL(15, 2)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tabelas já normalizadas para o csv de registro de operadoras

-- Tabela de Modalidades 
CREATE TABLE modalidades (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE
);

-- Tabela de Cargos 
CREATE TABLE cargos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE
);

-- Tabela de Regiões
CREATE TABLE regioes (
    id SERIAL PRIMARY KEY,
    codigo VARCHAR(50) NOT NULL UNIQUE
);

-- Tabela de Endereços
CREATE TABLE enderecos (
    id SERIAL PRIMARY KEY,
    logradouro VARCHAR(255),
    numero VARCHAR(10),
    complemento VARCHAR(255),
    bairro VARCHAR(100),
    cidade VARCHAR(100) NOT NULL,
    uf CHAR(2) NOT NULL,
    cep CHAR(8)
);

-- Tabela de Contatos
CREATE TABLE contatos (
    id SERIAL PRIMARY KEY,
    operadora_id VARCHAR(10) NOT NULL,
    tipo VARCHAR(20) CHECK (tipo IN ('telefone', 'fax', 'email')),
    valor VARCHAR(255) NOT NULL,
    FOREIGN KEY (operadora_id) REFERENCES operadoras(registro_ans)
);

-- Tabela Principal: Operadoras
CREATE TABLE operadoras (
    registro_ans VARCHAR(10) PRIMARY KEY,
    cnpj VARCHAR(14) NOT NULL,
    razao_social VARCHAR(255) NOT NULL,
    nome_fantasia VARCHAR(255),
    modalidade_id BIGINT UNSIGNED NOT NULL, 
    endereco_id BIGINT UNSIGNED NOT NULL,   
    representante VARCHAR(255),
    cargo_id BIGINT UNSIGNED,               
    regiao_id BIGINT UNSIGNED,              
    data_registro_ans DATE NOT NULL,
    FOREIGN KEY (modalidade_id) REFERENCES modalidades(id),
    FOREIGN KEY (endereco_id) REFERENCES enderecos(id),
    FOREIGN KEY (cargo_id) REFERENCES cargos(id),
    FOREIGN KEY (regiao_id) REFERENCES regioes(id)
);

show tables;
