import cx_Oracle

class DatabaseConnection:
    def __init__(self, username, password, host, port, service):
        self.connection = cx_Oracle.connect(f"{username}/{password}@{host}:{port}/{service}")
        self.cursor = self.connection.cursor()

    def close(self):
        self.cursor.close()
        self.connection.close()

