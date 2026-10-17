from dotenv import load_dotenv

load_dotenv()


from langchain.tools import tool
from typing import TypedDict
import requests
from bs4 import BeautifulSoup
import os
from firecrawl import Firecrawl


from fastapi import APIRouter, HTTPException, Query
from rich import print

# load clients

# fire crawl news fetching
api_key = os.getenv("FIRECRAWL_API_KEY")
firecrawl = Firecrawl(api_key=api_key) if api_key else None


class NewsArticle(TypedDict):
    title: str
    url: str
    snippet: str
    source: str
    date: str


class NewsSearchResult(TypedDict):
    query: str
    count: int
    articles: list[NewsArticle]


# -----------------------------
# create tools


# ----------------------------
# web serach tool
def search_news(query: str) -> NewsSearchResult:
    if firecrawl is None:
        raise HTTPException(
            status_code=500,
            detail="Firecrawl API key is not configured",
        )

    try:
        result = firecrawl.search(
            query,
            sources=["news"],
            limit=5,
        )
        # Current SDK groups results by source type.
        items = getattr(result, "news", None) or []

        articles: list[NewsArticle] = []
        for item in items:
            if isinstance(item, dict):
                get = item.get
            else:
                get = lambda key, default=None: getattr(item, key, default)

            articles.append(
                {
                    "title": get("title") or "",
                    "url": get("url") or "",
                    "snippet": get("snippet") or get("description") or "",
                    "source": get("source") or "",
                    "date": get("date") or "",
                }
            )

        return {
            "query": query,
            "count": len(articles),
            "articles": articles,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"News search failed: {str(exc)}",
        )


@tool
def web_search(query: str) -> NewsSearchResult:
    """Search the web for recent and reliable information on a topic. Returns titles, URLs, and snippets."""
    return search_news(query)


# ----------------------------
# ouput of web serach

# print(web_search.invoke("what is recent news of strike?"))
# {
#     'query': 'what is recent news of strike?',
#     'count': 5,
#     'articles': [
#         {
#             'title': 'Houthi Missiles Strike Government Headquarters in Yemen',
#             'url': 'https://www.nytimes.com/2026/10/15/world/middleeast/yemen-strike-aden-palace.html',
#             'snippet': 'Five people were killed when the Houthi militia struck the Maashiq Palace in Aden, a Yemeni minister said.',
#             'source': '',
#             'date': '17 hours ago'
#         },
#     ]
# }


# ------------------------------
# web page - scrapping
@tool
def web_page_scrapping(url: str) -> str:
    """Scrape and return clean text content from the given URL."""

    try:
        headers = {"User-Agent": "Mozilla/5.0"}

        response = requests.get(url, headers=headers, timeout=20)

        # Don't raise automatically
        if response.status_code != 200:
            return f"Unable to scrape URL. " f"HTTP Status: {response.status_code}"

        soup = BeautifulSoup(response.text, "lxml")

        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()

        text = soup.get_text(separator="\n", strip=True)

        if not text.strip():
            return "Page loaded but no readable content was found."

        return text[:3000]

    except requests.Timeout:
        return "Request timed out while scraping the webpage."

    except requests.ConnectionError:
        return "Could not connect to the webpage."

    except Exception as exc:
        return f"Scraping failed: {str(exc)}"


# ------------------------
# output for web scrapping

# print(
#     web_page_scrapping.invoke(
#         "https://www.nytimes.com/2026/10/15/world/middleeast/yemen-strike-aden-palace.html"
#     )
# )

# Houthi Missiles Strike Government Headquarters in Yemen - The New York Times
# Advertisement
# SKIP ADVERTISEMENT
# You have a preview view of this article while we are checking your access. When we have confirmed access, the full article content will
# load.
# The Houthi militia struck the headquarters of Yemen’s government with a missile barrage on Thursday, killing five people, officials said,
# as casualties mounted across several fronts of fierce fighting.
# Additionally, at least 16 people were injured in the Houthi attack on the Maashiq Palace in Aden, the southern Yemeni city that serves as
# the seat of the country’s internationally recognized government, health officials said.
# Shaya al-Zindani, the prime minister, was not hurt, according to the Yemeni information minister, Moammar al-Eryani. It was unclear
# whether Mr. al-Zindani was present at the time of the attack.
# While the extent of damage to the palace was unknown, videos shared on social media Thursday show smoke rising from near the building and
# visible over a mile away.
# Aden has been the seat of Yemen’s government since 2015, after the Houthis seized the capital city, Sanaa, igniting a decade-long war.
# While nominally the official authority in southern Yemen, the government has limited powers there, because in practice it has for years
# operated largely from exile in Riyadh, Saudi Arabia.
# Shortly after the strike on the palace, the Saudi-backed government in Yemen said that Houthi fighters had also launched several
# ballistic missiles at Marib, an oil-rich city in central Yemen.
# We are having trouble retrieving the article content.
# Please enable JavaScript in your browser settings.
# Thank you for your patience while we verify access. If you are in Reader mode please exit and
# log into
# your Times account, or
# subscribe
# for all of The Times.
# Thank you for your patience while we verify access.
# Already a subscriber?
# Log in
# .
# Want all of The Times?
# Subscribe
# .
# Related Content
# Advertisement
# SKIP ADVERTISEMENT
