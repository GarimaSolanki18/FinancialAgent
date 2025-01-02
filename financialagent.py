from phi.agent import Agent
from phi.model.groq import Groq
from phi.model.openai import OpenAIChat
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo
import os
import openai
from dotenv import load_dotenv
load_dotenv()
openai_api_key="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"

import openai
openai.api_key = openai_api_key
os.environ["OPENAI_API_KEY"] = openai_api_key

#Build Agents

web_search_agent=Agent(
    name="Web Search Agent",
    role="Search the internet for information",
    model=Groq(id="llama3-groq-70b-8192-tool-use-preview"),
    tools=[DuckDuckGo()],
    instructions=['Always include sources'],
    show_tools_calls=True,
    markdown=True

)

finance_agent=Agent(
    name="Financial Agent",
    role="Get the financial information",
    model=Groq(id="llama3-groq-70b-8192-tool-use-preview"),
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, stock_fundamentals=True)],
    instructions=['Use tables to display data'],
    show_tools_calls=True,
    markdown=True

)

multi_ai_agent=Agent(
    team=[web_search_agent,finance_agent],
    instructions=['Always include sources','Use tables to display data'],
    show_tools_calls=True,
    markdown=True
)

multi_ai_agent.print_response("Summarize analyst recommendation and share the news of NVDA",stream=True)