# Pytest Ta Dqe Int

# Environment setup

## Create environment for tests execution (Command prompt)
run pip install -r requirements.txt

## Requirements:
Create a test user (ex. test_user) for login (ex. test_user), enable authorization via SQL Server user.
In SQL Server Configuration Manager, enable TPC/IP, and restart all running services after all changes are made.

## Changes according to specifications
Add .env file with the following variables:
DB_SERVER=
DB_PORT=
DB_USER=
DB_PASSWORD=
DB_NAME=AdventureWorks2012


# Run pytests
cd path\to\test\script\pytest-ta-dqe-int\
pytest tests.py  --html=report.html --capture sys  -rP

# Report
Check your folder with report.html and open it in your browser.