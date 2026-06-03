# Cinema Management System (MongoDB + Python + Tkinter)

This project implements a cinema inventory and user management system with:
- User registration and history.
- Movie inventory management.
- Ticket purchasing with real-time availability updates.
- XML receipt generation.
- Simple reports for purchases and availability.

## Data Model (MongoDB collections)

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

## Default Run (Atlas + Docker App)

1) Create a .env file (use .env.example as a template):

```bash
copy .env.example .env
```

2) Edit .env with your Atlas URI and DB name.

3) Start the GUI container:

```bash
docker compose --profile gui up --build
```

4) Seed data (in a new terminal):

```bash
docker compose exec app python -m app.seed
```

5) The Tkinter window requires an X server and the DISPLAY env var configured.
   - Windows: set DISPLAY to host.docker.internal:0.0 in your shell before running docker compose.
   - Linux: export DISPLAY=:0 and allow X11 access.

## Optional: Local Mongo in Docker

If you want a local MongoDB instead of Atlas:

1) Start MongoDB:

```bash
docker compose --profile localdb up -d mongo
```

2) Set MONGO_URI to mongodb://mongo:27017 in .env

3) Start the GUI container:

```bash
docker compose --profile gui up --build
```

## Notes
- Receipts are saved to the receipts folder as XML files.
- Ticket availability is updated atomically during purchase.
