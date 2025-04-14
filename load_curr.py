'''
    Load Current Day Stocks from Fidelity downloads.

    To generate the download, 
    1. from the Fidelity Positions tab, click the 
       right hand submenu (three vertical dots) and choose "Download"
    2. move the downloaded file to this project's _data directory
    3. run "main.py"
    4. open the "_data/stock_current.csv" file
    5. delete "_data/stock_current.csv" file and Fidelity download files from "_data"

'''

import csv 

import global_vars as gv
import util
from table import Table

def load_stocks(hdr:list[str]):
    '''
        Given a line that represents the headers for stock data,
        load the stock data.
    '''
    # if stock table doesn't exist, create it
    if gv.stocks_curr == None:
        gv.stocks_curr = Table.new_table(hdr)

    while True:
        # read stocks until blank line read
        line = next(gv.reader,None)
        while len(line) > 0:
            gv.stocks_curr.append_row_fast(line)
            # print('...',account,line[0:3])
            line = next(gv.reader,None)

        # return nothing - ends read
        return None

def save_stock_data(fn="_data/stock_curr_summary.csv"):
    """
        Save Stock Data to CSV
    """
    stock_cols = ['Account Number','Description','Symbol','Current Value']
    with open(fn,'w',newline='') as cvsfile:
        w = csv.writer(cvsfile)

        prev_acct = ""
        for row in gv.stocks_curr:
            if prev_acct != row['Account Number']:
                prev_acct = row['Account Number']
                w.writerow("")

            w.writerow(util.concat_values(row,stock_cols))

def init():
    """
        Add to a function lookup dictionary which
        translates a header line into a load function.
    """
        
    # below are headers that identify accounts and stocks to be loaded
    ld_stock   = "Account Number,Account Name,Symbol,Description,Quantity,Last Price,Last Price Change,Current Value,Today's Gain/Loss Dollar,Today's Gain/Loss Percent,Total Gain/Loss Dollar,Total Gain/Loss Percent,Percent Of Account,Cost Basis Total,Average Cost Basis,Type"

    my_lookup = {
        ld_stock:load_stocks
    }

    gv.func_lookup.update(my_lookup)

def save_data():
    '''
        If any stock data has been loaded,
        save it to a csv file.
    '''
    if gv.stocks_curr != None:
        gv.stocks_curr.sort(['Account Name','Symbol'])
        save_stock_data() 