"""Seed sample data."""

from app import db


def run() -> None:
    db.ensure_indexes()

    if not db.list_users():
        db.create_user("Ana Perez", "ana@example.com", "Accion")
        db.create_user("Luis Gomez", "luis@example.com", "Drama")

    if not db.list_movies():
        db.create_movie("Horizonte", "Accion", "120", "18:00", 60, 7.5)
        db.create_movie("Noche Azul", "Drama", "105", "20:30", 50, 8.0)


if __name__ == "__main__":
    run()
