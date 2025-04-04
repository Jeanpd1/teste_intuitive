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

-- Consulta para o Último trimestre
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

-- Consulta para o Último Ano
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
