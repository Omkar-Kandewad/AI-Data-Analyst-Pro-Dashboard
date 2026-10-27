'''
import streamlit as st
import pandas as pd

st.title("Chai Sales Dashboard")
file=st.file_uploader("Upload your csv file",type=["csv"])
if file:
    df=pd.read_csv(file)
    st.subheader("Data Preview")
    st.dataframe(df)

if file:
    st.subheader("Summary stats")
    st.write(df.describe())

if file:
    city=df["BusinessTravel"].unique()
    selected=st.selectbox("Filter by city",city)
    filtered=df[df["BusinessTravel"]==selected]
    st.dataframe(filtered)
'''
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from openai import OpenAI

# API setup
client = OpenAI(api_key="your_api_key_here")

st.title("🚀 AI Data Analyst Pro Dashboard")

# File upload
file = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx"])

if file:
    # Read file
    if file.name.endswith(".csv"):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)

    st.subheader("📊 Data Preview")
    st.dataframe(df.head())

    # KPI Section
    st.subheader("📈 KPIs")
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns

    if len(numeric_cols) > 0:
        col = st.selectbox("Select column", numeric_cols)

        st.metric("Mean", round(df[col].mean(), 2))
        st.metric("Max", df[col].max())
        st.metric("Min", df[col].min())

        # Charts
        st.subheader("📊 Visualization")
        st.bar_chart(df[col])
        st.line_chart(df[col])

        # Pie chart
        st.subheader("🥧 Pie Chart")
        fig, ax = plt.subplots()
        df[col].value_counts().head(5).plot.pie(autopct='%1.1f%%', ax=ax)
        st.pyplot(fig)

    # AI Insights
    st.subheader("🤖 AI Insights")

    if st.button("Generate AI Insights"):
        prompt = f"""
        You are a senior data analyst.
        Analyze this dataset summary:
        {df.describe().to_string()}

        Give 5 business insights and 2 recommendations.
        """

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        st.write(response.choices[0].message.content)

    # Download Report
    st.subheader("📥 Download Data")
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download CSV", csv, "data.csv", "text/csv")
