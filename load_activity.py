'''
    Load detailed Fidelity activity and order downloads.
'''
import csv

import global_vars as gv
import util
from table import Table


# init output table
txn_col = ["Date", "Account", "Symbol", "Action", "Security Descr", "Quantity", "Price", "Amount"]
transactions   = Table.new_table(txn_col)

def load_fidelity_activity(hdr:list[str]):
    """
    """
    print("*********** loading fidelity activity and orders")

    # read to end of file
    data = next(gv.reader,None)
    while data != None and len(data) > 14:
        transactions.append_row_fast([data[0],data[1],data[4],data[3],data[5],data[11],data[10],data[16]])
        data = next(gv.reader,None)


def save_txn_data(fn="_data/fidelity_activity_orders.csv"):
    """
        Save Transacton Data to CSV
    """
    with open(fn,'w',newline='') as cvsfile:
        w = csv.writer(cvsfile)

        w.writerow(txn_col)
        for row in transactions:
            w.writerow(row._data)

def init():
    """
        Add to a function lookup dictionary which
        translates a header line into a load function.
    """

    # Initialize function lookup dictionary
    # below are headers that identify transactions to be loaded
    ld_activity = "Run Date,Account,Account Number,Action,Symbol,Description,Type,Exchange Quantity,Exchange Currency,Currency,Price,Quantity,Exchange Rate,Commission,Fees,Accrued Interest,Amount,Settlement Date"
    
    my_lookup = {
        ld_activity: load_fidelity_activity
    }

    gv.func_lookup.update(my_lookup)

def save_data():
    """
        If any transaction data has been loaded,
        save it to a csv file.
    """
    if len(transactions.rows()) > 0:
        transactions.sort(["Account","Date","Symbol","Action"])
        save_txn_data()