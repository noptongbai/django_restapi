# import pyodbc
from django.db import connections

# def initconncetion():
#     server = 'localhost'
#     database = 'TPC_270315'
#     username = 'sa'
#     password = 'passwOrd'
#     driver = '{ODBC Driver 13 for SQL Server}'
#     cnxn = pyodbc.connect(
#         'DRIVER=' + driver + ';PORT=1433;SERVER=' + server + ';PORT=1443;DATABASE=' + database + ';UID=' + username + ';PWD=' + password,
#         charset="utf8",
#         timeout=3)

    # return cnxn
#     # window server driver= {SQL Server}
#     # database = 'TPC Power Holding Public Company Limited'
#     # username = 'jak'
#     # password = 'P@ssw0rd'
#
#     # server = 'localhost'
#     # database = 'TPC_270315'
#     # username = 'sa'
#     # password = 'passwOrd'

def initconncetion():
    return connections['mgp_erp']
