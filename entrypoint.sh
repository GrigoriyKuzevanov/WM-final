python3 -m migration_utils upgrade head

python3 -m scripts.create_superuser

uvicorn main:app --host 0.0.0.0 --port 8000
