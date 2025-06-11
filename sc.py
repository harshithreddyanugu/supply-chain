# Supply Chain Management Dashboard App (Streamlit)

import streamlit as st
import pandas as pd
import plotly.express as px

# Page setup
st.set_page_config(
    page_title="🚀 Futuristic Supply Chain Dashboard",
    layout="wide",
    page_icon="📦"
)

# File Upload
st.sidebar.title("🧭 Navigation")
uploaded_file = st.sidebar.file_uploader("📤 Upload Supply Chain CSV", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    st.warning("⚠️ Please upload a CSV file to proceed.")
    st.stop()

# Sidebar Navigation
menu = st.sidebar.radio("Go to", [
    "🏠 Home",
    "📊 Executive Summary",
    "🏢 Warehouses",
    "📦 Availability",
    "📈 Excessive Stock",
    "🚫 Missing Stock",
    "📚 Historical Status",
    "📉 Stock Coverage",
    "🧾 Items",
    "🧪 Adhoc"
])

# Sidebar Filters
st.sidebar.markdown("---")
st.sidebar.header("🔍 Filters")
product = st.sidebar.selectbox("Select Product Type", df['Product Type'].unique())
location = st.sidebar.selectbox("Select Location", df['Location'].unique())
supplier = st.sidebar.selectbox("Select Supplier", df['Supplier name'].unique())
show_data = st.sidebar.checkbox("📑 Show Raw Data")

# Filtered Data
filtered_df = df[(df['Product Type'] == product) & (df['Location'] == location) & (df['Supplier name'] == supplier)]

# HOME
if menu == "🏠 Home":
    st.title("🚀 Welcome to the Futuristic SCM Dashboard")
    st.markdown("""
    This dashboard provides real-time insights to enhance your supply chain decisions 🧠📦.
    Use the navigation bar to explore different dimensions.
    """)

# EXECUTIVE SUMMARY
elif menu == "📊 Executive Summary":
    st.title("📊 Executive Summary")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📦 Total Products Sold", int(filtered_df['Number of products sold'].sum()))
    col2.metric("💰 Total Revenue", f"${filtered_df['Revenue generated'].sum():,.2f}")
    col3.metric("📉 Avg. Defect Rate", f"{filtered_df['Defect rates'].mean():.2f}%")
    col4.metric("⏳ Avg. Lead Time", f"{filtered_df['Lead times'].mean():.1f} days")

# WAREHOUSES
elif menu == "🏢 Warehouses":
    st.title("🏢 Warehouse Distribution")
    warehouse_fig = px.histogram(filtered_df, x='Location', y='Stock levels', color='Availability',
                                 title='Warehouse Stock Levels')
    st.plotly_chart(warehouse_fig, use_container_width=True)

# AVAILABILITY
elif menu == "📦 Availability":
    st.title("📦 Item Availability")
    inventory_fig = px.bar(filtered_df, x='SKU', y='Stock levels', color='Availability', title='Inventory by SKU')
    st.plotly_chart(inventory_fig, use_container_width=True)

# EXCESSIVE STOCK
elif menu == "📈 Excessive Stock":
    st.title("📈 Excessive Stock Items")
    excess_df = filtered_df[filtered_df['Availability'] == 'Overstock']
    excess_fig = px.bar(excess_df, x='SKU', y='Stock levels', color='Location', title='Excess Stock by SKU')
    st.plotly_chart(excess_fig, use_container_width=True)

# MISSING STOCK
elif menu == "🚫 Missing Stock":
    st.title("🚫 Missing or Out-of-Stock Items")
    missing_df = filtered_df[filtered_df['Availability'].isin(['Stock-out', 'Below Safety'])]
    miss_fig = px.bar(missing_df, x='SKU', y='Stock levels', color='Location', title='Items Missing Stock Threshold')
    st.plotly_chart(miss_fig, use_container_width=True)

# HISTORICAL STATUS
elif menu == "📚 Historical Status":
    st.title("📚 Inventory Historical Status")
    st.line_chart(filtered_df[['Stock levels', 'Lead times']])

# STOCK COVERAGE
elif menu == "📉 Stock Coverage":
    st.title("📉 Stock Coverage Analysis")
    st.bar_chart(filtered_df['Stock levels'])

# ITEMS
elif menu == "🧾 Items":
    st.title("🧾 Item-wise Details")
    st.dataframe(filtered_df[['SKU', 'Product Type', 'Stock levels', 'Availability', 'Revenue generated']])

# ADHOC
elif menu == "🧪 Adhoc":
    st.title("🧪 Adhoc Analysis")
    adhoc_fig = px.scatter(filtered_df, x='Manufacturing lead time', y='Manufacturing costs',
                           color='Defect rates', size='Revenue generated',
                           title='Lead Time vs Manufacturing Cost')
    st.plotly_chart(adhoc_fig, use_container_width=True)

# RAW DATA
if show_data:
    st.subheader("📋 Raw Filtered Data")
    st.dataframe(filtered_df)

# FOOTER
st.markdown("---")
st.markdown("Made with ❤️ by SCM Innovators Team ✨")
