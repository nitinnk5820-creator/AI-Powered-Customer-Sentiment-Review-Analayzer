import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from utils import analyze_sentiment

# Page Configuration
st.set_page_config(
    page_title="AI Sentiment Analyzer Pro",
    page_icon="🚀",
    layout="wide"
)

# Custom CSS for Professional Look
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        background-color: #ff4b4b;
        color: white;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar Configuration
st.sidebar.title("🎛️ Navigation & Info")
app_mode = st.sidebar.selectbox(
    "Choose Analysis Mode",
    ["Single Review Analysis", "Bulk Review & Market Analytics"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 👨‍💻 Project Info")
st.sidebar.info(
    "**Developer:** Nitin Kumar\r\n"
    "**Enrollment No.:** 20241697\r\n"
    "**Course:** B.Tech CSE (3rd Year)\r\n"
    "**Tech Stack:** Python, Streamlit, Plotly, NLP"
)

# Main Title Area
st.title("🚀 AI-Powered Customer Sentiment & Market Intelligence Hub")
st.markdown("An enterprise-grade sentiment analytics dashboard designed for automated feedback processing, polarity visualization, and actionable business insights.")
st.markdown("---")

if app_mode == "Single Review Analysis":
    st.subheader("📝 Single Customer Review Evaluation")
    review_text = st.text_area("Enter or paste customer review text below:")
    
    if st.button("Analyze Sentiment"):
        if review_text.strip() != "":
            sentiment, polarity, subjectivity = analyze_sentiment(review_text)
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Sentiment", sentiment)
            col2.metric("Polarity Score", f"{polarity:.2f}")
            col3.metric("Subjectivity Score", f"{subjectivity:.2f}")
            
            if sentiment == "Positive":
                st.success("The analyzed sentiment is predominantly positive and indicates strong consumer satisfaction.")
            elif sentiment == "Negative":
                st.error("The analyzed sentiment is predominantly negative and highlights critical areas for improvement.")
            else:
                st.warning("The analyzed sentiment is neutral, reflecting moderate or mixed user feedback.")
        else:
            st.warning("Please enter some text to analyze.")

elif app_mode == "Bulk Review & Market Analytics":
    st.subheader("📊 Bulk Review Analytics & Export Suite")
    uploaded_file = st.file_uploader("Upload customer feedback CSV file", type=["csv"])
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("### Dataset Preview", df.head())
        
        text_column = st.selectbox("Select the column containing review texts:", df.columns)
        
        if st.button("Run Advanced Market Analysis"):
            sentiments = []
            polarities = []
            
            for text in df[text_column]:
                if pd.isna(text):
                    sentiments.append("Neutral")
                    polarities.append(0.0)
                else:
                    sent, pol, _ = analyze_sentiment(str(text))
                    sentiments.append(sent)
                    polarities.append(pol)
                    
            df['Sentiment'] = sentiments
            df['Polarity'] = polarities
            
            st.write("### Processed Results Matrix", df.head())
            
            # Sentiment Count Breakdown
            sentiment_counts = df['Sentiment'].value_counts().reset_index()
            sentiment_counts.columns = ['Sentiment', 'Count']
            
            # Interactive Plotly Bar Chart
            fig = px.bar(
                sentiment_counts, 
                x='Sentiment', 
                y='Count', 
                color='Sentiment',
                title='Market Sentiment Distribution Matrix',
                color_discrete_map={'Positive': '#2ecc71', 'Negative': '#e74c3c', 'Neutral': '#3498db'}
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Enterprise Download CSV Button
            csv_data = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Analyzed Report as CSV",
                data=csv_data,
                file_name="market_sentiment_report.csv",
                mime="text/csv",
            )
            
            # Robust Word Cloud Generation
            st.subheader("☁️ Market Keyword Frequency Cloud")
            try:
                valid_texts = [str(t) for t in df[text_column] if pd.notna(t) and str(t).strip() != ""]
                text_data = " ".join(valid_texts)
                
                if len(text_data.strip()) > 0:
                    wordcloud = WordCloud(width=900, height=450, background_color='white', colormap='plasma').generate(text_data)
                    
                    fig_wc, ax = plt.subplots(figsize=(10, 5))
                    ax.imshow(wordcloud, interpolation='bilinear')
                    ax.axis('off')
                    st.pyplot(fig_wc)
                else:
                    st.warning("No valid text data available in the selected column for word cloud generation.")
            except Exception as e:
                st.info("Word cloud generation could not be completed.")