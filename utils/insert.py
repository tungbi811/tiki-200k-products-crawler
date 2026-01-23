import json
import psycopg2
from pathlib import Path
from config.config import load_config

def insert_products(cur, product_list):
    sql = """
        INSERT INTO products(id, name, url_key, price, description)
        VALUES (%s, %s, %s, %s, %s)
    """
    cur.executemany(sql, product_list)

def insert_images(cur, image_list):
    sql = """
        INSERT INTO product_images(product_id, image_url)
        VALUES (%s, %s)
    """
    cur.executemany(sql, image_list)

def insert_products_and_images(product_list, image_list):
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                insert_products(cur, product_list)
                insert_images(cur, image_list)
            conn.commit()
    except Exception as error:
        conn.rollback()
        print("Transaction failed:", error)

if __name__ == "__main__":
    pass