"""
Giao diện Gradio thân thiện cho graph `deep_agent` (thay cho việc nhập JSON trong Studio).

Chạy local/demo:
    uv run python gradio_app.py
rồi mở http://127.0.0.1:7860

Luồng:
  1) Nhập chủ đề + số analyst -> bấm "Sinh analyst".
  2) Graph dừng ở human_feedback (interrupt) -> hiển thị danh sách analyst.
     Gõ "continue" để duyệt, hoặc nhập góp ý để tạo lại -> bấm "Duyệt / Tạo lại".
  3) Khi xong -> hiển thị báo cáo Markdown + nút tải file.

Graph có interrupt nên dùng mô hình 2-lần-gọi: invoke -> paused -> resume(Command).
Local/demo nên checkpointer in-memory (MemorySaver) là đủ; không bền qua restart server.
"""

from __future__ import annotations

import os
import uuid

import gradio as gr
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command

from src.deep_agent import builder

# Compile graph với checkpointer in-memory để interrupt/resume hoạt động.
app = builder.compile(checkpointer=MemorySaver())

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))


def _render_analysts(analysts: list) -> str:
    """Chuyển danh sách analyst (dict) thành Markdown để người dùng dễ đọc."""
    if not analysts:
        return "_Không có analyst nào được sinh ra._"
    lines = []
    for i, a in enumerate(analysts, 1):
        name = a.get("name", "?") if isinstance(a, dict) else getattr(a, "name", "?")
        role = a.get("role", "") if isinstance(a, dict) else getattr(a, "role", "")
        aff = a.get("affiliation", "") if isinstance(a, dict) else getattr(a, "affiliation", "")
        desc = a.get("description", "") if isinstance(a, dict) else getattr(a, "description", "")
        lines.append(f"**{i}. {name}** — {role}  \n_{aff}_  \n{desc}\n")
    return "\n\n".join(lines)


def _report_path(topic: str) -> str:
    safe = "".join(c if c.isalnum() else "_" for c in topic)[:40] or "report"
    return os.path.join(OUTPUT_DIR, f"report_{safe}.md")


def run_step(thread_id, topic, max_analysts, feedback):
    """Một lần bấm = một bước của graph (bắt đầu HOẶC resume). Trả về (thread_id, analyst_md, report_md, status_md)."""
    try:
        if not thread_id:  # lần đầu: sinh analyst
            thread_id = uuid.uuid4().hex
            payload = {"topic": topic, "max_analysts": int(max_analysts)}
        else:  # đã có thread: resume bằng phản hồi của người dùng
            fb = (feedback or "").strip() or "continue"
            payload = Command(resume=fb)

        config = {"configurable": {"thread_id": thread_id}}
        result = app.invoke(payload, config)

        # Graph đang chờ người duyệt (interrupt)
        if isinstance(result, dict) and "__interrupt__" in result:
            intr = result["__interrupt__"][0]
            analysts = intr.value.get("analysts", []) if hasattr(intr, "value") else []
            analyst_md = _render_analysts(analysts)
            status = (
                "⏸️ **Đang chờ bạn duyệt.**  \n"
                "Gõ `continue` để **duyệt & chạy tiếp**, hoặc nhập **góp ý** (VD: *thêm góc nhìn phản biện*) "
                "rồi bấm **Duyệt / Tạo lại**."
            )
            return thread_id, analyst_md, "", status

        # Chạy tới END: có báo cáo cuối
        report = result.get("final_report", "") if isinstance(result, dict) else ""
        if report:
            path = _report_path(topic or "report")
            with open(path, "w", encoding="utf-8") as f:
                f.write(report)
            status = f"✅ **Hoàn tất.** Đã lưu vào `report_*.md` (bấm tab **Tải xuống**)."
            return thread_id, _render_analysts(result.get("analysts", [])), report, status

        return thread_id, "", "", "⚠️ Graph kết thúc mà không có `final_report`."

    except Exception as e:  # hiển thị lỗi ngay trên UI thay vì sập
        return thread_id, "", "", f"❌ **Lỗi:** `{type(e).__name__}` — {e}"


def reset(thread_id):
    """Bắt đầu một phiên nghiên cứu mới (thread mới; giữ lại các file .md đã lưu)."""
    return None, "", "", "", "🆕 Sẵn sàng. Nhập chủ đề rồi bấm **Sinh analyst**."


def make_demo_ui():
    with gr.Blocks(title="Trợ lý nghiên cứu (LangGraph + DeepSeek)") as demo:
        gr.Markdown("# 🔬 Trợ lý nghiên cứu đa tác tử\n"
                    "Nhập chủ đề → duyệt danh sách analyst → nhận báo cáo Markdown.")

        thread_state = gr.State(None)

        with gr.Row():
            topic = gr.Textbox(label="Chủ đề nghiên cứu", scale=4,
                               placeholder="AI agent cho doanh nghiệp vừa và nhỏ 2026")
            max_analysts = gr.Number(label="Số analyst", value=2, precision=0, scale=1)

        status = gr.Markdown("🆕 Sẵn sàng. Nhập chủ đề rồi bấm **Sinh analyst**.")

        with gr.Row():
            run_btn = gr.Button("Sinh analyst", variant="primary")
            reset_btn = gr.Button("Bắt đầu lại", variant="secondary")

        with gr.Column():
            gr.Markdown("### 👥 Analyst được đề xuất")
            analyst_md = gr.Markdown("")
            feedback = gr.Textbox(
                label="Phản hồi (gõ `continue` để duyệt, hoặc nhập góp ý để tạo lại)",
                placeholder="continue",
            )
            resume_btn = gr.Button("Duyệt / Tạo lại", variant="primary")

        with gr.Tabs():
            with gr.Tab("📄 Báo cáo"):
                report_md = gr.Markdown("_Báo cáo sẽ hiển thị ở đây sau khi hoàn tất._")
            with gr.Tab("⬇️ Tải xuống"):
                download = gr.File(label="Tải file báo cáo", interactive=False)

        inputs = [thread_state, topic, max_analysts, feedback]
        outputs = [thread_state, analyst_md, report_md, status]

        # "Sinh analyst" bỏ qua feedback (lần đầu), "Duyệt/Tạo lại" dùng feedback
        run_btn.click(
            fn=lambda t, top, n: run_step(t, top, n, ""),
            inputs=[thread_state, topic, max_analysts],
            outputs=outputs,
        )
        resume_btn.click(
            fn=lambda t, top, n, fb: run_step(t, top, n, fb),
            inputs=inputs,
            outputs=outputs,
        )
        # Sau khi có báo cáo -> cập nhật nút tải (tìm file .md mới nhất)
        def latest_file(*_):
            files = [f for f in os.listdir(OUTPUT_DIR) if f.startswith("report_") and f.endswith(".md")]
            if not files:
                return None
            newest = max((os.path.join(OUTPUT_DIR, f) for f in files), key=os.path.getmtime)
            return newest

        all_btns = [run_btn, resume_btn]
        for b in all_btns:
            b.click(fn=latest_file, inputs=None, outputs=[download], queue=False)

        reset_btn.click(
            fn=reset,
            inputs=[thread_state],
            outputs=[thread_state, analyst_md, report_md, status],
        )

    return demo


if __name__ == "__main__":
    demo = make_demo_ui()
    demo.launch(share=False)  # local/demo; đổi share=True nếu cần link tạm công khai
