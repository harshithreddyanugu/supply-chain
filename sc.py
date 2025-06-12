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
        df.columns = df.columns.str.strip()

        st.sidebar.markdown("### 🧾 Available Columns")
        for col in df.columns:
            st.sidebar.markdown(f"- {col}")

        # Navigation
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

        # Filters
        st.sidebar.markdown("---")
        st.sidebar.header("🔍 Filters")
        product = st.sidebar.selectbox("Select Product Type", df['Product type'].unique())
        location = st.sidebar.selectbox("Select Location", df['Location'].unique())
        supplier = st.sidebar.selectbox("Select Supplier", df['Supplier name'].unique())
        show_data = st.sidebar.checkbox("📑 Show Raw Data")

        filtered_df = df[(df['Product type'] == product) & 
                         (df['Location'] == location) & 
                         (df['Supplier name'] == supplier)]

        if menu == "🏠 Home":
            st.title("🚀 Welcome to the Futuristic SCM Dashboard")
            st.markdown("""
            Gain insights and take action on your supply chain performance 🌍⚙️.
            Use the navigation sidebar to explore each key aspect of your operations.
            """)

        elif menu == "📊 Executive Summary":
            st.title("📊 Executive Summary")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("🧮 Products Sold", int(filtered_df['Number of products sold'].sum()))
            col2.metric("💸 Revenue", f"${filtered_df['Revenue generated'].sum():,.2f}")
            col3.metric("⚠️ Avg. Defect Rate", f"{filtered_df['Defect rates'].mean():.2f}%")
            col4.metric("⏱️ Avg. Lead Time", f"{filtered_df['Lead times'].mean():.1f} days")

        elif menu == "🏢 Warehouses":
            st.title("🏢 Warehouse Distribution")
            fig = px.histogram(filtered_df, x='Location', y='Stock levels', color='Product type', barmode='group')
            st.plotly_chart(fig, use_container_width=True)

        elif menu == "📦 Availability":
            st.title("📦 Item Availability")
            fig = px.bar(filtered_df, x='SKU', y='Stock levels', color='Availability',
                         title='Stock Levels by SKU')
            st.plotly_chart(fig, use_container_width=True)

        elif menu == "📈 Excessive Stock":
            st.title("📈 Excessive Stock")
            excess_df = filtered_df[filtered_df['Stock levels'] > 75]
            fig = px.bar(excess_df, x='SKU', y='Stock levels', color='Location')
            st.plotly_chart(fig, use_container_width=True)

        elif menu == "🚫 Missing Stock":
            st.title("🚫 Missing Stock")
            missing_df = filtered_df[filtered_df['Stock levels'] < 10]
            fig = px.bar(missing_df, x='SKU', y='Stock levels', color='Location')
            st.plotly_chart(fig, use_container_width=True)

        elif menu == "📚 Historical Status":
            st.title("📚 Historical Inventory Trends")
            st.line_chart(filtered_df[['Stock levels', 'Lead times']])

        elif menu == "📉 Stock Coverage":
            st.title("📉 Stock Coverage")
            st.bar_chart(filtered_df['Stock levels'])

        elif menu == "🧾 Items":
            st.title("🧾 Detailed Item View")
            st.dataframe(filtered_df[[
                'SKU', 'Product type', 'Availability', 'Stock levels', 'Price',
                'Revenue generated', 'Lead times', 'Manufacturing costs'
            ]])

        elif menu == "🧪 Adhoc":
            st.title("🧪 Adhoc Analysis")
            fig = px.scatter(filtered_df, 
                             x='Manufacturing lead time', y='Manufacturing costs', 
                             size='Revenue generated', color='Defect rates', 
                             hover_data=['SKU'],
                             title='Lead Time vs Cost vs Defect Rate')
            st.plotly_chart(fig, use_container_width=True)

        if show_data:
            st.subheader("📋 Raw Filtered Data")
            st.dataframe(filtered_df)

        st.markdown("---")
        st.markdown("Made with ❤️ by SCM Innovators ✨")

    except Exception as e:
        st.error(f"❌ Error reading file: {e}")
else:
    st.warning("📂 Please upload a CSV file to get started.")
