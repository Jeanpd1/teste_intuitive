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
    codigo_conta CHAR(8) NOT NULL UNIQUE,
    descricao VARCHAR(255) NOT NULL
);


CREATE TABLE IF NOT EXISTS Demonstracoes_Contabeis (
    id_demonstracao INT AUTO_INCREMENT PRIMARY KEY,
    data DATE NOT NULL,
    registro_ans CHAR(6) NOT NULL,
    codigo_conta CHAR(8) NOT NULL,
    saldo_inicial DECIMAL(18,2) NOT NULL,
    saldo_final DECIMAL(18,2) NOT NULL,
    FOREIGN KEY (registro_ans) REFERENCES Operadoras(registro_ans),
    FOREIGN KEY (codigo_conta) REFERENCES Contas_Contabeis(codigo_conta)
);


-- Cria tabela temporária para receber dados brutos
CREATE TEMPORARY TABLE IF NOT EXISTS temp_dados_completos (
    data_str VARCHAR(255),
    registro_ans CHAR(255),
    codigo_conta CHAR(255),
    descricao VARCHAR(255),
    saldo_inicial_str VARCHAR(255),
    saldo_final_str VARCHAR(255)
);

-- Referencia
-- https://stackoverflow.com/questions/14127529/import-data-in-mysql-from-a-csv-file-using-load-data-infile
-- Seria LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/dados_demonstracoes_contabeis_tratados.csv' caso instale o banco manualmente
LOAD DATA INFILE '/var/lib/mysql-files/dados_demonstracoes_contabeis_tratados.csv'
INTO TABLE temp_dados_completos
FIELDS TERMINATED BY ';'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- Referencia
-- https://stackoverflow.com/questions/14127529/import-data-in-mysql-from-a-csv-file-using-load-data-infile
-- Seria LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/dados_operadoras_tratados.csv'
LOAD DATA INFILE '/var/lib/mysql-files/dados_operadoras_tratados_corrigido.csv'
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
    @data_registro_ans
)
SET data_registro_ans =
    STR_TO_DATE(@data_registro_ans, '%Y-%m-%d');


UPDATE Operadoras
SET data_registro_ans =
    CASE
        WHEN STR_TO_DATE(data_registro_ans, '%Y-%m-%d') IS NOT NULL
        THEN STR_TO_DATE(data_registro_ans, '%Y-%m-%d')
        ELSE NULL
    END;

ALTER TABLE Operadoras MODIFY data_registro_ans DATE;

INSERT IGNORE INTO Contas_Contabeis (codigo_conta, descricao)
SELECT DISTINCT codigo_conta, descricao
FROM temp_dados_completos;

DELETE FROM temp_dados_completos
WHERE registro_ans NOT IN (SELECT registro_ans FROM Operadoras);

# Parâmetros para permitir a inserção de mais de 1 milhão de registros
SET GLOBAL wait_timeout = 600;
SET GLOBAL interactive_timeout = 600;
SET GLOBAL net_read_timeout = 600;
SET GLOBAL net_write_timeout = 600;

INSERT INTO Demonstracoes_Contabeis (data, registro_ans, codigo_conta, saldo_inicial, saldo_final)
SELECT
    STR_TO_DATE(data_str, '%Y-%m-%d'),
    registro_ans,
    codigo_conta,
    saldo_inicial_str,
    saldo_final_str
FROM temp_dados_completos;

CREATE INDEX idx_reg_ans ON Demonstracoes_Contabeis (registro_ans);
CREATE INDEX idx_cd_conta ON Demonstracoes_Contabeis (codigo_conta);
CREATE INDEX idx_data ON Demonstracoes_Contabeis (data);

SELECT COUNT(*) AS total_inseridos FROM Demonstracoes_Contabeis;
SELECT COUNT(*) AS total_no_csv FROM temp_dados_completos;
select
	data,
	COUNT(*)
from Demonstracoes_Contabeis
GROUP BY data;

SELECT
    (SELECT COUNT(*) FROM Operadoras) AS Total_Operadoras,
    (SELECT COUNT(*) FROM Contas_Contabeis) AS Total_Contas,
    (SELECT COUNT(*) FROM Demonstracoes_Contabeis) AS Total_Demonstracoes;

-- Consultas analiticas

select * from Demonstracoes_Contabeis limit 100;
select * from Operadoras limit 100;
select * from Contas_Contabeis limit 100;
select * from Contas_Contabeis where descricao LIKE '%EVENTOS/SINISTROS%' limit 10;

-- Consulta para o Último Ano (por Texto)
SELECT
    o.registro_ans,
    o.razao_social,
    SUM(d.saldo_final - d.saldo_inicial) AS despesa_total,
    'Último Trimestre' AS periodo
FROM
    Demonstracoes_Contabeis d
JOIN
    Operadoras o ON d.registro_ans = o.registro_ans
JOIN
    Contas_Contabeis c ON d.codigo_conta = c.codigo_conta
WHERE
    c.descricao LIKE '%EVENTOS/SINISTROS%'
    AND d.data >= DATE_SUB((SELECT MAX(data) FROM Demonstracoes_Contabeis), INTERVAL 3 MONTH)
    AND d.data <= (SELECT MAX(data) FROM Demonstracoes_Contabeis)
GROUP BY
    o.registro_ans, o.razao_social
ORDER BY
    despesa_total DESC
LIMIT 10;

-- Consulta para o Último Ano (por Texto)
SELECT
    o.registro_ans,
    o.razao_social,
    SUM(d.saldo_final - d.saldo_inicial) AS despesa_total,
    'Último Ano' AS periodo
FROM
    Demonstracoes_Contabeis d
JOIN
    Operadoras o ON d.registro_ans = o.registro_ans
JOIN
    Contas_Contabeis c ON d.codigo_conta = c.codigo_conta
WHERE
    c.descricao LIKE '%EVENTOS/SINISTROS%'
    AND d.data >= DATE_SUB((SELECT MAX(data) FROM Demonstracoes_Contabeis), INTERVAL 1 YEAR)
    AND d.data <= (SELECT MAX(data) FROM Demonstracoes_Contabeis)
GROUP BY
    o.registro_ans, o.razao_social
ORDER BY
    despesa_total DESC
LIMIT 10;
