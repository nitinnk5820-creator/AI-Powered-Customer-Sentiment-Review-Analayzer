import streamlit as st
from utils import analyze_sentiment, preprocess_text
import pandas as pd
import matplotlib.pyplot as plt

# Page Configuration
st.set_page_config(
    page_title="AI Sentiment Analyzer",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS for Professional Look
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-size: 16px;
        font-weight: bold;
        border-radius: 8px;
        padding: 10px 24px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .sidebar .sidebar-content {
        background-color: #2c3e50;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar Design
st.sidebar.markdown("## 🧭 Navigation & Options")
app_mode = st.sidebar.selectbox(
    "Choose Analysis Mode",
    ["Single Review Analysis", "Bulk Reviews Analysis (CSV)"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📌 Project Info")
st.sidebar.info(
    "**Developer:** Nitin Kumar\n\n"
    "**Enrollment No.:** 20241697\n\n" 
    "**Course:** B.Tech CSE (3rd Year)\n\n"
    "**Tech Stack:** Python, Streamlit, TextBlob, Pandas"
)

# Main Title Area
st.title("🤖 AI-Powered Customer Sentiment & Review Analyzer")
st.markdown("This professional web application automatically processes unstructured customer reviews, evaluates their underlying sentiment using Natural Language Processing (NLP), and presents actionable polarity insights.")
st.markdown("---")

# Single Review Analysis Section
if app_mode == "Single Review Analysis":
    st.subheader("📝 Single Customer Review Evaluation")
    
    review_text = st.text_area(
        "Enter or paste customer review text below:",
        placeholder="e.g., The product quality is absolutely amazing and delivery was super fast!"
    )
    
    if st.button("Analyze Sentiment"):
        if review_text.strip() == "":
            st.warning("⚠️ Please enter some review text before analyzing.")
        else:
            sentiment, polarity, subjectivity = analyze_sentiment(review_text)
            
            st.markdown("### 📊 Analysis Results")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if sentiment == "Positive":
                    st.success(f"**Sentiment Classification:**\n\n 🟢 {sentiment}")
                elif sentiment == "Negative":
                    st.error(f"**Sentiment Classification:**\n\n 🔴 {sentiment}")
                else:
                    st.warning(f"**Sentiment Classification:**\n\n 🟡 {sentiment}")
                    
            with col2:
                st.metric(label="Polarity Score (-1 to +1)", value=f"{polarity:.4f}")
                
            with col3:
                st.metric(label="Subjectivity Score (0 to 1)", value=f"{subjectivity:.4f}")
                
            with st.expander("🔍 View Text Preprocessing Details"):
                cleaned = preprocess_text(review_text)
                st.write(f"**Original Text:** {review_text}")
                st.write(f"**Processed Text:** {cleaned}")

# Bulk Review Analysis Section
elif app_mode == "Bulk Reviews Analysis (CSV)":
    st.subheader("📂 Bulk Customer Reviews Analysis")
    
    uploaded_file = st.file_uploader("Upload a CSV file containing customer reviews (must have a column named 'Review')", type=["csv"])
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        
        if "Review" not in df.columns:
            st.error("🚨 The uploaded CSV file must contain a column named 'Review'.")
        else:
            st.success("✅ CSV file successfully uploaded!")
            st.write("### Preview of Uploaded Data:")
            st.dataframe(df.head())
            
            if st.button("Run Bulk Analysis"):
                sentiments = []
                polarities = []
                subjectivities = []
                
                for text in df["Review"]:
                    s, p, sub = analyze_sentiment(str(text))
                    sentiments.append(s)
                    polarities.append(p)
                    subjectivities.append(sub)
                    
                df["Sentiment"] = sentiments
                df["Polarity"] = polarities
                df["Subjectivity"] = subjectivities
                
                st.success("🎉 Bulk analysis completed successfully!")
                st.dataframe(df.head(10))
                
                st.markdown("---")
                st.subheader("📊 Visual Analytics & Sentiment Distribution")
                
                sentiment_counts = df["Sentiment"].value_counts()
                
                fig, ax = plt.subplots(figsize=(6, 4))
                colors = ['#2ca02c', '#d62728', '#1f77b4']
                sentiment_counts.plot(kind='bar', color=colors[:len(sentiment_counts)], ax=ax)
                ax.set_title("Distribution of Customer Sentiments")
                ax.set_xlabel("Sentiment Category")
                ax.set_ylabel("Number of Reviews")
                st.pyplot(fig)
                
                csv_data = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Analyzed Report as CSV",
                    data=csv_data,
                    file_name="sentiment_analysis_report.csv",
                    mime="text/csv",
                )