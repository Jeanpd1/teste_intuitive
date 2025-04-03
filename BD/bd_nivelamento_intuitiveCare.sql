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
SET sql_mode = '';

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/dados_operadoras_tratados.csv'
INTO TABLE Operadoras
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ';' 
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(
    registro_ans,
    cnpj,
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
    @data_registro_ans  -- Variável temporária
)
SET data_registro_ans = 
    STR_TO_DATE(@data_registro_ans, '%Y-%m-%d');  -- Formato corrigido pelo Python

SET SQL_SAFE_UPDATES = 0;  -- Desativa o modo seguro

-- Execute o UPDATE original
UPDATE Operadoras 
SET data_registro_ans = 
    CASE
        WHEN STR_TO_DATE(data_registro_ans, '%d/%m/%Y') IS NOT NULL 
        THEN STR_TO_DATE(data_registro_ans, '%d/%m/%Y')
        ELSE NULL
    END;


ALTER TABLE Operadoras 
MODIFY data_registro_ans DATE;
    
-- Popular Contas Contábeis
INSERT IGNORE INTO Contas_Contabeis (codigo_conta, descricao)
SELECT DISTINCT codigo_conta, descricao 
FROM temp_dados_completos;

DELETE FROM temp_dados_completos 
WHERE registro_ans NOT IN (SELECT registro_ans FROM Operadoras);

SET SQL_SAFE_UPDATES = 1;  -- Reativa o modo seguro

SET GLOBAL wait_timeout = 600;       -- Padrão: 28800 (8 horas)
SET GLOBAL interactive_timeout = 600;-- Padrão: 28800
SET GLOBAL net_read_timeout = 600;   -- Padrão: 30
SET GLOBAL net_write_timeout = 600;  -- Padrão: 60

CREATE INDEX idx_reg_ans ON Demonstracoes_Contabeis (registro_ans);
CREATE INDEX idx_cd_conta ON Demonstracoes_Contabeis (codigo_conta);

SET @batch_size = 50000;
SET @offset = 0;

DELIMITER $$

CREATE PROCEDURE Insert_Demonstracoes_Batch()
BEGIN
    DECLARE batch_size INT DEFAULT 50000;
    DECLARE offset_value INT DEFAULT 0;
    DECLARE total_rows INT;

    -- Conta quantas linhas existem no arquivo
    SELECT COUNT(*) INTO total_rows FROM temp_dados_completos;

    -- Loop de inserção em lotes
    WHILE offset_value < total_rows DO
        INSERT INTO Demonstracoes_Contabeis (data, registro_ans, codigo_conta, saldo_inicial, saldo_final)
        SELECT 
            STR_TO_DATE(DATA, '%Y-%m-%d'),
            REG_ANS,
            CD_CONTA_CONTABIL,
            VL_SALDO_INICIAL,
            VL_SALDO_FINAL
        FROM temp_dados_completos
        LIMIT batch_size OFFSET offset_value;

        -- Atualiza o offset para o próximo lote
        SET offset_value = offset_value + batch_size;
    END WHILE;
END $$

DELIMITER ;
SELECT COUNT(*) AS total_inseridos FROM Demonstracoes_Contabeis;
SELECT COUNT(*) AS total_no_csv FROM temp_dados_completos;
select * from temp_dados_completos limit 100;
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