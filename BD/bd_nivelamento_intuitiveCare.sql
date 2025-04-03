-- ------------------------------------------------------
-- 1. Criação do Banco de Dados e Tabelas
-- ------------------------------------------------------
drop database intuitivecare_bd;

-- ------------------------------------------------------
-- 1. Criação do Banco de Dados e Tabelas (Sintaxe Corrigida)
-- ------------------------------------------------------
CREATE DATABASE IF NOT EXISTS intuitivecare_bd;
USE intuitivecare_bd;

-- Tabela Operadoras (Corrigido tipo de dados e comentários)
CREATE TABLE IF NOT EXISTS Operadoras (
    id_operadora INT AUTO_INCREMENT PRIMARY KEY,
    registro_ans CHAR(6) NOT NULL UNIQUE,       -- Tipo corrigido
    cnpj CHAR(17) NOT NULL UNIQUE,
    razao_social VARCHAR(255) NOT NULL,
    nome_fantasia VARCHAR(255),
    modalidade VARCHAR(100),
    logradouro VARCHAR(255),
    numero VARCHAR(25),
    complemento VARCHAR(300),
    bairro VARCHAR(150),
    cidade VARCHAR(110) NOT NULL,
    uf CHAR(2) NOT NULL,
    cep VARCHAR(15),
    ddd CHAR(4),
    telefone VARCHAR(25),
    fax VARCHAR(25),
    endereco_eletronico VARCHAR(255),
    email VARCHAR(255),
    representante VARCHAR(255),
    cargo_representante VARCHAR(120),
    regiao_comercializacao VARCHAR(50),         -- Tipo corrigido
    data_registro_ans DATE
);

ALTER TABLE Operadoras 
CHANGE COLUMN data_registro data_registro_ans DATE;

-- Tabela Contas_Contabeis (Sem alterações)
CREATE TABLE IF NOT EXISTS Contas_Contabeis (
    id_conta INT AUTO_INCREMENT PRIMARY KEY,
    codigo_conta CHAR(8) NOT NULL UNIQUE,
    descricao VARCHAR(255) NOT NULL
);

-- Tabela Demonstracoes_Contabeis (Sintaxe corrigida)
CREATE TABLE IF NOT EXISTS Demonstracoes_Contabeis (  -- Nome corrigido
    id_demonstracao INT AUTO_INCREMENT PRIMARY KEY,
    data DATE NOT NULL,
    registro_ans CHAR(6) NOT NULL,                   -- Tipo compatível
    codigo_conta CHAR(8) NOT NULL,
    saldo_inicial DECIMAL(18,2) NOT NULL,
    saldo_final DECIMAL(18,2) NOT NULL,
    FOREIGN KEY (registro_ans) REFERENCES Operadoras(registro_ans),
    FOREIGN KEY (codigo_conta) REFERENCES Contas_Contabeis(codigo_conta)
);

-- ------------------------------------------------------
-- 2. Carga de Dados (Sintaxe Corrigida)
-- ------------------------------------------------------

-- Tabela temporária para staging
CREATE TEMPORARY TABLE IF NOT EXISTS temp_dados_completos (
    data_str VARCHAR(20),
    registro_ans CHAR(6),
    codigo_conta CHAR(8),
    descricao VARCHAR(255),
    saldo_inicial_str VARCHAR(50),
    saldo_final_str VARCHAR(50)
);

-- Carregar dados das demonstrações (Caminho ajustado)
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/dados_demonstracoes_contabeis_tratados.csv'
INTO TABLE temp_dados_completos
FIELDS TERMINATED BY ';' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- Carregar operadoras (Sintaxe corrigida)
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/dados_operadoras_tratados.csv'
INTO TABLE Operadoras
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ';'
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(
    registro_ans,  -- CHAR(6)
    cnpj,          -- CHAR(14)
    razao_social,
    nome_fantasia,
    modalidade,
    logradouro,
    numero,
    complemento,
    bairro,
    cidade,
    uf,
    cep,
    ddd,
    telefone,
    fax,
    endereco_eletronico,
    representante,
    cargo_representante,
    data_registro_ans
);

-- Popular Contas Contábeis
INSERT IGNORE INTO Contas_Contabeis (codigo_conta, descricao)
SELECT DISTINCT codigo_conta, descricao 
FROM temp_dados_completos;

-- Conversão segura de dados
INSERT INTO Demonstracoes_Contabeis (data, registro_ans, codigo_conta, saldo_inicial, saldo_final)
SELECT 
    CASE
        WHEN data_str REGEXP '^[0-9]{4}-[0-9]{2}-[0-9]{2}$' THEN STR_TO_DATE(data_str, '%Y-%m-%d')
        ELSE STR_TO_DATE(data_str, '%d/%m/%Y')
    END,
    registro_ans,
    codigo_conta,
    CAST(REPLACE(REPLACE(saldo_inicial_str, '.', ''), ',', '.') AS DECIMAL(18,2)),
    CAST(REPLACE(REPLACE(saldo_final_str, '.', ''), ',', '.') AS DECIMAL(18,2))
FROM temp_dados_completos;

-- ------------------------------------------------------
-- 3. Índices e Validação (Sintaxe Corrigida)
-- ------------------------------------------------------

-- Criar índices
ALTER TABLE Demonstracoes_Contabeis
    ADD INDEX idx_data (data),
    ADD INDEX idx_operadora (registro_ans),
    ADD INDEX idx_conta (codigo_conta);

-- Consulta de validação
SELECT 
    (SELECT COUNT(*) FROM Operadoras) AS Total_Operadoras,
    (SELECT COUNT(*) FROM Contas_Contabeis) AS Total_Contas,
    (SELECT COUNT(*) FROM Demonstracoes_Contabeis) AS Total_Demonstracoes;