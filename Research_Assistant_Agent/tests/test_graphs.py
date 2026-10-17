"""Integration/e2e test cho 2 graph với LLM + Tavily MOCK (chạy offline).

- TC-02: graph `create_analysts` dừng đúng interrupt + resume đúng nhánh (MT2).
- TC-06 + TC-03: `deep_agent` end-to-end: HITL → fan-out Send N analyst → fan-in
  sections → final_report đủ 4 phần + sources (MT3, MT5).

Nếu muốn chạy bằng API THẬT (như mục 3.3 biên bản): mark `live`
    uv run pytest -m live
"""
import pytest
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command

import src.utils.nodes as nodes
from conftest import make_mock_llm, make_mock_tavily


@pytest.fixture()
def agent_app(monkeypatch):
    monkeypatch.setattr(nodes, "llm", make_mock_llm())
    from src.agent import builder
    # compile lại với checkpointer để interrupt()/resume hoạt động
    return builder.compile(checkpointer=MemorySaver())


@pytest.fixture()
def deep_app(monkeypatch):
    monkeypatch.setattr(nodes, "llm", make_mock_llm())
    monkeypatch.setattr(nodes, "tavily_search", make_mock_tavily())
    from src.deep_agent import builder
    return builder.compile(checkpointer=MemorySaver())


class TestGraph1HITL:  # TC-02 / MT2
    def test_dung_dung_interrupt_va_resume_dung_nhanh(self, agent_app):
        cfg = {"configurable": {"thread_id": "tc02"}}
        r1 = agent_app.invoke({"topic": "AI cho SME", "max_analysts": 3}, cfg)

        # Dừng ở human_feedback (interrupt_before) — graph chưa thoát, chờ người
        assert "__interrupt__" in r1
        assert len(r1["analysts"]) == 3

        # Node chạy -> interrupt() bên trong node dừng lần nữa kèm payload danh sách analyst
        r2 = agent_app.invoke(None, cfg)
        assert "__interrupt__" in r2
        payload = r2["__interrupt__"][0].value
        assert payload["question"] == "Are these analysts okay?"
        assert len(payload["analysts"]) == 3

        # Gõ "perfect" -> human_feedback trả None -> should_continue -> dummy -> END
        r3 = agent_app.invoke(Command(resume="perfect"), cfg)
        assert "__interrupt__" not in r3
        assert r3.get("human_analyst_feedback") is None

    def test_feedback_khac_tao_lai_persona(self, agent_app):
        """Feedback không phải từ khóa duyệt -> quay lại create_analysts (vòng lặp HITL)."""
        cfg = {"configurable": {"thread_id": "tc02b"}}
        agent_app.invoke({"topic": "AI cho SME", "max_analysts": 3}, cfg)
        agent_app.invoke(None, cfg)  # tới lượt interrupt() trong node
        r = agent_app.invoke(Command(resume="thêm góc nhìn CFO"), cfg)
        # create_analysts mock luôn trả 3 analyst; quan trọng: graph pause lại ở HITL
        # (vòng lặp persona lần 2) chứ KHÔNG đi tới dummy/END.
        assert "__interrupt__" in r


class TestDeepAgentE2E:  # TC-06 + TC-03 / MT3, MT5
    def test_toan_trinh_voi_mock(self, deep_app):
        cfg = {"configurable": {"thread_id": "tc06"}}
        r1 = deep_app.invoke({"topic": "AI agent cho SME Việt Nam", "max_analysts": 3}, cfg)

        # 1) HITL pause
        assert "__interrupt__" in r1, "graph phải dừng ở human_feedback"

        # 2) Duyệt -> fan-out 3 analyst qua Send -> subgraph -> writers -> finalize
        final = deep_app.invoke(Command(resume="continue"), cfg)

        # MT3: fan-in đủ section cho từng analyst (reducer operator.add)
        assert len(final["sections"]) == 3, (
            f"kỳ vọng 3 section từ 3 analyst, nhận {len(final['sections'])}")

        # MT5: final_report đủ mở đầu / nội dung / kết luận / nguồn
        fr = final["final_report"]
        assert isinstance(fr, str) and len(fr) > 100
        assert "---" in fr                      # các phần được ghép bằng divider
        assert "## Sources" in fr               # mục nguồn (mock có trả về)
        assert "http://x" not in fr or "example.com" in fr

    def test_subgraph_interview_doc_lap(self, deep_app):
        """Graph 2 (interview_builder) chạy độc lập 1 phiên: hỏi→search→đáp→section."""
        from src.answering_questions import interview_builder
        from langchain.messages import HumanMessage
        app = interview_builder.compile()
        out = app.invoke({
            "analyst": {"name": "A", "role": "R", "affiliation": "F", "description": "ROI"},
            "max_num_turns": 1,
            "context": [],
            "sections": [],
            "messages": [HumanMessage(content="Bạn đang viết bài về AI agent?")],
        })
        assert out["interview"]                      # transcript đã lưu
        assert len(out["sections"]) == 1             # 1 section cho 1 phiên
        assert "example.com" in out["context"][0]    # context từ (mock) Tavily


@pytest.mark.live
def test_deep_agent_e2e_api_that():
    """Chạy bằng DeepSeek + Tavily THẬT (như biên bản 3.3). Cần .env key hợp lệ."""
    from src.deep_agent import graph as _  # noqa: F401  (env must load OK)
    from src.deep_agent import builder
    import uuid
    app = builder.compile(checkpointer=MemorySaver())
    cfg = {"configurable": {"thread_id": uuid.uuid4().hex}}
    r1 = app.invoke({"topic": "AI agent cho doanh nghiệp SME Việt Nam", "max_analysts": 1}, cfg)
    assert "__interrupt__" in r1
    final = app.invoke(Command(resume="continue"), cfg)
    assert len(final["final_report"]) > 500
