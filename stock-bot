import streamlit as st
import requests

st.set_page_config(page_title="📈 Stock News Bot", layout="centered")
st.title("📢 Quality Stock News Bot")
st.write("Get real-time, quality financial news. Powered by GNews API.")

def is_quality_news(title, description, source):
    quality_keywords = ['results', 'q1', 'q2', 'q3', 'q4', 'revenue', 'profit', 'dividend', 'net income', 'eps']
    noise_keywords = ['should you buy', 'top stocks', 'analyst', 'recommendation']
    trusted_sources = ['NDTV', 'Moneycontrol', 'Business Standard', 'Economic Times', 'Reuters', 'CNBC']

    text = f"{title} {description}".lower()
    return (
        any(k in text for k in quality_keywords)
        and not any(n in text for n in noise_keywords)
        and any(src.lower() in source.lower() for src in trusted_sources)
    )

def fetch_news(stock_name):
    API_KEY = da02e13257b03fb0e6f8f013d6e36ba4
    url = f"https://gnews.io/api/v4/search?q={stock_name}&lang=en&token={API_KEY}"
    response = requests.get(url)
    data = response.json()
    
    results = []
    for article in data.get('articles', []):
        title = article['title']
        desc = article['description']
        link = article['url']
        source = article['source']['name']
        time = article['publishedAt']
        
        if is_quality_news(title, desc, source):
            results.append((title, link, source, time))
    return results

stock_name = st.text_input("Enter Stock Name (e.g., IRFC, Reliance):")

if stock_name:
    with st.spinner("Fetching latest quality news..."):
        news_list = fetch_news(stock_name)
    if news_list:
        for title, url, source, time in news_list:
            st.markdown(f"### 📰 {title}")
            st.markdown(f"[🔗 Read More]({url})")
            st.markdown(f"📍 Source: *{source}* &nbsp;&nbsp;&nbsp;&nbsp; 🕒 *{time}*")
            st.markdown("---")
    else:
        st.warning("❌ No quality news found.")
