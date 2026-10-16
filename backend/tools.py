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
#{
#     'query': 'what is recent news of strike?',
#     'count': 5,
#     'articles': [
#         {
#             'title': 'US Weighs Using ‘Mother of All Bombs’ in New Iran Strike Plans: Report',
#             'url': 'https://themedialine.org/headlines/us-weighs-using-mother-of-all-bombs-in-new-iran-strike-plans-report/',
#             'snippet': 'The US military has developed new options for strikes on Iranian energy infrastructure and nuclear sites that 
# include the potential first...',
#             'source': '',
#             'date': '1 day ago'
#         },
#         {
#             'title': 'Houthi Missiles Strike Government Headquarters in Yemen',
#             'url': 'https://www.nytimes.com/2026/10/15/world/middleeast/yemen-strike-aden-palace.html',
#             'snippet': 'Five people were killed when the Houthi militia struck the Maashiq Palace in Aden, a Yemeni minister said.',
#             'source': '',
#             'date': '17 hours ago'
#         },
#         {
#             'title': 'Chicago Hotel Workers Continue Strike Monday as They Seek New Contract',
#             'url': 'https://news.wttw.com/2026/10/12/chicago-hotel-workers-continue-strike-monday-they-seek-new-contract',
#             'snippet': '## Chicago Hotel Workers Continue Strike Monday as They Seek New Contract\n![Chicago hotel workers picket as they
# go on strike on Oct. 9, 2026. (WTTW 
# News)](https://news.wttw.com/sites/default/files/styles/article_hero/public/field/image/r_hotel_workers_strike_frame_5308_0.jpeg?itok=krY
# jgwWO)Chicago hotel workers picket as they go on strike on Oct.\n\nThat union represents around 7,000 room attendants, cooks, 
# dishwashers, front desk agents, servers and other hospitality workers at more than 40 Chicago hotels, who have been without a contract 
# since Sept.\n\n## [View all sponsors](https://news.wttw.com/sponsors)\n#### Related Stories\n[![Cook County College Teachers Union Local 
# 1600 members picket outside Harold Washington College on Oct. 2, 2026. (WTTW 
# News)](https://news.wttw.com/sites/default/files/styles/json_lg/public/field/image/r_city_colleges_strike_date_frame_16566_0.jpeg?itok=WO
# pz-ndJ)](https://news.wttw.com/2026/10/02/city-colleges-staff-announce-oct-19-strike-date-contract-negotiations-continue)\n\n[City 
# Colleges Staff Announce Oct. 19 Strike Date as Contract Negotiations 
# Continue](https://news.wttw.com/2026/10/02/city-colleges-staff-announce-oct-19-strike-date-contract-negotiations-continue)',
#             'source': '',
#             'date': '3 days ago'
#         },
#         {
#             'title': 'Could SEIU Local 1000 get a last-minute deal? Mediations start ahead of strike',
#             'url': 'https://www.sacbee.com/news/politics-government/the-state-worker/article317623453.html',
#             'snippet': '![SEIU Local 1000 members picketed Wednesday, July 22, 2026, outside the California Department of Human 
# Resources.](https://www.sacbee.com/public/latest-news/7dx30j/picture316618112/alternates/LANDSCAPE_1200/07-22-26%20SEIU%20picket)\n\nSEIU
# Local 1000 members picketed Wednesday, July 22, 2026, outside the California Department of Human Resources.\n\n### [SEIU Local 1000 
# announces one-day strike after members give 
# authorization](https://www.sacbee.com/news/politics-government/the-state-worker/article317516133.html#storylink=related_inline)\n##### 
# Get one year of unlimited digital access for $159.99\n###### #ReadLocal\nOnly 44¢ per day\n\n[SUBSCRIBE 
# NOW](https://mycheckout.sacbee.com/subscribe?ofrgp_id=414&g2i_or_o=OnSite&g2i_or_p=CTA&cid=cta_dynamic-zone_3a_159.99-annually_202307)',
#             'source': '',
#             'date': '1 day ago'
#         },
#         {
#             'title': 'New v-c seeks to turn around Goldsmiths as record strike drags on',
#             'url': 'https://www.timeshighereducation.com/news/new-v-c-seeks-turn-around-goldsmiths-record-strike-drags',
#             'snippet': 'Exams going unmarked and temporary lecturers causing friction 130 days into industrial action but Joanna Newman 
# believes she can end crisis...',
#             'source': '',
#             'date': '18 hours ago'
#         }
#     ]
# }