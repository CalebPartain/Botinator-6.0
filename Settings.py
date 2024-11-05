import sqlite3

class Settings():
    def __init__(self, db_path):
        self.db_path = db_path
        self.initialize_database()
        self.get_settings()
        
    def initialize_database(self):
        print('Initializing database')
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Create settings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                setting_key TEXT NOT NULL UNIQUE,
                setting_value TEXT NOT NULL
            )
        ''')

    def save_setting(self, key, value):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        # Insert or replace setting (upsert behavior)
        cursor.execute('''
            INSERT INTO settings (setting_key, setting_value)
            VALUES (?, ?)
            ON CONFLICT(setting_key) DO UPDATE SET setting_value = excluded.setting_value
        ''', (key, value))
        conn.commit()
        conn.close()

    def get_setting(self, key):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT setting_value FROM settings WHERE setting_key = ?', (key,))
        result = cursor.fetchone()
        conn.close()

        if result:
            return result[0]
        else:
            return None

    def get_settings(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT setting_key, setting_value FROM settings')
        rows = cursor.fetchall()
        settings = {row[0]: row[1] for row in rows}
        conn.close()
        return settings


