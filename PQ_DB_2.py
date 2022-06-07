import csv
import sqlite3
import re

def generateTable(cur): # Create PQ Table. If it exists, ignore.
    try:
        cur.execute('CREATE TABLE PQ_Data (Batch_ID TEXT, Date TEXT)')
    except:
        pass

def getID():
    info_list = []
    pattern = re.compile('[0-9]{4}-[0-9]{2}-[0-9]{2}')
    ID_var = input('ID as Number Integer: ')
    info_list.append(ID_var)
    # Create functions we call later.
    def getInput():       
        Date_var = input('Date in "YYYY-MM-DD": ')
        return Date_var

    def checkInput(pattern, Date_var: str):
        if pattern.fullmatch(Date_var):
            info_list.append(Date_var)
            return Date_var
        else:
            print('Pattern is incorrect')
            Date_var = getInput()
            checkInput(pattern, Date_var)
            return Date_var

    Date_var = getInput()
    Date_var = checkInput(pattern, Date_var)
    print(f'ID is {ID_var} and date is {Date_var}')
    return info_list
    
def updateID(cur, info_list): # Read original file (replace with SQL) Use regex to find matches
    cur.execute("INSERT INTO PQ_Data VALUES (?, ?)", info_list)

def getReport(csr_name):
    pattern = re.compile("Y|N")

    def getInput():       
        input_var = input('Would you like a report "Y/N?": ')
        return input_var
    
    def checkInput(pattern, input_var):
        if pattern.fullmatch(input_var):
            return input_var
        else:
            print('Pattern is incorrect')
            input_var = getInput()
            checkInput(input_var)
            return input_var

    def title(csr_name):
        try:
            with open(csr_name, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerow(['Batch__ID', 'Date'])
        except:
            with open(csr_name, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerow(['Batch__ID', 'Date'])

    input_var = getInput()
    input_var = checkInput(pattern, input_var)

    if input_var == 'Y':
        title(csr_name)
        for row in cur.execute('SELECT * FROM PQ_Data'): 
            print(row)
            try:
                with open(csr_name, 'a', newline='') as csvfile:
                    writer = csv.writer(csvfile, delimiter=',')
                    row = list(row)
                    writer.writerow(row)
            except:
                with open(csr_name, 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile, delimiter=',')
                    row = list(row)
                    writer.writerow(row)
    else:
        pass

if __name__ == "__main__":
    csr_name = 'Sample_Report.csv'

    con = sqlite3.connect('PQ_Data.db') #instance of sqlite3 connection class. Change table
    cur = con.cursor()

    info_list = getID()
    generateTable(cur)
    updateID(cur, info_list)
    getReport(csr_name)

    con.commit() 
    con.close()