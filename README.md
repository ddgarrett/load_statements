# Load Fidelity CSV Statements

Parse and consolidate various downloads created by Fidelity, Chase, Wells Fargo and
American Express.

Parse Quarterly and Monthly CSV Files created by Fidelity Statements and generate a summary.csv
with a summary by account showing stock value.

Parse monthly transaction downloads from Fidelity Visa, Chase, Wells Fargo and 
American express and create a consolidated transaction.csv file.

When run, processes all of the data in _data directory. Note that the _data directory
is **not** backed up due to its sensitive nature such as account numbers.

After processing user should manually create a subdirectory in _data and move all .csv files to a that subdirectory.

Fidelity Statement data is used by Google Sheet "Finances Summary".

Monthly transaction data is used in Google Sheets "Monthly Expenses YYYY", 
where "YYYY" is the year for the monthly transaction data.

Both of the above processes help support replacements for Mint's transaction extract and
net worth functions. Mint is no longer available and CreditKarma does little more than show you 
your credit status and attempt to get you to sign up for credit cards.

## Add New CSV Processor

CSV Processors process a particular type of CSV file to produce another CSV which 
contains a reformatted or summarize version of the input CSV data.

To create a new CSV processor:
1. Create new file (module) with code to detect and process a specific CSV
   1. Assumes the input CSV column  headings are unique to that particular processor
   2. If the CSV column headings are not unique, make a slight change to the heading names to make them unique
   3. See load_txn.py for an example
   4. All processors must have
        - init() - to initialize module
        - save_data() - to save the final results, if any
        - for each input CSV type, a load_xxx(header:list[str]) which loads input CSV data for a specific type of CSV.
2. Modify main.py to use the module:
    1. import the module as modname
    2. call modname.init()
    3. call modname.save()