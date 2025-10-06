import psycopg
import os
from dotenv import load_dotenv
from psycopg_pool import ConnectionPool

# Load environment variables from .env file
load_dotenv()

class PostgresConnector:
    def __init__(self):
        self.host = os.getenv("POSTGRES_HOSTNAME")
        self.port = os.getenv("POSTGRES_PORT")
        self.database = os.getenv("POSTGRES_DATABASE")
        self.user = os.getenv("POSTGRES_USER")
        self.password = os.getenv("POSTGRES_PASSWORD")

    def connect(self):
        try:
            return psycopg.connect(
                host=self.host, 
                port=self.port, 
                dbname=self.database, 
                user=self.user, 
                password=self.password
            )
        except psycopg.OperationalError as e:
            print(f"Database connection failed: {e}")
            print(f"Connection details: host={self.host}, port={self.port}, database={self.database}, user={self.user}")
            raise

    def get_connection_pool(self):
        conninfo = f"host={self.host} port={self.port} dbname={self.database} user={self.user} password={self.password}"
        
        print(f"Connecting to PostgreSQL with: {conninfo}")
        
        return ConnectionPool(
            conninfo=conninfo,
            min_size=2,
            max_size=10
        )

