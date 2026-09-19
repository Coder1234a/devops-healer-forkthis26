import os
import sys
import time
import logging
import psycopg2
from psycopg2 import OperationalError

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("DevOpsAgent-TestApp")

def initialize_telemetry():
    # mock function to simulate setting up an opentelemetry exporter
    logger.info("initializing opentelemetry exporter")
    time.sleep(1)
    logger.info("telemetry initialized successfully")

def connect_to_db():
    # attempts a direct connection to the postgresql database instance
    logger.info("attempting to establish database connection")
    
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("POSTGRES_DB", "app_db"),
        user=os.getenv("POSTGRES_USER", "admin"),
        password=os.getenv("POSTGRES_PASSWORD", "secret")
    )
    
    logger.info("database connection established successfully")
    return conn

def execute_migrations(conn):
    # creates the base tables we need if they do not already exist
    logger.info("checking for pending database migrations")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS service_logs (
            id SERIAL PRIMARY KEY,
            event_name VARCHAR(100) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    logger.info("migrations up to date")
    cursor.close()

def main():
    logger.info("starting microservice application")
    initialize_telemetry()
    
    try:
        conn = connect_to_db()
        execute_migrations(conn)
    except OperationalError as e:
        logger.error(f"failed to connect to the database: {e}")
        sys.exit(1)
        
    logger.info("service is ready to accept traffic")
    
    try:
        # keep the container alive to simulate an active web server
        while True:
            time.sleep(15)
    except KeyboardInterrupt:
        logger.info("received shutdown signal, exiting gracefully")
        if conn:
            conn.close()

if __name__ == "__main__":
    main()