from dotenv import load_dotenv
import tavily

from typing import List
from pydantic import BaseModel, Field

load_dotenv()
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

from langchain_tavily import TavilySearch

class TavilyQueryInput(BaseModel):
    query: str = Field(description="Search query to look up")

search_tool = TavilySearch(
    max_results=5,
    include_domains=["linkedin.com"],  # baked in, not a tool arg
    args_schema=TavilyQueryInput,
)

class Source(BaseModel):
    """
    Schema for the  source used by the agent
    """
    url: str = Field(description="The URL of the source")

class AgentResponse(BaseModel):
    """
    Schema for agent Responses with answers and sources
    """

    answer: str = Field(description="The agent's answer to the query")
    sources: List[Source] = Field(
        default_factory=List,
        description="List of sources used to generate an answer"
    )


# from tavily import TavilyClient

# tavily = TavilyClient()

# @tool
# def search(query: str) -> str:
#     """
#     Tool that searches over internet
#     Args:
#         query: The query to search for 
#     Returns:
#         The search result
#     """
#     print(f"Searching for {query}")
#     #return "Tokyo Weather Is Sunny"
#     return tavily.search(query = query)

# llm = ChatOpenAI()
# tools=[search]
# agent = create_agent(model=llm, tools=tools)

llm = ChatOpenAI(model = "gpt-5")
tools = [search_tool]
agent = create_agent(model = llm, tools=tools, response_format=AgentResponse,
system_prompt=(
        "You are a research assistant. Use tavily_search at most 3 times total. "
        "If you cannot find enough results after 3 searches, answer with what you found "
        "and clearly state the limitation instead of searching again."
    ))

def main():
    print("Hello")
    result = agent.invoke({"messages":HumanMessage(content = "search for 3 job postings for an ai engineer using langchain in the bay area on Naukri/Indeed and list their details?")})
    print(result)




if __name__ == "__main__":
    main()