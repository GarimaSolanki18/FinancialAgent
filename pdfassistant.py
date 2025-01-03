import typer
from typing import Optional,List
from phi.assistant import assistant
from phi.storage.assistant.postgres import PgAssistantStorage
from phi.knowledge.pdf import PDFUrlKnowledgeBase
from phi.vectordb.pgvector import PgVector2

import os
from dotenv import load_dotenv
load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
print(os.environ["GROQ_API_KEY"])

db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai" # Check port of docker that is running

knowledge_base = PDFUrlKnowledgeBase(
    urls=["https://phi-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"],
    vector_db=PgVector2(collection="recipes", db_url=db_url),
)

knowledge_base.load()

storage=PgAssistantStorage(table_name="pdf_assistant",db_url=db_url)


def pdf_assistant(new: bool=False, user: str = "user"):
    run_id: Optional[str]=None

    if not new:
        existing_run_ids: List[str]=storage.get_all_run_ids(user)
        if len(existing_run_ids)>0:
            run_id=existing_run_ids[0]

    assistant = assistant(
    run_id=run_id,
    user_id=user,
    knowledge_base=knowledge_base,
    storage=storage,
    # Add a tool to read chat history.
    read_chat_history=True,
    show_tool_calls=True,
    markdown=True,
    # debug_mode=True,
)
    
    if run_id is None:
      run_id=assistant.run_id
      print(f"Started Run: {run_id}\n")
    else:
      print(f"Continuing Run: {run_id}\n")
assistant.cli_app(markdown=True)