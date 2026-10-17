# User Guide — Trợ lý nghiên cứu đa tác tử (LangGraph + DeepSeek)

Tài liệu hướng dẫn **cài đặt, chạy trong PyCharm và sử dụng agent**. Dành cho bản dự án đã chuyển sang **DeepSeek** (`ChatDeepSeek`, gói `langchain-deepseek`).

> Cấu trúc repo: 3 graph đăng ký trong `langgraph.json` — `create_analysts` (sinh persona), `asnwer_question` (1 phiên phỏng vấn), `deep_agent` (toàn trình: persona → duyệt → phỏng vấn song song → báo cáo).

---

## 1. Chuẩn bị (Prerequisites)

| Yêu cầu | Ghi chú |
| --- | --- |
| Python 3.12+ | Bắt buộc theo `pyproject.toml` |
| [`uv`](https://docs.astral.sh/uv/) | Trình quản lý package & venv |
| PyCharm (Community hoặc Professional) | IDE để chạy/debug |
| **DeepSeek API key** | Lấy tại https://platform.deepseek.com → mục *API Keys* |
| **Tavily API key** | Lấy tại https://app.tavily.com |
| **LangGraph CLI/Studio** | Chạy local qua `langgraph dev`; Studio mở trên trình duyệt |

Kiểm tra nhanh:

```bash
python --version   # cần >= 3.12
uv --version
```

Nếu chưa có `uv`:

```bash
pip install uv
# hoặc trên macOS:
brew install uv
```

---

## 2. Mở dự án trong PyCharm

### 2.1. trỏ PyCharm vào thư mục dự án

`File → Open` → chọn thư mục **`LangGraph_Research_Assistant_Agent-main`**.

### 2.2. Tạo virtualenv bằng `uv` (khuyên dùng)

Mở terminal ngay trong PyCharm (nút **Terminal** ở đáy cửa sổ), đảm bảo đang ở thư mục dự án rồi chạy:

```bash
uv venv --python 3.12
uv sync
```

- `uv venv` tạo thư mục `.venv/`.
- `uv sync` cài toàn bộ phụ thuộc (đã có `langchain-deepseek`).

### 2.3. Chọn Python interpreter của PyCharm vào `.venv`

`PyCharm → Settings (⌘,) → Project: … → Python Interpreter → Add Interpreter → Add Local Interpreter → Select existing`
trỏ tới:

- macOS: `<project>/.venv/bin/python`
- Windows: `<project>\.venv\Scripts\python.exe`

PyCharm sẽ hiển thị `Python 3.12 (…/.venv)` ở góc dưới phải → đã nhận đúng môi trường.

### 2.4. Tạo file `.env`

Ở gốc dự án, tạo file **`.env`** (có sẵn `.env.example` để copy):

```bash
cp .env.example .env   # macOS/Linux
copy .env.example .env # Windows (cmd)
```

Điền key thật:

```env
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxx
DEEPSEEK_MODEL=deepseek-chat
TAVILY_API_KEY=tvly-xxxxxxxxxxxxxxxx
```

> `.env` đã nằm trong `.gitignore` — không lo commit lộ key. `models.py` và `langgraph.json` (`"env": ".env"`) tự nạp file này.

---

## 3. Nạp biến môi trường vào PyCharm

Code đã tự đọc `.env` qua `load_dotenv()`, nên **chạy bằng terminal trong PyCharm thì không cần cấu hình gì thêm**. Nếu bạn muốn chạy/nạp cấu hình Run Configuration của PyCharm (không dùng terminal), chọn 1 trong 2 cách:

**Cách A — Plugin EnvFile (PyCharm Professional):**
`Settings → Plugins → EnvFile` → bật. Mở `Run → Edit Configurations → Environment variables → EnvFile tab` → tick *Enable EnvFile* → thêm đường dẫn file `.env`.

**Cách B — khai báo trực tiếp (mọi bản PyCharm):**
`Run → Edit Configurations → Environment variables` → thêm:
```
DEEPSEEK_API_KEY=sk-…;TAVILY_API_KEY=tvly-…
```

---

## 4. Chạy agent

Có 2 chế độ. **Chế độ 4.1 (LangGraph Studio)** là chính, dùng cho demo/bảo vệ. **Chế độ 4.2 (CLI runner)** để ra file báo cáo nhanh.

### 4.1. Chạy qua LangGraph dev server + Studio (khuyên dùng)

Trong terminal PyCharm:

```bash
uv run langgraph dev
```

Kết quả:
- Server khởi động, in ra **URL Studio** (dạng `https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024`).
- Mở URL đó trên trình duyệt → Studio load 3 graph từ `langgraph.json`.

**Để PyCharm debug được khi chạy `langgraph dev`:** tạo Run Configuration kiểu *Shell Script*, command `uv run langgraph dev`, interpreter = `.venv`. Chạy bằng nút 🐞 Debug nếu muốn breakpoint trong `src/utils/nodes.py`.

### 4.2. Chạy CLI ra file báo cáo (tùy chọn)

`main.py` hiện chỉ là placeholder. Nếu muốn chạy nhanh từ terminal và lưu báo cáo ra Markdown, tạo file **`run_report.py`** ở gốc dự án với nội dung dưới đây rồi chạy `uv run python run_report.py "chủ đề của bạn"`.

<details>
<summary>Bấm để xem <code>run_report.py</code></summary>

```python
"""CLI runner tối thiểu cho graph deep_agent (có xử lý human-in-the-loop)."""
import sys
import uuid

from langgraph.types import Command
from langgraph.checkpoint.memory import MemorySaver

from src.deep_agent import graph  # graph đã compile; ta compile lại với checkpointer ở dưới
from src.utils.states import ResearchGraphState  # noqa: F401 (tham chiếu)

def main():
    topic = sys.argv[1] if len(sys.argv) > 1 else "Impact of AI agents on software teams"
    max_analysts = int(sys.argv[2]) if len(sys.argv) > 2 else 3

    # Bọc lại graph với checkpointer để interrupt/resume hoạt động
    from src.deep_agent import builder
    app = builder.compile(checkpointer=MemorySaver())

    config = {"configurable": {"thread_id": uuid.uuid4().hex}}
    inputs = {"topic": topic, "max_analysts": max_analysts}

    result = app.invoke(inputs, config)

    # Graph dừng ở human_feedback (interrupt) → duyệt persona
    while "__interrupt__" in result:
        intr = result["__interrupt__"][0]
        print("\n=== Analysts được sinh ra ===")
        for a in intr.value.get("analysts", []):
            print(f"- {a.get('name')} | {a.get('role')} | {a.get('affiliation')}")
        fb = input("Gửi feedback để tạo lại (Enter = duyệt & tiếp tục): ").strip()
        result = app.invoke(Command(resume=fb or "continue"), config)

    report = result.get("final_report", "")
    out = "final_report.md"
    with open(out, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"\nĐã lưu báo cáo vào {out} ({len(report)} ký tự).")

if __name__ == "__main__":
    main()
```

</details>

> Lưu ý: trong Studio không cần script này — Studio tự hiển thị điểm `interrupt` và có ô để nhập/approve.

---

## 5. Sử dụng agent (quy trình nghiệp vụ)

### Bước 1 — Nhập chủ đề

Chọn graph `deep_agent` trong Studio, điền input:

```json
{
  "topic": "The business impact of retrieval-augmented generation in enterprise support teams",
  "max_analysts": 3
}
```

| Trường | Ý nghĩa | Gợi ý |
| --- | --- | --- |
| `topic` | Chủ đề nghiên cứu | Càng cụ thể, báo cáo càng sát |
| `max_analysts` | Số analyst tối đa | 2–4 (kiểm soát chi phí; xem mục 7) |

Bấm **Submit**. Graph chạy `create_analysts` (gọi DeepSeek sinh persona theo Pydantic schema).

### Bước 2 — Duyệt persona (Human-in-the-loop)

Graph dừng ở node `human_feedback`, Studio hiện danh sách analyst (tên, vai trò, affiliation, persona). Bạn có 2 lựa chọn:

| Hành động | Cách làm trong Studio | Kết quả |
| --- | --- | --- |
| **Duyệt / approve** | Ở ô resume, nhập `continue` (hoặc để trống) | Chuyển sang phỏng vấn song song |
| **Gửi feedback tạo lại** | Nhập yêu cầu, ví dụ `"thêm một góc nhìn phản biện chính sách"` | Quay lại `create_analysts` với ràng buộc mới |

Điểm dừng này **có chủ đích**: lọc hướng nghiên cứu *trước khi* tốn chi phí API cho các phiên phỏng vấn.

### Bước 3 — Phỏng vấn song song (fan-out)

Sau khi approve, `Send` API fan-out **mỗi analyst một subgraph `answer_question`** chạy đồng thời. Trong mỗi phiên lặp:

```
ask_question → ask_search_question → search_web / search_web2 (Tavily) → answer_question → (lặp tới max_turns) → save_interview → write_section
```

- `answer_question` **chỉ trả lời dựa trên ngữ cảnh Tavily trả về** và giữ URL nguồn (chống hallucination).
- Quan sát từng node thực thi và inspect state theo thời gian thực trong Studio.

### Bước 4 — Nhận báo cáo cuối

Các section được fan-in, rồi graph chạy map-reduce: `write_report` (body) + `write_introduction` + `write_conclusion` → `finalize_report`. Kết quả là trường **`final_report`** — Markdown gồm: mở đầu, nội dung theo section, kết luận, danh mục tài liệu tham khảo (URL khử trùng lặp). Tải/copy từ Studio, hoặc nếu dùng `run_report.py` sẽ lưu ra `final_report.md`.

---

## 6. Dùng riêng từng graph (nâng cao)

| Graph | Khi nào dùng | Input tối thiểu |
| --- | --- | --- |
| `create_analysts` | Chỉ muốn sinh + duyệt persona, không cần báo cáo | `{"topic": "...", "max_analysts": 3}` |
| `asnwer_question` | Test 1 phiên phỏng vấn độc lập cho 1 analyst đã có | state `InterviewState` (analyst + `max_num_turns`) |
| `deep_agent` | Toàn trình topic → báo cáo | `{"topic": "...", "max_analysts": 3}` |

---

## 7. Đổi mô hình & kiểm soát chi phí

### Đổi DeepSeek model

Sửa `DEEPSEEK_MODEL` trong `.env` (không cần đụng code):

| Giá trị | Mô hình | Khi dùng |
| --- | --- | --- |
| `deepseek-chat` | DeepSeek-V3 | Mặc định, nhanh, rẻ — hợp cho demo |
| `deepseek-reasoner` | DeepSeek-R1 | Lập luận sâu hơn, chậm/đắt hơn |

> Nếu `deepseek-reasoner` không tương thích `with_structured_output` ở một số node, chuyển về `deepseek-chat`. Đây cũng là **phương án dự phòng chi phí** đã ghi trong Action Plan: giữ node phụ chạy `deepseek-chat`, chỉ bật `deepseek-reasoner` cho node quan trọng.

### Giảm chi phí khi test

- Hạ `max_analysts` (2–3) và `max_turns` thấp.
- Thử trước bằng graph `create_analysts` (chỉ tốn vài lời gọi persona).
- Bật cache kết quả search theo query (đang ở mục cải tiến).

---

## 8. Khắc phục lỗi thường gặp

| Hiện tượng | Nguyên nhân | Cách xử lý |
| --- | --- | --- |
| `Did not find deepseek_api_key` / lỗi auth 401 | Thiếu/sai `DEEPSEEK_API_KEY` | Kiểm tra `.env`, đảm bảo chạy trong đúng thư mục dự án |
| `Did not find tavily_api_key` | Thiếu `TAVILY_API_KEY` | Thêm vào `.env` |
| `ModuleNotFoundError: No module named 'src'` | chưa bật venv / interpreter | Chọn interpreter `.venv` (mục 2.3) và `uv run …` |
| `uv run langgraph dev` báo thiếu gói | chưa `uv sync` | Chạy `uv sync` |
| Chạy trong PyCharm không đọc được `.env` | EnvFile/ENV chưa cấu hình | Dùng terminal PyCharm (mục 3) hoặc plugin EnvFile |
| Graph không dừng ở `human_feedback` | đang chạy bản không checkpointer | Dùng Studio hoặc `run_report.py` (đã compile checkpointer) |
| `langgraph-cli ... extra named inemem` (warning) | typo `inemem` trong `pyproject.toml` | Cảnh báo vô hại; có thể sửa `langgraph-cli[inmem]` |
| Persona/câu trả lời lệch schema | lệch khuôn structured output | Tăng `temperature`? không — siết prompt; thử `deepseek-chat` |

---

## 9. Mẹo khi demo / bảo vệ

- Chạy sẵn `uv run langgraph dev` trước buổi demo; mở Studio ở tab riêng, input mẫu đã chuẩn bị.
- Tại `human_feedback`, chủ động **gửi feedback** ("thêm góc nhìn quốc tế") để minh họa vòng lặp tạo lại — đây là điểm ăn hình nhất của HITL.
- Chỉ vào **URL nguồn** trong `final_report` để chứng minh grounding.
- Nếu API chậm/không ổn định lúc demo: chuẩn bị sẵn 1 file báo cáo mẫu (ảnh chụp Studio) làm phương án dự phòng.

---

## 10. Tệp & thư mục liên quan

| Đường dẫn | Vai trò |
| --- | --- |
| `src/utils/models.py` | Khởi tạo `ChatDeepSeek` (đọc `DEEPSEEK_API_KEY`, `DEEPSEEK_MODEL`) |
| `src/utils/nodes.py` | Node: sinh persona, hỏi, tìm, trả lời, viết section/report |
| `src/utils/tools.py` | Node tìm kiếm Tavily |
| `src/deep_agent.py` | Graph toàn trình |
| `src/agent.py` / `src/answering_questions.py` | Graph persona & subgraph phỏng vấn |
| `.env.example` | Mẫu khai báo key |
| `langgraph.json` | Đăng ký 3 graph + nạp `.env` |
