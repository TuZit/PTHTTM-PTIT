import os

from dotenv import load_dotenv
from langchain_deepseek import ChatDeepSeek

load_dotenv()

# `deepseek-chat` (V3) by default; DEEPSEEK_MODEL=deepseek-reasoner switches to R1.
llm = ChatDeepSeek(model=os.getenv("DEEPSEEK_MODEL", "deepseek-chat"), temperature=0)

# Language the agent writes analyst personas, interviews and report sections in.
# Prompts are English, so without this the output drifts to English/mixed even for
# a Vietnamese topic. Change via REPORT_LANGUAGE in .env (e.g. "English").
output_language = os.getenv("REPORT_LANGUAGE", "Tiếng Việt")
