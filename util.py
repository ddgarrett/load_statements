"""
    Utility functions used by various modules
"""
import global_vars as gv

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

def concat_values(row,cols):
    """
        Concatentate the specified columns from row
        into a single list. Should be called project_row?
    """
    data = []
    for c in cols:
        data.append(row[c])

    return data
