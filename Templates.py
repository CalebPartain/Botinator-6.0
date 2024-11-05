import sqlite3

class Templates():
    def __init__(self, db_path):
        self.db_path = db_path
        self.initialize_database()
        
    def initialize_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Create contacts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS templates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                issue TEXT NOT NULL UNIQUE,
                csr TEXT NOT NULL,
                entered_by TEXT NOT NULL,
                dm TEXT NOT NULL,
                added_contacts TEXT NOT NULL,
                cc_contacts TEXT NOT NULL,
                email TEXT NOT NULL
            )
        ''')

    def save_template(self, issue, csr, entered_by, dm, added_contacts, cc_contacts, email):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO templates (issue, csr, entered_by, dm, added_contacts, cc_contacts, email)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(issue) DO UPDATE SET 
                    csr = excluded.csr,
                    entered_by = excluded.entered_by,
                    dm = excluded.dm,
                    added_contacts = excluded.added_contacts,
                    cc_contacts = excluded.cc_contacts,
                    email = excluded.email            
        ''', (issue, csr, entered_by, dm, added_contacts, cc_contacts, email))
        conn.commit()
        conn.close()

    def delete_template(self, issue):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM templates WHERE issue = ?', (issue,))
        conn.commit()
        conn.close()

    def get_template_by_name(self, issue):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT issue, csr, entered_by, dm, added_contacts, cc_contacts, email FROM templates WHERE issue = ?', (issue,))
        template_tuple = cursor.fetchall()
        conn.close()
        template = []
        for item in template_tuple:
            template.extend(item)
        return template

    def get_template_names(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT issue FROM templates')
        templates = cursor.fetchall()
        conn.close()
        template_names = []
        for template in templates:
            template_names.append(template[0])
        return template_names


