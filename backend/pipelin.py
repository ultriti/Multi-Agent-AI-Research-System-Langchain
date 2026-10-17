import json

from agents import build_reader_agent, critics_chain, writer_chain
from tools import search_news


def to_text(content) -> str:
    """Gemini can return a list of blocks; flatten to a plain string."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(
            b.get("text", "") if isinstance(b, dict) else str(b) for b in content
        ).strip()
    return str(content)


def run_search_pipeline(topic: str, on_step=None) -> dict:
    # on_step(step_id, status) is optional, used by the API to report progress
    emit = on_step or (lambda step, status: None)
    state = {}

    print("\n" + "=" * 40)
    print("step 1 - searching for sources ...")
    print("\n" + "=" * 40)
    emit("search", "running")

    search_data = search_news(topic)
    state["sources"] = [
        {"title": article["title"], "url": article["url"]}
        for article in search_data["articles"]
        if article["url"]
    ]
    state["search_results"] = json.dumps(search_data, ensure_ascii=False, indent=2)
    print("search results:", state["search_results"])
    emit("search", "done")

    print("\n" + "=" * 40)
    print("step 2 - reader agent is scraping the sources ...")
    print("\n" + "=" * 40)
    emit("read", "running")

    reader_agent = build_reader_agent()
    reader_result = reader_agent.invoke(
        {
            "messages": [
                (
                    "user",
                    f"Based on the following search results about '{topic}', "
                    f"pick the most relevant URL and scrape it for deeper content. "
                    f"Use the URLs exactly as provided.\n\n"
                    f"Search Results:\n{state['search_results'][:3000]}",
                )
            ]
        }
    )
    state["scraped_content"] = to_text(reader_result["messages"][-1].content)
    print("\n\nscraped content:", state["scraped_content"])
    emit("read", "done")

    print("\n" + "=" * 40)
    print("step 3 - writer is drafting the report ...")
    print("\n" + "=" * 40)
    emit("write", "running")

    research_combined = (
        f"SEARCH RESULTS:\n{state['search_results']}\n\n"
        f"DETAILED SCRAPED CONTENT:\n{state['scraped_content']}"
    )
    report = to_text(
        writer_chain.invoke({"topic": topic, "research": research_combined})
    )
    source_list = "\n".join(
        f"- [{source['title'] or source['url']}]({source['url']})"
        for source in state["sources"]
    ) or "- No source URLs were returned by the search provider."
    state["report"] = f"{report.rstrip()}\n\n## Sources\n\n{source_list}"
    print("\n\nFinal Report:\n", state["report"])
    emit("write", "done")

    print("\n" + "=" * 40)
    print("step 4 - critic is reviewing the report ...")
    print("\n" + "=" * 40)
    emit("critic", "running")

    state["feedback"] = to_text(critics_chain.invoke({"report": state["report"]}))
    print("\n\nFeedback report:\n", state["feedback"])
    emit("critic", "done")

    return state


# if __name__ == "__main__":
#     run_search_pipeline("latest news about tesla flying car's ")
