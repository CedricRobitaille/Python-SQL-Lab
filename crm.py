# Create a terminal based customer relationship management tool
# # the user should be able to create, read, update, and delete both companies and employees
# # relate employees to companies, so companies can have many employees and each employee has one employer

import sqlite3
connection = sqlite3.connect("crm_db.db")

cursor = connection.cursor()
cursor.execute(
  "CREATE TABLE companies (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(16))"
)
cursor.execute(
  "CREATE TABLE employees (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(32), company_id, INT)"
)


connection.close()