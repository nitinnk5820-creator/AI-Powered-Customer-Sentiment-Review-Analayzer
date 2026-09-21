from textblob import TextBlob

def preprocess_text(text):
    # Basic text cleaning (can be expanded if needed)
    cleaned_text = str(text).strip()
    return cleaned_text

def analyze_sentiment(text):
    # Clean text first
    processed = preprocess_text(text)
    
    # Create TextBlob object
    analysis = TextBlob(processed)
    
    # Get polarity score (-1 to +1)
    polarity = analysis.sentiment.polarity
    # Get subjectivity score (0 to 1)
    subjectivity = analysis.sentiment.subjectivity
    
    # Classify sentiment
    if polarity > 0:
        sentiment = "Positive"
    elif polarity < 0:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"
        
    return sentiment, polarity, subjectivity