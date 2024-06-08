# Backend na aplikacje-mobilne

Może nie najlepiej, ale jako tako

![image](https://github.com/mkaszkowiak-cs-put/aplikacje-mobilne-backend/assets/6163715/85196258-72a3-4bcb-8025-96f4a32cbded)

```
docker compose up -d                                # With Docker
uvicorn app.main:app --host 0.0.0.0 --port 2137     # With local Python

ngrok http --domain=resolved-heron-pleasing.ngrok-free.app 2137
```

**Dane się zresetują przy reboocie lub modyfikacji plików**

Aby zdeployować z fly.io, z wykorzystaniem `flyctl`:

```
fly launch  # pierwsze uruchomienie
fly deploy  # każde kolejne
```

Podglądanie logów:

```
flyctl logs
```
