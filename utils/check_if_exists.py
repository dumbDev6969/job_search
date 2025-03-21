
from utils.database import DatabaseManager
from sqlalchemy import text
def check_column_exists(table_name: str, column: str, value: str) -> bool:
    """
    Check if a value exists in a specified table and column.
    
    Args:
        table_name (str): The name of the table to check
        column (str): The name of the column in the table
        value (str): The value to check
        
    Returns:
        bool: True if value exists, False otherwise
    """
    try:
        db = DatabaseManager('mysql', 'mysql+pymysql://root@localhost/job_portal_db')
        query = text(f"SELECT COUNT(*) as count FROM {table_name} WHERE {column} = :value")
        
        # Execute the query with parameters dictionary
        result = db.execute_query(query, {'value': value})
        
        if not result['success']:
            print(f"Query execution failed: {result['message']}")
            return False
            
        # Safely access the count value
        if result['output'] and len(result['output']) > 0:
            count = result['output'][0]['count']
            return count > 0
        
        return False
        
    except Exception as e:
        print(f"Error checking value existence: {str(e)}")
        return False
    finally:
        if 'db' in locals():
            db.close()





a = check_column_exists('qualifications', 'seeker_id',124)
print(a)