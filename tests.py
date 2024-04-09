"""
Connects to a SQL database using pyodbc
"""
import os
from dotenv import load_dotenv
import pymssql
import pytest

# Load environment variables
load_dotenv()

# Use fixture to set up the connection and cursor for the extent of the module
@pytest.fixture(scope='session')
def db_conn_curs():
    #Connect to MS SQL
    try:
        conn = pymssql.connect(
            server=os.getenv('DB_SERVER'),
            port=os.getenv('DB_PORT'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )  
        #Establish a cursor
        cursor = conn.cursor()
    except Exception as e:
        print(f"Failed to establish a connection or cursor: {e}")
        return None
    yield cursor
    conn.close()

def test_db_conn(db_conn_curs):
    assert db_conn_curs is not None

#Test case 1 - Address - Consistency:
#Check Referential integrity of Address and StateProvince
def test_adrs_ref_int(db_conn_curs):
    q1 = 'SELECT count(StateProvinceID) FROM [Person].[Address] WHERE StateProvinceID NOT IN (SELECT StateProvinceID FROM [Person].[StateProvince])'
    db_conn_curs.execute(q1)
    res1 = db_conn_curs.fetchall()
    assert res1[0][0] == 0, "The values of [Person].[Address].[StateProvinceID] are not in [Person].[StateProvince].[StateProvinceID]."

#Test case 2 - Address - Validity: 
#Validation of ModificationDate range
def test_adrs_mod_date_rng(db_conn_curs):
    q2 = "SELECT ModifiedDate AS mx FROM [Person].[Address] WHERE ModifiedDate < '2006-06-23 00:00:00.000' OR ModifiedDate > CURRENT_TIMESTAMP"
    db_conn_curs.execute(q2)
    res2 = db_conn_curs.fetchall()
    assert len(res2) == 0 , f"Values of ModifiedDate is out of range: {res2}"


#Test case 3 - Document - Completeness: 
#Check row counts
def test_doc_row_cnt(db_conn_curs):
    q3 = 'SELECT COUNT(DocumentNode) FROM [Production].[Document]'
    q3_expected = 13 ##hardcoded for the purpose of the test
    db_conn_curs.execute(q3)
    res3 = db_conn_curs.fetchall()
    assert res3[0][0] == q3_expected, "Row counts are different"


# #Test case 4 - Document - Uniqueness: 
# #Check for duplicates on PK
def test_doc_dupl(db_conn_curs):
    q4 = ' SELECT DocumentNode, COUNT(*) FROM [Production].[Document] GROUP BY DocumentNode HAVING COUNT(*)>1'
    db_conn_curs.execute(q4)
    res4 = db_conn_curs.fetchall()
    assert len(res4) == 0, f"Duplicates are present. Example: {res4}"


# #Test case 5 - UnitMeasure - Consistency: 
# #Check length of each UnitMeasureCode
def test_unm_len_cod(db_conn_curs):
    q5 = 'SELECT LEN(UnitMeasureCode) as Length FROM [Production].[UnitMeasure]'
    db_conn_curs.execute(q5)
    res5 = db_conn_curs.fetchall()
    for row in res5:
        assert 1 <= row[0] <= 3, "The length of Unit Measure Code is not compliant: {row}"


# #Test case 6 - UnitMeasure - Completeness: 
# #Check that all columns are present
def test_unm_col_pres(db_conn_curs):
    q6_act = "SELECT [Column_Name] FROM [INFORMATION_SCHEMA].[COLUMNS] WHERE [TABLE_NAME] = 'UnitMeasure'"
    db_conn_curs.execute(q6_act)
    res6_act= db_conn_curs.fetchall().sort()
    q6_exp = "SELECT 'UnitMeasureCode'UNION SELECT 'ModifiedDate' UNION SELECT 'Name'"
    db_conn_curs.execute(q6_exp)
    res6_exp = db_conn_curs.fetchall().sort()
    assert res6_act == res6_exp, "The columns don't match the requirements"
