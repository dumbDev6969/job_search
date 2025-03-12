from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Global database instance
_db_instance = None

def get_db():
    """Get a database connection instance"""
    global _db_instance
    if _db_instance is None:
        _db_instance = DatabaseManager('mysql', 'mysql+pymysql://root@localhost/job_portal_db')
    return _db_instance

class DatabaseManager:
    """
    A simple database manager for MySQL and SQLite3 using SQLAlchemy.
    
    Usage:
    # For SQLite
    db = DatabaseManager('sqlite', 'sqlite:///example.db')
    
    # For MySQL
    db = DatabaseManager('mysql', 'mysql+pymysql://user:password@localhost/dbname')
    
    # Execute a query
    results = db.execute_query("SELECT * FROM my_table")
    
    # Close the connection
    db.close()
    """

    def __init__(self, db_type, connection_string):
        """
        Initializes the DatabaseManager with the database type and connection string.
        
        :param db_type: Type of database ('sqlite' or 'mysql')
        :param connection_string: Connection string for the database
        """
        self.engine = create_engine(connection_string)
        self.Session = sessionmaker(bind=self.engine)

    def execute_query(self, query, params=None):
        """
        Executes a SQL query and returns the results.
        
        :param query: The SQL query to execute
        :return: A dictionary containing success flag, message, affected rows, and query output
        """
        try:
            with self.Session() as session:
                result = session.execute(query, params if params else {})
                # For INSERT, UPDATE, DELETE queries
                if str(query).strip().upper().startswith(('INSERT', 'UPDATE', 'DELETE')):
                    session.commit()
                    return {
                        "success": True,
                        "message": "Query executed successfully",
                        "affected_rows": result.rowcount,
                        "output": []
                    }
                # For SELECT queries
                output = [dict(row._mapping) for row in result]
                return {
                    "success": True,
                    "message": "Query executed successfully",
                    "affected_rows": result.rowcount,
                    "output": output
                }
        except Exception as e:
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

