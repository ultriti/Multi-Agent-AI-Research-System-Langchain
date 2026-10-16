# create agent - using langraph
from dotenv import load_dotenv

load_dotenv()


from langchain.agents import create_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq

import os

from tools import web_search, web_page_scrapping

# models
gemini_model = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite", temperature=0)
groq_model = ChatGroq(model="openai/gpt-oss-20b", temperature=0)


# --------------------------
# 1st agent - web search
def build_search_agent():
    return create_agent(
        model=groq_model,
        tools=[web_search],
    )


# -----------------------------
# 2nd agent - web scrapping and info scrappin
def build_reader_agent():
    return create_agent(model=groq_model, tools=[web_page_scrapping])


# ----------------------------------
# writer chain prompt

writer_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert research writer. Write clear, structured and insightful reports.",
        ),
        (
            "human",
            """
                Write a detailed research report on the topic below.

                Topic: {topic}

                Research Gathered:
                {research}

                Structure the report as:
                - Introduction
                - Key Findings (minimum 3 well-explained points)
                - Conclusion
                - Sources (list all URLs found in the research)

                Be detailed, factual and professional.
            """,
        ),
    ]
)

# writer chain ------------------
writer_chain = writer_prompt | groq_model | StrOutputParser()


# --------------------------------
# critic chain - score the research n key improval
critics_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a sharp and constructive research critic. Be honest and specific.",
        ),
        (
            "human",
            """
                Review the research report below and evaluate it strictly.

                Report:
                {report}

                Respond in this exact format:

                Score: X/10

                Strengths:
                - ...
                - ...

                Areas to Improve:
                - ...
                - ...

                One line verdict:
                ...
            """,
        ),
    ]
)

# critic chain ---------------------
critics_chain = critics_prompt | groq_model | StrOutputParser()




