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

# Upload CSV File
st.sidebar.title("📁 Upload Supply Chain CSV")
uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        df.columns = df.columns.str.strip()  # Strip spaces from column names

        # Print available column names for user
        st.sidebar.markdown("### 🧾 Available Columns in Dataset")
        for col in df.columns:
            st.sidebar.markdown(f"- {col}")

        # Required columns check
        required_cols = ['Product type', 'Location', 'Supplier name']
        missing_cols = [col for col in required_cols if col not in df.columns]

        if missing_cols:
            st.error(f"🚫 Missing required columns: {', '.join(missing_cols)}")
            st.stop()

        # Sidebar Navigation
        st.sidebar.title("🧭 Navigation")
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
        product = st.sidebar.selectbox("Select Product Type", df['Product type'].unique())
        location = st.sidebar.selectbox("Select Location", df['Location'].unique())
        supplier = st.sidebar.selectbox("Select Supplier", df['Supplier name'].unique())
        show_data = st.sidebar.checkbox("📑 Show Raw Data")

        # Filtered Data
        filtered_df = df[(df['Product type'] == product) & (df['Location'] == location) & (df['Supplier name'] == supplier)]

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
            st.dataframe(filtered_df[['SKU', 'Product type', 'Stock levels', 'Availability', 'Revenue generated']])

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

    except Exception as e:
        st.error(f"❌ Error reading file: {e}")
else:
    st.warning("📂 Please upload a CSV file to get started.")



