import sqlite3

class PassKeeper:
    def __init__(self, db_path='passkeeper.db'):
        self.db_path = db_path
        self._connect()
        self._create_tables()

    def _connect(self):
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()

    def _create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                service TEXT NOT NULL,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        self.connection.commit()

    def add_password(self, service, username, password):
        """Añade una nueva contraseña al sistema."""
        self.cursor.execute('''
            INSERT INTO passwords (service, username, password)
            VALUES (?, ?, ?)
        ''', (service, username, password))
        self.connection.commit()

    def edit_password(self, service, new_password):
        """Edita una contraseña existente."""
        self.cursor.execute('''
            UPDATE passwords
            SET password = ?
            WHERE service = ?
        ''', (new_password, service))
        self.connection.commit()

    def delete_password(self, service):
        """Elimina una contraseña del sistema."""
        self.cursor.execute('''
            DELETE FROM passwords WHERE service = ?
        ''', (service,))
        self.connection.commit()

    def view_passwords(self):
        """Devuelve todas las contraseñas almacenadas."""
        self.cursor.execute('SELECT service, username, password FROM passwords')
        return self.cursor.fetchall()
