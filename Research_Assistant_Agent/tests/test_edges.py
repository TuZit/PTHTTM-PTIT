"""Unit test cho các edge/routing (mục 4 Thiết kế): should_continue, route_messages,
initiate_all_interviews."""
import pytest
from langchain.messages import AIMessage, HumanMessage

from src.utils.edges import should_continue, route_messages, initiate_all_interviews
from conftest import MOCK_ANALYSTS


class TestShouldContinue:
    def test_perfect_di_dummy(self):
        assert should_continue({"topic": "t", "max_analysts": 1,
                                "human_analyst_feedback": "perfect"}) == "dummy"

    def test_co_gop_y_quay_lai_create_analysts(self):
        assert should_continue({"topic": "t", "max_analysts": 1,
                                "human_analyst_feedback": "them goc nhin phan biem"}) == "create_analysts"

    @pytest.mark.parametrize("state", [
        {"topic": "t", "max_analysts": 1},
        {"topic": "t", "max_analysts": 1, "human_analyst_feedback": None},
    ])
    def test_khong_co_feedback_di_dummy(self, state):
        assert should_continue(state) == "dummy"


class TestRouteMessages:
    def _state(self, msgs, turns=2):
        return {"messages": msgs, "max_num_turns": turns, "analyst": MOCK_ANALYSTS[0],
                "context": [], "interview": "", "sections": []}

    def test_du_max_turns_thi_luu_interview(self):
        msgs = [HumanMessage(content="seed"),
                AIMessage(content="c1"), AIMessage(content="a1", name="expert"),
                AIMessage(content="c2"), AIMessage(content="a2", name="expert")]
        assert route_messages(self._state(msgs, turns=2)) == "save_interview"

    def test_cau_ket_thuc_luu_interview(self):
        msgs = [HumanMessage(content="seed"),
                AIMessage(content="Thank you so much for your help!"),
                AIMessage(content="a1", name="expert")]
        assert route_messages(self._state(msgs, turns=5)) == "save_interview"

    def test_chua_du_thoi_lap_tiep(self):
        msgs = [HumanMessage(content="seed"),
                AIMessage(content="ROI la bao nhieu?"),
                AIMessage(content="a1", name="expert")]
        assert route_messages(self._state(msgs, turns=5)) == "ask_question"


class TestInitiateAllInterviews:
    def test_co_feedback_quay_lai_persona(self):
        out = initiate_all_interviews({"topic": "t", "max_analysts": 2,
                                       "analysts": MOCK_ANALYSTS,
                                       "human_analyst_feedback": "them nguoi phan bien"})
        assert out == "create_analysts"

    def test_khong_feedback_fan_out_send(self):
        """MT3: N analyst → N Send tới conduct_interview, mỗi Send có state riêng."""
        out = initiate_all_interviews({"topic": "AI cho SME", "max_analysts": 3,
                                       "analysts": MOCK_ANALYSTS})
        assert isinstance(out, list) and len(out) == 3
        assert all(s.node == "conduct_interview" for s in out)
        assert all("analyst" in s.arg and "messages" in s.arg for s in out)
