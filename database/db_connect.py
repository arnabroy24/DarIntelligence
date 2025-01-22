import psycopg2
from psycopg2 import sql
import uuid 
import hashlib

def database_create():
    try:
        conn = psycopg2.connect(
            database="postgres",
            user='kali',
            password='kali',
            host='localhost',
            port='5432'
        )
        conn.autocommit = True
        cursor = conn.cursor()
        create_table_query = """
        CREATE DATABASE intelligence;
        """
        cursor.execute(create_table_query)
        print("Database created successfully!")
    except Exception as e:
        print("Error working with the database:", e)
    finally:
        if conn:
            cursor.close()
            conn.close()

def create_table():
    try:
        conn = psycopg2.connect(
            database="intelligence",
            user='kali',
            password='kali',
            host='localhost',
            port='5432'
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        create_table_query_1 = """
        CREATE TABLE IF NOT EXISTS uplinks (
            id VARCHAR(50) PRIMARY KEY,
            link VARCHAR(300),
            hash VARCHAR(100) UNIQUE
        );
        """
        cursor.execute(create_table_query_1)
        print("UP-links table created successfully!")
        
        create_table_query_2 = """
        CREATE TABLE IF NOT EXISTS downlinks (
            id VARCHAR(50) PRIMARY KEY,
            link VARCHAR(300),
            hash VARCHAR(100) UNIQUE
        );
        """
        cursor.execute(create_table_query_2)
        print("DOWN-links table created successfully!")
    except Exception as e:
        print("Error working with the database:", e)
    finally:
        if conn:
            cursor.close()
            conn.close()

def uplink_commit(link):
    try:
        conn = psycopg2.connect(
            database="intelligence",
            user='kali',
            password='kali',
            host='localhost',
            port='5432'
        )
        conn.autocommit = True
        cursor = conn.cursor()
        uniqueid = uuid.uuid4()
        hashed = hashlib.sha256(link.encode('utf-8')).hexdigest()
        
        # Check for duplicate in downlinks
        check_query = """
        SELECT link FROM downlinks WHERE link = %s
        """
        cursor.execute(check_query, (link,))
        if cursor.fetchone():
            delete_query = """
            DELETE FROM downlinks WHERE link = %s
            """
            cursor.execute(delete_query, (link,))
            print("Duplicate deleted from downlink")
            
        insert_query = """
        INSERT INTO uplinks (id, link, hash) 
        VALUES (%s, %s, %s) 
        ON CONFLICT (hash) DO NOTHING;
        """
        cursor.execute(insert_query, (str(uniqueid), link, hashed))
        conn.commit()
        print("Up Link Data inserted successfully!")
    except Exception as e:
        print("Error working with the database:", e)
    finally:
        if conn:
            cursor.close()
            conn.close()

def downlink_commit(link):
    try:
        conn = psycopg2.connect(
            database="intelligence",
            user='kali',
            password='kali',
            host='localhost',
            port='5432'
        )
        conn.autocommit = True
        cursor = conn.cursor()
        uniqueid = uuid.uuid4()
        hashed = hashlib.sha256(link.encode('utf-8')).hexdigest()
        
        insert_query = """
        INSERT INTO downlinks (id, link, hash) 
        VALUES (%s, %s, %s) 
        ON CONFLICT (hash) DO NOTHING;
        """
        cursor.execute(insert_query, (str(uniqueid), link, hashed))
        conn.commit()
        print("Down Link Data inserted successfully!")
    except Exception as e:
        print("Error working with the database:", e)
    finally:
        if conn:
            cursor.close()
            conn.close()

def update_base():
    try:
        conn = psycopg2.connect(
            database="intelligence",
            user='kali',
            password='kali',
            host='localhost',
            port='5432'
        )
        cursor = conn.cursor()
        
        select_query = """
        SELECT link FROM uplinks;
        """
        cursor.execute(select_query)
        rows = cursor.fetchall()
        
        print("Updating base files")
        with open("/home/kali/Desktop/DarIntelligence/base_list.txt", "w") as file:
            for row in rows:
                file.write(f"{row[0]}\n")
    except Exception as e:
        print("Error working with the database:", e)
    finally:
        if conn:
            cursor.close()
            conn.close()