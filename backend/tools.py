from dotenv import load_dotenv

load_dotenv()


from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
import os
from firecrawl import Firecrawl
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate


from fastapi import APIRouter, HTTPException, Query
from rich import print

# load clients

# fire crawl news fetching
api_key = os.getenv("FIRECRAWL_API_KEY")
firecrawl = Firecrawl(api_key=api_key) if api_key else None

# gemini mode
llm_model = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite", temperature=0)


# -----------------------------
# create tools


@tool
def web_search(query: str, limit: int = Query(5, ge=1, le=5)) -> str:
    """Search the web for recent and reliable information on a topic. Returns Titles, URLs, Snippet"""

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

        articles = []
        for item in items:
            if isinstance(item, dict):
                get = item.get
            else:
                get = lambda key, default=None: getattr(item, key, default)

            articles.append(
                {
                    "title": get("title", ""),
                    "url": get("url", ""),
                    "snippet": get("snippet") or get("description", ""),
                    "source": get("source", ""),
                    "date": get("date", ""),
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
def web_page_scrapping(url):
    """Scrape and return clean text content from the given url for deeper reading"""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}

        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "lxml")

        # Remove unwanted tags
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()

        text = soup.get_text(separator="\n", strip=True)

        return text[:4000]  # avoid huge context

    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"News search failed: {str(exc)}",
        )
