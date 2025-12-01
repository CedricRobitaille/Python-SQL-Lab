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


# Employee Portal to decide on actions for the Company DB
def companiesPortal():
  print("\n\n\nCompanies Portal")
  print("Select an action to perform:")
  print("1. View all Companies")
  print("2. Show a Company")
  print("3. Create a Company")
  print("4. Update a Company")
  print("5. Delete a Company")
  print("6. Back to Home Portal")

  selection = input("> ")
  if (selection == "1" or selection == "view"):
    print("View")
  elif (selection == "2" or selection == "show"):
    print("Show")
  elif (selection == "3" or selection == "create"):
    print("Create")
  elif (selection == "4" or selection == "update"):
    print("Update")
  elif (selection == "5" or selection == "delete"):
    print("Delete")
  elif (selection == "6" or selection == "back"):
    print("View")
    root()
  else:
    print("Invalid Selection. Please try again.")
    companiesPortal()


# Employee Portal to decide on actions for the employee DB
def employeesPortal():
  print("\n\n\nEmployees Portal")


# Root Portal to decide between actions.
def root():
  print("\n\n\nWelcome to your Customer Relationship Management Tool.")
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






# Initial Load 
root()



# All actions completes.
print("Shutting Down.")

## Killing connection
connection.close()
print("Connection Closed")