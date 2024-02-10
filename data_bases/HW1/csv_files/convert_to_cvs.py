import pandas as pd

excel_file = 'customer_and_transaction.xlsx'
sheets = pd.read_excel(excel_file, sheet_name=None)
transactions_csv_path = 'transactions.csv'
customers_csv_path = 'customers.csv'
sheets['transaction'].to_csv(transactions_csv_path, sep=';', index=False, encoding='utf-8')
sheets['customer'].to_csv(customers_csv_path, sep=';', index=False, encoding='utf-8')
