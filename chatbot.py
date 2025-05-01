import streamlit as st
import requests

# Set page config
st.set_page_config(page_title="📈 Stock News Bot", layout="centered")
st.title("📢 Quality Stock News Bot")
st.write("Get real-time, high-quality financial news. Powered by GNews API.")

# ✅ Define Quality Filter
def is_quality_news(title, description, source):
    quality_keywords = [
        'results', 'q1', 'q2', 'q3', 'q4', 'quarterly',
        'financials', 'revenue', 'profit', 'loss', 'net loss',
        'net income', 'earnings', 'eps', 'ebitda',
        'net profit', 'gross profit', 'operating profit', 'operating income',
        'margins', 'margin', 'topline', 'bottomline', 'income statement', 'price',

        'growth', 'forecast', 'guidance', 'projection', 'outlook',
        'expectation', 'estimates', 'expansion', 'scaling',

        'dividend', 'payout', 'bonus issue', 'stock split',
        'merger', 'acquisition', 'joint venture', 'buyback', 'ipo',
        'fpo', 'spin off', 'listing', 'fundraising', 'allotment',

        'business update', 'performance update', 'plant commissioning',
        'product launch', 'capacity expansion', 'ramp up', 'options',

        'board meeting', 'agm', 'egm', 'regulatory filing', 'press release',
        'shareholding pattern', 'annual report', 'investor presentation',
        'filing with sebi', 'announcement to bse', 'stock exchange filing',

        'debt', 'capital expenditure', 'capex', 'cash flow',
        'interest coverage', 'leverage', 'fund infusion', 'liquidity',

        'shareholder', 'board resolution', 'audit report',
        'corporate action', 'disclosure', 'corporate governance',

        'credit rating', 'upgrade', 'downgrade', 'fitch', 'care ratings',
        'crisil', 'moodys', 'investment by fii', 'investment by dii'
    ]

    noise_keywords = [
        'should you buy', 'top stocks', 'analyst', 'recommendation',
        'buy or sell', 'hot picks', 'multibagger'
    ]

    trusted_sources = [
        'Moneycontrol', 'Economic Times', 'ETMarkets', 'Business Standard',
        'LiveMint', 'CNBC TV18', 'Zee Business', 'NDTV Profit', 'Financial Express',
        'BloombergQuint', 'Hindu Business Line', 'Times of India', 'Business Today',

        'Reuters', 'Bloomberg', 'Yahoo Finance', 'CNBC', 'Forbes', 'Wall Street Journal',
        'Investing.com', 'Nasdaq', 'MarketWatch', 'Barron\'s', 'FT', 'Seeking Alpha',

        'SEBI', 'BSE India', 'NSE India', 'RBI', 'MoFPI', 'Gov.in', 'PIB India',

        'CRISIL', 'ICRA', 'Care Ratings', 'Fitch', 'Moody\'s', 'S&P Global',

        'Business Insider', 'The Economist', 'The Guardian Business', 'BBC Business'
    ]

    text = f"{title or ''} {description or ''}".lower()
    source = source or ""

    return (
        any(k in text for k in quality_keywords)
        and not any(n in text for n in noise_keywords)
        and any(src.lower() in source.lower() for src in trusted_sources)
    )

# ✅ Fetch News Function
def fetch_news(stock_name):
    API_KEY = 'da02e13257b03fb0e6f8f013d6e36ba4'
    url = f"https://gnews.io/api/v4/search?q={stock_name}&lang=en&country=in&max=10&token={API_KEY}"
    response = requests.get(url)
    data = response.json()

    results = []
    for article in data.get('articles', []):
        title = article.get('title', '')
        desc = article.get('description', '')
        link = article.get('url', '')
        source = article.get('source', {}).get('name', '')
        time = article.get('publishedAt', '')

        if is_quality_news(title, desc, source):
            results.append((title, desc, link, source, time))

    return results

# ✅ Streamlit UI
stock_name = st.text_input("Enter Stock Name (e.g., IRFC, Reliance):")

if stock_name:
    with st.spinner("🔍 Fetching latest quality news..."):
        news_list = fetch_news(stock_name)

    if news_list:
        st.success(f"✅ Found {len(news_list)} quality news articles.")
        for title, desc, url, source, time in news_list:
            with st.expander(f"📰 {title}"):
                if desc:
                    st.markdown(f"**Summary:** {desc}")
                st.markdown(f"[🔗 Read Full Article]({url})", unsafe_allow_html=True)
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"📍 **Source:** *{source}*")
                with col2:
                    st.markdown(f"🕒 **Published:** *{time}*")
    else:
        st.warning("❌ No quality news found. Try a different stock name or keyword.")
