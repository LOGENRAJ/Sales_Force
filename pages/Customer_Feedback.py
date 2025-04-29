import streamlit as st
import pandas as pd
from textblob import TextBlob

FEEDBACK_FILE = "customer_feedback.csv"

# Load Feedback Data
@st.cache_data
def load_feedback():
    try:
        return pd.read_csv(FEEDBACK_FILE)
    except FileNotFoundError:
        return pd.DataFrame(columns=["Customer_Name", "Product", "Rating", "Feedback", "Sentiment"])

# Save Feedback
def save_feedback(df):
    df.to_csv(FEEDBACK_FILE, index=False)

st.title("💬 Customer Feedback & Insights")

# ---- Customer Feedback Form ----
with st.form("feedback_form"):
    customer_name = st.text_input("👤 Your Name")
    product_name = st.text_input("📦 Product Purchased")
    rating = st.slider("⭐ Rating (1-5)", 1, 5, 3)
    feedback_text = st.text_area("📝 Share Your Feedback")
    submit_button = st.form_submit_button("Submit Feedback")

    if submit_button:
        sentiment = "Positive" if TextBlob(feedback_text).sentiment.polarity > 0 else "Negative"
        feedback_df = load_feedback()
        new_entry = pd.DataFrame([[customer_name, product_name, rating, feedback_text, sentiment]],
                                 columns=["Customer_Name", "Product", "Rating", "Feedback", "Sentiment"])
        feedback_df = pd.concat([feedback_df, new_entry], ignore_index=True)
        save_feedback(feedback_df)
        st.success("✅ Feedback Submitted Successfully!")

# ---- Display Feedback Data ----
feedback_df = load_feedback()

st.subheader("📊 Customer Feedback Dashboard")
if not feedback_df.empty:
    st.dataframe(feedback_df)

    # ---- Sentiment Analysis ----
    sentiment_counts = feedback_df["Sentiment"].value_counts()
    st.subheader("📊 Feedback Sentiment Analysis")
    st.bar_chart(sentiment_counts)
else:
    st.info("No feedback received yet.")
