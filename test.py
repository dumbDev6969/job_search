from gzip import READ
from utils.database import get_db
from sqlalchemy import text


db = get_db()
query = text("SELECT * FROM jobs")
res = db.execute_query(query)
db.close()
print(res)  