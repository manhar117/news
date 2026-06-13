import streamlit as st
import requests
import pandas as pd

# -------------------------------------------------
# CONFIG
# -------------------------------------------------

st.set_page_config(
    page_title="Advanced News Dashboard",
    page_icon="📰",
    layout="wide"
)

API_KEY = st.secrets["NEWS_API_KEY"]

TOP_HEADLINES_URL = "https://newsapi.org/v2/top-headlines"
EVERYTHING_URL = "https://newsapi.org/v2/everything"

# -------------------------------------------------
# TITLE
# -------------------------------------------------

st.title("📰 Advanced News Dashboard")
st.markdown("Search and filter the latest news headlines")

# -------------------------------------------------
# SIDEBAR FILTERS
# -------------------------------------------------

st.sidebar.header("Filters")

countries = {
    "India": "in",
    "United States": "us",
    "United Kingdom": "gb",
    "Australia": "au",
    "Canada": "ca",
    "Germany": "de",
    "France": "fr",
    "Japan": "jp"
}

categories = [
    "general",
    "business",
    "entertainment",
    "health",
    "science",
    "sports",
    "technology"
]

country = st.sidebar.selectbox(
    "Select Country",
    list(countries.keys())
)

category = st.sidebar.selectbox(
    "Select Category",
    categories
)

keyword = st.sidebar.text_input(
    "Search Keywords"
)

page_size = st.sidebar.slider(
    "Number of Articles",
    min_value=5,
    max_value=50,
    value=10
)

search_btn = st.sidebar.button("Fetch News")

# -------------------------------------------------
# FUNCTION TO FETCH NEWS
# -------------------------------------------------

def fetch_news(country_code, category, keyword, page_size):

    headers = {
        "Authorization": API_KEY
    }

    try:

        # If keyword entered -> use Everything endpoint
        if keyword.strip():

            params = {
                "q": keyword,
                "pageSize": page_size,
                "language": "en",
                "sortBy": "publishedAt",
                "apiKey": API_KEY
            }

            response = requests.get(
                EVERYTHING_URL,
                params=params,
                timeout=15
            )

        else:

            params = {
                "country": country_code,
                "category": category,
                "pageSize": page_size,
                "apiKey": API_KEY
            }

            response = requests.get(
                TOP_HEADLINES_URL,
                params=params,
                timeout=15
            )

        response.raise_for_status()

        return response.json()

    except Exception as e:
        st.error(f"Error fetching news: {e}")
        return None

# -------------------------------------------------
# FETCH NEWS
# -------------------------------------------------

if search_btn:

    with st.spinner("Fetching latest news..."):

        news_data = fetch_news(
            countries[country],
            category,
            keyword,
            page_size
        )

        if news_data and news_data["status"] == "ok":

            articles = news_data["articles"]

            st.success(f"Found {len(articles)} articles")

            for article in articles:

                st.markdown("---")

                col1, col2 = st.columns([1, 2])

                with col1:

                    image_url = article.get("urlToImage")

                    if image_url:
                        st.image(image_url, use_container_width=True)

                with col2:

                    st.subheader(article.get("title"))

                    st.write(
                        f"**Source:** {article['source']['name']}"
                    )

                    st.write(
                        f"**Published:** {article.get('publishedAt', 'N/A')}"
                    )

                    description = article.get("description")

                    if description:
                        st.write(description)

                    url = article.get("url")

                    if url:
                        st.markdown(
                            f"[Read Full Article]({url})"
                        )

        else:
            st.warning("No articles found.")

# -------------------------------------------------
# DEFAULT LOAD
# -------------------------------------------------

if not search_btn:

    st.info(
        "Select filters from the sidebar and click 'Fetch News'"
    )