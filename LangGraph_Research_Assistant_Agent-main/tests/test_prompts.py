"""TC-07 (P0): 6 prompt sinh văn bản format được với language= và chứa chỉ thị ngôn ngữ."""
import pytest

from src.utils import prompts as p
from src.utils.models import output_language


@pytest.mark.parametrize("name,formatted", [
    ("analyst", lambda: p.analyst_instructions.format(topic="t", human_analyst_feedback="", max_analysts=3, language=output_language)),
    ("question", lambda: p.question_instructions.format(goals="g", language=output_language)),
    ("answer", lambda: p.answer_instructions.format(goals="g", context="c", language=output_language)),
    ("section", lambda: p.section_writer_instructions.format(focus="f", language=output_language)),
    ("report", lambda: p.report_writer_instructions.format(topic="t", context="c", language=output_language)),
    ("intro_conclusion", lambda: p.intro_conclusion_instructions.format(topic="t", formatted_str_sections="s", language=output_language)),
])
def test_tc07_prompt_format_khong_loi_va_chi_dinh_ngon_ngu(name, formatted):
    s = formatted()          # KeyError nếu template/nodes lệch placeholder
    assert output_language in s, f"{name} thiếu chỉ thị ngôn ngữ '{output_language}'"


def test_tc07_tat_ca_nodes_truyen_du_language():
    """Mọi chỗ .format() trong nodes.py phải truyền language= (nguồn lỗi KeyError tiềm ẩn)."""
    import inspect
    import src.utils.nodes as nodes

    src_text = inspect.getsource(nodes)
    for fmt_call in ["analyst_instructions.format", "question_instructions.format",
                     "answer_instructions.format", "section_writer_instructions.format",
                     "report_writer_instructions.format", "intro_conclusion_instructions.format"]:
        assert fmt_call in src_text
    # đếm số lời gọi .format(...) có language= phải bằng số chỗ format prompt
    assert src_text.count("language=output_language") == src_text.count("_instructions.format")
