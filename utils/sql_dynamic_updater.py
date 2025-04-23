from database import DatabaseManager, get_db
from sqlalchemy import text

class SQLDynamicUpdater:
    def __init__(self) -> None:
        self.db = get_db()

    def insert_record(self, table: str, data: dict[str, str]) -> dict:
        """
        Insert a record into the specified table.
        Args:
            table (str): Table name
            data (dict): Column-value pairs
        Returns:
            dict: Result of the operation
        """
        columns = ', '.join(data.keys())
        placeholders = ', '.join([f':{k}' for k in data.keys()])
        query = text(f"INSERT INTO {table} ({columns}) VALUES ({placeholders})")
        return self.db.execute_query(query, data)

    def update_record(self, table: str, data: dict[str, str], where: dict[str, str]) -> dict:
        """
        Update a record in the specified table.
        Args:
            table (str): Table name
            data (dict): Column-value pairs to update
            where (dict): WHERE clause column-value pairs
        Returns:
            dict: Result of the operation
        """
        set_clause = ', '.join([f"{k} = :{k}" for k in data.keys()])
        where_clause = ' AND '.join([f"{k} = :w_{k}" for k in where.keys()])
        params = {**data, **{f"w_{k}": v for k, v in where.items()}}
        query = text(f"UPDATE {table} SET {set_clause} WHERE {where_clause}")
        return self.db.execute_query(query, params)

    def validate_form_columns(self, table: str, form_data: dict) -> bool:
        """
        Validates that each column in form_data exists in the specified table.
        Args:
            table (str): Table name
            form_data (dict): Form data received from Flask
        Returns:
            bool: True if all columns are valid, False otherwise
        """
        from sqlalchemy import inspect
        inspector = inspect(self.db.engine)
        valid_columns = set([col['name'] for col in inspector.get_columns(table)])
        for k in form_data.keys():
            if k not in valid_columns:
                return False
        return True

    def format_and_validate_form(self, table: str, form_data: dict) -> dict:
        """
        Formats form data and checks if each column exists in the specified table.
        Args:
            table (str): Table name
            form_data (dict): Form data received from Flask
        Returns:
            dict: Filtered data with only valid columns
        """
        # Get columns from the table using SQLAlchemy's inspector
        from sqlalchemy import inspect
        inspector = inspect(self.db.engine)
        valid_columns = set([col['name'] for col in inspector.get_columns(table)])
        filtered_data = {k: v for k, v in form_data.items() if k in valid_columns}
        return filtered_data

# Example usage:
if __name__ == "__main__":
    updater = SQLDynamicUpdater()
    # # Insert example
    # insert_result = updater.insert_record(
    #     "admin",
    #     {"username": "newuser", "email": "newuser@admin.com", "password": "hashedpass"}
    # )
    # print("Insert result:", insert_result)

    # # Update example
    # update_result = updater.update_record(
    #     "admin",
    #     {"password": "newhashedpass"},
    #     {"email": "newuser@admin.com"}
    # )
    # print("Update result:", update_result)

    # Jobs table insert example
    jobs_data = {"title": "Software Engineer", "location": "Remote", "salary_range": "120000"}
    valid = updater.validate_form_columns("jobs", jobs_data)
    validated_jobs_data = updater.format_and_validate_form("jobs", jobs_data)
    # jobs_insert_result = updater.insert_record(
    #     "jobs",
    #     validated_jobs_data
    # )
    print("Jobs insert result:", validated_jobs_data)