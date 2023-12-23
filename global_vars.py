'''
    Global fields including configuration values
'''

from __future__ import annotations

from table import Table

accounts:Table = None   # Table defining accounts
stocks:Table   = None   # Table defining stocks within an account

txn_col = ["Date","Description","Amount","Account Name","Labels"]
transactions   = Table.new_table(txn_col)

reader = None  # CSV Reader

func_lookup:dict[list[str],callable] = {}