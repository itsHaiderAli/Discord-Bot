import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name='moderation.db'):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute('''CREATE TABLE IF NOT EXISTS warnings (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    user_id INTEGER NOT NULL,
                                    reason TEXT,
                                    timestamp TEXT
                                )''')

            self.conn.execute('''CREATE TABLE IF NOT EXISTS mutes (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    user_id INTEGER NOT NULL,
                                    duration INTEGER,
                                    reason TEXT,
                                    timestamp TEXT
                                )''')

            self.conn.execute('''CREATE TABLE IF NOT EXISTS bans (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    user_id INTEGER NOT NULL,
                                    reason TEXT,
                                    timestamp TEXT
                                )''')

    def add_warning(self, user_id, reason):
        with self.conn:
            self.conn.execute('''INSERT INTO warnings (user_id, reason, timestamp)
                                 VALUES (?, ?, ?)''',
                              (user_id, reason, datetime.now()))

    def add_mute(self, user_id, duration, reason):
        with self.conn:
            self.conn.execute('''INSERT INTO mutes (user_id, duration, reason, timestamp)
                                 VALUES (?, ?, ?)''',
                              (user_id, duration, reason, datetime.now()))

    def add_ban(self, user_id, reason):
        with self.conn:
            self.conn.execute('''INSERT INTO bans (user_id, reason, timestamp)
                                 VALUES (?, ?, ?)''',
                              (user_id, reason, datetime.now()))

    def get_warnings(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT reason, timestamp FROM warnings WHERE user_id = ?', (user_id,))
        return cursor.fetchall()
