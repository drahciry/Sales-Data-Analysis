# Import analysis funcions
from .analysis_functions import income_history, best_sales_history, sales_by_state

# ------- Starting ETL -------

print('Starting ETL...')

print('Create a worksheet for incomes...')
income_history()

print('Create a worksheet for best sales history...')
best_sales_history()

print('Create a worksheet for sales by state...')
sales_by_state()