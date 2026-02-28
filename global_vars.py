'''
    Global fields including configuration values
'''

from __future__ import annotations

from table import Table

accounts:Table = None   # Table defining accounts
stocks:Table   = None   # Table defining stocks within an account

stocks_curr:Table = None # Table defining stocks for current day

# lookup: header key -> callable(reader, fileName, line) -> next line or None
func_lookup: dict[str, callable] = {}