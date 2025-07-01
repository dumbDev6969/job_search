from utils.database import DatabaseManager
from sqlalchemy import text

def get_values_without_key(table_name: str, column: str, condition_column: str | None = None, condition_value: str | None = None, condition_operator: str = '=') -> list:
    """
    Retrieve specified column values from a database table without using a key.
    Optionally, filter results based on a condition.

    Args:
        table_name (str): The name of the table to query.
        column (str): The column(s) to retrieve. Can be a single column or multiple columns separated by commas.
        condition_column (str, optional): The column to apply a condition on. Defaults to None.
        condition_value (str, optional): The value for the condition. Defaults to None.
        condition_operator (str, optional): The operator for the condition (e.g., '=', '>', '<'). Defaults to '='.

    Returns:
        list: A list of values from the specified column(s). Returns empty list if query fails.
    """
    try:
        db = DatabaseManager('mysql', 'mysql+pymysql://root@localhost/job_portal_db')
        
        # Construct the base query
        query_str = f"SELECT {column} FROM {table_name}"
        
        # Add condition if provided
        params = {}
        if condition_column and condition_value:
            query_str += f" WHERE {condition_column} {condition_operator} :condition_value"
            params['condition_value'] = condition_value
            
        query = text(query_str)
        
        # Execute the query
        result = db.execute_query(query, params)
        
        if not result['success']:
            print(f"Query execution failed: {result['message']}")
            return []
            
        # Extract the output
        return result['output']
        
    except Exception as e:
        print(f"Error retrieving values: {str(e)}")
        return []
    finally:
        if 'db' in locals():
            db.close()

# Example usage
if __name__ == "__main__":
    # Example 1: Retrieve all usernames from admin table without any condition
    usernames = get_values_without_key('admin', 'username')
    print("Usernames in admin table:", usernames)
    
    
