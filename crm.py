# Create a terminal based customer relationship management tool
# # the user should be able to create, read, update, and delete both companies and employees
# # relate employees to companies, so companies can have many employees and each employee has one employer

#! Highlighted Functionality:
#! Within the `create` function on line 73...
#! When creating a new employee, I created a system to allow the user to search / create a company.
#! The search functionality allows the user to search for a company name, to which the app returns all companies with that name.
#! If the correct company was found, then the user can select the company, and it will add the company's ID to that new user's entry.

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
  if portal == "company":
    print("\n\n\nEnter the Company's ID")
    company_id = input("> ")

    result = cursor.execute(
      "SELECT * FROM companies WHERE id = ?", 
      [company_id]
    )
    print(result.fetchone())
    companiesPortal()

  if portal == "employee":
    print("\n\n\nEnter the Employee's ID")
    employee_id = input("> ")

    result = cursor.execute(
      "SELECT * FROM employees WHERE id = ?",
      [employee_id]
    )
    print(result.fetchone())
    employeesPortal()



# Create a new entry
## Portal = DB type (Company / Employee)
def create(portal):
  # In the company Portal
  if portal == "company":
    print("\n\n\nCreating a new company.")
    print("Please insert the company's name:")
    name = input("> ")
    # Created a new company with the user inputted name
    cursor.execute(
      "INSERT INTO companies (name) VALUES (?)",
      [name]
    )
    connection.commit()
    companiesPortal()

  # In the employee portal
  if portal == "employee":
    print("\n\n\nCreating a new employee.")
    print("Please insert the employee's full name:")
    name = input("> ") # Collect the employee's name

    # Function calls to find / create a company to link the employee too.
    ## Returns the company as a tuple
    def employerFinder():
      print("\nWhere does the employee work?")
      print("Please choose one of the following:")
      print("1. Search for Existing Companies")
      print("2. Create a new Company")
      # User selects to either:
      ## search for an existing company
      ## create a new company
      selection = input("> ") 
      
      # Search for an existing company
      if selection == "1" or selection == "search" or selection == "Search":
        # Function to find existing companies
        def employerSearch():
          print("\nInput the company's name:")
          searchName = input("> ") ## The company name being queried for
          searchResults = cursor.execute( ## Returns all companies under that name (can be many, one, or none)
            "SELECT * FROM companies WHERE name = ?",
            [searchName]
          )
          allResults = searchResults.fetchall()

          ## No companies were found by that name.
          if len(allResults) == 0:
            print("Could not find " + searchName + ".")
            print("Please try again.")
            employerSearch() ## Let the user search again

          ## 1 company was found with that name.
          ### Simple Yes/No to confirm
          elif len(allResults) == 1:
            print("\nThe following company was found:")
            print(allResults)
            print("Is this the correct company?")
            print("1. Yes")
            print("2. No")
            selection = input("> ")
            if selection == "1" or selection == "Yes" or selection == "yes":
              # Correct company found.
              ## Return the found company 
              ## Since it comes out in a list [()], we need to specify the first element of the list.
              return allResults[0] 
            else:
              # Incorrect result
              ## Send them back to search for a new company.
              employerSearch()
          
          # 2 or more companies were found under the specified name.
          else:
            # Function to allow the user to select one of the many companies.
            def multiCompanySelection():
              print("\nThe following companies were found:")
              ## Loop through each search result found, so the user can see the options.
              for index, result in range(len(searchResults)):
                print(f"{index+1}.")
                print(searchResults[result])
              print(f"{len(searchResults)+2}. None of the above")
              selection = input("> ")

              # The user selects a number within the scope of the search results
              ## Return the SINGLE result based on the user's input
              ## Based on the index of the list [(X),(),()]
              if int(selection) > 0 and int(selection) <= len(searchResults)+1:
                return searchResults[int(selection)]

              # The user selected the last option which was "none of the above"
              ## Let the user input a new company name to search for.
              elif int(selection) == len(searchResults)+2:
                employerSearch()

              # The user inputed a key that was not valid.
              ## Make them remake their selection.
              else:
                print("Invalid selection.")
                multiCompanySelection()
            
            # Run function to have the user select A company from the found companies.
            acceptedCompany = multiCompanySelection()
            ## Only proceed if a company was added. If none were added, then we dont return anything.
            if acceptedCompany:
              return acceptedCompany

        # Allow the user to search for a company.
        ## Results in a company tuple (ID, NAME)
        company = employerSearch()  
        return company # Returns the selected company to the employee creator's company_id
        
      # The user chose to Create a new company.
      if selection == "2" or selection == "create" or selection == "Create":
        # Function to create a new company
        def createCompany():
          print("\nCreating a new Company.")
          print("Insert the Company's Name:")
          companyName = input("> ")

          ## If the user inputs a valid company name, it creates a new company by that name.
          if companyName:
            cursor.execute(
              "INSERT INTO companies (name) VALUES (?) RETURNING id, name",
              [companyName]
              )
            # Returns the newly created company, so that it can be used in the employee creation.
            newCompany = cursor.fetchone()
            connection.commit()
            # Returns the created company
            return newCompany
          
          ## The user pressed ENTER without adding any text.
          else:
            createCompany() # Allow the user to try again.
        
        # Initates the company creation.
        createdCompany = createCompany()
        # Returns the company that was created.
        return createdCompany

    # Gets the company the employee belongs to.
    ## Returned a tuple containing the company info (ID, name)
    ## We are only retaining the companyID for our one-to-many relationship.
    company = employerFinder()[0]
    print(company)
    cursor.execute(
      "INSERT INTO employees (name, company_id) VALUES (?,?)",
      [name, company]
    )
    connection.commit()
    employeesPortal()


# Update specified entry
## Search by: ID
## Portal = DB type (Company / Employee)
def update(portal):
  if portal == "company":
    def companySelection():
      print("\n\n\nInput the Company ID for the company you would like to update:")
      company_id = input("> ")

      results = cursor.execute(
        "SELECT * FROM companies WHERE id = ?",
        [company_id]
      )
      company = results.fetchone()
      print("\nWould you like to edit:")
      print(company)
      print("1. Yes")
      print("2. No")
      selection = input("> ")
      if selection == "1" or selection == "Yes" or selection == "yes":
        return company
      else:
        return companySelection()

    company = companySelection()[0]
    print("\nInput a new Company Name:")
    name = input("> ")

    cursor.execute(
      "UPDATE companies SET name = ? WHERE id = ?",
      [name, company]
    )
    connection.commit()
    companiesPortal()
    
  
  if portal == "employee":
    def employeeSelection():
      print("\n\n\nInput the Employee ID for the Employee you would like to update:")
      employee_id = input("> ")

      results = cursor.execute(
        "SELECT * FROM employees WHERE id = ?",
        [employee_id]
      )
      employee = results.fetchone()
      print("\nWould you like to edit:")
      print(employee)
      print("1. Yes")
      print("2. No")
      selection = input("> ")
      if selection == "1" or selection == "Yes" or selection == "yes":
        return employee
      else:
        return employeeSelection()

    employee = employeeSelection()[0]
    print("\nInput a new Employee Name:")
    name = input("> ")

    print("\nInput a new Company ID:")
    company_id = input("> ")

    cursor.execute(
      "UPDATE employees SET name = ?, company_id = ? WHERE id = ?",
      [name, company_id, employee]
    )
    connection.commit()
    employeesPortal()



# View specified entry
## Delete by: ID
## Portal = DB type (Company / Employee)
def delete(portal):
  if portal == "company":
    print("\n\n\nEnter the Company's ID")
    company_id = input("> ")

    result = cursor.execute(
      "DELETE FROM companies WHERE id = ?", 
      [company_id]
    )
    connection.commit()
    print("Deleted Company")
    companiesPortal()

  if portal == "employee":
    print("\n\n\nEnter the Employee's ID")
    employee_id = input("> ")

    result = cursor.execute(
      "DELETE FROM employees WHERE id = ?",
      [employee_id]
    )
    connection.commit()
    print("Deleted Employee")
    employeesPortal()



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