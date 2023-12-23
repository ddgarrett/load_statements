'''
    Main program for Load Statements.

    Read a CSV line by line, splitting it by commas.

    Ignore any blank lines
    If line[0] == 'Account Type' process account summary.
    Else if line[0] == 'Symbol/CUSIP' process account details.
    Else ignore the line.

'''
from __future__ import annotations
from typing import Callable

import csv
from os import listdir
from os.path import isfile, join

import global_vars as gv
from table import Table


def load_account(hdr:list[str]):
    '''
        Given a line that represents the headers for the account data
        load account data from CSV.
    '''
    # If account table is None, create it using hdr
    if gv.accounts == None:
        gv.accounts = Table.new_table(hdr)

    line  = next(gv.reader,None)
    while len(line) == len(hdr):
        gv.accounts.append_row_fast(line)
        line  = next(gv.reader,None)

    return line

def load_stocks(hdr:list[str]):
    '''
        Given a line that represents the headers for stock data,
        load the stock data.
    '''
    # if stock table doesn't exist, create it
    if gv.stocks == None:
        hdr.extend(['Account','Type'])
        gv.stocks = Table.new_table(hdr)

    # skip two lines
    next(gv.reader)
    next(gv.reader)

    while True:
        # read account number and type
        account = next(gv.reader)[0].strip()
        type = next(gv.reader)[0]
        # print('...',account,type[0])

        # read stocks until 'Subtotal of...' read
        line = next(gv.reader,None)
        while not line[0].startswith('Subtotal of'):
            line.extend([account,type]) 
            gv.stocks.append_row_fast(line)
            # print('...',account,line[0:3])
            line = next(gv.reader,None)

        # skip one line
        line = next(gv.reader,None)

        # if no next line, return
        if line == None:
            return None

def negate_amount(amount:str) -> str:
    '''
        Given a number as a string,
        return the negative of that number.
    '''
    if len(amount) == 0:
        return "0"
    
    if amount[0] == '-':
        return amount[1:]
    else:
        return ('-' + amount)

def load_wells_txn(hdr:list[str]):
    print("*********** loading wells fargo")

    # read to end of file
    data = next(gv.reader,None)
    while data != None and len(data) > 4:
        gv.transactions.append_row_fast([data[0],data[4],negate_amount(data[1]),"wellsfargo","fixed"])
        data = next(gv.reader,None)

def load_fidel_txn(hdr:list[str]):
    print("*********** loading fidelity")

    # read to end of file
    data = next(gv.reader,None)
    while data != None and len(data) > 4:
        # print(data)
        gv.transactions.append_row_fast([data[0],data[2],negate_amount(data[4]),"fidelity","fixed"])
        data = next(gv.reader,None)

def load_chase_txn(hdr:list[str]):
    print("*********** loading chase")

    # read to end of file
    data = next(gv.reader,None)
    while data != None and len(data) > 5:
        # print(data)
        gv.transactions.append_row_fast([data[0],data[2],negate_amount(data[5]),"chase","fixed"])
        data = next(gv.reader,None)

def load_amex_txn(hdr:list[str]):
    print("*********** loading amex")

    # read to end of file
    data = next(gv.reader,None)
    while data != None:
        # print(data)
        gv.transactions.append_row_fast([data[0],data[1],data[2],"amex","fixed"])
        data = next(gv.reader,None)

def test_line(tst:str,line:list[str]) -> bool:
    '''
        Return True if the string array 'line'
        starts with the same strings as 'tst'.
    '''
    l = ','.join(line)
    return l.startswith(tst)
        
def line_func(line:list[str]) -> callable:
    '''
        Given a parsed CSV line, return the function
        which processes statements after the line
    '''
    for key in gv.func_lookup:
         if test_line(key,line):
              return gv.func_lookup[key]
         
    return None

def concat_values(row,cols):
    data = []
    for c in cols:
        data.append(row[c])

    return data

def save_stock_data(fn="_data/stock_summary.csv"):
    """
        Save Account and Stock Data to CSV
    """
    acct_cols = ['Account Type','Account','Ending mkt Value']
    stock_cols = ['Account','Description','Symbol/CUSIP','Ending Value']
    with open(fn,'w',newline='') as cvsfile:
        w = csv.writer(cvsfile)

        for row in gv.accounts:
            w.writerow(concat_values(row,acct_cols))

        prev_acct = ""
        for row in gv.stocks:
            if prev_acct != row['Account']:
                prev_acct = row['Account']
                w.writerow("")

            w.writerow(concat_values(row,stock_cols))

def save_txn_data(fn="_data/transactions.csv"):
    """
        Save Transacton Data to CSV
    """
    with open(fn,'w',newline='') as cvsfile:
        w = csv.writer(cvsfile)

        w.writerow(gv.txn_col)
        for row in gv.transactions:
            w.writerow(row._data)

def main():
    # below are headers that identify accounts and stocks to be loaded
    ld_stk_account = "Account Type,Account,Beginning mkt Value,Change in Investment"
    ld_stock   = "Symbol/CUSIP,Description,Quantity,Price"

    ld_wells = "Date,Amount,na1,na2,Description"
    ld_fidel = "Date,Transaction,Name,Memo,Amount"
    ld_chase = "Transaction Date,Post Date,Description,Category,Type,Amount,Memo"
    ld_amex  = "Date,Description,Amount"

    gv.func_lookup = {
        ld_stk_account:load_account,
        ld_stock:load_stocks,

        ld_wells: load_wells_txn,
        ld_fidel: load_fidel_txn,
        ld_chase: load_chase_txn,
        ld_amex:  load_amex_txn

    }

    mypath = '_data'
    onlyfiles = [join(mypath,f) for f in listdir(mypath) if isfile(join(mypath, f))]
    
    for fn in onlyfiles:
        with open(fn, newline='') as csvfile:
            gv.reader = csv.reader(csvfile)
            line  = next(gv.reader,None)
            while not line == None:
                # is csv line a recognized header line?
                func = line_func(line)
                if func:
                    line = func(line)
                else:
                    line  = next(gv.reader,None)

    # sort accounts by account and stocks by account and symbol
    if gv.accounts != None:
        gv.accounts.sort(['Account'])
        gv.stocks.sort(['Account','Symbol/CUSIP'])
        save_stock_data()  

    if len(gv.transactions.rows()) > 0:
        # gv.transactions.sort(['Date','Account Name']) - doesn't work - date and amounts are not date,numeric columns
        save_txn_data()

    

if __name__ == '__main__':
    main()

