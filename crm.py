# Create a terminal based customer relationship management tool
# # the user should be able to create, read, update, and delete both companies and employees
# # relate employees to companies, so companies can have many employees and each employee has one employer

import sqlite3
connection = sqlite3.connect("crm_db.db")
print("Connected!")
cursor = connection.cursor()
## Create Tables into the SQLite CRM-DB
# cursor.execute(
#   "CREATE TABLE companies (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(16))"
# )
# cursor.execute(
#   "CREATE TABLE employees (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(32), company_id, INT)"
# )


print("Welcome to your Customer Relationship Management Tool.")

def companiesPortal():
  print("\n\n\nCompanies Portal")

def employeesPortal():
  print("\n\n\nEmployees Portal")

def root():
  print("Select the portal you would like to enter:")
  print("1. Companies\n2. Employees")
  selection = input("> ")

  if selection == "1" or selection == "Companies" or selection == "companies":
    companiesPortal()

  elif selection == "2" or selection == "Employees" or selection == "employees":
    employeesPortal()

  else:
    print("Invalid Selection. Please try again.")
    root()


root()

print("Finished All Actions")

connection.close()
print("Connection Closed")