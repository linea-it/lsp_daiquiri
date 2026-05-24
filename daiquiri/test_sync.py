import pyvo
import requests

# Endpoint TAP do LIneA
# url = "https://userquery.linea.org.br/tap"
url = "http://localhost:8000/tap"


# Seu token de API (obtenha em User Query → API Token)
token = "Token ................................"

# Criar sessão autenticada
session = requests.Session()
session.headers["Authorization"] = token

print("Conectando ao serviço TAP...")

# Conectar ao serviço TAP
tap = pyvo.dal.TAPService(url, session=session)

print("Conectado ao serviço TAP.")

# Executar consulta
query = "SELECT TOP 10 coadd_object_id, ra, dec, mag_auto_g FROM des_dr2.main"
result = tap.run_sync(query)
print("Consulta executada com sucesso.")

# Converter para tabela e exibir
table = result.to_table()
print(table)
