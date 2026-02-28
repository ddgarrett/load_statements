'''
    Global fields including configuration values
'''

from __future__ import annotations

from table import Table

accounts:Table = None   # Table defining accounts
stocks:Table   = None   # Table defining stocks within an account

stocks_curr:Table = None # Table defining stocks for current day

reader = None  # CSV Reader
fileName = None  # CSV File Name

# lookup function to call 
# based on CSV header
func_lookup:dict[list[str],callable] = {}