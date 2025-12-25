# ------------------------------------------------------------
# Flipkart Customer Segmentation Dashboard (Streamlit App)
# ------------------------------------------------------------

import streamlit as st
import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
import os
import pyodbc

warnings.filterwarnings('ignore')
sns.set(style="whitegrid")

# ------------------------------------------------------------
# Streamlit UI
# ------------------------------------------------------------
st.set_page_config(page_title="Flipkart Customer Segmentation", layout="wide")

st.title("🛒 Flipkart Customer Segmentation Dashboard")
st.markdown("### A Data-Driven Clustering Approach using MS SQL + K-Means")

# ------------------------------------------------------------
# Step 1: Database Connection Parameters (User Input)
# ------------------------------------------------------------
with st.sidebar:
    st.header("⚙️ Database Connection")
    server = st.text_input("Server", "DESKTOP-F3O24D7")
    database = st.text_input("Database", "flipkart2")
    username = st.text_input("Username", "sa")
    password = st.text_input("Password", "sujitha123", type="password")
    driver = st.text_input("Driver", "ODBC Driver 18 for SQL Server")

    if st.button("🔗 Connect to Database"):
        try:
            connection_string = f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver={driver}'
            db_engine = create_engine(connection_string)
            st.success("✅ Connected to MS SQL Server successfully!")
            st.session_state["db_engine"] = db_engine
        except Exception as e:
            st.error(f"❌ Connection failed: {e}")
# ------------------------------------------------------------
# Step 2: Load Data
# ------------------------------------------------------------
if "db_engine" in st.session_state:
    db_engine = st.session_state["db_engine"]

    st.subheader("📊 Step 1: Load Data from SQL")
    try:
        df1 = pd.read_sql("SELECT * FROM customers", db_engine)
        df2 = pd.read_sql("SELECT * FROM orders", db_engine)
        st.write("✅ Data loaded successfully!")
        st.write("**Customers Table (Sample):**")
        st.dataframe(df1.head())
        st.write("**Orders Table (Sample):**")
        st.dataframe(df2.head())
    except Exception as e:
        st.error(f"Error loading data: {e}")

    # ------------------------------------------------------------
    # Step 3: RFM Feature Engineering
    # ------------------------------------------------------------
    rfm_query = """
    SELECT
        o.CustomerID,
        DATEDIFF(DAY, MAX(o.OrderDate), GETDATE()) AS Recency,
        COUNT(o.OrderID) AS Frequency,
        SUM(o.OrderAmount) AS Monetary
    FROM Orders o
    GROUP BY o.CustomerID
    """

    st.subheader("📈 Step 2: RFM Feature Engineering")
    rfm_df = pd.read_sql(rfm_query, db_engine)
    st.dataframe(rfm_df.head())

    # ------------------------------------------------------------
    # Step 4: Merge and Clean Data
    # ------------------------------------------------------------
    merged_df = pd.merge(df1, rfm_df, on='CustomerID', how='inner')
    merged_df = merged_df.fillna(0)
    merged_df = merged_df[(merged_df['Monetary'] > 0)]

    st.subheader("🧹 Step 3: Cleaned and Merged Data")
    st.dataframe(merged_df.head())

    # ------------------------------------------------------------
    # Step 5: Feature Scaling
    # ------------------------------------------------------------
    features = merged_df[['Recency', 'Frequency', 'Monetary']]
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)

    # ------------------------------------------------------------
    # Step 6: Elbow Method for Optimal K
    # ------------------------------------------------------------
    inertia = []
    for k in range(2, 10):
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(scaled_features)
        inertia.append(kmeans.inertia_)

    st.subheader("📊 Step 4: Elbow Method for Optimal Clusters")

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(range(2, 10), inertia, marker='o')
    ax.set_title('Elbow Method - Inertia vs K')
    ax.set_xlabel('Number of Clusters')
    ax.set_ylabel('Inertia')
    st.pyplot(fig)

    # ------------------------------------------------------------
    # Step 7: Final KMeans Model
    # ------------------------------------------------------------
    selected_k = st.slider("Select Number of Clusters (K)", 2, 10, 4)
    kmeans_final = KMeans(n_clusters=selected_k, random_state=42)
    merged_df['Cluster'] = kmeans_final.fit_predict(scaled_features)

    st.subheader("🏷️ Step 5: Cluster Summary")
    cluster_summary = merged_df.groupby('Cluster')[['Recency','Frequency','Monetary']].mean().round(2)
    st.dataframe(cluster_summary)

    # ------------------------------------------------------------
    # Step 8: Visualize Clusters
    # ------------------------------------------------------------
    st.subheader("🎨 Step 6: Cluster Visualization")

    fig2, ax2 = plt.subplots(figsize=(8, 6))
    sns.scatterplot(
        data=merged_df,
        x='Recency',
        y='Monetary',
        hue='Cluster',
        palette='Set2',
        s=100,
        ax=ax2
    )
    ax2.set_title("Customer Segments by Recency vs Monetary")
    st.pyplot(fig2)

    # ------------------------------------------------------------
    # Step 9: Save and Download Results
    # ------------------------------------------------------------
    csv_path = 'flipkart_customer_segments.csv'
    merged_df.to_csv(csv_path, index=False)

    st.success("✅ Segmentation complete! Results saved.")
    st.download_button(
        label="📥 Download Segmentation CSV",
        data=open(csv_path, 'rb').read(),
        file_name='flipkart_customer_segments.csv',
        mime='text/csv'
    )


    st.info(f"📁 File saved at: {os.path.abspath(csv_path)}")



