

mkdir userquery-dev
cd userquery-dev
mkdir -p data data/download data/files data/upload logs metadatas certificates
chmod -R g+w data logs

cp ../userquery-dev_old/.env .
cp ../userquery-dev_old/docker-compose.yml .
cp ../userquery-dev_old/docker-compose.yml .
cp ../userquery-dev_old/local_settings.py .
cp ../userquery-dev_old/nginx.conf .
cp -r ../userquery-dev_old/metadatas .
cp -r ../userquery-dev_old/certificates/ .
cp -r ../userquery-dev_old/certificates/ .

docker compose exec -it backend python -c "import secrets; print(secrets.token_urlsafe())"

docker compose exec backend python manage.py loaddata /app/fixtures/initial_data.json

docker compose exec backend python manage.py loaddata /app/fixtures/query_samples.json

docker compose exec backend python manage.py setup_groups

docker compose exec backend python manage.py setup_tap_metadata

docker compose exec backend python manage.py createsuperuser
