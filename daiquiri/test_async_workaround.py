import time
from io import BytesIO

import pyvo
import requests
from astropy.table import Table

# Endpoint TAP do LIneA
url = "https://userquery-dev.linea.org.br/tap"
# Seu token de API (obtenha em User Query → API Token)
token = "Token ................................"
queue = "five_minutes"


class HTTPSForcedSession(requests.Session):
    """
    Workaround para o caso em que o servidor retorna Location: http:// no redirect
    (PROXY=true não está configurado no servidor).
    O requests remove o header Authorization em redirects https->http (downgrade de scheme),
    causando 404 nos jobs async pois o job não é encontrado para usuário anônimo.
    Esta sessão força https:// no URL antes de requests decidir remover o header.
    """

    def rebuild_auth(self, prepared_request, response):
        prepared_request.url = prepared_request.url.replace("http://", "https://", 1)
        super().rebuild_auth(prepared_request, response)


# Criar sessão autenticada
session = HTTPSForcedSession()
session.headers["Authorization"] = token

print("Conectando ao serviço TAP...")

# Conectar ao serviço TAP
tap = pyvo.dal.TAPService(url, session=session)

print("Conectado ao serviço TAP.")

# Executar consulta
query = "SELECT TOP 10 coadd_object_id, ra, dec, mag_auto_g FROM des_dr2.main"

# Opções de QUEUE (locais): "default" (30s), "five_minutes", "fifteen_minutes"
# Em produção também existe: "two_hours"
job = tap.submit_job(query, QUEUE=queue)
print("Job submitted")
print(f"Job ID: {job.job_id}")

job.run()

print("Job is running...")

print(f"Job ID: {job.job_id}")

while job.phase not in ("COMPLETED", "ERROR", "ABORTED"):
    print(f"Status: {job.phase}", end="\r")
    time.sleep(5)

print(f"Status: {job.phase}")

if job.phase == "COMPLETED":
    print("Fetching the results...", end="\r")

    # Construir a URL do resultado manualmente para evitar problemas de resolução de links do PyVO
    result_url = f"{url}/async/{job.job_id}/results/result"

    # Obter o resultado
    r = requests.get(result_url, headers=session.headers)
    table = Table.read(BytesIO(r.content), format="votable")
    print("Query completed successfully.")
    print(table)
else:
    print(f"Job failed with status: {job.phase}")
