# Sistema de Gestion de Cine (MongoDB + Python + Tkinter)

Este proyecto implementa un sistema de inventario y gestion de usuarios para una sala de cine con:
- Registro de usuarios y historial.
- Gestion del inventario de peliculas.
- Compra de entradas con actualizacion en tiempo real.
- Generacion de recibos en XML.
- Reportes simples de compras y disponibilidad.

## Modelo de datos (colecciones en MongoDB)

users:
- name
- email (unique)
- preference
- created_at

movies:
- name
- genre
- duration
- schedule
- available_tickets
- price
- created_at

purchases:
- user_id
- user_name
- movie_id
- movie_name
- quantity
- total
- schedule
- purchased_at

## Ejecucion por defecto (Atlas + App en Docker)

1) Cree un archivo .env (use .env.example como plantilla):

```bash
copy .env.example .env
```

2) Edite .env con su URI de Atlas y el nombre de la BD.

3) Inicie el contenedor con la GUI:

```bash
docker compose --profile gui up --build
```

4) Cargue datos de prueba (en otra terminal):

```bash
docker compose exec app python -m app.seed
```

5) La ventana Tkinter requiere un servidor X y la variable DISPLAY configurada.
   - Windows: establezca DISPLAY en host.docker.internal:0.0 antes de ejecutar docker compose.
   - Linux: export DISPLAY=:0 y habilite acceso X11.

## Opcional: Mongo local en Docker

Si quiere MongoDB local en lugar de Atlas:

1) Inicie MongoDB:

```bash
docker compose --profile localdb up -d mongo
```

2) Configure MONGO_URI en .env con mongodb://mongo:27017

3) Inicie el contenedor con la GUI:

```bash
docker compose --profile gui up --build
```

## Notas
- Los recibos se guardan en la carpeta receipts como archivos XML.
- La disponibilidad de entradas se actualiza de forma atomica al comprar.
