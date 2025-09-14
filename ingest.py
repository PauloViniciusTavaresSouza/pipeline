import pandas as pd
from sqlalchemy import create_engine

# Configurações do banco
USER = "postgres"
PASSWORD = "senha123"   # mesma senha que usou no docker run
HOST = "localhost"
PORT = "5232"
DB = "postgres"

# Conexão com o PostgreSQL
engine = create_engine(f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}")



# Ler o CSV
df = pd.read_csv("data/temperature_readings.csv")

# Renomear colunas (ajusta se o CSV tiver nomes diferentes)
df = df.rename(columns={
    "room_id/id": "id_dispositivo",
    "noted_date": "data_registro",
    "temp": "temperatura",
    "out/in": "local"   # só pra não perder essa info
})
print(df.head)
# Converter a coluna de timestamp para datetime

df["data_registro"] = pd.to_datetime(df["data_registro"], dayfirst=True, errors="coerce")

# Inserir no banco
df.to_sql("temperature_readings", engine, if_exists="append", index=False)
print("✅ Dados inseridos com sucesso!")
