from database import DatabaseManager
from sqlalchemy import text

def check_email_exists(table_name: str, email_column: str, email: str) -> bool:
    """
    Check if an email exists in a specified table and column.
    
    Args:
        table_name (str): The name of the table to check
        email_column (str): The name of the email column in the table
        email (str): The email address to check
        
    Returns:
        bool: True if email exists, False otherwise
    """
    try:
        db = DatabaseManager('mysql', 'mysql+pymysql://root@localhost/job_portal_db')
        query = text(f"SELECT COUNT(*) as count FROM {table_name} WHERE {email_column} = :email")
        
        # Execute the query with parameters dictionary
        result = db.execute_query(query, {'email': email})
        
        if not result['success']:
            print(f"Query execution failed: {result['message']}")
            return False
            
        # Safely access the count value
        if result['output'] and len(result['output']) > 0:
            count = result['output'][0]['count']
            return count > 0
        
        return False
        
    except Exception as e:
        print(f"Error checking email existence: {str(e)}")
        return False
    finally:
        if 'db' in locals():
            db.close()


email = check_email_exists("users","email","abcd@ansdn.com")
print(email)