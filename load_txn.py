'''
    Load detailed transaction history downloaded from 
    Wells Fargo, Chase, Fidelity and American Express.

    Generate a file which combines the transactions
    into a single CSV.
'''
import csv

import global_vars as gv
import util
from table import Table


# init output table
txn_col = ["Date","Description","Amount","Account Name","Labels"]
transactions   = Table.new_table(txn_col)

def load_wells_txn(hdr:list[str]):

    account = "wellsfargo"
    if gv.fileName.startswith("CreditCard"):
        account = "wfcc"

    print(f"*********** loading {account}")

    # read to end of file
    data = next(gv.reader,None)
    while data != None and len(data) > 4:
        transactions.append_row_fast([data[0],data[4],util.negate_amount(data[1]),account,"fixed"])
        data = next(gv.reader,None)

def load_fidel_txn(hdr:list[str]):
    print("*********** loading fidelity")

    # read to end of file
    data = next(gv.reader,None)
    while data != None and len(data) > 4:
        # print(data)
        # reformat date from yyyy-mm-dd to mm/dd/yyyy
        date = data[0]
        date_fmt = f'{date[5:7]}/{date[8:10]}/{date[0:4]}'
        transactions.append_row_fast([date_fmt,data[2],util.negate_amount(data[4]),"fidelity","fixed"])
        data = next(gv.reader,None)

def load_chase_txn(hdr:list[str]):
    print("*********** loading chase")

    # read to end of file
    data = next(gv.reader,None)
    while data != None and len(data) > 5:
        # print(data)
        transactions.append_row_fast([data[0],data[2],util.negate_amount(data[5]),"chase","fixed"])
        data = next(gv.reader,None)

def load_amex_txn(hdr:list[str]):
    print("*********** loading amex")

    # read to end of file
    data = next(gv.reader,None)
    while data != None:
        # print(data)
        transactions.append_row_fast([data[0],data[1],data[2],"amex","fixed"])
        data = next(gv.reader,None)


def save_txn_data(fn="_data/transactions.csv"):
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
    ld_wells = "Date,Amount,na1,na2,Description"
    ld_fidel = "Date,Transaction,Name,Memo,Amount"
    ld_chase = "Transaction Date,Post Date,Description,Category,Type,Amount,Memo"
    ld_amex  = "Date,Description,Amount"

    my_lookup = {
        ld_wells: load_wells_txn,
        ld_fidel: load_fidel_txn,
        ld_chase: load_chase_txn,
        ld_amex:  load_amex_txn
    }

    gv.func_lookup.update(my_lookup)

def save_data():
    """
        If any transaction data has been loaded,
        save it to a csv file.
    """
    if len(transactions.rows()) > 0:
        transactions.sort(["Date","Description","Amount"])
        save_txn_data()