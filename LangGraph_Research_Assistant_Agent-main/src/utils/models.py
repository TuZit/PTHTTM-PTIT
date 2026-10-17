import os

from dotenv import load_dotenv
from langchain_deepseek import ChatDeepSeek

load_dotenv()

# `deepseek-chat` (V3) by default; DEEPSEEK_MODEL=deepseek-reasoner switches to R1.
llm = ChatDeepSeek(model=os.getenv("DEEPSEEK_MODEL", "deepseek-chat"), temperature=0)
