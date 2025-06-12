import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Generate dummy data
def generate_dummy_data():
    current_inventory_value = np.random.randint(20, 30) * 1_000_000  # $20M - $30M
    missing_stock_amount = np.random.randint(1, 7) * 1_000_000        # $1M - $7M
    excess_stock_value = np.random.randint(1, 3) * 1_000_000          # $1M - $3M

    total_items = np.random.randint(50, 100)
    total_positions = np.random.randint(200, 300)

    stock_out = int(total_items * np.random.uniform(0.05, 0.15))
    below_safety_stock = int(total_items * np.random.uniform(0.15, 0.35))
    at_stock = int(total_items * np.random.uniform(0.25, 0.55))
    over_stock = total_items - stock_out - below_safety_stock - at_stock

    inventory_status_data = pd.DataFrame({
        'Status': ['STOCK-OUT', 'BELOW SAFETY STOCK', 'AT-STOCK', 'OVER-STOCK'],
        'Count': [stock_out, below_safety_stock, at_stock, over_stock],
        'Color': ['#DC2626', '#F59E0B', '#10B981', '#6366F1']
    })

    return {
        'kpis': {
            'inventory_value': current_inventory_value,
            'missing_stock_amount': missing_stock_amount,
            'excess_stock_value': excess_stock_value
        },
        'inventory_status': {
            'total_items': total_items,
            'total_positions': total_positions,
            'breakdown': inventory_status_data
        }
    }

# Initialize dashboard data
dashboard_data = generate_dummy_data()

# Streamlit Layout
st.set_page_config(page_title="Inventory Dashboard", layout="wide")

# Sidebar - Navigation
st.sidebar.title("Salesforce Inventory")
st.sidebar.image("https://placehold.co/80x80/cccccc/333333?text=User", width=80)
st.sidebar.write("Welcome, User!")
nav_options = ['Home', 'Executive Summary', 'Warehouses', 'Availability', 'Excess Stock',
               'Missing Stock', 'Historical Status', 'Stock Coverage', 'Item', 'Adhoc']
active_nav = st.sidebar.radio("Navigate", nav_options)

# Main content
st.title("📦 Inventory Dashboard")

# KPI Cards
col1, col2, col3 = st.columns(3)
col1.metric("Inventory Value", f"${dashboard_data['kpis']['inventory_value'] / 1_000_000:.2f}M")
col2.metric("Missing Stock Amount", f"${dashboard_data['kpis']['missing_stock_amount'] / 1_000_000:.2f}M", delta=None)
col3.metric("Excess Stock Value", f"${dashboard_data['kpis']['excess_stock_value'] / 1_000_000:.2f}M")

st.markdown("---")

# Inventory Status Section
st.subheader("Inventory Status as of June 12, 2025")

col_items, col_chart = st.columns([1, 3])
with col_items:
    st.metric("Total Items", dashboard_data['inventory_status']['total_items'])
    st.metric("Total Positions", dashboard_data['inventory_status']['total_positions'])

with col_chart:
    fig = px.bar(
        dashboard_data['inventory_status']['breakdown'],
        x='Count',
        y='Status',
        orientation='h',
        color='Status',
        color_discrete_map={
            'STOCK-OUT': '#DC2626',
            'BELOW SAFETY STOCK': '#F59E0B',
            'AT-STOCK': '#10B981',
            'OVER-STOCK': '#6366F1'
        },
        height=400
    )
    fig.update_layout(showlegend=False, yaxis_title=None, xaxis_title=None)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Action Buttons (Streamlit buttons don't support inline icons but we simulate)
st.subheader("What do you want to do?")

action_cols = st.columns(3)
if action_cols[0].button("Assess 🔍"):
    st.success("Assess clicked!")

if action_cols[1].button("Evaluate 📊"):
    st.success("Evaluate clicked!")

if action_cols[2].button("Reduce Risks ⚠️"):
    st.success("Reduce Risks clicked!")

action_cols2 = st.columns(3)
if action_cols2[0].button("Optimize ⚙️"):
    st.success("Optimize clicked!")

if action_cols2[1].button("Assess Improvements 📈"):
    st.success("Assess Improvements clicked!")

if action_cols2[2].button("Deep-dive 🔬"):
    st.success("Deep-dive clicked!")

st.markdown("---")
st.button("🚀 Start")

