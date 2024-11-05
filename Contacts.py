import sqlite3

class Contacts():
    def __init__(self, db_path):
        self.db_path = db_path
        self.initialize_database()
        
    def initialize_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Create contacts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL
            )
        ''')

    def add_contact(self, name, email):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO contacts (name, email)
            VALUES (?, ?)
            ON CONFLICT(name) DO UPDATE SET email = excluded.email
        ''', (name, email))
        conn.commit()
        conn.close()

    def delete_contact(self, name, email):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM contacts WHERE name = ? AND email = ?', (name, email))
        conn.commit()
        conn.close()

    def get_contact_by_name(self, name):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT name, email FROM contacts WHERE name = ?', (name,))
        contacts = cursor.fetchall()
        conn.close()

        if contacts: return contacts[0][1]
        return None

    def get_contacts(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT name, email FROM contacts')
        contacts = cursor.fetchall()
        conn.close()
        return contacts


