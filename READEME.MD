Pipeline de Dados com IoT e Docker

1. Visão geral

Este projeto implementa um pipeline simples de ingestão e visualização de leituras de temperatura
provenientes de dispositivos IoT.
Os dados vêm de um CSV (dataset do Kaggle), são tratados em Python e inseridos em um banco
PostgreSQL rodando em Docker.
Em seguida foram criadas **views** SQL para facilitar as análises e um **dashboard** em Streamlit +
Plotly para visualização interativa.

2. Estrutura do projeto (arquivos importantes)

- `ingest.py` - script Python que lê o CSV, trata colunas e insere no PostgreSQL.
- `dashboard.py` - app Streamlit que consome as _views_ do banco e plota gráficos com Plotly.
- `data/temperature_readings.csv` - arquivo CSV de origem (Kaggle).

3. Requisitos

- Python 3.10+
- Docker (Docker Desktop no Windows)
- Bibliotecas Python: `pandas`, `sqlalchemy`, `psycopg2-binary`, `streamlit`, `plotly`
- Ferramenta opcional: DBeaver (para explorar o banco)

4. Como subir o PostgreSQL com Docker (exemplo)

```bash
docker run --name postgres-iot -e POSTGRES_PASSWORD=senha123 -p 5432:5432 -d postgres
```

> Ajuste `POSTGRES_PASSWORD` para a senha que preferir. Confirme a porta (`5432`) e ajuste
> `HOST`/`PORT` nos scripts se usar outra porta.

5. Criar a tabela (SQL usado no projeto)
   A tabela usada no projeto é a seguinte:

```sql
CREATE TABLE temperature_readings (
id SERIAL PRIMARY KEY,
id_dispositivo INT NOT NULL,
temperatura NUMERIC(5,2) NOT NULL,
data_registro TIMESTAMP NOT NULL,
local VARCHAR(10)
);
```

> Observação: se os identificadores de dispositivo no CSV forem texto (ex.: "Room Admin"), mude
> `id_dispositivo` para `TEXT` ou trate na ingestão.

6. Views criadas e explicação detalhada
   6.1 `media_temperatura_por_dispositivo`

```sql
CREATE VIEW media_temperatura_por_dispositivo AS
SELECT
id_dispositivo,
AVG(temperatura) as media_temperatura
FROM temperature_readings
GROUP BY id_dispositivo;
```

**Propósito:** calcula a média de temperatura por dispositivo. Útil para comparar desempenho/condições
entre salas/dispositivos e identificar outliers.
6.2 `variacao_temperatura_dia`

```sql
CREATE VIEW variacao_temperatura_dia as
SELECT
date(data_registro) as dia,
temperatura
FROM temperature_readings
ORDER BY data_registro;
```

**Propósito:** fornece as leituras agrupadas por dia (cada linha é uma leitura com a data). Ideal para
construir séries temporais diárias e observar picos/vales ao longo de cada dia.
6.3 `variacao_temperatura_mes`

```sql
CREATE VIEW variacao_temperatura_mes as
SELECT
extract(month from data_registro) as mes,
avg(temperatura) as media_temperatura
FROM temperature_readings
group by
extract(month from data_registro)
ORDER BY
mes asc;
```

**Propósito:** calcula a média mensal de temperatura (agregação por mês). Bom para acompanhar
tendências sazonais e comparar meses.

7. Como rodar o pipeline (passo a passo)
1. Ative seu ambiente virtual e instale dependências:

````bash
python -m venv venv
venv\Scripts\activate

2. Suba o container PostgreSQL

3. Crie a tabela e as views no banco (rode os SQLs apresentados).
4. Ajuste `ingest.py` se necessário (HOST/PORT/USER/PASSWORD/DB) e rode:
```bash
python ingest.py
````

5. Verifique dados inseridos:

```sql
SELECT COUNT(*) FROM temperature_readings;
```

6. Rode o dashboard Streamlit:

```bash
streamlit run dashboard.py

8. Principais insights (sugestões)
- Identificar dispositivos com temperatura média anômala.
- Monitorar picos diários e criar alertas automáticos.
- Acompanhar tendências mensais para manutenção preditiva.
```
