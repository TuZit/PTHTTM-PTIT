"""Unit test node: TC-01 (create_analysts/Pydantic), TC-02 logic (human_feedback),
TC-04 (fallback search_web — regression bug 'NoneType' object has no attribute 'search_query')."""
from types import SimpleNamespace
from unittest import mock

import pytest
from langchain.messages import AIMessage, HumanMessage

import src.utils.nodes as nodes
from src.utils.objects import Analyst, Perspectives
from conftest import make_mock_llm, make_mock_tavily, MOCK_ANALYSTS, MOCK_ANSWER, interview_state  # noqa: F401


class TestCreateAnalysts:  # TC-01 / MT1
    def test_tra_dung_schema_analyst(self, monkeypatch):
        monkeypatch.setattr(nodes, "llm", make_mock_llm())
        out = nodes.create_analysts({"topic": "AI cho SME", "max_analysts": 3})
        assert isinstance(out["analysts"], list) and len(out["analysts"]) == 3
        assert all(isinstance(a, Analyst) for a in out["analysts"])

    def test_prompt_chua_language(self, monkeypatch):
        captured = {}

        def wso(schema, **kw):
            m = mock.MagicMock()
            def _invoke(msgs):
                captured["system"] = msgs[0].content
                return Perspectives(analysts=MOCK_ANALYSTS)
            m.invoke.side_effect = _invoke
            return m

        fake = mock.MagicMock()
        fake.with_structured_output.side_effect = wso
        monkeypatch.setattr(nodes, "llm", fake)
        nodes.create_analysts({"topic": "AI cho SME", "max_analysts": 3})
        assert "Tiếng Việt" in captured["system"]  # TC-08 một phần: directive ngôn ngữ vào prompt


class TestHumanFeedbackLogic:  # TC-02 / MT2
    @pytest.mark.parametrize("feedback,expected", [
        (None, None),
        ("", None),
        ("perfect", None),
        ("continue", None),
        ("APPROVED", None),
        ("yes", None),
        ("them goc nhin CFO", "them goc nhin CFO"),
        (123, None),
    ])
    def test_bang_quyet_dinh_feedback(self, monkeypatch, feedback, expected):
        monkeypatch.setattr(nodes, "interrupt", lambda payload: feedback)
        out = nodes.human_feedback({"topic": "t", "max_analysts": 1, "analysts": MOCK_ANALYSTS})
        assert out == {"human_analyst_feedback": expected}

    def test_interrupt_payload_du_analyst(self, monkeypatch):
        seen = {}
        monkeypatch.setattr(nodes, "interrupt", lambda payload: seen.update(payload) or "continue")
        nodes.human_feedback({"topic": "t", "max_analysts": 1, "analysts": MOCK_ANALYSTS})
        assert len(seen["analysts"]) == 3 and "question" in seen


class TestSearchWebFallback:  # TC-04 / regression BUG-01
    def _patch(self, monkeypatch, structured_ret, plain_ret, results=None):
        s = mock.MagicMock(); s.invoke.return_value = structured_ret
        llm_mock = mock.MagicMock()
        llm_mock.with_structured_output.return_value = s
        llm_mock.invoke.return_value = plain_ret
        tav = make_mock_tavily(results)
        monkeypatch.setattr(nodes, "llm", llm_mock)
        monkeypatch.setattr(nodes, "tavily_search", tav)
        return tav

    def test_khong_crash_khi_structured_tra_None(self, monkeypatch, interview_state):
        tav = self._patch(monkeypatch, None, AIMessage(content="ROI AI agents SME 2025"))
        out = nodes.search_web(interview_state)
        assert tav.invoke.call_args[0][0]["query"] == "ROI AI agents SME 2025"
        assert len(out["context"]) == 1 and "example.com" in out["context"][0]

    def test_structured_None_va_plain_rong_fallback_message_cuoi(self, monkeypatch, interview_state):
        tav = self._patch(monkeypatch, None, AIMessage(content="   "))
        nodes.search_web(interview_state)
        q = tav.invoke.call_args[0][0]["query"]
        assert q == "Chào bạn, tôi là chuyên gia AI."  # tin nhắn cuối không rỗng

    def test_structured_OK(self, monkeypatch, interview_state):
        tav = self._patch(monkeypatch, SimpleNamespace(search_query="q hay"), None)
        nodes.search_web(interview_state)
        assert tav.invoke.call_args[0][0]["query"] == "q hay"

    def test_tavily_tra_rong_khong_crash(self, monkeypatch, interview_state):
        self._patch(monkeypatch, SimpleNamespace(search_query="q"), None, results=[])
        out = nodes.search_web(interview_state)
        assert out == {"context": []}

    def test_doc_thieu_url_bi_loai(self, monkeypatch, interview_state):
        self._patch(monkeypatch, SimpleNamespace(search_query="q"), None,
                    results=[{"content": "khong url"}, {"url": "http://ok", "content": "co url"}])
        out = nodes.search_web(interview_state)
        assert "http://ok" in out["context"][0] and out["context"][0].count("<Document") == 1


class TestWriterNodes:  # TC-05/MT5 một phần (cấu trúc)
    def test_write_section_tra_sections_khong_phai_str(self, monkeypatch, interview_state):
        monkeypatch.setattr(nodes, "llm", make_mock_llm())
        st = dict(interview_state, interview="transcript", context=["doc"])
        out = nodes.write_section(st)
        assert isinstance(out["sections"], list) and out["sections"] == [MOCK_ANSWER]

    def test_finalize_report_gop_du_va_tach_sources(self):
        st = {"topic": "t", "sections": ["s1", "s2"],
              "content": "## Insights\n\nnoi dung\n\n## Sources\n[1] http://x",
              "introduction": "# Tiêu đề\n## Introduction\nGIỚI THIỆU",
              "conclusion": "## Conclusion\nKẾT LUẬN"}
        out = nodes.finalize_report(st)
        fr = out["final_report"]
        assert "GIỚI THIỆU" in fr and "KẾT LUẬN" in fr
        assert "## Sources" in fr and "[1] http://x" in fr
