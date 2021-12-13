import sqlite3

conn = sqlite3.connect('database.db');
conn.execute('CREATE TABLE user (name TEXT, email TEXT, phone TEXT, pass TEXT , dateOfBirth TEXT)');
conn.close()