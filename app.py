import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import streamlit as st
from textblob import TextBlob
from wordcloud import WordCloud

# Page Configuration
st.set_page_config(
    page_title="AI Sentiment Analyzer Pro", page_icon="🚀", layout="wide"
)

# Sidebar Navigation & Info
st.sidebar.title("Navigation & Info")
analysis_mode = st.sidebar.selectbox(
    "Choose Analysis Mode", ["Single Review Analysis", "Bulk Review & Market Hub"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📌 Project Info")
st.sidebar.markdown("**Developer:** Nitin Kumar")
st.sidebar.markdown("**Enrollment No.:** 20241697")
st.sidebar.markdown("**Course:** B.Tech CSE (3rd Year)")
st.sidebar.markdown(
    "**Tech Stack:** Python, Streamlit, Plotly, TextBlob, WordCloud, NLP"
)


# Helper function for sentiment analysis
def analyze_sentiment(text):
  analysis = TextBlob(text)
  polarity = analysis.sentiment.polarity
  if polarity > 0.1:
    sentiment = "Positive"
  elif polarity < -0.1:
    sentiment = "Negative"
  else:
    sentiment = "Neutral"
  return polarity, sentiment


# Mode 1: Single Review Analysis
if analysis_mode == "Single Review Analysis":
  st.title("🚀 AI-Powered Customer Sentiment & Market Intelligence Hub")
  st.markdown(
      "An enterprise-grade sentiment analytics dashboard designed for automated"
      " feedback processing, polarity visualization, and actionable business"
      " insights."
  )
  st.markdown("---")

  st.subheader("Single Customer Review Evaluation")
  review_text = st.text_area(
      "Enter or paste customer review text below",
      placeholder="Type your review here...",
  )

  if st.button("Analyze Sentiment"):
    if review_text.strip() != "":
      polarity, sentiment = analyze_sentiment(review_text)

      col1, col2, col3 = st.columns(3)
      col1.metric("Sentiment", sentiment)
      col2.metric("Polarity Score", f"{polarity:.2f}")
      col3.metric("Confidence", "High")

      if sentiment == "Positive":
        st.success("✅ The customer review is predominantly Positive!")
      elif sentiment == "Negative":
        st.error("❌ The customer review indicates Negative sentiment.")
      else:
        st.warning("⚠️ The customer review is Neutral.")
    else:
        st.error("Please enter some review text before analyzing.")

# Mode 2: Bulk Review & Market Hub
else:
  st.title("🚀 AI-Powered Customer Sentiment & Market Intelligence Hub")
  st.markdown("---")

  st.subheader("📊 Bulk Review Analytics & Export Suite")
  st.markdown(
      "Upload a customer feedback CSV file or paste CSV content below for"
      " batch processing."
  )

  # File uploader without strict type restriction for mobile friendliness
  uploaded_file = st.file_uploader(
      "Upload customer feedback CSV file (Columns required: review, sentiment"
      " or text)"
  )

  df = None

  # Mobile Fallback: Direct CSV Text Area input if file uploader behaves up
  if uploaded_file is not None:
    try:
      df = pd.read_csv(uploaded_file)
    except Exception as e:
      st.error(f"Error reading file: {e}")
  else:
    st.info(
        "💡 **Mobile Tip:** Agar phone mein file uploader gallery khol raha"
        " hai, toh aap apne CSV ka data yahan niche paste kar sakte hain!"
    )
    csv_paste = st.text_area(
        "Or paste CSV rows here (Format: review,rating)",
        placeholder=(
            "review,rating\nGreat product and fast delivery!,5\nWorst quality"
            " ever.,1"
        ),
    )
    if csv_paste.strip() != "":
      import io

      try:
        df = pd.read_csv(io.StringIO(csv_paste))
      except Exception as e:
        st.error(f"Invalid CSV format in text area: {e}")

  if df is not None:
    st.success("Data successfully loaded!")
    st.dataframe(df.head())

    # Check for text column
    text_col = None
    for col in df.columns:
      if (
          "review" in col.lower()
          or "text" in col.lower()
          or "comment" in col.lower()
      ):
        text_col = col
        break

    if text_col:
      st.info(f"Analyzing sentiments using column: **{text_col}**")
      polarities = []
      sentiments = []
      for text in df[text_col].astype(str):
        p, s = analyze_sentiment(text)
        polarities.append(p)
        sentiments.append(s)

      df["Polarity"] = polarities
      df["Sentiment"] = sentiments

      # Display metrics & charts
      st.subheader("Sentiment Distribution Summary")
      sentiment_counts = df["Sentiment"].value_counts()
      fig = px.pie(
          names=sentiment_counts.index,
          values=sentiment_counts.values,
          title="Customer Sentiment Breakdown",
          hole=0.4,
      )
      st.plotly_chart(fig, use_container_width=True)
    else:
      st.warning(
          "Could not find a review/text column in the uploaded dataset. Please"
          " ensure your CSV has a column named 'review' or 'text'."
      )
