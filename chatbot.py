import streamlit as st
import requests

st.set_page_config(page_title="📈 Stock News Bot", layout="centered")
st.title("📢 Quality Stock News Bot")
st.write("Get real-time, high-quality financial news. Powered by GNews API.")

# ✅ Define Quality Filter
def is_quality_news(title, description, source):
    quality_keywords = [
        # Earnings & Performance
        'results', 'q1', 'q2', 'q3', 'q4', 'quarterly',
        'financials', 'revenue', 'profit', 'loss', 'net loss',
        'net income', 'earnings', 'eps', 'ebitda',
        'net profit', 'gross profit', 'operating profit', 'operating income',
        'margins', 'margin', 'topline', 'bottomline', 'income statement',

        # Growth & Forecasts
        'growth', 'forecast', 'guidance', 'projection', 'outlook',
        'expectation', 'estimates', 'expansion', 'scaling',

        # Announcements & Strategic Moves
        'dividend', 'payout', 'bonus issue', 'stock split',
        'merger', 'acquisition', 'joint venture', 'buyback', 'ipo',
        'fpo', 'spin off', 'listing', 'fundraising', 'allotment',

        # Operational Updates
        'business update', 'performance update', 'plant commissioning',
        'product launch', 'capacity expansion', 'ramp up', 'options',

        # Financial Events & Filings
        'board meeting', 'agm', 'egm', 'regulatory filing', 'press release',
        'shareholding pattern', 'annual report', 'investor presentation',
        'filing with sebi', 'announcement to bse', 'stock exchange filing',

        # Debt, Capital, Liquidity
        'debt', 'capital expenditure', 'capex', 'cash flow',
        'interest coverage', 'leverage', 'fund infusion', 'liquidity',

        # Compliance & Governance
        'shareholder', 'board resolution', 'audit report',
        'corporate action', 'disclosure', 'corporate governance',

        # Ratings & Institutional Activity
        'credit rating', 'upgrade', 'downgrade', 'fitch', 'care ratings',
        'crisil', 'moodys', 'investment by fii', 'investment by dii'
    ]

    noise_keywords = [
        'should you buy', 'top stocks', 'analyst', 'recommendation',
        'buy or sell', 'hot picks', 'multibagger'
    ]

    trusted_sources = [
        # Indian financial media
        'Moneycontrol', 'Economic Times', 'ETMarkets', 'Business Standard',
        'LiveMint', 'CNBC TV18', 'Zee Business', 'NDTV Profit', 'Financial Express',
        'BloombergQuint', 'Hindu Business Line', 'Times of India', 'Business Today',

        # Global financial media
        'Reuters', 'Bloomberg', 'Yahoo Finance', 'CNBC', 'Forbes', 'Wall Street Journal',
        'Investing.com', 'Nasdaq', 'MarketWatch', 'Barron\'s', 'FT', 'Seeking Alpha',

        # Official and regulatory
        'SEBI', 'BSE India', 'NSE India', 'RBI', 'MoFPI', 'Gov.in', 'PIB India',

        # Ratings & analytics
        'CRISIL', 'ICRA', 'Care Ratings', 'Fitch', 'Moody\'s', 'S&P Global',

        # International business sites (optional)
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
    API_KEY = 'da02e13257b03fb0e6f8f013d6e36ba4'  # Replace with your own key if needed
    url = f"https://gnews.io/api/v4/search?q={stock_name}&lang=en&token={API_KEY}"
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
            return True 
            results.append((title, link, source, time))
    return results

# ✅ Streamlit UI
stock_name = st.text_input("Enter Stock Name (e.g., IRFC, Reliance):")

if stock_name:
    with st.spinner("🔍 Fetching latest quality news..."):
        news_list = fetch_news(stock_name)

    if news_list:
        st.success(f"✅ Found {len(news_list)} quality news articles.")
        for title, url, source, time in news_list:
            st.markdown(f"### 📰 {title}")
            st.markdown(f"[🔗 Read More]({url})")
            st.markdown(f"📍 Source: *{source}* &nbsp;&nbsp;&nbsp;&nbsp; 🕒 *{time}*")
            st.markdown("---")
    else:
        st.warning("❌ No quality news found. Try a different stock name or keyword.")

