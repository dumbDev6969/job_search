# Job Portal Application

A Flask-based job portal application that connects job seekers with employers.

## Prerequisites

- Python 3.x
- MySQL Server or XAMPP
- pip (Python package installer)

## Installation

1. Clone the repository or download the source code.

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # On Windows
   source venv/bin/activate  # On Unix/MacOS
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Database Setup

1. Start your MySQL server

2. Create the database and tables:
   - Open MySQL client or phpMyAdmin
   - Import the SQL file:
     ```bash
     mysql -u root < employers.sql
     ```
   - Or copy and execute the contents of `employers.sql` in your MySQL client

## Configuration

1. Create a `.env` file in the project root directory with the following content:
   ```env
   FLASK_APP=flask_app.py
   FLASK_ENV=development
   DATABASE_URL=mysql+pymysql://root@localhost/job_portal_db
   ```

2. Adjust the database connection string in `.env` if your MySQL credentials are different

## Running the Application

1. Make sure your virtual environment is activated

2. Start the Flask application:
   ```bash
   flask run
   ```

3. Access the application in your web browser at:
   ```
   http://localhost:5000
   ```

## Project Structure

- `/routes` - Application routes and endpoints
- `/static` - Static files (CSS, JavaScript, images)
- `/templates` - HTML templates
- `/utils` - Utility functions and helpers
- `/tests` - Test files

## Features

- User authentication (Job Seekers and Employers)
- Job posting and application
- Geographic location services
- Real-time chat
- Email notifications
- OTP verification

## Testing

To run the tests:
```bash
python -m pytest tests/
```