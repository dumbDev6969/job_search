from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import sqlite3
from datetime import datetime

# Global database instance
_db_instance = None

def get_db():
    """Get a database connection instance"""
    global _db_instance
    if _db_instance is None:
        _db_instance = DatabaseManager('mysql', 'mysql+pymysql://root@localhost/job_portal_db')
    return _db_instance

class QueryLogger:
    """Handles logging of database queries to SQLite"""
    def __init__(self, db_path='utils/query_logs.db'):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize the SQLite database for query logging"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS query_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query_text TEXT NOT NULL,
                execution_time TIMESTAMP NOT NULL,
                success BOOLEAN NOT NULL,
                error_message TEXT,
                affected_rows INTEGER,
                execution_duration REAL
            )
        """)
        conn.commit()
        conn.close()

    def log_query(self, query_text, success, error_message=None, affected_rows=0, execution_duration=0.0):
        """Log a query execution to SQLite"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO query_logs 
            (query_text, execution_time, success, error_message, affected_rows, execution_duration)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            str(query_text),
            datetime.now().isoformat(),
            success,
            error_message,
            affected_rows,
            execution_duration
        ))
        conn.commit()
        conn.close()

class DatabaseManager:
    """A simple database manager for MySQL and SQLite3 using SQLAlchemy."""

    def __init__(self, db_type, connection_string):
        self.engine = create_engine(connection_string)
        self.Session = sessionmaker(bind=self.engine)
        self.query_logger = QueryLogger()

    def execute_query(self, query, params=None):
        """Executes a SQL query and returns the results."""
        start_time = datetime.now()
        try:
            with self.Session() as session:
                result = session.execute(query, params if params else {})
                if str(query).strip().upper().startswith(('INSERT', 'UPDATE', 'DELETE')):
                    session.commit()
                    execution_time = (datetime.now() - start_time).total_seconds()
                    self.query_logger.log_query(
                        query_text=str(query),
                        success=True,
                        affected_rows=result.rowcount,
                        execution_duration=execution_time
                    )
                    return {
                        "success": True,
                        "message": "Query executed successfully",
                        "affected_rows": result.rowcount,
                        "output": []
                    }
                output = [dict(row._mapping) for row in result]
                execution_time = (datetime.now() - start_time).total_seconds()
                self.query_logger.log_query(
                    query_text=str(query),
                    success=True,
                    affected_rows=result.rowcount,
                    execution_duration=execution_time
                )
                return {
                    "success": True,
                    "message": "Query executed successfully",
                    "affected_rows": result.rowcount,
                    "output": output
                }
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            self.query_logger.log_query(
                query_text=str(query),
                success=False,
                error_message=str(e),
                execution_duration=execution_time
            )
            return {
                "success": False,
                "message": str(e),
                "affected_rows": 0,
                "output": []
            }

    def close(self):
        """Closes the database connection."""
        self.engine.dispose()


def test_mysql():
    # Initialize the MySQL DatabaseManager
    mysql_db = DatabaseManager('mysql', 'mysql+pymysql://root@localhost/job_portal_db')
    
    # Query the table with parameterized query
    query = text("INSERT INTO `job_seekers` (`seeker_id`, `email`, `password_hash`, `created_at`, `last_login`, `first_name`, `last_name`, `phone`, `province`, `municipality`, `degree`, `portfolio_url`) VALUES (:seeker_id, :email, :password_hash, current_timestamp(), :last_login, :first_name, :last_name, :phone, :province, :municipality, :degree, :portfolio_url)")
    
    params = {
        'seeker_id': '123',
        'email': 'asd',
        'password_hash': 'asd',
        'last_login': 'asd',
        'first_name': 'asd',
        'last_name': 'asd',
        'phone': 'asd',
        'province': 'asd',
        'municipality': 'asd',
        'degree': 'asd',
        'portfolio_url': 'asd'
    }
    
    results = mysql_db.execute_query(query, params)
    print("MySQL Results:", results)

    # Close the MySQL connection
    mysql_db.close()

