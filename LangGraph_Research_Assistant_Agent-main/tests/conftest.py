"""Cấu hình môi trường test: chạy OFFLINE, không gọi API thật.

Đặt env key GIẢ trước khi bất kỳ module nào của src được import,
vì `models.py` khởi tạo ChatDeepSeek và `nodes.py` khởi tạo TavilySearch
ngay lúc import (chúng đòi key tồn tại, nhưng test sẽ mock mọi lời gọi).
"""
import os

from dotenv import load_dotenv

# Nạp .env THẬT trước (cho test -m live); key giả chỉ là chốt dự phòng
# để import models.py/nodes.py không sập khi chạy offline CI.
load_dotenv()
os.environ.setdefault("DEEPSEEK_API_KEY", "sk-test-offline")
os.environ.setdefault("DEEPSEEK_MODEL", "deepseek-chat")
os.environ.setdefault("TAVILY_API_KEY", "tvly-test-offline")

import pytest
from unittest import mock
from types import SimpleNamespace

from langchain.messages import AIMessage, HumanMessage
from src.utils.objects import Analyst, Perspectives

# Nội dung "LLM" trả về khi mock — có Both heading để test finalize_report tách sources
MOCK_ANSWER = (
    "## Insights\n\n"
    "Nội dung trả lời tiếng Việt giả lập. [1]\n\n"
    "## Sources\n"
    "[1] https://example.com/1"
)

MOCK_ANALYSTS = [
    Analyst(name="Nguyễn A", role="Chuyên gia AI", affiliation="VNG",
            description="tập trung chi phí triển khai"),
    Analyst(name="Trần B", role="Nhà phản biện chính sách", affiliation="Viện X",
            description="lo ngại rủi ro pháp lý"),
    Analyst(name="Lê C", role="CFO", affiliation="Quỹ Y",
            description="đánh giá ROI"),
]


def make_mock_llm(analysts=None):
    """LLM giả: with_structured_output trả đúng schema theo yêu cầu,
    invoke thường trả AIMessage tiếng Việt."""
    perspectives = Perspectives(analysts=analysts if analysts is not None else list(MOCK_ANALYSTS))

    def _with_structured(schema, **kwargs):
        m = mock.MagicMock()
        if schema is Perspectives:
            m.invoke.return_value = perspectives
        else:  # SearchQuery
            m.invoke.return_value = SimpleNamespace(search_query="truy van mock")
        return m

    llm_mock = mock.MagicMock()
    llm_mock.with_structured_output.side_effect = _with_structured
    llm_mock.invoke.side_effect = lambda msgs: AIMessage(content=MOCK_ANSWER)
    return llm_mock


def make_mock_tavily(results=None):
    tav = mock.MagicMock()
    tav.invoke.return_value = {
        "results": results if results is not None else [{"url": "https://example.com/1", "content": "tai lieu mock"}]
    }
    return tav


@pytest.fixture()
def interview_state():
    return {
        "messages": [
            HumanMessage(content="So you said you were writing an article on AI agents for SMEs?"),
            AIMessage(content="Chào bạn, tôi là chuyên gia AI."),
        ],
        "analyst": MOCK_ANALYSTS[0],
        "max_num_turns": 2,
        "context": [],
        "interview": "",
        "sections": [],
    }
