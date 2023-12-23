# Load Fidelity CSV Statements

Parse and consolidate various downloads created by Fidelity, Chase, Wells Fargo and
American Express.

Parse Quarterly and Monthly CSV Files created by Fidelity Statements and generate a summary.csv
with a summary by account showing stock value.

Parse monthly transaction downloads from Fidelity Visa, Chase, Wells Fargo and 
American express and create a consolidated transaction.csv file.

When run, processes all of the data in _data directory. Note that the _data directory
is **not** backed up due to its sensitive nature such as account numbers.

After processing user should manually create and move all .csv files to a subdirectory
for that month or quarter.
