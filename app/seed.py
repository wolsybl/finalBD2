"""Seed sample data."""

from app import db

def run() -> None:
    db.ensure_indexes()

    # Usuarios iniciales
    if not db.list_users():
        db.create_user("Ana Perez", "ana-d@example.com", "Acción")
        db.create_user("Luis Gomez", "luis-d@example.com", "Drama")
        db.create_user("Maria Torres", "maria-d@example.com", "Comedia")
        db.create_user("Carlos Ruiz", "carlos-d@example.com", "Ciencia Ficción")

    # Películas iniciales
    if not db.list_movies():
        db.create_movie("Horizonte", "Acción", "120", "18:00", 60, 7.5)
        db.create_movie("Noche Azul", "Drama", "105", "20:30", 50, 8.0)
        db.create_movie("Inception", "Ciencia Ficción", "148", "21:00", 70, 9.0)
        db.create_movie("Titanic", "Romance", "195", "17:00", 80, 8.5)
        db.create_movie("The Dark Knight", "Acción", "152", "22:00", 65, 9.1)
        db.create_movie("Parasite", "Drama", "132", "19:30", 55, 8.6)
        db.create_movie("Interstellar", "Ciencia Ficción", "169", "20:00", 60, 8.7)
        db.create_movie("La La Land", "Musical", "128", "16:30", 50, 8.0)
        db.create_movie("Avengers: Endgame", "Acción", "181", "15:00", 100, 8.4)
        db.create_movie("Coco", "Animación", "105", "14:00", 75, 8.2)

if __name__ == "__main__":
    run()
