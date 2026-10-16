from agents import build_reader_agent, build_search_agent, writer_chain, critics_chain


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

    # step 1 -----------------------
    print("\n" + "=" * 40)
    print("step 1 - search agent is working ...")
    print("\n" + "=" * 40)
    emit("search", "running")

    search_agent = build_search_agent()
    search_result = search_agent.invoke(
        {"messages": [("user", f"Find the recent, reliable and detailed information about : {topic}")]}
    )
    state["search_results"] = to_text(search_result["messages"][-1].content)

    print("\n" + "=" * 40)
    print("search result :", state["search_results"])
    emit("search", "done")

    # step 2 ---------------
    print("\n" + "=" * 40)
    print("step 2 - Reader agent is scrapping the resoures ...")
    print("\n" + "=" * 40)
    emit("read", "running")

    reader_agent = build_reader_agent()
    reader_result = reader_agent.invoke(
        {
            "messages": [
                (
                    "user",
                    f"Based on the following search results about '{topic}', "
                    f"pick the most relevant URL and scrape it for deeper content.\n\n"
                    f"Search Results:\n{state['search_results'][:3000]}",
                )
            ]
        }
    )
    state["scraped_content"] = to_text(reader_result["messages"][-1].content)

    print("\n\nscrapped content : ", state["scraped_content"])
    emit("read", "done")

    # step 3 --------------------------
    print("\n" + "=" * 40)
    print("step 3 - writer is drafting the report ...")
    print("\n" + "=" * 40)
    emit("write", "running")

    research_combined = (
        f"SEARCH RESULTS :\n {state['search_results']} \n\n"
        f"DETAILED SCRAPPED CONTENT : \n {state['scraped_content']}"
    )

    state["report"] = to_text(
        writer_chain.invoke({"topic": topic, "research": research_combined})
    )

    print("\n\nFinal Report : \n", state["report"])
    emit("write", "done")

    # step 4 ------------------------
    print("\n" + "=" * 40)
    print("step 4 - Cretic is revewing the report ...")
    print("\n" + "=" * 40)
    emit("critic", "running")

    state["feedback"] = to_text(critics_chain.invoke({"report": state["report"]}))

    print("\n\nfeedback Report : \n", state["feedback"])
    emit("critic", "done")

    return state