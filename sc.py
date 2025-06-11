# 🚀 Futuristic Supply Chain Management Dashboard App using Streamlit

import streamlit as st
import pandas as pd
import plotly.express as px

# Streamlit page config
st.set_page_config(
    page_title="🚀 Futuristic Supply Chain Dashboard",
    layout="wide",
    page_icon="📦"
)

# Sidebar for file upload
st.sidebar.title("📁 Upload Supply Chain CSV")
uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        df.columns = df.columns.str.strip()  # Clean up column names

        # Display column names
        st.sidebar.markdown("### 🧾 Dataset Columns")
        for col in df.columns:
            st.sidebar.markdown(f"🔹 {col}")

        # Check required fields
        required_cols = ['Product type', 'Location', 'Supplier name']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            st.error(f"❌ Missing required columns: {', '.join(missing_cols)}")
            st.stop()

        # Navigation menu
        st.sidebar.title("🧭 Dashboard Sections")
        menu = st.sidebar.radio("Navigate to", [
            "🏠 Home", "📊 Executive Summary", "🏢 Warehouses", "📦 Availability", 
            "📈 Excessive Stock", "🚫 Missing Stock", "📚 Historical Status", 
            "📉 Stock Coverage", "🧾 Items", "🧪 Adhoc"
        ])

        # Sidebar filters
        st.sidebar.header("🔍 Filters")
        product = st.sidebar.selectbox("🧴 Product Type", df['Product type'].unique())
        location = st.sidebar.selectbox("📍 Location", df['Location'].unique())
        supplier = st.sidebar.selectbox("🏭 Supplier", df['Supplier name'].unique())
        show_data = st.sidebar.checkbox("📋 Show Filtered Data")

        # Apply filters
        filtered_df = df[
            (df['Product type'] == product) & 
            (df['Location'] == location) & 
            (df['Supplier name'] == supplier)
        ]

        # 🏠 HOME
        if menu == "🏠 Home":
            st.title("🤖 Welcome to the Futuristic Supply Chain Dashboard")
            st.markdown("""
            > Designed for smart monitoring, optimization & automation.  
            Navigate through each section to explore powerful visualizations!  
            📦🚛🧪📊💡
            """)

        # 📊 EXECUTIVE SUMMARY
        elif menu == "📊 Executive Summary":
            st.title("📊 Executive Summary")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("📦 Total Products Sold", int(filtered_df['Number of products sold'].sum()))
            col2.metric("💰 Revenue", f"${filtered_df['Revenue generated'].sum():,.2f}")
            col3.metric("🔧 Avg. Defect Rate", f"{filtered_df['Defect rates'].mean():.2f}%")
            col4.metric("⏱️ Avg. Lead Time", f"{filtered_df['Lead times'].mean():.1f} days")

        # 🏢 WAREHOUSES
        elif menu == "🏢 Warehouses":
            st.title("🏢 Warehouse Stock Overview")
            fig = px.histogram(filtered_df, x='Location', y='Stock levels', color='Availability')
            st.plotly_chart(fig, use_container_width=True)

        # 📦 AVAILABILITY
        elif menu == "📦 Availability":
            st.title("📦 Item Availability")
            fig = px.bar(filtered_df, x='SKU', y='Stock levels', color='Availability')
            st.plotly_chart(fig, use_container_width=True)

        # 📈 EXCESSIVE STOCK
        elif menu == "📈 Excessive Stock":
            st.title("📈 Overstock Items")
            excess_df = filtered_df[filtered_df['Availability'] == 'Overstock']
            fig = px.bar(excess_df, x='SKU', y='Stock levels', color='Location')
            st.plotly_chart(fig, use_container_width=True)

        # 🚫 MISSING STOCK
        elif menu == "🚫 Missing Stock":
            st.title("🚫 Stock-Outs & Low Stock Items")
            missing_df = filtered_df[filtered_df['Availability'].isin(['Stock-out', 'Below Safety'])]
            fig = px.bar(missing_df, x='SKU', y='Stock levels', color='Location')
            st.plotly_chart(fig, use_container_width=True)

        # 📚 HISTORICAL STATUS
        elif menu == "📚 Historical Status":
            st.title("📚 Historical Inventory Status")
            if {'Stock levels', 'Lead times'}.issubset(filtered_df.columns):
                st.line_chart(filtered_df[['Stock levels', 'Lead times']])
            else:
                st.warning("Historical columns not found in filtered data.")

        # 📉 STOCK COVERAGE
        elif menu == "📉 Stock Coverage":
            st.title("📉 Stock Coverage")
            st.bar_chart(filtered_df['Stock levels'])

        # 🧾 ITEMS
        elif menu == "🧾 Items":
            st.title("🧾 Item Details")
            st.dataframe(filtered_df[['SKU', 'Product type', 'Stock levels', 'Availability', 'Revenue generated']])

        # 🧪 ADHOC
        elif menu == "🧪 Adhoc":
            st.title("🧪 Adhoc Analytics")
            fig = px.scatter(
                filtered_df, 
                x='Manufacturing lead time', 
                y='Manufacturing costs',
                color='Defect rates',
                size='Revenue generated',
                hover_data=['SKU'],
                title="🧪 Lead Time vs Manufacturing Cost"
            )
            st.plotly_chart(fig, use_container_width=True)

        # 📋 Show data
        if show_data:
            st.subheader("📋 Raw Filtered Data")
            st.dataframe(filtered_df)

        # Footer
        st.markdown("---")
        st.markdown("💡 Created by **SCM Futurist Labs** | ✨ Innovate. Optimize. Deliver.")

    except Exception as e:
        st.error(f"❌ Error reading file: {e}")

else:
    st.warning("📂 Please upload a CSV file to begin.")
