'''
    Main program for Load Statements.

    Read a CSV line by line, splitting it by commas.

    Call stock or transaction loading functions
    based on unique headers for downloaded csv files.

'''
from __future__ import annotations

import csv
from os import listdir
from os.path import isfile, join

import global_vars as gv

import load_stocks as ldstk
import load_txn    as ldtxn
import load_activity as ldact

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
        which processes statements after the header line
    '''
    for key in gv.func_lookup:
         if test_line(key,line):
              return gv.func_lookup[key]
         
    return None

def main():

    # initialize stock and transaction loading modules
    ldstk.init()
    ldtxn.init()
    ldact.init()

    mypath = '_data'
    onlyfiles = [join(mypath,f) for f in listdir(mypath) if isfile(join(mypath, f))]
    
    for fn in onlyfiles:
        with open(fn, newline='') as csvfile:
            gv.reader = csv.reader(csvfile)
            line  = next(gv.reader,None)
            while not line == None:
                # if csv line a recognized header line
                # call the function that processes that csv file
                func = line_func(line)
                if func:
                    line = func(line)
                else:
                    line  = next(gv.reader,None)

    # store any data loaded by stock and transaction loading modules
    ldstk.save_data()
    ldtxn.save_data() 
    ldact.save_data() 

if __name__ == '__main__':
    main()

