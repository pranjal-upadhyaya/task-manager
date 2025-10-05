import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class PostgresConnector:
    def __init__(self):
        self.host = os.getenv("POSTGRES_HOST")
        self.port = os.getenv("POSTGRES_PORT")
        self.database = os.getenv("POSTGRES_DATABASE")
        self.user = os.getenv("POSTGRES_USER")
        self.password = os.getenv("POSTGRES_PASSWORD")

    def connect(self):
        try:
            return psycopg2.connect(
                host=self.host, 
                port=self.port, 
                database=self.database, 
                user=self.user, 
                password=self.password
            )
        except psycopg2.OperationalError as e:
            print(f"Database connection failed: {e}")
            print(f"Connection details: host={self.host}, port={self.port}, database={self.database}, user={self.user}")
            raise