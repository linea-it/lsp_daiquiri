import pyvo
import requests

# Endpoint TAP do LIneA

# Production Environment
# url = "https://userquery.linea.org.br/tap"
# token = "Token ed6bb9a4ae928a6032a51e79dc6eb2a37d3318c6"

# # Staging environment
url = "https://userquery-dev.linea.org.br/tap"
token = "Token 6b858d629028a1ba90c1f84c55579254f5278540"

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
