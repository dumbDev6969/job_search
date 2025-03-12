from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

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

    def execute_query(self, query):
        """
        Executes a SQL query and returns the results.
        
        :param query: The SQL query to execute
        :return: A dictionary containing success flag, message, affected rows, and query output
        """
        try:
            with self.Session() as session:
                result = session.execute(text(query))
                # Convert result rows to dictionaries using proper column access
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
    
 
    # Query the table
    results = mysql_db.execute_query("")
    print("MySQL Results:", results)

    # Close the MySQL connection
    mysql_db.close()

