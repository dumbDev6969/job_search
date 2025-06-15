@echo off
mysqldump -u root -h localhost -P 3306 job_portal_db --no-tablespaces --skip-comments --skip-triggers > database_backup.sql
echo Database backup completed.