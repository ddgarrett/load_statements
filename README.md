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