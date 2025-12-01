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


# View all entries
## Portal = DB type (Company / Employee)
def view(portal):
  results = ""
  if portal == "company":
    results = cursor.execute("SELECT * FROM companies")
    print("\n\n")
    print(results.fetchall())
    companiesPortal()

  elif portal == "employee":
    results = cursor.execute("SELECT * FROM employees")
    print("\n\n")
    print(results.fetchall())
    employeesPortal()



# View specified entry
## Search by: ID or Name
## Portal = DB type (Company / Employee)
def show(portal):
  print("Show " + portal)


# Create a new entry
## Portal = DB type (Company / Employee)
def create(portal):
  if portal == "company":
    print("Creating a new company.")
    print("Please insert the company's name:")
    name = input("> ")
    cursor.execute(
      "INSERT INTO companies (name) VALUES (?)",
      [name]
    )
    connection.commit()

  if portal == "employee":
    print("Creating a new employee.")
    print("Please insert the employee's full name:")
    name = input("> ")

    def employerFinder():
      print("Where does the employee work?")
      print("Please choose one of the following:")
      print("1. Search for Existing Companies")
      print("2. Create a new Company")
      selection = input("> ")

      if selection == "1" or selection == "search" or selection == "Search":
        def employerSearch():
          print("Input the company's name:")
          searchName = input("> ")
          searchResults = cursor.execute(
            "SELECT * FROM companies WHERE name = ?",
            [searchName]
          )
          allResults = searchResults.fetchall()
          if len(allResults) == 0:
            print("Could not find " + searchName + ".")
            print("Please try again.")
            employerSearch()

          elif len(allResults) == 1:
            print("The following company was found:")
            print(allResults)
            print("Is this the correct company?")
            print("1. Yes")
            print("2. No")
            selection = input("> ")
            if selection == "1":
              return allResults[0]
            else:
              employerSearch()
            
          else:
            def multiCompanySelection():
              print("The following companies were found:")
              for index, result in range(len(searchResults)):
                print(f"{index+1}.")
                print(searchResults[result])
              print(f"{len(searchResults)+2}. None of the above")

              selection = input("> ")
              if int(selection) > 0 and int(selection) <= len(searchResults)+1:
                return searchResults[int(selection)]

              elif int(selection) == len(searchResults)+2:
                employerSearch()

              else:
                multiCompanySelection()
            
            acceptedCompany = multiCompanySelection()
            if acceptedCompany:
              return acceptedCompany

        company = employerSearch()  
        return company
        
      if selection == "2" or selection == "create" or selection == "Create":
        def createCompany():
          print("Creating a new Company.")
          print("Insert the Company's Name:")
          companyName = input("> ")
          if companyName:
            cursor.execute(
              "INSERT INTO companies (name) VALUES (?) RETURNING id, name",
              [companyName]
              )
            newCompany = cursor.fetchone()
            connection.commit()
            return newCompany
          else:
            createCompany()
        createdCompany = createCompany()
        return createdCompany



    company = employerFinder()[0]
    print(company)
    cursor.execute(
      "INSERT INTO employees (name, company_id) VALUES (?,?)",
      [name, company]
    )
    connection.commit()


# Update specified entry
## Search by: ID
## Portal = DB type (Company / Employee)
def update(portal):
  print("Update " + portal)


# View specified entry
## Delete by: ID
## Portal = DB type (Company / Employee)
def delete(portal):
  print("Delete " + portal)



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
    view("company")
  elif (selection == "2" or selection == "show"):
    show("company")
  elif (selection == "3" or selection == "create"):
    create("company")
  elif (selection == "4" or selection == "update"):
    update("company")
  elif (selection == "5" or selection == "delete"):
    delete("company")
  elif (selection == "6" or selection == "back"):
    root()
  else:
    print("Invalid Selection. Please try again.")
    companiesPortal()



# Employee Portal to decide on actions for the employee DB
def employeesPortal():
  print("\n\n\nEmployees Portal")
  print("Select an action to perform:")
  print("1. View all Employees")
  print("2. Show an Employee")
  print("3. Create a Employee")
  print("4. Update a Employee")
  print("5. Delete a Employee")
  print("6. Back to Home Portal")

  selection = input("> ")
  if (selection == "1" or selection == "view"):
    view("employee")
  elif (selection == "2" or selection == "show"):
    show("employee")
  elif (selection == "3" or selection == "create"):
    create("employee")
  elif (selection == "4" or selection == "update"):
    update("employee")
  elif (selection == "5" or selection == "delete"):
    delete("employee")
  elif (selection == "6" or selection == "back"):
    root()
  else:
    print("Invalid Selection. Please try again.")
    employeesPortal()



# Root Portal to decide between actions.
def root():
  print("\n\n\nWelcome to your Customer Relationship Management Tool.")
  print("Select the portal you would like to enter:")
  print("1. Companies")
  print("2. Employees")
  print("9. Shut Down")

  selection = input("> ")
  if selection == "1" or selection == "Companies" or selection == "companies":
    companiesPortal()

  elif selection == "2" or selection == "Employees" or selection == "employees":
    employeesPortal()

  elif selection == "9" or selection == "close" or selection == "Close" or selection == "shut down" or selection == "Shut down" or selection == "Shut Down":
    # All actions completes.
    print("Shutting Down.")

  else:
    print("Invalid Selection. Please try again.")
    root()



# Initial Load 
root()

# Shut down requested.
## Killing connection
connection.close()
print("Connection Closed")