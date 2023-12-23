'''
    Load Stocks and Releated Account Information from Fidelity downloads.
'''

import csv 

import global_vars as gv
import util
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

def save_stock_data(fn="_data/stock_summary.csv"):
    """
        Save Account and Stock Data to CSV
    """
    acct_cols = ['Account Type','Account','Ending mkt Value']
    stock_cols = ['Account','Description','Symbol/CUSIP','Ending Value']
    with open(fn,'w',newline='') as cvsfile:
        w = csv.writer(cvsfile)

        for row in gv.accounts:
            w.writerow(util.concat_values(row,acct_cols))

        prev_acct = ""
        for row in gv.stocks:
            if prev_acct != row['Account']:
                prev_acct = row['Account']
                w.writerow("")

            w.writerow(util.concat_values(row,stock_cols))

def init():
    # below are headers that identify accounts and stocks to be loaded
    ld_stk_account = "Account Type,Account,Beginning mkt Value,Change in Investment"
    ld_stock   = "Symbol/CUSIP,Description,Quantity,Price"

    my_lookup = {
        ld_stk_account:load_account,
        ld_stock:load_stocks
    }

    gv.func_lookup.update(my_lookup)

def save_data():
    '''
        If any stock data has been loaded,
        save it to a csv file.
    '''
    if gv.accounts != None:
        gv.accounts.sort(['Account'])
        gv.stocks.sort(['Account','Symbol/CUSIP'])
        save_stock_data() 