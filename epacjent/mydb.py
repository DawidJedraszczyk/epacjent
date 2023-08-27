import mysql.connector

#todo użyć pliku .env

dataBase = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = 'Dragon11'
)

cursorObject = dataBase.cursor()

