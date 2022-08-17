import datetime

#Provide Details
#super User Account Details
def provideSuperDetails():
    try:
        superFile = open('superAccount.txt', 'r')
    except: 
        return False
    superFileContent = superFile.readlines()
    superFileContentList = []
    for content in superFileContent:
        currentContent = content.strip().split(",")
        currentContentList = [content.strip() for content in currentContent]
        superFileContentList.append(currentContentList)
    superFile.close()
    return superFileContentList

#admin Account Details
def provideAdminDetails():
    try:
        adminFile = open('adminAccount.txt', 'r')
    except:
        return False
    adminFileContent = adminFile.readlines()
    adminFileContentList = []
    for content in adminFileContent:
        currentContent = content.strip().split(",")
        currentContentList = [content.strip() for content in currentContent]
        adminFileContentList.append(currentContentList)
    adminFile.close()
    return adminFileContentList

#customer Account Details
def provideCustomerDetails():
    try:
        customerFile = open('customerAccount.txt', 'r')
    except:
        return False
    customerFileContent = customerFile.readlines()
    customerFileContentList = []
    for content in customerFileContent:
        currentContent = content.strip().split(",")
        currentContentList = [content.strip() for content in currentContent]
        customerFileContentList.append(currentContentList)
    customerFile.close()
    return customerFileContentList

#provide transation Details
def provideTransactionDetails():
    try:
        transactionFile = open('transactionData.txt', 'r')
    except:
        return False
    transactionFileContent = transactionFile.readlines()
    transactionFileContentList = []
    for content in transactionFileContent:
        currentContent = content.strip().split(",")
        transactionFileContentList.append(currentContent)
    transactionFile.close()
    return transactionFileContentList

#Write new data into text file  
def writeDetailsIntoFile(filename, thedetails):
    with open(filename, 'w') as currentFile:
        currentFile.seek(0)
        for detail in thedetails:
            currentString = ",".join(detail)
            currentFile.write(currentString)
            currentFile.write('\n')


#Creating accounts

#creating super user account
def createSuperUserAccount(detailList):
    if provideSuperDetails() == False:
        currentString = ",".join(detailList)
        with open('superAccount.txt', 'w') as newfile:
            newfile.write(currentString)
            newfile.write('\n')

#creating admin account
def createAdminAccount(detailList):
    if provideAdminDetails() == False:
        currentString = ",".join(detailList)
        with open('adminAccount.txt', 'w') as newfile:
            newfile.write(currentString)
            newfile.write('\n')
    else:
        adminFileContentList = provideAdminDetails()
        adminFileContentList.append(detailList)
        writeDetailsIntoFile('adminAccount.txt', adminFileContentList)

#creating customer account      
def createCustomerAccount(detailList):
    #Details to be stored: name, age, password, accountnumber
    if provideCustomerDetails() == False:
        customerFileContentList = []
    else:
        customerFileContentList = provideCustomerDetails()

    customerName = detailList[0]
    customerAge = detailList[1]
    customerEmail = detailList[2]
    accountType = detailList[3]
    balanceAmount = detailList[4]
    
    if len(customerFileContentList) > 0:
        finalAccountNumber = customerFileContentList[-1][-1]
        accountNumber = accountNumberGenerator(finalAccountNumber)
        customerPassword = passwordGenerator(customerName, customerAge, accountNumber)
    else:
        accountNumber = accountNumberGenerator()
        customerPassword = passwordGenerator(customerName, customerAge, accountNumber)

    theString = customerName + "," + customerAge + "," + customerEmail + "," + accountType + "," + customerPassword + "," + accountNumber
    customerFileContentList.append(theString.split(","))
    writeDetailsIntoFile('customerAccount.txt', customerFileContentList)
   
        
    transactionData = []
    transactionData.append(customerName)
    transactionData.append(accountNumber)
    transactionData.append(accountType)
    transactionData.append(balanceAmount)
    tday = datetime.date.today()
    transactionData.append(["Account Created on {}".format(tday)])

    storeTransactionData(transactionData)
    return (customerPassword, accountNumber)

# to store transaction data in text file
def storeTransactionData(detailList):
    theString = ";".join(detailList[-1]) 
    if provideTransactionDetails() == False:
        transactionFileContentList = []
    else:    
        transactionFileContentList = provideTransactionDetails()
    del detailList[-1]
    detailList.append(theString)
    transactionFileContentList.append(detailList)
    writeDetailsIntoFile('transactionData.txt', transactionFileContentList)
  
# storeTransactionData(['john', '0000000001', 'Savings', '250', ['Deposited 200 from Mark']])

def addTransactionalHistoryData(accountNumber, theData):
    transactionFileContentList = provideTransactionDetails()
    for i in range(len(transactionFileContentList)):
            content = transactionFileContentList[i]
            if accountNumber in content:
                originalData = transactionFileContentList[i][-1]
                finalString = originalData + ";" + theData[0]
                transactionFileContentList[i][-1] = finalString
    writeDetailsIntoFile('transactionData.txt', transactionFileContentList)


# to update customer's account balance amount                 
def updateBalanceAmount(accountNumber, newBalanceAmount):
    transactionFileContentList = provideTransactionDetails()
    for i in range(len(transactionFileContentList)):
            content = transactionFileContentList[i]
            if accountNumber in content:
                transactionFileContentList[i][3] = newBalanceAmount
                break
    writeDetailsIntoFile('transactionData.txt', transactionFileContentList)

  
# to get customer's account balance amount   
def getBalanceAmount(accountNumber):
    transactionFileContentList = provideTransactionDetails()
    for i in range(len(transactionFileContentList)):
            content = transactionFileContentList[i]
            if accountNumber in content:
                return transactionFileContentList[i][3]
    
# to get customer's account type
def getAccountType(accountNumber):
    transactionFileContentList = provideTransactionDetails()
    for i in range(len(transactionFileContentList)):
            content = transactionFileContentList[i]
            if accountNumber in content:
                return transactionFileContentList[i][2]

# to get customer's transaction data
def getTransactionData(accountNumber, startTime, endTime):
    transactionFileContentList = provideTransactionDetails()
    finalData = []
    for i in range(len(transactionFileContentList)):
        content = transactionFileContentList[i]
        if accountNumber in content:
            transactionDetails = transactionFileContentList[i][-1]
            transactionDetailList = transactionDetails.split(';')
            break
    
    for data in transactionDetailList:
        currentString = data.split(' ')
        theDate = datetime.datetime.strptime(currentString[-1], '%Y-%m-%d')
        if theDate >= startTime and theDate <= endTime:
            finalData.append(data)
    return finalData

# to get customer's account creation date
def getAccountCreationDate(accountNumber):
    transactionFileContentList = provideTransactionDetails()
    finalData = ""
    for i in range(len(transactionFileContentList)):
        content = transactionFileContentList[i]
        if accountNumber in content:
            transactionDetails = transactionFileContentList[i][-1]
            transactionDetailList = transactionDetails.split(';')
            finalData += transactionDetailList[0]
    finalDataList = finalData.split(' ')
    return finalDataList[-1]

# to get the duration(time) between the account creation and the end date
def getTime(accountNumber, endDate):
    accountStartDate = datetime.datetime.strptime(getAccountCreationDate(accountNumber), '%Y-%m-%d')  
    ourData = endDate.year - accountStartDate.year
    return int(ourData)

# to calculate simple interest
def simpleInterest(balance, totalTime, percentage):
    return float(balance)*int(totalTime)*int(percentage)    

# to generate customer's acccount report
def printAccountReport(accountNumber, startTime, endTime):
    transactionFileContentList = provideTransactionDetails()
    existAccount = False
    userName = ""
    useraccountNumber = ""
    accountType = ""
    balance = ""
    
    for i in range(len(transactionFileContentList)):
            content = transactionFileContentList[i]
            if accountNumber in content:
                existAccount = True
                userName = content[0]
                useraccountNumber = content[1]
                accountType = content[2]
                balance = content[3]
                break
                
    if existAccount == False:
        return False           
        
    transactionHistory = getTransactionData(accountNumber, startTime, endTime)
    transactionHistory = "  --> ".join(transactionHistory)
    totalTime = getTime(accountNumber, endTime)
    if accountType == 'Savings':
        interestAmmount = simpleInterest(balance, totalTime, 4)
    else:
        interestAmmount = 0
    
    deduction1 = 10 if float(balance) > 120 else 0
    deduction2 = 10 if float(balance) > 120 else 0

    formatString = """

              **ACCOUNT REPORT**

    Name: {}
    Account Number: {}
    Account Type: {}
    Adjusted Cash Balance: {}
    Transactional History : 
    * {}  *
    Interest: {}
    Deduction: Sevice Charges: {}
               Error on Check: {}
    Adjusted Cash Balance: {}


              **END OF REPORT**
    """.format(userName, useraccountNumber, accountType, balance, transactionHistory, interestAmmount, str(deduction1), str(deduction2), float(balance)+float(interestAmmount)-(deduction1+deduction2))
    return formatString
# print(printAccountReport('0000000001'))


#Account Number Generation
def accountNumberGenerator(previousAccountNumber='0'):
    if previousAccountNumber == '0':
        return '0000000000'
    else:
        currentValue = str(int(previousAccountNumber) + 1)
        additionalZeros = '0' * (10 - len(currentValue))
        return additionalZeros + currentValue

      
#password generation
def passwordGenerator(name, age, accountNumber):
    return name + str(age) + accountNumber[-4:]



#Finding and Validating account with the given password and account number

# to check whether the details entered by the super user match the data in the system
def validateSuperUserAccount(username, userpassword):
    superFileContentList = provideSuperDetails()
    for content in superFileContentList:
        if content[0] == username and content[1] == userpassword:
            return True
    return False
    
# to check whether the details entered by the admin match the data in the system
def validateAdminAccount(username, userpassword):
    if provideAdminDetails() == False:
        return False
    adminFileContentList = provideAdminDetails()
    
    for content in adminFileContentList:
        if content[0] == username and content[1] == userpassword:
            return True

    return False

# to check whether the admin's password already exist in the system or not (for newly registering admin staff)   
def checkAdminPasswordExist(thepassword):
    if provideAdminDetails() == False:
        return False
    adminFileContentList = provideAdminDetails()
    
    for content in adminFileContentList:
        if thepassword in content:
            return True
    return False

def checkCustomerPasswordExist(thepassword):
    if provideCustomerDetails() == False:
        return False
    customerFileContentList = provideCustomerDetails()

    for content in customerFileContentList:
        if thepassword in content:
            return True
    return False


def checkAccountNumberExist(theaccountNumber):
    if provideCustomerDetails() == False:
        return False
    customerFileContentList = provideCustomerDetails()

    for content in customerFileContentList:
        if theaccountNumber in content:
            return True
    return False



# to check whether the details entered by the customer match the data stored in the system
def validateCustomerAccount(userpassword, accountNumber):
    if provideCustomerDetails() == False:
        return False
    customerFileContentList = provideCustomerDetails()
    for content in customerFileContentList:
        if content[-2] == userpassword and content[-1] == accountNumber:
            return True
    return False

# to check whether the customer's account details already exist in the system or not (for newly registering customers)
def checkDuplicateCustomerAccount(theDetails):
    if provideCustomerDetails() == False:
        return False
    customerFileContentList = provideCustomerDetails()
    for content in customerFileContentList:
        if content[:5] == theDetails:
            return True
    return False
 


#Modify Account Details

# to modify admin's account
def modifyAdminAccount(adminName, adminPassword, newDetails):
    adminFileContentList = provideAdminDetails()
    for i in range(len(adminFileContentList)):
        content = adminFileContentList[i]
        if content[0] == adminName and content[1] == adminPassword:
            adminFileContentList[i] = newDetails
    writeDetailsIntoFile('adminAccount.txt', adminFileContentList)
 

# to remove admin account
def removeAdminAccount(username, userpassword):
    adminFileContentList = provideAdminDetails()
    for i in range(len(adminFileContentList)):
        content = adminFileContentList[i]
        if content[0] == username and content[1] == userpassword:
            del adminFileContentList[i]
            break
    writeDetailsIntoFile('adminAccount.txt', adminFileContentList)

# to remove customer account
def removeCustomerAccount(accountNumber):
    customerFileContentList = provideCustomerDetails()
    for i in range(len(customerFileContentList)):
        content = customerFileContentList[i]
       
        if accountNumber in content:
            
            del customerFileContentList[i]
            break

    writeDetailsIntoFile('customerAccount.txt', customerFileContentList)
    removeTransactionData(accountNumber)

# to remove transaction data of customer
def removeTransactionData(accountNumber):
    transactionFileContentList = provideTransactionDetails()
    for i in range(len(transactionFileContentList)):
            content = transactionFileContentList[i]
            if accountNumber in content:
                del transactionFileContentList[i]
                break
    writeDetailsIntoFile('transactionData.txt', transactionFileContentList)

# to modify customer account
def modifyCustomerAccount(originalPassword, customerPassword, customerAge, customerEmail, customerAccountType):
    customerFileContentList = provideCustomerDetails()
    for i in range(len(customerFileContentList)):
        content = customerFileContentList[i]
        if originalPassword in content:
            customerFileContentList[i][1] = customerAge     
            customerFileContentList[i][2] = customerEmail
            customerFileContentList[i][3] = customerAccountType
            customerFileContentList[i][-2] = customerPassword
    writeDetailsIntoFile('customerAccount.txt', customerFileContentList)

# to change customer's password
def customerPasswordChange(accountNumber, newPassword):
    customerFileContentList = provideCustomerDetails()
    for i in range(len(customerFileContentList)):
        content = customerFileContentList[i]
        if accountNumber in content:
            customerFileContentList[i][-2] = newPassword
            break
    writeDetailsIntoFile('customerAccount.txt', customerFileContentList)
    
    

# to validate the entered email address
def validateEmailAddress(emailAddress):
    if '@' in emailAddress:
        return True
    else:
        return False

#for name check
def nameCheck(thequery):
    if thequery.isalpha():
        return True
    return False

#for age check
def numCheck(thequery):
    if thequery.isnumeric():
        return True
    return False

def moneycheck(themoney):
    try:
        float(themoney)
        return True
    except ValueError:
        return False

#for password check
def passwordCheck(thequery):
    if thequery.isalnum():
        return True
    return False

#to print additional lines in the terminal for better visibility
def printAdditionalLines():
    for i in range(2):
        print(" ")


#interface Design

def welcomeInterface():
    printAdditionalLines()

    theString = """
     ***          1. SuperUser         ***
     ***          2. Admin Staff       ***
     ***          3. Customer          ***

         ** Enter "R" to exit **
                """
            
    print(theString) 
    userOption = input("Plase select one of the options (1/2/3): ")
    while userOption != '1' and userOption != '2' and userOption != '3' and userOption != 'R':
        print("Invalid Option is selected. Please enter one of the given options (1/2/3)")
        userOption = input("Enter your option: ")   

    if userOption == '1':
        superUserLoginInterface()
    elif userOption == '2':
        adminLoginInterface()
    elif userOption == '3':
        customerLoginInterface()
    else:
        print("Thank you. Bye")
        return



def superUserLoginInterface():
    printAdditionalLines()
    firstString = """
    Hello! Please Enter your Login Credentials!
         ** Enter "R" to return back **
    """
    print(firstString)

    while True:
        userName = input("Enter your username: ")
        if userName == "R":
            welcomeInterface()
            return
        userPassword = input("Enter your password: ")
        if userPassword == "R":
            welcomeInterface()
            return
        if validateSuperUserAccount(userName, userPassword) == True:
            break
        print("Plase Reenter. Seems like the username or password entered is wrong")

    superInterface()


def adminLoginInterface():
    printAdditionalLines()
    firstString = """
    Hello! Please Enter your Login Credentials!
           ** Enter "R" to return back **
    """
    print(firstString)
    userName = input("Enter your username: ")
    if userName == "R":
        welcomeInterface()
        return
        
    userPassword = input("Enter your password: ")
    if userName == "R":
        welcomeInterface()
        return
    while validateAdminAccount(userName, userPassword) == False:
        print("Plase Reenter. Seems like the username or password entered is wrong")
        userName = input("Enter your username: ")
        userPassword = input("Enter your password: ")
    adminInterface(userName, userPassword)

def customerLoginInterface():
    printAdditionalLines()
    firstString = """
         Hello! Please Enter your Login Credentials!
                ** Enter "R" to return back **
    """
    print(firstString)
    userName = input("Enter your name sir: ")
    if userName == "R":
        welcomeInterface()
        return
    userPassword = input("Enter your password: ")
    if userPassword == "R":
        welcomeInterface()
        return
    userAccountNumber = input("Enter your account number: ")
    if userAccountNumber == "R":
        welcomeInterface()
        return
    while validateCustomerAccount(userPassword, userAccountNumber) == False:
        print("Plase Reenter. Seems like the username or password entered is wrong")
        userName = input("Enter your name sir: ")
        userPassword = input("Enter your password: ")
        userAccountNumber = input("Enter your account number: ")
    customerInterface(userName, userPassword, userAccountNumber)



def superInterface():
    printAdditionalLines()
    print("Hello mark. What do you want to Perform? ")
    theString = """
    1. Register Admin Account
    2. Update Admin Account Details

      **Enter "R" to return back**
    """
    print(theString)
    userInput = input("Please Select one of the Options: ")
    while userInput != '1' and userInput != '2' and userInput != "R":
        print("Invalid input is entered. Please select from the given options (1/2)")
        userInput = input("Enter the selected option: ")
    if userInput == '1':
        superUserFirstInterface()
    elif userInput == '2':
        superUserSecondInterface()
    else:
        superUserLoginInterface()
    

def customerInterface(userName, userPassword, userAccountNumber):
    printAdditionalLines()
    print("Hello {}. What do you want to Perform? ".format(userName))
    theString = """
    1. Change Password
    2. Deposit Money
    3. Withdraw Money
    4. Print Account Report
            ** Enter "R" to return back **
    """
    print(theString) 
    userInput = input("Please Select one of the Options: ")
    while userInput != '1' and userInput != '2' and userInput != '3' and userInput != '4' and userInput != "R":
        print("Invalid input is entered. Please select from the given options (1/2/3/4)")
        userInput = input("Enter the selected option: ")
    if userInput == '1':
        firstCustomerInterface(userName, userPassword, userAccountNumber)
    elif userInput == '2':
        secondCustomerInterface(userName, userPassword, userAccountNumber)
    elif userInput == '3':
        thirdCustomerInterface(userName, userPassword, userAccountNumber)
    elif userInput == '4':
        fourthCustomerInterface(userName, userPassword, userAccountNumber)
    else:
        customerLoginInterface()


def adminInterface(userName, userPassword):
    printAdditionalLines()
    print("Hello {}. What do you want to Perform? ".format(userName))
    theString = """
    1. Register Customer Account
    2. Update Customer Account Details
    3. Print Account Report
            ** Enter "R" to return back **
    """
    print(theString)
    userInput = input("Please Select one of the Options: ")
    while userInput != '1' and userInput != '2' and userInput != '3' and userInput != "R":
        print("Invalid input is entered. Please select from the given options (1/2/3)")
        userInput = input("Enter the selected option: ")
    if userInput == '1':
        adminFirstInterface(userName, userPassword)
    elif userInput == '2':
        adminSecondInterface(userName, userPassword)
    elif userInput == '3':
        adminThirdInterface(userName, userPassword)
    else:
        adminLoginInterface()


def superUserFirstInterface():
    printAdditionalLines()
    displayString = """
    Press "R" to return back
    
    """
    username = input("Enter the username: ")
    while nameCheck(username) == False:
        print("Sorry invalid name is entered. Please Reenter")
        username = input("Enter the username: ")
    userpassword = input("Enter the password for the admin: ")
    while checkAdminPasswordExist(userpassword):
        print("The password already exist. Please enter another password")
        userpassword = input("Enter the password for the admin: ")

    detailList = []
    detailList.append(username)
    detailList.append(userpassword)
    createAdminAccount(detailList)
    print("The admin account for {} has been succesfully created".format(username))

    while True:
        userInput = input("Enter 'R' to return back: ")
        if userInput == "R":
            superInterface()
            break

    
def superUserSecondInterface():
    printAdditionalLines()
    adminName = input("Enter the admin name: ")
    adminPassword = input("Enter the admin password: ")
    while validateAdminAccount(adminName, adminPassword) == False:
        print("Admin details entered are not correct. Please Reenter")
        adminName = input('Enter the admin name: ')
        adminPassword = input("Enter the admin password: ")

    displayString = """
    1. Update Admin Details
    2. Remove Admin Account
            ** Enter "R" to return back **
    """
    print(displayString)
    userInput = input("Please enter one of the options: ")
    while userInput != '1' and userInput != '2' and userInput != 'R':
        print("Invalid Input. Please Reenter")
        userInput = input("Please enter one of the options: ")
    if userInput == '1':
        updateAdminAccount(adminName, adminPassword)
    elif userInput == '2':
        removeAdminAccount(adminName, adminPassword)
        print("The admin account has been successfully removed")
        while True:
            userInput = input("Enter 'R' to return back: ")
            if userInput == "R":
                superInterface()
                break
    else:
        superInterface()

def updateAdminAccount(adminName, adminPassword):
    printAdditionalLines()
    newusername = input("Enter the new username: ")
    while nameCheck(newusername) == False:
        print("Invalid name is entered. Please Reenter")
        newusername = input("Enter the new username: ")
    newpassword = input("Enter the new password: ")
    detailList = []
    newpassword = " " + newpassword
    detailList.append(newusername)
    detailList.append(newpassword)
    modifyAdminAccount(adminName, adminPassword, detailList)
    print("The admin account has been successfully modified")
   
    while True:
        userInput = input("Enter 'R' to return back: ")
        if userInput == "R":
            superInterface()
            break


def adminFirstInterface(userName, userPassword):
    printAdditionalLines()
    while True:
        username = input("Enter the name: ")
        userage = input("Enter the customer age: ")
        while numCheck(userage) == False:
            print("Invalid age is entered. Please Reenter")
            userage = input("Enter the customer age: ")
        useremail = input("Enter the customer's email address: ")
        useraccountType = input("Enter the type of account created(Savings/Current): ")
        while useraccountType != "Savings" and useraccountType != "Current":
            print("Please enter either 'Savings' or 'Current'")
            useraccountType = input("Enter the type of account created(Savings/Current): ")

        if useraccountType == 'Savings':
          
            while True:
                userOpeningBalance = input("Enter the opening balance: ")
                if moneycheck(userOpeningBalance) == True:
                    if float(userOpeningBalance) >= 100:
                        break
                    print("The opening balance does not meet the minimum balance of the account which is 100. Please Reenter")
                    continue
                else:
                    print("Invalid input is entered. Please Reenter")

        else:
             while True:
                userOpeningBalance = input("Enter the opening balance: ")
                if moneycheck(userOpeningBalance) == True:
                    if float(userOpeningBalance) >= 500:
                        break
                    print("The opening balance does not meet the minimum balance of the account which is 500. Please Reenter")
                    continue
                else:
                    print("Invalid input is entered. Please Reenter")

        detailList = []
        detailList.append(username)
        detailList.append(userage)
        detailList.append(useremail)
        detailList.append(useraccountType)
        detailList.append(userOpeningBalance)
        if checkDuplicateCustomerAccount(detailList) == True:
            print("The account already exist. Please Reenter your details")
            continue
        else:
            break
    
    userpassword, useraccountNumber = createCustomerAccount(detailList)
    print("{}'s password is {} and the account number is {}".format(username, userpassword, useraccountNumber))
    
    while True:
        userInput = input('Enter "R" to return back: ')
        if userInput == "R":
            adminInterface(userName, userPassword)
            break
    

def adminSecondInterface(userName, userPassword):
    printAdditionalLines()
    displayString = """
    1. Update Customer Details
    2. Remove Customer Account
            ** Enter "R" to return back **
    """
    print(displayString)
    userInput = input("Please enter one of the options: ")
    while userInput != '1' and userInput != '2' and userInput != 'R':
        print("Invalid Input. Please Enter a valid input")
        print(displayString)
        userInput = input("Please enter one of the options: ")
    if userInput == '1':
        updateCustomerAccount(userName, userPassword)
    elif userInput == '2':
        adminRemoveCustomer(userName, userPassword)
    else:
        adminInterface(userName, userPassword)

def updateCustomerAccount(userName, userPassword):
    printAdditionalLines()
    originalPassword = input("Enter the customer's original password for verification purpose: ")
    while checkCustomerPasswordExist(originalPassword) == False:
        print("Sorry the password doesn't exist. Please Reneter")
        originalPassword = input("Enter the customer's original password for verification purpose: ")
        
    customerAge = input("Enter the latest customer age: ")
    while numCheck(customerAge) == False:
        print("Invalid age is entered. Please Reenter")
        customerAge = input("Enter the latest customer age: ")
    customerEmail = input("Enter the latest customer email address: ")
    customerAccountType = input("Enter the latest customer account type: ")
    while customerAccountType != "Savings" and customerAccountType != "Current":
        print("Please enter either 'Savings' or 'Current'")
        customerAccountType = input("Enter the type of account created: ")
    customerPassword = input("Enter the latest customer password: ")
    modifyCustomerAccount(originalPassword, customerPassword, customerAge, customerEmail, customerAccountType)
    print("The customer account has been successfully modified.")

    while True:
        userInput = input('Enter "R" to return back: ')
        if userInput == "R":
            adminInterface(userName, userPassword)
            break
    

def adminRemoveCustomer(userName, userPassword):
    printAdditionalLines()
    while True:
        userAccountNumber = input("Please Enter Customer's account number: ")
        if checkAccountNumberExist(userAccountNumber) == True:
            break
        print("The account number entered doesn't exist. Please Reenter")

    removeCustomerAccount(userAccountNumber)

    print("The customer account has been successfully removed.")
    while True:
        userInput = input('Enter "R" to return back: ')
        if userInput == "R":
            adminInterface(userName, userPassword)
            break


def adminThirdInterface(userName, userPassword):
    printAdditionalLines()
    userAccountNumber = input("Enter the customer's account number: ")
    while True:
        startDate = input("Please enter the starting date (YYYY/MM/DD): ")
        try:
            startDate2 = datetime.datetime.strptime(startDate, '%Y/%m/%d')
            if startDate2 > datetime.datetime.today():
                print("Invalid date is entered. Please Reenter")
                continue
            break
        except ValueError:
            print("Invalid date is entered. Please Reenter")

    while True:
        endDate = input("Please enter the end date (YYYY/MM/DD): ")
        try:
            endDate2 = datetime.datetime.strptime(endDate, '%Y/%m/%d')
            break
        except:
            print("Invalid date is entered. Please Reenter")
    
    while printAccountReport(userAccountNumber, startDate2, endDate2) == False:
        print("Account Number doesn't exist. Please Reenter")
        userAccountNumber = input("Enter the customer's account number: ")
    
    print(printAccountReport(userAccountNumber, startDate2, endDate2))
    while True:
        userInput = input('Enter "R" to return back: ')
        if userInput == "R":
            adminInterface(userName, userPassword)
            break

def firstCustomerInterface(userName, userPassword, userAccountNumber):
    printAdditionalLines()
    userNewPassword = input("Enter the new password: ")
    while len(userNewPassword) < 10 or passwordCheck(userNewPassword) == False:
        print("")
        print("The entered password is not strong enough. Make sure it fulfills all the specified criteria")
        thestring = """
        1. Password length should be at least 10 characters
        2. Password should contain both alphabet and numbers 3
        """
        print(thestring)
        userNewPassword = input("Enter the new password: ")

    customerPasswordChange(userAccountNumber, userNewPassword)
    print("The password has been successfully changed")

    while True:
        userInput = input('Enter "R" to return back: ')
        if userInput == "R":
            customerInterface(userName, userPassword, userAccountNumber)
            break

def secondCustomerInterface(userName, userPassword, userAccountNumber):
    printAdditionalLines()
    while True:
        depositAmount = input("Enter the amount: ")
        if moneycheck(depositAmount) == True:
            break
        print("Invalid ammount is entered. Please Reenter")

    currentBalance = getBalanceAmount(userAccountNumber)
    newBalance = float(depositAmount) + float(currentBalance)
    updateBalanceAmount(userAccountNumber, str(newBalance))
    tday = datetime.date.today()
    addTransactionalHistoryData(userAccountNumber, ['Deposited {} on {}'.format(depositAmount, tday)])

    print("{} amount has been deposited into your account. The current balance is {}".format(depositAmount, str(newBalance)))
    
    while True:
        userInput = input('Enter "R" to return back: ')
        if userInput == "R":
            customerInterface(userName, userPassword, userAccountNumber)
            break
    

def thirdCustomerInterface(userName, userPassword, userAccountNumber):
    printAdditionalLines()
    currentBalance = getBalanceAmount(userAccountNumber)
    accountType = getAccountType(userAccountNumber)

    while True:
        withdrawAmount = input("Enter the amount: ")
        if moneycheck(withdrawAmount) == False:
            print("Invalid amount is entered. Please Reenter")
            continue
        newBalance = float(currentBalance) - float(withdrawAmount)
        
        if accountType == "Savings" and newBalance < 100:
            print("Sorry, Withdrawing {} amount will make the minimum amount in your account lower that 100. Please Reenter".format(withdrawAmount))
            continue
        elif accountType == "Current" and newBalance < 500:
            print("Sorry, Withdrawing {} amount will make the minimum amount in your account lower that 500. Please Reenter".format(withdrawAmount))
            continue
        else:
            break
        

    updateBalanceAmount(userAccountNumber, str(newBalance))
    tday = datetime.date.today()
    addTransactionalHistoryData(userAccountNumber, ['Withdrawn {} on {}'.format(withdrawAmount, tday)])
    print("{} has been withdrawn from your account. The current balance is {}.".format(withdrawAmount, str(newBalance)))
    while True:
        userInput = input('Enter "R" to return back: ')
        if userInput == "R":
            customerInterface(userName, userPassword, userAccountNumber)
            break

def fourthCustomerInterface(userName, userPassword, userAccountNumber):
    printAdditionalLines()
    while True:
        startDate = input("Please enter the starting date (YYYY/MM/DD): ")
        try:
            startDate2 = datetime.datetime.strptime(startDate, '%Y/%m/%d')
            if startDate2 > datetime.datetime.today():
                print("Invalid date is entered. Please Reenter")
                continue
            break
        except ValueError:
            print("Invalid date is entered. Please Reenter")

    while True:
        endDate = input("Please enter the end date (YYYY/MM/DD): ")
        try:
            endDate2 = datetime.datetime.strptime(endDate, '%Y/%m/%d')
            break
        except:
            print("Invalid date is entered. Please Reenter")
       
    print(printAccountReport(userAccountNumber, startDate2, endDate2))

    while True:
        userInput = input('Enter "R" to return back: ')
        if userInput == "R":
            customerInterface(userName, userPassword, userAccountNumber)
            break


#Create Default Super User Account
createSuperUserAccount(['mark', 'mark123'])


#main program
print(" ")
print("Hello sir/madam")
print("Who are you?")
theString = """
     ***          1. SuperUser         ***
     ***          2. Admin Staff       ***
     ***          3. Customer          ***

         ** Enter "R" to exit **
                """
            
print(theString) 
userOption = input("Plase select one of the options (1/2/3): ")
while userOption != '1' and userOption != '2' and userOption != '3' and userOption != 'R':
    print("Invalid Option is selected. Please enter one of the given options (1/2/3)")
    userOption = input("Enter your option: ")   

if userOption == '1':
    superUserLoginInterface()
elif userOption == '2':
    adminLoginInterface()
elif userOption == '3':
    customerLoginInterface()
else:
    print("Thank you. Bye")
        




            