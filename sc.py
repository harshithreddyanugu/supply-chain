import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
import numpy as np # For numerical operations, e.g., NaN checks

# --- Helper Functions ---

def format_currency(value):
    """Formats a numerical value into a currency string in millions."""
    if value is None or pd.isna(value):
        return '$N/A'
    return f"${(value / 1000000):.2f}M"

def format_currency_k(value):
    """Formats a numerical value into a currency string in thousands."""
    if value is None or pd.isna(value):
        return '$N/A'
    return f"${(value / 1000):.0f}K"

# --- Dummy Data Generation (Fallback) ---

def generate_dummy_data():
    """Generates realistic-looking dummy data for the dashboard."""
    current_inventory_value = np.random.randint(20, 30) * 1000000
    missing_stock_amount = np.random.randint(1, 7) * 1000000
    excess_stock_value = np.random.randint(1, 3) * 1000000

    total_items = np.random.randint(50, 100)
    total_positions = np.random.randint(200, 300)

    stock_out = int(total_items * (np.random.rand() * 0.1 + 0.05))
    below_safety_stock = int(total_items * (np.random.rand() * 0.2 + 0.15))
    at_stock = int(total_items * (np.random.rand() * 0.3 + 0.25))
    over_stock = total_items - stock_out - below_safety_stock - at_stock

    inventory_status_data = [
        {'name': 'STOCK-OUT', 'value': stock_out, 'color': '#DC2626'},
        {'name': 'BELOW SAFETY STOCK', 'value': below_safety_stock, 'color': '#F59E0B'},
        {'name': 'AT-STOCK', 'value': at_stock, 'color': '#10B981'},
        {'name': 'OVER-STOCK', 'value': over_stock, 'color': '#6366F1'},
    ]

    today = datetime.date.today()
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    # Executive Summary Data
    inventory_evolution_data = []
    for i in range(12):
        date = today - datetime.timedelta(days=30 * i)
        inventory_evolution_data.append({
            'month': f"{months[date.month - 1]} {date.year % 100}",
            'value': np.random.randint(20, 28) * 1000000
        })
    inventory_evolution_data.reverse() # To show from older to newer

    warehouse_summary_data = [
        {'name': 'WH Seattle', 'inventoryValue': np.random.randint(4, 8) * 1000000, 'excessStock': np.random.rand() * 0.8 * 1000000, 'missingStock': np.random.rand() * 1.5 * 1000000, 'positions': np.random.randint(20, 50)},
        {'name': 'WH Chicago', 'inventoryValue': np.random.randint(4, 8) * 1000000, 'excessStock': np.random.rand() * 0.8 * 1000000, 'missingStock': np.random.rand() * 1.5 * 1000000, 'positions': np.random.randint(20, 50)},
        {'name': 'WH New Delhi', 'inventoryValue': np.random.randint(4, 8) * 1000000, 'excessStock': np.random.rand() * 0.8 * 1000000, 'missingStock': np.random.rand() * 1.5 * 1000000, 'positions': np.random.randint(20, 50)},
        {'name': 'WH London', 'inventoryValue': np.random.randint(4, 8) * 1000000, 'excessStock': np.random.rand() * 0.8 * 1000000, 'missingStock': np.random.rand() * 1.5 * 1000000, 'positions': np.random.randint(20, 50)},
        {'name': 'WH Istanbul', 'inventoryValue': np.random.randint(4, 8) * 1000000, 'excessStock': np.random.rand() * 0.8 * 1000000, 'missingStock': np.random.rand() * 1.5 * 1000000, 'positions': np.random.randint(20, 50)},
    ]

    item_evolution_data = []
    for i in range(12):
        date = today - datetime.timedelta(days=30 * i)
        item_evolution_data.append({
            'month': f"{months[date.month - 1]} {date.year % 100}",
            'items': np.random.randint(15, 30)
        })
    item_evolution_data.reverse()

    executive_summary_kpis = {
        'inventory_value': current_inventory_value,
        'missing_stock_amount': missing_stock_amount,
        'excess_stock_value': excess_stock_value,
    }

    # Warehouses Data (simplified from executive_summary_data for consistency)
    warehouse_chart_data = []
    for wh in warehouse_summary_data:
        warehouse_chart_data.append({
            'name': wh['name'],
            'inventoryValue': wh['inventoryValue'],
            'excessStock': wh['excessStock'],
            'missingStock': wh['missingStock'],
            'positions': wh['positions'],
            'stockBreakdown': [
                {'name': 'OVER-STOCK', 'value': np.random.randint(5, 15), 'color': '#6366F1'},
                {'name': 'AT-STOCK', 'value': np.random.randint(10, 20), 'color': '#10B981'},
                {'name': 'BELOW-SAFETY-STOCK', 'value': np.random.randint(5, 15), 'color': '#F59E0B'},
                {'name': 'STOCK-OUT', 'value': np.random.randint(1, 5), 'color': '#DC2626'},
            ]
        })

    # Availability Data
    availability_data = {
        'missingStockAmount': missing_stock_amount,
        'excessStockValue': excess_stock_value,
        'inventoryValue': current_inventory_value,
        'stockOutForecast': [
            {'range': 'within 3 days', 'items': np.random.randint(1, 5)},
            {'range': '4 to 10 days', 'items': np.random.randint(1, 5)},
            {'range': '11 to 20 days', 'items': np.random.randint(1, 5)},
            {'range': '21 to 30 days', 'items': np.random.randint(1, 5)},
        ],
        'itemsToStockOutSoon': [
            {'name': 'Armanda ALW 400', 'days': np.random.randint(1, 30), 'forecast': 'STOCK-OUT'},
            {'name': 'eBike 7', 'days': np.random.randint(1, 30), 'forecast': 'BELOW-SAFETY-STOCK'},
            {'name': 'Armanda BMV 560E', 'days': np.random.randint(1, 30), 'forecast': 'STOCK-OUT'},
            {'name': 'Zebra - Mitorina105', 'days': np.random.randint(1, 30), 'forecast': 'BELOW-SAFETY-STOCK'},
            {'name': 'FlyFighter 120', 'days': np.random.randint(1, 30), 'forecast': 'STOCK-OUT'},
        ],
        'currentInventoryByItem': [
            {'name': 'Armanda ALW 400', 'onHand': np.random.randint(10, 50), 'status': 'STOCK-OUT'},
            {'name': 'eBike 7', 'onHand': np.random.randint(10, 50), 'status': 'BELOW-SAFETY-STOCK'},
            {'name': 'FlyFighter 120', 'onHand': np.random.randint(10, 50), 'status': 'BELOW-SAFETY-STOCK'},
            {'name': 'Armanda BMV 560E', 'onHand': np.random.randint(10, 50), 'status': 'AT-STOCK'},
            {'name': 'Zebra - Mitorina105 C', 'onHand': np.random.randint(10, 50), 'status': 'OVER-STOCK'},
        ],
        'theoreticalOnHandQuantity': [{
            'date': (today + datetime.timedelta(days=i)).strftime('%b %d'),
            'value': np.random.randint(100, 300)
        } for i in range(20)],
    }

    # Excess Stock Data
    excess_stock_data = {
        'percentOverStock': (np.random.rand() * 10) + 20,
        'excessStockValue': excess_stock_value,
        'shareOfExcessStockValue': (np.random.rand() * 5) + 1,
        'excessStockEvolution': [{
            'month': f"{months[((today - datetime.timedelta(days=30*i)).month - 1)]} {((today - datetime.timedelta(days=30*i)).year % 100)}",
            'inventoryValue': np.random.randint(20, 28) * 1000000,
            'excessValue': np.random.rand() * 1.5 * 1000000,
            'excessShare': np.random.rand() * 5 + 1,
        } for i in range(12)],
        'highestExcessItems': [
            {'name': 'Armanda TTR 900', 'excessValue': np.random.randint(100000, 300000), 'share': np.random.rand() * 10 + 20},
            {'name': 'Hiraki F250', 'excessValue': np.random.randint(100000, 300000), 'share': np.random.rand() * 10 + 20},
            {'name': 'Wedside 560', 'excessValue': np.random.randint(100000, 300000), 'share': np.random.rand() * 10 + 20},
            {'name': 'Kamoucha - FB20', 'excessValue': np.random.randint(50000, 300000), 'share': np.random.rand() * 10 + 20},
            {'name': 'Rolad 500 Electric', 'excessValue': np.random.randint(50000, 300000), 'share': np.random.rand() * 10 + 20},
            {'name': 'Van Torino', 'excessValue': np.random.randint(50000, 300000), 'share': np.random.rand() * 10 + 20},
        ],
    }
    excess_stock_data['excessStockEvolution'].reverse()

    # Missing Stock Data
    missing_stock_data = {
        'percentBelowSafetyStock': (np.random.rand() * 20) + 30,
        'percentOutOfStock': (np.random.rand() * 5) + 2,
        'amountToRefill': missing_stock_amount,
        'evolutionOfMissingStockItems': [{
            'month': months[((today - datetime.timedelta(days=30*i)).month - 1)],
            'items': np.random.randint(10, 30)
        } for i in range(10)],
        'evolutionOfMissingStockAmount': [{
            'month': months[((today - datetime.timedelta(days=30*i)).month - 1)],
            'amount': np.random.randint(1, 5) * 1000000
        } for i in range(10)],
        'mostImportantMissingItems': [
            {'name': 'Armanda BMV 560E', 'amount': np.random.randint(50000, 100000), 'status': 'STOCK-OUT'},
            {'name': 'FlyFighter 120', 'amount': np.random.randint(50000, 100000), 'status': 'BELOW SAFETY STOCK'},
            {'name': 'eBike 7', 'amount': np.random.randint(50000, 100000), 'status': 'STOCK-OUT'},
            {'name': 'Armanda BMV 600X', 'amount': np.random.randint(50000, 100000), 'status': 'BELOW SAFETY STOCK'},
            {'name': 'Armanda REG 100', 'amount': np.random.randint(50000, 100000), 'status': 'BELOW SAFETY STOCK'},
        ],
    }
    missing_stock_data['evolutionOfMissingStockItems'].reverse()
    missing_stock_data['evolutionOfMissingStockAmount'].reverse()


    # Historical Status Data
    historical_status_data = {
        'stockStatusOverview': {
            'stockOut': round(np.random.rand() * 0.5 + 0.1, 1),
            'belowSafetyStock': round(np.random.rand() * 10 + 40, 1),
            'atStock': round(np.random.rand() * 10 + 30, 1),
            'overStock': round(np.random.rand() * 5 + 10, 1),
        },
        'evolutionInPositionStatus': [{
            'item': f"Item {i + 1}",
            'statuses': [np.random.choice(['STOCK-OUT', 'BELOW-SAFETY-STOCK', 'AT-STOCK', 'OVER-STOCK']) for _ in range(12)],
        } for i in range(10)],
        'mostInventoryIssues': [
            {'name': 'Armanda ALW 400', 'positions': np.random.randint(10, 100), 'status': 'Out-of-Stock'},
            {'name': 'Kantouza - CEB100', 'positions': np.random.randint(10, 100), 'status': 'Below-Safety'},
            {'name': 'eViteza 500', 'positions': np.random.randint(10, 100), 'status': 'At-Stock'},
            {'name': 'FlyFighter 120', 'positions': np.random.randint(10, 100), 'status': 'Over-Stock'},
            {'name': 'Armanda BMV 560E', 'positions': np.random.randint(10, 100), 'status': 'Out-of-Stock'},
        ],
    }

    # Stock Coverage Data
    stock_coverage_data = {
        'abcXyzClassification': [
            {
                'consumption': 'HIGH Consumption', 'stability': 'STABLE Demand', 'class': 'AX',
                'totalOutflowValue': np.random.randint(200000, 500000), 'numItems': np.random.randint(1, 5),
                'recommended': 'Automated replenishment', 'buffer': 'LOW buffer - JIT or consignment transfers the responsibility for security.', 'control': 'Perpetual inventory',
                'details': [{'name': 'Kantouza - CEB100', 'value': np.random.randint(10000, 100000)}, {'name': 'FlyFighter 120', 'value': np.random.randint(10000, 100000)}]
            },
            {
                'consumption': 'HIGH Consumption', 'stability': 'VOLATILE Demand', 'class': 'AY',
                'totalOutflowValue': np.random.randint(200000, 500000), 'numItems': np.random.randint(1, 5),
                'recommended': 'Automated with manual intervention', 'buffer': 'LOW buffer accept stock out risk', 'control': 'Perpetual inventory',
                'details': [{'name': 'Armanda BMV 560E', 'value': np.random.randint(10000, 100000)}, {'name': 'TRICA EC200', 'value': np.random.randint(10000, 100000)}]
            },
            {
                'consumption': 'MEDIUM Consumption', 'stability': 'STABLE Demand', 'class': 'BX',
                'totalOutflowValue': np.random.randint(50000, 200000), 'numItems': np.random.randint(1, 5),
                'recommended': 'Automated replenishment', 'buffer': 'LOW buffer - safety first', 'control': 'Periodic count: MEDIUM security',
                'details': [{'name': 'Pale 500', 'value': np.random.randint(5000, 50000)}]
            },
        ]
    }

    # Item Deep-dive Data
    item_deep_dive_data = {
        'selectedItem': 'Armanda BMV 560E',
        'itemFamily': 'Road & Gravel Bikes',
        'stockStatus': {
            'onHandQty': np.random.randint(200, 300),
            'inventoryValue': np.random.randint(500000, 1000000),
            'excessStock': np.random.randint(0, 100000),
            'missingStock': np.random.randint(50000, 500000),
        },
        'warehouseBreakdown': [
            {'wh': 'WH Chicago', 'onHand': np.random.randint(10, 50), 'value': np.random.randint(10000, 50000), 'excess': np.random.randint(0, 5000), 'missing': np.random.randint(0, 10000)},
            {'wh': 'WH Seattle', 'onHand': np.random.randint(10, 50), 'value': np.random.randint(10000, 50000), 'excess': np.random.randint(0, 5000), 'missing': np.random.randint(0, 10000)},
            {'wh': 'WH New Delhi', 'onHand': np.random.randint(10, 50), 'value': np.random.randint(10000, 50000), 'excess': np.random.randint(0, 5000), 'missing': np.random.randint(0, 10000)},
        ],
        'dailyForecast': [{
            'day': i + 1,
            'expectedOnHand': np.random.randint(50, 200),
            'inflow': np.random.randint(0, 20),
            'outflow': np.random.randint(0, 20),
        } for i in range(30)],
    }

    # Adhoc Analysis Data
    adhoc_analysis_data = {
        'inventoryValueTrends': [{
            'month': f"{months[(today - datetime.timedelta(days=30*i)).month - 1]} {((today - datetime.timedelta(days=30*i)).year % 100)}",
            'value': np.random.randint(20, 28) * 1000000,
        } for i in range(24)],
        'inventoryValueByItemFamily': [
            {'name': 'Road & Gravel Bikes', 'value': np.random.randint(500000, 1500000), 'share': round(np.random.rand() * 10 + 20, 1)},
            {'name': 'Electric Bikes', 'value': np.random.randint(300000, 1000000), 'share': round(np.random.rand() * 10 + 10, 1)},
            {'name': 'Urban Bikes', 'value': np.random.randint(200000, 800000), 'share': round(np.random.rand() * 10 + 5, 1)},
            {'name': 'Mountain Bikes', 'value': np.random.randint(150000, 700000), 'share': round(np.random.rand() * 5 + 5, 1)},
            {'name': 'Folding Bikes', 'value': np.random.randint(100000, 500000), 'share': round(np.random.rand() * 5 + 3, 1)},
        ],
        'paretoAnalysis': [
            {'name': 'Road & Gravel Bikes', 'value': np.random.randint(500000, 1500000)},
            {'name': 'Electric Bikes', 'value': np.random.randint(300000, 1000000)},
            {'name': 'Urban Bikes', 'value': np.random.randint(200000, 800000)},
            {'name': 'Mountain Bikes', 'value': np.random.randint(150000, 700000)},
            {'name': 'Folding Bikes', 'value': np.random.randint(100000, 500000)},
            {'name': 'Hybrid Bikes', 'value': np.random.randint(50000, 300000)},
            {'name': 'Kids Bikes', 'value': np.random.randint(20000, 200000)},
        ],
    }
    adhoc_analysis_data['inventoryValueTrends'].reverse()

    return {
        'kpis': {
            'inventoryValue': current_inventory_value,
            'missingStockAmount': missing_stock_amount,
            'excessStockValue': excess_stock_value,
        },
        'inventoryStatus': {
            'totalItems': total_items,
            'totalPositions': total_positions,
            'breakdown': inventory_status_data, # This is now a list of dicts
        },
        'executiveSummary': {
            'inventoryEvolution': inventory_evolution_data,
            'warehouseSummary': warehouse_summary_data,
            'itemEvolution': item_evolution_data,
        },
        'warehouses': warehouse_chart_data,
        'availability': availability_data,
        'excessStock': excess_stock_data,
        'missingStock': missing_stock_data,
        'historicalStatus': historical_status_data,
        'stockCoverage': stock_coverage_data,
        'itemDeepDive': item_deep_dive_data,
        'adhocAnalysis': adhoc_analysis_data,
        'isLoadedFromCSV': False,
    }

# --- CSV Data Processing ---

def process_csv_data(df):
    """Processes pandas DataFrame from CSV to dashboard data structure."""
    if df.empty:
        # If CSV is empty, return an empty dataset that signals no data is loaded
        return None

    # --- Rename and Prepare Columns ---
    # Map CSV columns to expected dashboard column names
    column_mapping = {
        'Stock levels': 'On-hand Quantity',
        'Location': 'Warehouse',
        'SKU': 'Item',
        'Product type': 'Item Family',
        'Price': 'Price', # Keep 'Price' as it's needed for calculation
    }

    # Rename columns that exist in the mapping
    df = df.rename(columns=column_mapping)

    # Ensure critical numerical columns are numeric, handling errors
    for col in ['Price', 'On-hand Quantity']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        else:
            st.warning(f"Required column '{col}' not found in CSV. Some calculations might be affected.")
            df[col] = 0 # Default to 0 if column is missing

    # Add a dummy 'Date' column if not present. For time series, a single date per row isn't ideal but necessary for now.
    # In a real scenario, 'Date' would likely be part of the historical inventory data.
    if 'Date' not in df.columns:
        # Create a Series of today's date, converted to datetime objects for consistency
        df['Date'] = pd.to_datetime([datetime.date.today()] * len(df))
    else:
        # Ensure the existing 'Date' column is converted to datetime
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df.dropna(subset=['Date'], inplace=True) # Drop rows where Date parsing failed

    # Calculate Inventory Value
    df['Inventory Value'] = df['Price'] * df['On-hand Quantity']

    # Derive Safety Stock (as a simple heuristic, e.g., 20% of on-hand quantity)
    # This is a placeholder; a real Safety Stock would come from business rules or demand forecasting.
    df['Safety Stock'] = df['On-hand Quantity'] * 0.2
    df['Safety Stock'] = df['Safety Stock'].apply(lambda x: max(0, x)) # Ensure non-negative

    # Derive Missing Stock Amount
    df['Missing Stock Amount'] = np.where(
        df['On-hand Quantity'] < df['Safety Stock'],
        (df['Safety Stock'] - df['On-hand Quantity']) * df['Price'],
        0
    )

    # Derive Excess Stock Value
    # Arbitrary threshold: if On-hand is more than 150% of Safety Stock, consider it excess.
    # This is a placeholder; a real Excess Stock definition is business-specific.
    df['Excess Stock Value'] = np.where(
        df['On-hand Quantity'] > df['Safety Stock'] * 1.5,
        (df['On-hand Quantity'] - df['Safety Stock'] * 1.5) * df['Price'],
        0
    )


    # --- KPIs ---
    total_inventory_value = df['Inventory Value'].sum()
    total_missing_stock_amount = df['Missing Stock Amount'].sum()
    total_excess_stock_value = df['Excess Stock Value'].sum()
    total_items_count = len(df)
    total_positions_count = len(df) # Assuming each row is a position

    # --- Inventory Status Breakdown ---
    df['Calculated Stock Status'] = 'UNKNOWN'
    if 'Stock Status' in df.columns:
        # Use existing 'Stock Status' if provided in CSV
        df['Calculated Stock Status'] = df['Stock Status'].astype(str).str.upper().str.replace(' ', '-')
    else:
        # Derive if 'Stock Status' is not in CSV
        df.loc[df['On-hand Quantity'] <= 0, 'Calculated Stock Status'] = 'STOCK-OUT'
        df.loc[(df['On-hand Quantity'] > 0) & (df['On-hand Quantity'] < df['Safety Stock']), 'Calculated Stock Status'] = 'BELOW-SAFETY-STOCK'
        df.loc[df['Excess Stock Value'] > 0, 'Calculated Stock Status'] = 'OVER-STOCK'
        # Any items not falling into the above categories are 'AT-STOCK'
        df.loc[df['Calculated Stock Status'] == 'UNKNOWN', 'Calculated Stock Status'] = 'AT-STOCK'


    inventory_status_breakdown = df['Calculated Stock Status'].value_counts().reset_index()
    inventory_status_breakdown.columns = ['name', 'value']
    color_map = {
        'STOCK-OUT': '#DC2626',
        'BELOW-SAFETY-STOCK': '#F59E0B',
        'AT-STOCK': '#10B981',
        'OVER-STOCK': '#6366F1',
        'UNKNOWN': '#CCCCCC'
    }
    inventory_status_breakdown['color'] = inventory_status_breakdown['name'].map(color_map)

    # --- Executive Summary ---
    executive_summary_data = {
        'inventoryEvolution': [],
        'warehouseSummary': [],
        'itemEvolution': [],
    }

    # Group by month for inventory evolution
    if not df.empty:
        df['MonthYear'] = df['Date'].dt.to_period('M')
        monthly_inventory = df.groupby('MonthYear')['Inventory Value'].sum().reset_index()
        monthly_inventory['month'] = monthly_inventory['MonthYear'].dt.strftime('%b %y')
        executive_summary_data['inventoryEvolution'] = monthly_inventory[['month', 'Inventory Value']].rename(columns={'Inventory Value': 'value'}).to_dict('records')

        monthly_items = df.groupby('MonthYear').size().reset_index(name='items')
        monthly_items['month'] = monthly_items['MonthYear'].dt.strftime('%b %y')
        executive_summary_data['itemEvolution'] = monthly_items[['month', 'items']].to_dict('records')


    # Warehouse Summary
    warehouse_grouped = df.groupby('Warehouse').agg(
        inventoryValue=('Inventory Value', 'sum'),
        excessStock=('Excess Stock Value', 'sum'),
        missingStock=('Missing Stock Amount', 'sum'),
        positions=('Item', 'count') # Count items as positions for simplification
    ).reset_index()
    executive_summary_data['warehouseSummary'] = warehouse_grouped.rename(columns={'Warehouse': 'name'}).to_dict('records')

    # --- Warehouses Data ---
    warehouses_data = []
    for index, row in warehouse_grouped.iterrows():
        # Corrected: Access 'Warehouse' column directly as it's the actual column name in warehouse_grouped DataFrame
        wh_df = df[df['Warehouse'] == row['Warehouse']]
        stock_breakdown_wh = wh_df['Calculated Stock Status'].value_counts().reset_index()
        stock_breakdown_wh.columns = ['name', 'value']
        stock_breakdown_wh['color'] = stock_breakdown_wh['name'].map(color_map)
        warehouses_data.append({
            'name': row['Warehouse'], # Corrected: Use 'Warehouse' column from row Series
            'inventoryValue': row['inventoryValue'],
            'excessStock': row['excessStock'],
            'missingStock': row['missingStock'],
            'positions': row['positions'],
            'stockBreakdown': stock_breakdown_wh.to_dict('records')
        })

    # --- Availability Data ---
    availability_data_processed = {
        'missingStockAmount': total_missing_stock_amount,
        'excessStockValue': total_excess_stock_value,
        'inventoryValue': total_inventory_value,
        'stockOutForecast': [], # Hard to derive accurately from a static CSV, will use dummy values
        'itemsToStockOutSoon': [], # Hard to derive, will use dummy values
        'currentInventoryByItem': [],
        'theoreticalOnHandQuantity': [] # Hard to derive, will use dummy values
    }

    item_on_hand = df.groupby('Item').agg(
        onHand=('On-hand Quantity', 'first'), # Assuming first value is representative
        status=('Calculated Stock Status', lambda x: x.mode()[0] if not x.empty else 'UNKNOWN') # Most frequent status
    ).reset_index().rename(columns={'Item': 'name'})
    availability_data_processed['currentInventoryByItem'] = item_on_hand.to_dict('records')

    # Dummy values for forecast as they need complex time-series analysis not in static CSV
    today = datetime.date.today()
    availability_data_processed['stockOutForecast'] = [
        {'range': 'within 3 days', 'items': np.random.randint(1, 5)},
        {'range': '4 to 10 days', 'items': np.random.randint(1, 5)},
        {'range': '11 to 20 days', 'items': np.random.randint(1, 5)},
        {'range': '21 to 30 days', 'items': np.random.randint(1, 5)},
    ]
    availability_data_processed['itemsToStockOutSoon'] = [
        {'name': 'Item A', 'days': np.random.randint(1, 30), 'forecast': 'STOCK-OUT'},
        {'name': 'Item B', 'days': np.random.randint(1, 30), 'forecast': 'BELOW-SAFETY-STOCK'},
    ]
    availability_data_processed['theoreticalOnHandQuantity'] = [{
        'date': (today + datetime.timedelta(days=i)).strftime('%b %d'),
        'value': np.random.randint(100, 300)
    } for i in range(20)],


    # --- Excess Stock Data ---
    excess_stock_data_processed = {
        'percentOverStock': (df[df['Calculated Stock Status'] == 'OVER-STOCK'].shape[0] / total_items_count * 100) if total_items_count > 0 else 0,
        'excessStockValue': total_excess_stock_value,
        'shareOfExcessStockValue': (total_excess_stock_value / total_inventory_value * 100) if total_inventory_value > 0 else 0,
        'excessStockEvolution': [],
        'highestExcessItems': [],
    }

    if not df.empty:
        monthly_excess = df.groupby('MonthYear').agg(
            inventoryValue=('Inventory Value', 'sum'),
            excessValue=('Excess Stock Value', 'sum')
        ).reset_index()
        monthly_excess['excessShare'] = (monthly_excess['excessValue'] / monthly_excess['inventoryValue'] * 100).fillna(0)
        monthly_excess['month'] = monthly_excess['MonthYear'].dt.strftime('%b %y')
        excess_stock_data_processed['excessStockEvolution'] = monthly_excess[['month', 'inventoryValue', 'excessValue', 'excessShare']].to_dict('records')

        highest_excess_items = df.groupby('Item')['Excess Stock Value'].sum().sort_values(ascending=False).reset_index()
        highest_excess_items.columns = ['name', 'excessValue']
        total_excess_sum = highest_excess_items['excessValue'].sum()
        highest_excess_items['share'] = (highest_excess_items['excessValue'] / total_excess_sum * 100).fillna(0) if total_excess_sum > 0 else 0
        excess_stock_data_processed['highestExcessItems'] = highest_excess_items.head(6).to_dict('records')


    # --- Missing Stock Data ---
    missing_stock_data_processed = {
        'percentBelowSafetyStock': (df[df['Calculated Stock Status'] == 'BELOW-SAFETY-STOCK'].shape[0] / total_items_count * 100) if total_items_count > 0 else 0,
        'percentOutOfStock': (df[df['Calculated Stock Status'] == 'STOCK-OUT'].shape[0] / total_items_count * 100) if total_items_count > 0 else 0,
        'amountToRefill': total_missing_stock_amount,
        'evolutionOfMissingStockItems': [],
        'evolutionOfMissingStockAmount': [],
        'mostImportantMissingItems': [],
    }
    if not df.empty:
        monthly_missing_items = df[df['Calculated Stock Status'].isin(['STOCK-OUT', 'BELOW-SAFETY-STOCK'])].groupby('MonthYear').size().reset_index(name='items')
        monthly_missing_items['month'] = monthly_missing_items['MonthYear'].dt.strftime('%b')
        missing_stock_data_processed['evolutionOfMissingStockItems'] = monthly_missing_items[['month', 'items']].to_dict('records')

        monthly_missing_amount = df.groupby('MonthYear')['Missing Stock Amount'].sum().reset_index()
        monthly_missing_amount['month'] = monthly_missing_amount['MonthYear'].dt.strftime('%b')
        missing_stock_data_processed['evolutionOfMissingStockAmount'] = monthly_missing_amount[['month', 'Missing Stock Amount']].rename(columns={'Missing Stock Amount': 'amount'}).to_dict('records')

        most_important_missing_items = df.groupby('Item').agg(
            amount=('Missing Stock Amount', 'sum'),
            status=('Calculated Stock Status', lambda x: x.mode()[0] if not x.empty else 'UNKNOWN')
        ).sort_values(by='amount', ascending=False).reset_index().rename(columns={'Item': 'name'})
        missing_stock_data_processed['mostImportantMissingItems'] = most_important_missing_items[most_important_missing_items['amount'] > 0].head(5).to_dict('records')


    # --- Historical Status Data ---
    historical_status_data_processed = {
        'stockStatusOverview': {
            'stockOut': missing_stock_data_processed['percentOutOfStock'],
            'belowSafetyStock': missing_stock_data_processed['percentBelowSafetyStock'],
            'atStock': (df[df['Calculated Stock Status'] == 'AT-STOCK'].shape[0] / total_items_count * 100) if total_items_count > 0 else 0,
            'overStock': excess_stock_data_processed['percentOverStock'],
        },
        'evolutionInPositionStatus': [],
        'mostInventoryIssues': [],
    }

    if not df.empty:
        # Simplified evolution in position status for display
        evolution_status_list = []
        for item, group in df.groupby('Item'):
            statuses_over_time = group.sort_values('Date')['Calculated Stock Status'].tolist()
            evolution_status_list.append({'item': item, 'statuses': statuses_over_time})
        historical_status_data_processed['evolutionInPositionStatus'] = evolution_status_list

        # Most inventory issues
        issue_items = df[df['Calculated Stock Status'].isin(['STOCK-OUT', 'BELOW-SAFETY-STOCK'])].groupby('Item').agg(
            positions=('Item', 'count'),
            status=('Calculated Stock Status', lambda x: x.mode()[0] if not x.empty else 'UNKNOWN')
        ).sort_values(by='positions', ascending=False).reset_index().rename(columns={'Item': 'name'})
        historical_status_data_processed['mostInventoryIssues'] = issue_items.head(5).to_dict('records')


    # --- Stock Coverage Data ---
    # This is highly conceptual and relies on very specific CSV columns not generally available.
    # We will use dummy data or create a very simple structure.
    stock_coverage_data_processed = {
        'abcXyzClassification': generate_dummy_data()['stockCoverage']['abcXyzClassification'] # Use dummy for now
    }
    # If CSV had 'Consumption Volume', 'Consumption Stability', 'Class', 'Total Outflow Value', 'Num Items'
    # we could process it here.

    # --- Item Deep-dive Data (select first item from processed data for simplicity) ---
    item_deep_dive_data_processed = {}
    if not df.empty:
        first_item_row = df.iloc[0]
        item_deep_dive_data_processed = {
            'selectedItem': first_item_row.get('Item', 'N/A'),
            'itemFamily': first_item_row.get('Item Family', 'N/A'),
            'stockStatus': {
                'onHandQty': first_item_row.get('On-hand Quantity', 0),
                'inventoryValue': first_item_row.get('Inventory Value', 0),
                'excessStock': first_item_row.get('Excess Stock Value', 0),
                'missingStock': first_item_row.get('Missing Stock Amount', 0),
            },
            'warehouseBreakdown': warehouses_data, # Use the processed warehouse data
            'dailyForecast': availability_data_processed['theoreticalOnHandQuantity'], # Use theoretical on hand as forecast
        }
    else:
        item_deep_dive_data_processed = generate_dummy_data()['itemDeepDive']


    # --- Adhoc Analysis Data ---
    adhoc_analysis_data_processed = {
        'inventoryValueTrends': executive_summary_data['inventoryEvolution'], # Re-use
        'inventoryValueByItemFamily': [],
        'paretoAnalysis': [],
    }

    if not df.empty:
        # Inventory Value by Item Family
        item_family_value = df.groupby('Item Family')['Inventory Value'].sum().reset_index()
        item_family_value.columns = ['name', 'value']
        total_inv_value = item_family_value['value'].sum()
        item_family_value['share'] = (item_family_value['value'] / total_inv_value * 100).fillna(0) if total_inv_value > 0 else 0
        adhoc_analysis_data_processed['inventoryValueByItemFamily'] = item_family_value.to_dict('records')

        # Pareto Analysis
        pareto_items = df.groupby('Item')['Inventory Value'].sum().sort_values(ascending=False).reset_index()
        pareto_items.columns = ['name', 'value']
        adhoc_analysis_data_processed['paretoAnalysis'] = pareto_items.head(7).to_dict('records') # Top 7 items


    return {
        'kpis': {
            'inventoryValue': total_inventory_value,
            'missingStockAmount': total_missing_stock_amount,
            'excessStockValue': total_excess_stock_value,
        },
        'inventoryStatus': {
            'totalItems': total_items_count,
            'totalPositions': total_positions_count,
            'breakdown': inventory_status_breakdown.to_dict('records'), # This is already a list of dicts from .to_dict('records')
        },
        'executiveSummary': executive_summary_data,
        'warehouses': warehouses_data,
        'availability': availability_data_processed,
        'excessStock': excess_stock_data_processed,
        'missingStock': missing_stock_data_processed,
        'historicalStatus': historical_status_data_processed,
        'stockCoverage': stock_coverage_data_processed,
        'itemDeepDive': item_deep_dive_data_processed,
        'adhocAnalysis': adhoc_analysis_data_processed,
        'isLoadedFromCSV': True,
    }


# --- Streamlit UI Components ---

def HomeContent(data):
    st.title("Inventory")
    st.write("Salesforce")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Inventory Value as of November 8, 2022", value=format_currency(data['kpis']['inventoryValue']))
    with col2:
        st.metric(label="Missing Stock Amount", value=format_currency(data['kpis']['missingStockAmount']), delta_color="inverse")
    with col3:
        st.metric(label="Excess Stock Value", value=format_currency(data['kpis']['excessStockValue']), delta_color="off")

    st.subheader("Inventory Status as of November 8, 2022")
    col_items, col_chart = st.columns([1, 3])
    with col_items:
        st.markdown(f"<h1 style='text-align: center; color: #3b82f6;'>{data['inventoryStatus']['totalItems']}</h1><p style='text-align: center;'>Items</p>", unsafe_allow_html=True)
    with col_chart:
        # Ensure data['inventoryStatus']['breakdown'] is a list of dicts here
        fig = px.bar(data['inventoryStatus']['breakdown'], y='name', x='value', orientation='h',
                     color='name', color_discrete_map={item['name']: item['color'] for item in data['inventoryStatus']['breakdown']},
                     height=150, title="", labels={'value': '', 'name': ''})
        fig.update_layout(showlegend=False, margin=dict(l=0, r=0, t=0, b=0),
                          xaxis_visible=False, yaxis_ticksuffix=" ") # Adjust yaxis ticksuffux to push labels to the right
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    st.markdown(f"<p style='text-align: center; margin-top: -30px;'><h1 style='text-align: center; color: #10B981;'>{data['inventoryStatus']['totalPositions']}</h1>Positions</p>", unsafe_allow_html=True)

    st.subheader("What you want to:")
    actions = [
        ("Assess", "M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.003 12.003 0 002 12c0 2.514.905 4.882 2.457 6.77A11.952 11.952 0 0012 21c2.514 0 4.882-.905 6.77-2.457A11.952 11.952 0 0022 12c0-2.514-.905-4.882-2.457-6.77z"),
        ("Evaluate", "M9 19V6l12-3v13M9 19c-1.38 0-2.5-.68-2.5-1.5s1.12-1.5 2.5-1.5 2.5.68 2.5 1.5-1.12 1.5-2.5 1.5zm0 0v-6m0 6l-8-8"),
        ("Reduce Risks", "M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"),
        ("Optimize", "M11 4a2 2 0 10-4 0v1a1 1 0 001 1h3a1 1 0 001-1V4zm0 16a2 2 0 10-4 0v1a1 1 0 001 1h3a1 1 0 001-1v-1zm-1-8a2 2 0 10-4 0v1a1 1 0 001 1h3a1 1 0 001-1v-1zM11 8a2 2 0 10-4 0v1a1 1 0 001 1h3a1 1 0 001-1V8zm-1 4a2 2 0 10-4 0v1a1 1 0 001 1h3a1 1 0 001-1v-1z"),
        ("Assess Improvements", "M14 10h4.764a2 2 0 011.789 2.894l-3.5 7A2 2 0 0115.263 21H6.5a2 2 0 01-2-2v-6a2 2 0 012-2h2l2.5-3.5a2 2 0 013.098 0z"),
        ("Deep-dive", "M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z")
    ]
    cols = st.columns(len(actions))
    for i, (text, svg_path) in enumerate(actions):
        with cols[i]:
            # Removed HTML from button label, keeping only the text.
            # Custom styling for buttons in Streamlit typically requires custom components or careful CSS injection.
            st.button(text, key=f"action_btn_{text}", use_container_width=True, help=f"Click to {text}")


def ExecutiveSummaryContent(data):
    st.header("Executive Summary")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Inventory Status by Warehouse")
        for wh in data['executiveSummary']['warehouseSummary']:
            st.markdown(f"**{wh['name']}**")
            # Ensure positions is not zero before division
            if wh['positions'] > 0:
                st.progress(wh['positions'] / 50, text=f"{wh['positions']} positions") # Assuming max 50 for progress bar
            else:
                st.progress(0, text="0 positions")
    with col2:
        st.subheader("Evolution of our inventory Items")
        df_item_evolution = pd.DataFrame(data['executiveSummary']['itemEvolution'])
        if not df_item_evolution.empty:
            fig = px.line(df_item_evolution, x='month', y='items', labels={'items': 'Number of Items'})
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No item evolution data available.")

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Are we efficiently mobilizing our capital in our inventory?")
        st.markdown(f"<h1 style='font-size: 3rem; font-weight: bold;'>{format_currency(data['kpis']['inventoryValue'])}</h1>", unsafe_allow_html=True)
        st.write(f"Total Inventory Value (Excess Stock {format_currency(data['kpis']['excessStockValue'])})")
        st.markdown(f"<h1 style='font-size: 3rem; font-weight: bold; color: #ef4444;'>{format_currency(data['kpis']['missingStockAmount'])}</h1>", unsafe_allow_html=True)
        st.write("to refill Missing Stock")
    with col2:
        st.subheader("How is the total value of our inventory evolving?")
        df_inv_evolution = pd.DataFrame(data['executiveSummary']['inventoryEvolution'])
        if not df_inv_evolution.empty:
            fig = px.bar(df_inv_evolution, x='month', y='value', labels={'value': 'Inventory Value'},
                         color_discrete_sequence=['#82ca9d'])
            fig.update_layout(yaxis_tickprefix="$", yaxis_tickformat=".1fM")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No inventory evolution data available.")


def WarehousesContent(data):
    st.header("Inventory by Warehouse")

    for wh in data['warehouses']:
        st.markdown("---")
        st.subheader(wh['name'])
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"**{wh['positions']}** Positions")
        with col2:
            st.markdown("**Inventory Positions Breakdown**")
            df_breakdown = pd.DataFrame(wh['stockBreakdown'])
            if not df_breakdown.empty:
                fig = px.bar(df_breakdown, y='name', x='value', orientation='h',
                             color='name', color_discrete_map={item['name']: item['color'] for item in wh['stockBreakdown']},
                             height=150, labels={'value': '', 'name': ''})
                fig.update_layout(showlegend=False, margin=dict(l=0, r=0, t=0, b=0), xaxis_visible=False, yaxis_ticksuffix=" ")
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            else:
                st.info("No stock breakdown data.")
        with col3:
            st.markdown(f"**Inventory Value:** {format_currency(wh['inventoryValue'])}")
            st.markdown(f"**Excess Stock:** {format_currency(wh['excessStock'])}")
        with col4:
            st.markdown(f"**Missing Stock Amount:** {format_currency(wh['missingStock'])}")


def AvailabilityContent(data):
    st.header("Item Availability")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Missing Stock Amount", value=format_currency(data['availability']['missingStockAmount']), delta_color="inverse")
    with col2:
        st.metric(label="Excess Stock Value", value=format_currency(data['availability']['excessStockValue']), delta_color="off")
    with col3:
        st.metric(label="Inventory Value", value=format_currency(data['availability']['inventoryValue']))

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Forecast: Next Stock-out Items")
        for forecast in data['availability']['stockOutForecast']:
            st.write(f"{forecast['range']} ({forecast['items']} items)")
            # Ensure items is not zero for division, also handle the case where forecast['items'] might be 0
            if forecast['items'] > 0:
                st.progress(forecast['items'] / 10) # Max 10 items for progress bar
            else:
                st.progress(0)
    with col2:
        st.subheader("Forecast: Items to Stock-out Soon")
        df_stock_out_soon = pd.DataFrame(data['availability']['itemsToStockOutSoon'])
        if not df_stock_out_soon.empty:
            st.dataframe(df_stock_out_soon, use_container_width=True, hide_index=True)
        else:
            st.info("No items expected to stock out soon.")

    st.markdown("---")

    st.subheader("Current Inventory by Item")
    df_current_inventory = pd.DataFrame(data['availability']['currentInventoryByItem'])
    if not df_current_inventory.empty:
        st.dataframe(df_current_inventory, use_container_width=True, hide_index=True)
    else:
        st.info("No current inventory data available.")

    st.subheader("Theoretical On Hand Quantity (Next 20 days)")
    df_theoretical_on_hand = pd.DataFrame(data['availability']['theoreticalOnHandQuantity'])
    if not df_theoretical_on_hand.empty:
        fig = px.line(df_theoretical_on_hand, x='date', y='value', labels={'value': 'Quantity'})
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No theoretical on-hand quantity data available.")


def ExcessStockContent(data):
    st.header("Excess Stock")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Percentage of Over-Stock Items", value=f"{data['excessStock']['percentOverStock']:.1f}%")
    with col2:
        st.metric(label="Excess Stock Value", value=format_currency(data['excessStock']['excessStockValue']))
    with col3:
        st.metric(label="Share of Excess-Stock Value", value=f"{data['excessStock']['shareOfExcessStockValue']:.1f}%")

    st.markdown("---")

    st.subheader("How has our Excess-stock value evolved?")
    df_excess_evolution = pd.DataFrame(data['excessStock']['excessStockEvolution'])
    if not df_excess_evolution.empty:
        fig = px.line(df_excess_evolution, x='month', y=['excessValue', 'excessShare'],
                      labels={'excessValue': 'Excess Value ($)', 'excessShare': 'Excess Share (%)'},
                      height=300)
        fig.update_traces(yaxis='y1', selector=dict(name='excessValue'))
        fig.update_traces(yaxis='y2', selector=dict(name='excessShare'))
        fig.update_layout(yaxis=dict(title='Excess Value ($)', side='left'),
                          yaxis2=dict(title='Excess Share (%)', overlaying='y', side='right'))
        fig.update_layout(hovermode="x unified")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No excess stock evolution data available.")


    st.markdown("---")

    st.subheader("Which Items have the highest Excess-stock value?")
    df_highest_excess = pd.DataFrame(data['excessStock']['highestExcessItems'])
    if not df_highest_excess.empty:
        st.dataframe(df_highest_excess.assign(
            excessValue=df_highest_excess['excessValue'].apply(format_currency_k),
            share=df_highest_excess['share'].apply(lambda x: f"{x:.1f}%")
        ), use_container_width=True, hide_index=True)
    else:
        st.info("No highest excess items data available.")


def MissingStockContent(data):
    st.header("Missing Stock")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Share of Missing Stock Items")
        st.markdown(f"<h1 style='font-size: 3rem; font-weight: bold; color: #ef4444;'>{data['missingStock']['percentBelowSafetyStock']:.1f}%</h1>", unsafe_allow_html=True)
        st.write("of items are Below Safety Stock")
        st.markdown(f"<h1 style='font-size: 2rem; font-weight: bold; color: #ef4444;'>{data['missingStock']['percentOutOfStock']:.1f}%</h1>", unsafe_allow_html=True)
        st.write("of items are Out-of-Stock")
    with col2:
        st.subheader("Amount Needed to Refill Positions")
        st.markdown(f"<h1 style='font-size: 3rem; font-weight: bold; color: #fbbf24;'>{format_currency(data['missingStock']['amountToRefill'])}</h1>", unsafe_allow_html=True)
        st.write("Missing Stock Amount")

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Evolution of Missing Stock Items (Count)")
        df_missing_items_evolution = pd.DataFrame(data['missingStock']['evolutionOfMissingStockItems'])
        if not df_missing_items_evolution.empty:
            fig = px.line(df_missing_items_evolution, x='month', y='items', labels={'items': 'Number of Missing Items'},
                          color_discrete_sequence=['#FF7043'])
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No missing items evolution data available.")
    with col2:
        st.subheader("Evolution of Missing Stock Amount")
        df_missing_amount_evolution = pd.DataFrame(data['missingStock']['evolutionOfMissingStockAmount'])
        if not df_missing_amount_evolution.empty:
            fig = px.line(df_missing_amount_evolution, x='month', y='amount', labels={'amount': 'Missing Stock Amount'},
                          color_discrete_sequence=['#FFB300'])
            fig.update_layout(yaxis_tickprefix="$", yaxis_tickformat=".1fM")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No missing stock amount evolution data available.")

    st.markdown("---")

    st.subheader("Which Items Represent the Most Important Inventory to Refill?")
    df_most_important_missing = pd.DataFrame(data['missingStock']['mostImportantMissingItems'])
    if not df_most_important_missing.empty:
        st.dataframe(df_most_important_missing.assign(
            amount=df_most_important_missing['amount'].apply(format_currency_k)
        ), use_container_width=True, hide_index=True)
    else:
        st.info("No most important missing items data available.")


def HistoricalStatusContent(data):
    st.header("Inventory Historical Status")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("What was the Items' status in our inventory over the selected period?")
        status_overview = data['historicalStatus']['stockStatusOverview']
        st.info(f"**Out-of-Stock:** {status_overview['stockOut']}%")
        st.warning(f"**Below Safety Stock:** {status_overview['belowSafetyStock']}%")
        st.success(f"**At Stock:** {status_overview['atStock']}%")
        st.info(f"**Over Stock:** {status_overview['overStock']}%")
    with col2:
        st.subheader("Which Items have had the most inventory issues?")
        df_most_issues = pd.DataFrame(data['historicalStatus']['mostInventoryIssues'])
        if not df_most_issues.empty:
            st.dataframe(df_most_issues, use_container_width=True, hide_index=True)
        else:
            st.info("No items with historical issues.")

    st.markdown("---")

    st.subheader("Evolution in Position Status (Simulated)")
    for item_data in data['historicalStatus']['evolutionInPositionStatus']:
        st.write(f"**{item_data['item']}**")
        status_html = ""
        for status in item_data['statuses']:
            color_class = {
                'STOCK-OUT': 'bg-red-500',
                'BELOW-SAFETY-STOCK': 'bg-yellow-500',
                'AT-STOCK': 'bg-green-500',
                'OVER-STOCK': 'bg-blue-500',
                'UNKNOWN': 'bg-gray-300'
            }.get(status, 'bg-gray-300')
            status_html += f"<span class='status-square {color_class}' title='{status}'></span>"
        st.markdown(f"<div style='display: flex; flex-wrap: wrap; gap: 4px;'>{status_html}</div>", unsafe_allow_html=True)


def StockCoverageContent(data):
    st.header("Stock Coverage Analysis")
    st.write("The ABC-XYZ analysis is an algorithm to classify your products by volume (ABC - high, medium, low consumption) and predictability (XYZ - stable, volatile, high volatile consumption).")
    st.write("Each combination (AX, BX, CY) implies a suggested way to manage inventory (replenishment, buffer stock, inventory control).")

    st.subheader("ABC-XYZ Classification: How to optimize and reduce my inventory coverage?")
    df_abc_xyz = pd.DataFrame(data['stockCoverage']['abcXyzClassification'])
    if not df_abc_xyz.empty:
        # Flatten details for display if necessary, or simplify
        df_abc_xyz['Detail by Product'] = df_abc_xyz['details'].apply(lambda x: ", ".join([f"{d['name']}: {format_currency_k(d['value'])}" for d in x]))
        st.dataframe(df_abc_xyz[[
            'consumption', 'stability', 'class', 'totalOutflowValue', 'numItems',
            'recommended', 'buffer', 'control', 'Detail by Product'
        ]].assign(
            totalOutflowValue=df_abc_xyz['totalOutflowValue'].apply(format_currency_k)
        ), use_container_width=True, hide_index=True)
    else:
        st.info("No ABC-XYZ classification data available.")


def ItemContent(data):
    st.header("Item Deep-dive")

    st.subheader(f"Inventory as of November 8, 2022 - {data['itemDeepDive']['selectedItem']}")
    st.write(f"Item Family: {data['itemDeepDive']['itemFamily']}")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="On-hand Qty", value=data['itemDeepDive']['stockStatus']['onHandQty'])
    with col2:
        st.metric(label="Inventory Value", value=format_currency_k(data['itemDeepDive']['stockStatus']['inventoryValue']))
    with col3:
        st.metric(label="Excess Stock", value=format_currency_k(data['itemDeepDive']['stockStatus']['excessStock']), delta_color="off")
    with col4:
        st.metric(label="Missing Stock", value=format_currency_k(data['itemDeepDive']['stockStatus']['missingStock']), delta_color="inverse")

    st.markdown("---")

    st.subheader("Stock Status by Warehouse")
    df_warehouse_breakdown = pd.DataFrame(data['itemDeepDive']['warehouseBreakdown'])
    if not df_warehouse_breakdown.empty:
        st.dataframe(df_warehouse_breakdown.assign(
            value=df_warehouse_breakdown['value'].apply(format_currency_k),
            excess=df_warehouse_breakdown['excess'].apply(format_currency_k),
            missing=df_warehouse_breakdown['missing'].apply(format_currency_k)
        ), use_container_width=True, hide_index=True)
    else:
        st.info("No warehouse breakdown data for this item.")

    st.markdown("---")

    st.subheader("Daily Forecast: Expected On-Hand Quantities for the coming 30 days")
    df_daily_forecast = pd.DataFrame(data['itemDeepDive']['dailyForecast'])
    if not df_daily_forecast.empty:
        fig = px.line(df_daily_forecast, x='day', y=['expectedOnHand', 'inflow', 'outflow'],
                      labels={'expectedOnHand': 'Expected On-Hand', 'inflow': 'Inflow', 'outflow': 'Outflow'})
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No daily forecast data available for this item.")


def AdhocContent(data):
    st.header("Adhoc Analysis")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Inventory Value Trends")
        df_inv_trends = pd.DataFrame(data['adhocAnalysis']['inventoryValueTrends'])
        if not df_inv_trends.empty:
            fig = px.bar(df_inv_trends, x='month', y='value', labels={'value': 'Inventory Value'},
                         color_discrete_sequence=['#8884d8'])
            fig.update_layout(yaxis_tickprefix="$", yaxis_tickformat=".1fM")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No inventory value trends data available.")
    with col2:
        st.subheader("Inventory Value by Item Family")
        df_inv_by_family = pd.DataFrame(data['adhocAnalysis']['inventoryValueByItemFamily'])
        if not df_inv_by_family.empty:
            fig = px.bar(df_inv_by_family, x='value', y='name', orientation='h',
                         labels={'value': 'Inventory Value', 'name': 'Item Family'},
                         color_discrete_sequence=['#82ca9d'])
            fig.update_layout(xaxis_tickprefix="$", xaxis_tickformat=".0fK")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No inventory value by item family data available.")

    st.markdown("---")

    st.subheader("Pareto Analysis")
    df_pareto = pd.DataFrame(data['adhocAnalysis']['paretoAnalysis'])
    if not df_pareto.empty:
        fig = px.bar(df_pareto, x='name', y='value', labels={'value': 'Value', 'name': 'Item'},
                     color_discrete_sequence=['#8884d8'])
        fig.update_layout(yaxis_tickprefix="$", yaxis_tickformat=".1fM")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No Pareto analysis data available.")


# --- Main Streamlit Application Logic ---

def main():
    st.set_page_config(layout="wide")

    # --- Sidebar ---
    with st.sidebar:
        st.markdown(
            """
            <div style="display: flex; align-items: center; margin-bottom: 2rem;">
                <svg xmlns="http://www.w3.org/2000/svg" style="height: 32px; width: 32px; color: white; margin-right: 8px;" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 15H9v-2h2v2zm0-4H9v-2h2v2zm0-4H9V7h2v2zm4 8h-2v-2h2v2zm0-4h-2v-2h2v2zm0-4h-2V7h2v2z"/></svg>
                <span style="font-size: 1.5rem; font-weight: bold; color: white;">Salesforce</span>
            </div>
            <div style="text-align: center; margin-bottom: 2rem;">
                <img src="https://placehold.co/80x80/cccccc/333333?text=User" style="border-radius: 50%; width: 80px; height: 80px; border: 2px solid white; margin-bottom: 8px;">
                <p style="font-size: 0.875rem; color: white;">Welcome, User!</p>
            </div>
            """, unsafe_allow_html=True
        )

        st.markdown("<h2 style='font-size: 1.25rem; font-weight: 600; color: #bfdbfe; margin-bottom: 1rem;'>Inventory</h2>", unsafe_allow_html=True)

        uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"], help="Upload your supply chain data CSV to populate the dashboard.")

        # Navigation
        st.markdown("""
            <style>
                .stRadio > label {
                    padding-left: 0.75rem;
                    padding-right: 1rem;
                    padding-top: 0.75rem;
                    padding-bottom: 0.75rem;
                    border-radius: 0.5rem;
                    margin-bottom: 0.5rem;
                    cursor: pointer;
                    transition: all 0.2s ease;
                    font-weight: 500;
                    display: flex;
                    align-items: center;
                }
                .stRadio > label:hover {
                    background-color: rgba(255, 255, 255, 0.2);
                }
                .stRadio [aria-checked="true"] > div {
                    background-color: rgba(255, 255, 255, 0.3) !important;
                }
            </style>
        """, unsafe_allow_html=True)


        current_nav_index = st.session_state.get('nav_index', 0)
        nav_options = ['Home', 'Executive Summary', 'Warehouses', 'Availability', 'Excess Stock', 'Missing Stock', 'Historical Status', 'Stock Coverage', 'Item', 'Adhoc']
        selected_nav = st.radio("Navigation", nav_options, index=current_nav_index, key="main_nav")


    # --- Data Loading and Processing ---
    dashboard_data = None
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            dashboard_data = process_csv_data(df)
            st.session_state['dashboard_data'] = dashboard_data
            st.session_state['nav_index'] = nav_options.index(selected_nav) # Keep current tab after upload
            st.success("CSV loaded successfully! Displaying your data.")
        except Exception as e:
            st.error(f"Error processing CSV: {e}. Please ensure it's a valid CSV with expected columns. Dashboard content cleared.")
            # Clear data from session state on error, forcing user to re-upload
            if 'dashboard_data' in st.session_state:
                del st.session_state['dashboard_data']
            # dashboard_data will remain None, leading to the "Please upload" message below
    elif 'dashboard_data' in st.session_state:
        # If no new file uploaded, but data exists from a previous successful upload
        dashboard_data = st.session_state['dashboard_data']
    else:
        # No file uploaded yet, and no previous data in session state.
        # dashboard_data remains None, which will trigger the "Please upload" message in the main content area.
        pass # Do nothing, let dashboard_data remain None

    # Display status of loaded data (sidebar)
    if dashboard_data is None:
        st.sidebar.markdown("<p style='color: #FFC107; font-weight: bold; margin-top: 1rem;'>⚠️ Please upload a CSV file to view the dashboard.</p>", unsafe_allow_html=True)
    elif dashboard_data.get('isLoadedFromCSV', False):
        st.sidebar.markdown("<p style='color: #4CAF50; font-weight: bold; margin-top: 1rem;'>✅ Displaying your CSV data</p>", unsafe_allow_html=True)
    else: # This case should ideally not happen if logic is strict, but good for robustness
        st.sidebar.markdown("<p style='color: #FFC107; font-weight: bold; margin-top: 1rem;'>⚠️ An issue occurred. Please upload a valid CSV.</p>", unsafe_allow_html=True)


    # --- Main Content Area ---
    if dashboard_data:
        if selected_nav == 'Home':
            HomeContent(dashboard_data)
        elif selected_nav == 'Executive Summary':
            ExecutiveSummaryContent(dashboard_data) # Corrected: passed dashboard_data
        elif selected_nav == 'Warehouses':
            WarehousesContent(dashboard_data)
        elif selected_nav == 'Availability':
            AvailabilityContent(dashboard_data)
        elif selected_nav == 'Excess Stock':
            ExcessStockContent(dashboard_data)
        elif selected_nav == 'Missing Stock':
            MissingStockContent(dashboard_data)
        elif selected_nav == 'Historical Status':
            HistoricalStatusContent(dashboard_data)
        elif selected_nav == 'Stock Coverage':
            StockCoverageContent(dashboard_data)
        elif selected_nav == 'Item':
            ItemContent(dashboard_data)
        elif selected_nav == 'Adhoc':
            AdhocContent(dashboard_data)
    else:
        st.info("Please upload your supply chain data CSV file using the uploader in the sidebar to populate the dashboard.")
        st.info("No data is currently loaded.")
        st.image("https://placehold.co/800x400/eeeeee/000000?text=Upload+CSV+to+see+dashboard", caption="Dashboard awaiting CSV upload")


if __name__ == "__main__":
    main()
