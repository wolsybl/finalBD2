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

## Ejecucion local (GUI + Atlas)

1) Cree un archivo .env (use .env.example como plantilla):

```bash
copy .env.example .env
```

2) Edite .env con su URI de Atlas y el nombre de la BD.

3) Cree un venv e instale dependencias:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

4) Cargue datos de prueba:

```bash
python -m app.seed
```

5) Ejecute la GUI:

```bash
python -m app.main
```

## Notas
- Los recibos se guardan en la carpeta receipts como archivos XML.
- La disponibilidad de entradas se actualiza de forma atomica al comprar.
