import streamlit as st
import pandas as pd
import google.generativeai as genai

st.set_page_config(page_title="AI Data Analyzer", page_icon="📊", layout="wide")

st.title("📊 AI-Powered CSV Data Analyzer")
st.write("Upload any CSV dataset, explore its structure, and ask AI for insights.")

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("Enter your Gemini API Key:", type="password")
    st.caption("Get your free API key from [Google AI Studio](https://aistudio.google.com/)")
    
    if api_key:
        genai.configure(api_key=api_key)

# Main app logic
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    # Load dataset
    df = pd.read_csv(uploaded_file)
    
    st.subheader("1. Data Preview")
    st.dataframe(df.head())
    
    st.subheader("2. Dataset Profile")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Rows", df.shape[0])
    col2.metric("Total Columns", df.shape[1])
    col3.metric("Missing Values", df.isna().sum().sum())
    
    st.divider()
    
    st.subheader("3. Ask the AI")
    user_query = st.text_input("What would you like to know about this data? (e.g., 'What are the key trends?', 'Summarize the numeric columns')")
    
    if st.button("Analyze Data"):
        if not api_key:
            st.error("Please enter your Gemini API Key in the sidebar first.")
        elif not user_query:
            st.warning("Please enter a question to analyze.")
        else:
            with st.spinner("Analyzing dataset..."):
                try:
                    # Construct data context to send to the LLM
                    columns_info = f"Columns: {', '.join(df.columns.tolist())}"
                    sample_data = df.head(10).to_string()
                    
                    prompt = f"""
                    You are an expert Data Analyst. Here is a sample of a dataset:
                    {columns_info}
                    
                    Data Sample:
                    {sample_data}
                    
                    User Query: {user_query}
                    
                    Provide a concise, analytical answer based on the provided data sample and structure.
                    """
                    
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    response = model.generate_content(prompt)
                    
                    st.success("Analysis Complete!")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"An error occurred during AI analysis: {e}")