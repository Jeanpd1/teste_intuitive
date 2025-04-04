-- Referencia
-- https://stackoverflow.com/questions/14127529/import-data-in-mysql-from-a-csv-file-using-load-data-infile
-- Seria LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/dados_operadoras_tratados.csv'
LOAD DATA INFILE '/var/lib/mysql-files/dados_operadoras_tratados_corrigido.csv'
INTO TABLE Operadoras
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ';'
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
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
    regiao_comercializacao,
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

-- Cria tabela temporária para receber dados brutos
DROP TABLE IF EXISTS temp_dados_completos;
CREATE TEMPORARY TABLE temp_dados_completos (
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
	IF(data_str = '' OR data_str IS NULL,
       NULL,
       CASE
           WHEN data_str REGEXP '^[0-9]{2}/[0-9]{2}/[0-9]{4}$' THEN STR_TO_DATE(data_str, '%d/%m/%Y')
           WHEN data_str REGEXP '^[0-9]{4}-[0-9]{2}-[0-9]{2}$' THEN STR_TO_DATE(data_str, '%Y-%m-%d')
           ELSE NULL
       END),
    registro_ans,
    codigo_conta,
    saldo_inicial_str,
    saldo_final_str
FROM temp_dados_completos;

CREATE INDEX idx_reg_ans ON Demonstracoes_Contabeis (registro_ans);
CREATE INDEX idx_cd_conta ON Demonstracoes_Contabeis (codigo_conta);
CREATE INDEX idx_data ON Demonstracoes_Contabeis (data);