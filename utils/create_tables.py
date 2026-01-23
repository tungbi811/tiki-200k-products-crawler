import psycopg2
from config.config import load_config

def create_tables():
    commands = (
        """
        CREATE TABLE IF NOT EXISTS products (
            id BIGINT PRIMARY KEY,
            name TEXT NOT NULL,
            url_key TEXT,
            price INTEGER,
            description TEXT
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS product_images (
            id SERIAL PRIMARY KEY,
            product_id BIGINT REFERENCES products(id) ON DELETE CASCADE,
            image_url TEXT NOT NULL
        );
        """
    )

    try: 
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                for command in commands:
                    cur.execute(command)
    except (psycopg2.DataError, Exception) as error:
        print(error)

if __name__ == "__main__":
    create_tables()