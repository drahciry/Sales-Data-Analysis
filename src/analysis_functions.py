# ------- Imports -------

# Import necessary classes
from decimal import Decimal, getcontext
from datetime import date
import pandas as pd
import os
import re

# ------- Top Logicals -------

# Increase the context to 18
getcontext().prec = 18

# Spreadsheet's path complete
script_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(script_dir)
FULL_PATH_RAW = os.path.join(parent_dir, 'data', 'raw', 'sales_relatory.xlsx')
FULL_PATH_PROCESSED = os.path.join(parent_dir, 'data', 'processed')

# Today date
today = date.today()

# Open all sheets and save in dataframes
df_clients = pd.read_excel(FULL_PATH_RAW, 'Clients')
df_products = pd.read_excel(FULL_PATH_RAW, 'Products')
df_sales = pd.read_excel(FULL_PATH_RAW, 'Sales')

# Converts the date to format datetime
df_sales['sale_date'] = pd.to_datetime(df_sales['sale_date'], format='%d/%m/%Y')

# Converts the cost to string
df_sales['cost_str'] = df_sales['cost'].astype(str)
# Before, converts the cost to Decimal()
df_sales['cost_decimal'] = df_sales['cost_str'].apply(Decimal)

# ------- Functions -------

def validate_id(**id) -> bool:
    """
    Validate if the id exists and, if exists,
    validate the id using regex.

    Args:
        **id (dict): The id key with id value.
    Returns:
        bool: Returns if the id is valid with boolean value.
    """
    # ID -> id_client
    if id.get('id_client'):
        pattern = r'C\d{3,}'
        if re.fullmatch(pattern=pattern, string=id['id_client']):
            return True
    # ID -> id_product
    elif id.get('id_product'):
        pattern = r'P\d{3,}'
        if re.fullmatch(pattern=pattern, string=id['id_product']):
            return True
    # ID -> id_sale
    elif id.get('id_sale'):
        pattern = r'V\d{3,}'
        if re.fullmatch(pattern=pattern, string=id['id_sale']):
            return True
    # ID -> doesn't exists
    else:
        raise KeyError("The ID does't exists.")
    return False

def income_day(date: str) -> Decimal:
    """
    Performs a query on dataframe 'df_sales' with date
    and returns the day income.

    Args:
        date (str): Desired date for returns day income.
    Returns:
        Decimal: The values income at day informed.
    """
    # Converts the date to format datetime
    date = pd.to_datetime(date)
    # Filter the incomes at day
    incomes = df_sales['cost_decimal'][df_sales['sale_date'] == date]
    # Verify if income is empty
    if incomes.empty:
        return Decimal('0')
    # Returns sum incomes as Decimal
    return incomes.sum()

def client_income_day(id_client: str, date: str) -> Decimal:
    """
    Performs a query on dataframe 'df_sales' with date
    and returns the client day income.

    Args:
        date (str): Desired date for returns client day income.
    Returns:
        Decimal: The client values income at day informed.
    """
    # Converts the date to format datetime
    date = pd.to_datetime(date, format='%d/%m/%Y')
    # Verify if 'id_client' is valid
    if not validate_id(id_client=id_client):
        return None
    # Filter the income at day
    income = df_sales['cost_decimal'][(df_sales['id_client'] == id_client) & (df_sales['sale_date'] == date)]
    # Verify if income is empty
    if income.empty:
        return Decimal('0')
    # Returns sum incomes as Decimal
    return income.sum()

def better_clients(beginning: str='01/01/2025', ending: str=today) -> pd.DataFrame:
    """
    In dataframe 'df_sales', verify wich clients (top 5)
    is buying more than others between the dates informed. 

    Args:
        beginning (str): Beginning date of period.
        ending (str): ending date of period.
    Returns:
        DataFrame: A dataframe with top 5 better clients.
    """
    # Converts the dates to format datetime
    beginning = pd.to_datetime(beginning, format='%d/%m/%Y')
    ending = pd.to_datetime(ending, format='%d/%m/%Y')
    # Filter clients adding incomes between the dates, adding 'cost'
    clients_incomes = df_sales[(df_sales['sale_date'] >= beginning) & (df_sales['sale_date'] <= ending)].groupby('id_client')['cost_decimal'].sum()
    # Find the top 5 better clients
    top_five = clients_incomes.nlargest(5, 'last')
    # Returns top 5
    return top_five

def worse_clients(beginning: str='01/01/2025', ending: str=today) -> pd.DataFrame:
    """
    In dataframe 'df_sales', verify wich clients (top 5)
    is buying less than others between the dates informed. 

    Args:
        beginning (str): Beginning date of period.
        ending (str): ending date of period.
    Returns:
        DataFrame: A dataframe with top 5 worse clients.
    """
    # Converts the dates to format datetime
    beginning = pd.to_datetime(beginning, format='%d/%m/%Y')
    ending = pd.to_datetime(ending, format='%d/%m/%Y')
    # Filter clients adding incomes between the dates, adding 'cost'
    clients_incomes = df_sales[(df_sales['sale_date'] >= beginning) & (df_sales['sale_date'] <= ending)].groupby('id_client')['cost_decimal'].sum()
    # Find the top 5 better clients
    top_five = clients_incomes.nsmallest(5, 'last')
    # Returns top 5
    return top_five

def income_history(beginning: str='01/01/2025', ending: str=today) -> pd.DataFrame:
    """
    Create a dataframe with all 
    days since beginning until ending.
    
    Args:
        beginning (str): Beginnig date of period (default: 01/01/2025).
        ending (str): ending date of period.
    Returns:
        DataFrame: A dataframe with income history
        the beginning and the ending. 
    """
    # Converts the dates to format datetime
    beginning = pd.to_datetime(beginning, format='%d/%m/%Y')
    ending = pd.to_datetime(ending, format='%d/%m/%Y')
    # Capture and sort dates between the beginning and the ending
    dates = pd.date_range(start=beginning, end=ending, freq='D')
    # Create history for save accumulated income
    history = []
    # Dictionary with accumulated income
    accumulated_income = {pid: Decimal('0') for pid in df_sales['id_client']}
    # Capture and sort all id_client
    id_clients = df_clients['id_client'].unique()
    # Iter in 'dates' for save income by date
    for actual_date in dates:
        # Iter in 'id_clients' for save income by client
        for pid in id_clients:
            # Income at day (actual_date)
            daily_income = client_income_day(pid, actual_date)
            # Accumulate income by client
            accumulated_income[pid] = accumulated_income[pid] + daily_income
            # Captures the name and surname's client
            name = df_clients['name'][df_clients['id_client'] == pid].item()
            surname = df_clients['surname'][df_clients['id_client'] == pid].item()
            # Appending all datas to history
            history.append(
                {
                    'id_client': pid,
                    'full_name': " ".join([name, surname]),
                    'date': actual_date,
                    'daily_income': float(daily_income),
                    'accumulated_income': float(accumulated_income[pid])
                }
            )
    # Convert history to dataframe
    df_history = pd.DataFrame(history)
    # Guarantees that column 'date' is a datetime
    df_history['date'] = pd.to_datetime(df_history['date'], format='%d/%m/%Y')
    # Create the file 'history_income_{ending}.xlsx'
    df_history.to_excel(os.path.join(FULL_PATH_PROCESSED, f'history_income_{today}.xlsx'), index=False, sheet_name='Incomes')
    # Value columns list
    columns = ['daily_income', 'accumulated_income']
    # Converts value columns to Decimal
    for column in columns:
        df_history[column + '_str'] = df_history[column].astype(str)
        df_history[column + '_decimal'] = df_history[column + '_str'].apply(Decimal)
    # Returns the dataframe df_history
    return df_history

def best_sellers_day(date: str) -> pd.DataFrame:
    """
    Performs a query in df_sales and group all products
    at day for verify wich is the best sellers. 

    Args:
        date (str): Desired date for returns the best sellers at day.
    Returns:
        DataFrame: a dataframe with the best sellers and yours quantity.
    """
    # Converts date to format datetime
    date = pd.to_datetime(date, format='%d/%m/%Y')
    # Filter the sales with date
    product_quantity = df_sales[['id_product', 'quantity']][df_sales['sale_date'] == date].groupby('id_product').sum()
    # Sort products by quantity
    product_quantity = product_quantity.sort_values('quantity', ascendinging=False)
    # Save the biggest quantity finded
    biggest_quantity = product_quantity['quantity'].iloc[0]
    # Filter with biggest quantity
    best_seller = product_quantity[product_quantity['quantity'] == biggest_quantity] 
    # Returns the best_sellers
    return best_seller

def sales_with_product_names() -> pd.DataFrame:
    """
    Get a dataframe with all sales and products name.
    Uses a pd.merge for this.

    Returns:
        DataFrame: A dataframe with sales and yours products name.
    """
    sales_named = pd.merge(
        df_sales,
        df_products[['id_product', 'name_product']],
        on='id_product'
    )
    # Returns the dateframe 'sales_named'
    return sales_named

def products_running_out() -> pd.DataFrame:
    """
    Verify wich products are running out.

    Rule: Products with less or equal 50 unities.
    
    Returns:
        DataFrame: a dataframe with products and yours quantity.
    """
    # Returns products running out
    return df_products[['id_product', 'stock']][df_products['stock'] <= 50].sort_values('stock')

def best_sales(date: str=None) -> pd.DataFrame:
    """
    The best sales made on period. If data is None, will be
    all. But if doesn't be, will be just at day informed.

    Rule: Sales greater or equal 4,500.00 cost.

    Args:
        data (str): Desired date for returns best sales on period.
        The date will be defined as None (default).
    Returns:
        DataFrame: A dataframe with the best sales on period.
    """
    # Columns that will be used
    columns = ['id_sale', 'sale_date', 'id_product', 'cost']
    # Filter all the best sales
    sales = df_sales[columns][df_sales['cost'] >= 4500.0]
    # Verify if the date is None
    if not date:
        # If checked, returns all sales greater than 4,500.00
        return sales
    # If isn't None, converts the date to format datetime
    date = pd.to_datetime(date, format='%d/%m/%Y')
    # Filter sales by date and drop column 'sale_date'
    sales = sales[sales['sale_date'] == date]
    # Returns best sales at day greater than 4,500.00
    return sales

def best_sales_history(beginning: str='01/01/2025', ending: str=today) -> pd.DataFrame:
    """
    Create a worksheet with best sales using
    merge for capture name of products.

    Args:
        beginning (str): Start of period desired (default = '01/01/2025').
        ending (str): ending of period desired.
    Returns:
        DataFrame: A dataframe with best sales and yours name.
    """
    # Converts the dates to format datetime
    beginning = pd.to_datetime(beginning, format='%d/%m/%Y')
    ending = pd.to_datetime(ending, format='%d/%m/%Y')
    # Capture all best sales (greater or equal 4,500.00 cost)
    sales = best_sales()
    # Filter best sales with date
    sales = sales[(sales['sale_date'] >= beginning) & (sales['sale_date'] <= ending)]
    # Uses 'df_products' for merge
    sales_named = pd.merge(
        sales[['id_sale', 'sale_date', 'id_product', 'cost']],
        df_products[['id_product', 'name_product']],
        on='id_product'
    )
    # Create a worksheet with 'df_sales'
    sales_named.to_excel(os.path.join(FULL_PATH_PROCESSED, f'best_sales_{today}.xlsx'), index=False, sheet_name='Best Sales')
    # Create new Series for cost_decimal
    sales_named['cost_str'] = sales_named['cost'].astype(str)
    sales_named['cost_decimal'] = sales_named['cost_str'].apply(Decimal)
    # Returns the dataframe with the best sales history on period
    return df_sales

def sales_by_state(beginning: str='01/01/2025', ending: str=today) -> pd.DataFrame:
    """
    Get a dataframe with sales by state and
    create a worksheet.

    Args:
        beginning (str): Start of period desired (default = '01/01/2025').
        ending (str): ending of period desired.
    Returns: 
        DataFrame: A dataframe with sales and yours states.
    """
    # Converts the dates to format datetime
    beginning = pd.to_datetime(beginning, format='%d/%m/%Y')
    ending = pd.to_datetime(ending, format='%d/%m/%Y')
    # Columns that will be used
    columns = ['id_client', 'quantity', 'cost']
    # Filter the sales by the dates
    sales = df_sales[columns][(df_sales['sale_date'] >= beginning) & (df_sales['sale_date'] <= ending)]
    # Merge 'sales' with 'df_clients'
    state_sales = pd.merge(
        sales,
        df_clients[['id_client', 'state']],
        on='id_client'
    )
    # Convert column 'cost' to Decimal
    state_sales['cost'] = state_sales['cost'].astype(str)
    state_sales['cost'] = state_sales['cost'].apply(Decimal)
    # Drop column 'id_client', group by 'state' and sum quantity & cost
    state_sales = state_sales.drop(columns=['id_client']).groupby('state').sum()
    # Back with float on 'coast'
    state_sales['cost'] = state_sales['cost'].astype(float)
    # Reset Index
    state_sales.reset_index(inplace=True)
    # Create a worksheet
    state_sales.to_excel(os.path.join(FULL_PATH_PROCESSED, f'sales_by_state_{today}.xlsx'), index=False, sheet_name='Sales by State')
    # Create columns 'cost_str' and 'cost_decimal'
    state_sales['cost_str'] = state_sales['cost'].astype(str)
    state_sales['cost_decimal'] = state_sales['cost_str'].apply(Decimal)
    # Returns the dataframe with sales by state
    return state_sales