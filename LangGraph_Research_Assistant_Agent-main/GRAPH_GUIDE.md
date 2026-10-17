# GUIDE — Graph là gì & cách dùng 3 loại Graph trong dự án này

> Tài liệu giải thích **mô hình hoạt động** của code (graph/node/edge/state) và **cách chạy từng graph**.
> Đi kèm với `USER_GUIDE.md` (cái đó lo cài đặt + chạy PyCharm, còn file này lo *hiểu kiến trúc*).

---

## Phần 1 — Graph là gì? (giải thích từ số 0)

### 1.1. Thay vì nghĩ "một chuỗi lệnh", hãy nghĩ "một sơ đồ quy trình"

Cách lập trình thông thường (gọi là *script*):

```python
ket_qua = buoc_1()
ket_qua = buoc_2(ket_qua)
ket_qua = buoc_3(ket_qua)
```

Nó chạy **một chiều, cứng từ trên xuống**. Nhưng với agent thì có nhiều thứ "không thẳng hàng":

- Đôi khi phải **quay lại** bước trước (con người chê danh sách analyst → sinh lại).
- Đôi khi phải **chạy song song** (5 analyst cùng phỏng vấn một lúc).
- Đôi khi phải **dừng lại chờ người bấm duyệt** giữa chừng.

Viết mấy luồng đó bằng `if/for` lồng nhau sẽ rất rối. **LangGraph** cho ta cách vẽ nó thành **đồ thị (graph)**: các ô (node) nối nhau bằng mũi tên (edge), và có một "bảng thông tin chung" (state) mà các ô cùng đọc/ghi.

### 1.2. 3 khái niệm cốt lõi

Hãy tưởng tượng một **dây chuyền nhà máy**:

| Khái niệm LangGraph | Ẩn dụ nhà máy | Trong code |
| --- | --- | --- |
| **State** | Tấm bảng kẹp giấy đi cùng dây chuyền, ghi lại mọi thứ đã làm được | một `TypedDict` / `MessagesState` (xem `src/utils/states.py`) |
| **Node** | Một trạm công nhân: nhận tấm bảng, làm việc, viết thêm vào tấm bảng | một **hàm** nhận `state`, `return` một dict các key muốn cập nhật (`src/utils/nodes.py`) |
| **Edge** | Băng chuyền nối trạm này sang trạm khác | `add_edge` / `add_conditional_edges` (`src/utils/edges.py`) |

Và có **2 trạm đặc biệt** luôn tồn tại: `START` (điểm vào) và `END` (điểm ra).

### 1.3. Cycle sống của một graph

```
        ┌──────────────────────────────────────────────┐
        │                  STATE (bảng chung)           │
        │  topic, analysts, sections, final_report ...  │
        └───────▲───────────────────────────▲──────────┘
                │ đọc/ghi                    │ đọc/ghi
          ┌─────┴─────┐   edge   ┌──────────┴─┐
   START ▶│   Node A  │──────── ▶│   Node B   │▶ ... ▶ END
          └───────────┘          └────────────┘
```

1. Bạn **invoke** graph với một state ban đầu (ví dụ `{"topic": "AI", "max_analysts": 3}`).
2. Graph chạy node đầu, node đó **đọc** state, làm việc (gọi LLM, search web...), rồi **trả về phần state cần đổi**.
3. LangGraph **gộp** (merge) phần trả về vào state chung, rồi đi tiếp theo mũi tên edge.
4. Lặp lại cho tới khi tới `END`, hoặc **dừng giữa chừng (interrupt)** chờ người.

### 1.4. Vài chi tiết kỹ thuật hay gây khó hiểu

**(a) Node chỉ trả về *phần thay đổi*, không trả về toàn bộ state.**

```python
def create_analysts(state):
    ...
    return {"analysts": analysts.analysts}   # chỉ cập nhật key "analysts"
```

**(b) Reducer — khi nhiều node/luồng cùng ghi một key.**
Mặc định ghi key sẽ **ghi đè**. Nhưng nếu khai báo:

```python
sections: Annotated[list, operator.add]   # trong states.py
```

thì mỗi lần ghi sẽ **nối thêm** (append) thay vì đè. Đây là cách `deep_agent` gom được section từ 5 analyst chạy song song mà không cái nào đè cái nào. Key `context` và `sections` dùng cơ chế này.

**(c) Key tùy chọn.** `NotRequired[Optional[str]]` nghĩa là key đó **không bắt buộc có ngay từ đầu** (ví dụ `human_analyst_feedback` — lúc mới chạy chưa có phản hồi của người).

**(d) `START` và `END`** không phải node bạn viết, mà là hai "cổng" có sẵn của LangGraph.

---

## Phần 2 — 3 loại Graph trong dự án

`langgraph.json` đăng ký đúng **3 graph**:

```json
"create_analysts":    "./src/agent.py:graph",
"asnwer_question":    "./src/answering_questions.py:question_answer_graph",
"deep_agent":         "./src/deep_agent.py:graph"
```

Mối quan hệ giữa chúng:

```
┌───────────────────── deep_agent (graph "full") ─────────────────────┐
│                                                                      │
│   create_analysts ──▶ human_feedback ──▶ [phỏng vấn song song] ──▶   │
│   (logic từ graph   (human-in-the-       ▲                          │
│    "create_analysts")  loop)              │                          │
│                                        interview_builder (= graph   │
│                                          "asnwer_question", chạy     │
│                                          cho TỪNG analyst)          │
│                                                                      │
│   ──▶ write_report / write_introduction / write_conclusion ──▶       │
│        finalize_report ──▶ END                                       │
└──────────────────────────────────────────────────────────────────────┘
```

Nói ngắn:
- **Graph 1** = chỉ tạo + duyệt danh sách analyst.
- **Graph 2** = chỉ chạy 1 phiên phỏng vấn (hỏi↔đáp + search) cho 1 analyst.
- **Graph 3** = ghép cả quy trình lớn; nó *dùng lại* logic của Graph 1 và *nhúng* Graph 2 làm subgraph cho từng analyst.

---

### Graph 1 — `create_analysts`  (file `src/agent.py`)

**Mục đích:** sinh ra danh sách "chuyên gia phân tích" (analyst persona) cho 1 chủ đề, và **cho phép người duyệt/chê** trước khi chốt.

**State dùng:** `GenerateAnalystsState`

```python
topic: str                 # chủ đề nghiên cứu
max_analysts: int          # muốn mấy analyst
human_analyst_feedback: ...# phản hồi của người (tùy chọn)
analysts: [Analyst]        # kết quả: danh sách analyst
```

**Sơ đồ luồng:**

```
START ─▶ create_analysts ─▶ human_feedback ─(should_continue)─┬─▶ create_analysts  (quay lại sinh lại)
 (node)         (node)          (conditional edge)           │
                                                             └─▶ dummy ─▶ END
```

- `create_analysts`: gọi LLM (kèm prompt + ép kiểu bằng Pydantic `Perspectives`) → trả về `{"analysts": [...]}`.
- `human_feedback`: **dừng graph** bằng `interrupt(...)` để hiện danh sách analyst cho người xem. Người gõ:
  - `"perfect"` / `"continue"` / rỗng → **duyệt**, đi tiếp.
  - một câu góp ý khác → **chê**, edge `should_continue` đưa về `create_analysts` sinh lại (vòng lặp).
- `dummy`: node "rỗng" (no-op) chỉ để nối tới `END`.

**Điểm đặc biệt:** `graph = builder.compile(interrupt_before=['human_feedback'])`
→ graph **tự động pause** ngay trước `human_feedback`, đây là cơ chế *human-in-the-loop*.

**Chạy thử (Python):**

```python
from src.agent import graph
from langgraph.checkpoint.memory import MemorySaver

# cần checkpointer để interrupt/resume hoạt động
graph = builder.compile(checkpointer=MemorySaver())  # (trong code thật đã compile sẵn)

config = {"configurable": {"thread_id": "nghiencuu-1"}}
result = graph.invoke(
    {"topic": "AI agent cho doanh nghiệp vừa và nhỏ", "max_analysts": 3},
    config,
)
# lần invoke đầu sẽ DỪNG ở human_feedback -> kiểm tra result["__interrupt__"]
# rồi gửi phản hồi:
result = graph.invoke(Command(resume="perfect"), config)
```

---

### Graph 2 — `asnwer_question` / interview  (file `src/answering_questions.py`)

**Mục đích:** mô phỏng **một phiên phỏng vấn** với MỘT analyst: đặt câu hỏi → search web lấy ngữ cảnh → trả lời → lặp lại đủ số lượt → lưu transcript → viết section.

**State dùng:** `InterviewState` (kế thừa `MessagesState`, nên tự có key `messages`)

```python
max_num_turns: int               # tối đa mấy lượt hỏi-đáp
context: Annotated[list, add]    # kết quả search web (tự nối thêm)
analyst: Analyst                 # analyst đang được phỏng vấn
interview: str                   # transcript sau khi lưu
sections: list                   # bài viết rút ra từ phiên phỏng vấn
messages: [...]                  # hội thoại (từ MessagesState)
```

**Sơ đồ luồng:**

```
                    ┌─▶ search_web ──┐
START ─▶ ask_question                ├─▶ answer_question ─(route_messages)─┬─▶ ask_question (vòng lặp)
              │  └─▶ search_web2 ───┘                                      │
              └─────────────────────────────────────────────────────────── ┴─▶ save_interview ─▶ write_section ─▶ END
```

- `ask_question` (`generate_question`): LLM đóng vai người phỏng vấn, sinh 1 câu hỏi.
- `search_web` + `search_web2`: **hai node search Tavily chạy song song** (cùng từ `ask_question`, cùng đổ về `answer_question`). Kết quả gộp vào `context` (nhờ reducer `operator.add`).
- `answer_question` (`generate_answer`): LLM đóng vai chuyên gia, trả lời **dựa trên `context`** vừa search.
- `route_messages` (conditional edge): nếu **đủ `max_num_turns`** hoặc câu hỏi chứa `"Thank you so much for your help"` → sang `save_interview`; chưa đủ → **quay lại `ask_question`** (tạo vòng hỏi-đáp).
- `save_interview`: dồn `messages` thành chuỗi transcript.
- `write_section`: từ transcript + context → viết 1 section báo cáo, append vào `sections`.

**Chạy thử:** vì state yêu cầu `analyst`, ta đưa 1 analyst vào `Send`/input:

```python
from src.answering_questions import question_answer_graph
from langchain.messages import HumanMessage

result = question_answer_graph.invoke({
    "analyst": {
        "name": "Tran A", "role": "Chuyen gia AI",
        "affiliation": "VNG", "description": "quan tam chi phi trien khai",
    },
    "max_num_turns": 2,
    "context": [],
    "sections": [],
    "messages": [HumanMessage(content="Ban dang viet bai ve chu de AI agent?")],
})
print(result["sections"])
```

---

### Graph 3 — `deep_agent`  (file `src/deep_agent.py`)  ← graph "全" 

**Mục đích:** toàn bộ pipeline nghiên cứu: **tạo analyst → người duyệt → chạy N phiên phỏng vấn SONG SONG → gom section → viết thân bài/mở bài/kết bài → ghép báo cáo cuối.**

**State dùng:** `ResearchGraphState` (state "to", nhiều key nhất)

```python
topic, max_analysts, human_analyst_feedback, analysts   # như Graph 1
sections: Annotated[list, operator.add]   # gom từ nhiều analyst (reducer!)
introduction / content / conclusion       # các mảnh của báo cáo
final_report: str                          # kết quả cuối
```

**Sơ đồ luồng:**

```
START ─▶ create_analysts ─▶ human_feedback ─(initiate_all_interviews)─┬─▶ create_analysts (bị chê)
                                                                       │
                                                                       └─▶ conduct_interview ─┬─▶ write_report ────┐
                                                            (nhúng Graph 2,           ├─▶ write_introduction ─┤
                                                             chạy SONG SONG           └─▶ write_conclusion ───┤
                                                             cho TỪNG analyst)                                 ▼
                                                                                              finalize_report ─▶ END
```

Hai chỗ quan trọng nhất:

**(1) `conduct_interview` = chính là Graph 2 được nhúng làm subgraph:**

```python
builder.add_node("conduct_interview", interview_builder.compile())
```

Node này **không phải một hàm**, mà là **một graph con** (`interview_builder` ở `answering_questions.py`). Đây là kỹ thuật *subgraph* — graph to gọi graph nhỏ như một trạm.

**(2) Fan-out bằng `Send()` API (chỗ `initiate_all_interviews` trong `edges.py`):**

```python
return [Send("conduct_interview", {"analyst": analyst, "messages": [...]})
        for analyst in state["analysts"]]
```

Thay vì chạy tuần tự, nó **phóng (send) mỗi analyst vào `conduct_interview` một cách độc lập, cùng lúc**. Kết quả `sections` từ các luồng gộp lại nhờ reducer `operator.add`. Đây là mô hình **map** (chia để trị).

**(3) Chỗ `write_report / write_introduction / write_conclusion`:** cả 3 cùng đọc `sections` và chạy **song song** (3 edge cùng từ `conduct_interview`), sau đó **chở về `finalize_report`** — node này **ghép 3 mảnh** thành `final_report` (mở bài + thân + kết + nguồn). Đây là mô hình **reduce**.

→ Cả pipeline Graph 3 = **Map (`Send`) → Reduce (`finalize_report`)**.

**Chạy thử (có human-in-the-loop):**

```python
from src.deep_agent import graph
from langgraph.types import Command

config = {"configurable": {"thread_id": "full-1"}}
# graph sẽ pause ở human_feedback (checkpointer phải bật khi chạy qua langgraph dev/Studio)
graph.invoke({"topic": "AI agent cho SME 2026", "max_analysts": 3}, config)
graph.invoke(Command(resume="perfect"), config)      # duyệt -> bắt đầu phỏng vấn song song
# sau khi chạy xong:
print(graph.get_state(config).values["final_report"])
```

---

## Phần 2.5 — Cách chạy `asnwer_question` và `deep_agent` (thao tác thật)

Có **2 cách**: (A) qua **LangGraph Studio** (đồ họa, hợp demo), và (B) bằng **code Python / CLI** (ra kết quả nhanh). Chạy ở thư mục dự án, đã `uv sync` và có `.env` (xem `USER_GUIDE.md` mục 2).

---

### Chạy `asnwer_question` (graph 2)

Graph này **không có `interrupt`**, nên chạy thẳng một mạch tới `END`, không cần checkpointer.

**Cách A — Studio:**

```bash
uv run langgraph dev
```

Mở URL Studio in ra → chọn graph **`asnwer_question`** → dán input:

```json
{
  "analyst": {
    "name": "Tran A",
    "role": "Chuyen gia AI doanh nghiep",
    "affiliation": "VNG",
    "description": "lo ngai chi phi trien khai va ROI"
  },
  "max_num_turns": 2,
  "context": [],
  "sections": [],
  "messages": [
    { "role": "human", "content": "So you said you were writing an article on AI agents for SMEs?" }
  ]
}
```

Bấm **Submit**. Xem mục `sections` trong state cuối để lấy bài đã viết.

> ⚠️ Lưu ý: `messages` bắt buộc có vì `InterviewState` kế thừa `MessagesState`; `analyst` có thể truyền dạng dict (code tự `Analyst.model_validate`). `max_num_turns` quyết định vòng hỏi-đáp chạy mấy lần.

**Cách B — Python script** (tạo `run_interview.py` ở gốc dự án):

```python
from src.answering_questions import question_answer_graph
from langchain.messages import HumanMessage

result = question_answer_graph.invoke({
    "analyst": {
        "name": "Tran A", "role": "Chuyen gia AI doanh nghiep",
        "affiliation": "VNG", "description": "lo ngai chi phi trien khai va ROI",
    },
    "max_num_turns": 2,
    "context": [],
    "sections": [],
    "messages": [HumanMessage(content="So you said you were writing an article on AI agents for SMEs?")],
})

print("=== SECTION ===")
for s in result["sections"]:
    print(s.content if hasattr(s, "content") else s)
```

```bash
uv run python run_interview.py
```

---

### Chạy `deep_agent` (graph 3)

Graph này **có `interrupt` ở `human_feedback`**, nên **bắt buộc có checkpointer** để pause rồi resume.

**Cách A — Studio (khuyên dùng, đơn giản nhất):**

```bash
uv run langgraph dev
```

`langgraph dev` **tự động bật checkpointer in-memory** — bạn không phải code gì thêm. Mở Studio → chọn graph **`deep_agent`** → input:

```json
{
  "topic": "AI agents cho doanh nghiệp vừa và nhỏ 2026",
  "max_analysts": 3
}
```

Quy trình:
1. Submit → graph chạy `create_analysts` rồi **dừng** ở `human_feedback`, Studio hiện danh sách analyst.
2. Ở ô **Resume**:
   - nhập `continue` / `perfect` / để trống → **duyệt**, graph fan-out các phiên phỏng vấn song song.
   - nhập một câu góp ý (vd `"them goc nhin phan biem"`) → graph **quay lại** `create_analysts` sinh lại.
3. Chờ tới `END`, xem trường **`final_report`** (Markdown đầy đủ: mở bài + nội dung + kết + nguồn).

**Cách B — Python / CLI:**

Code trong `src/deep_agent.py` compile graph **không kèm checkpointer**, nên nếu `import graph` rồi `invoke` thì `interrupt` sẽ không pause đúng. **Hãy compile lại từ `builder` với `MemorySaver()`** như sau (tạo `run_report.py` ở gốc dự án):

```python
import sys, uuid
from langgraph.types import Command
from langgraph.checkpoint.memory import MemorySaver
from src.deep_agent import builder          # import BUILDER, không phải graph đã compile

app = builder.compile(checkpointer=MemorySaver())   # compile lại có checkpointer

topic = sys.argv[1] if len(sys.argv) > 1 else "AI agents cho SME 2026"
max_analysts = int(sys.argv[2]) if len(sys.argv) > 2 else 3
config = {"configurable": {"thread_id": uuid.uuid4().hex}}

result = app.invoke({"topic": topic, "max_analysts": max_analysts}, config)

# Graph dừng ở human_feedback -> nhập phản hồi, lặp tới khi không còn interrupt
while "__interrupt__" in result:
    intr = result["__interrupt__"][0]
    print("\n=== Analysts ===")
    for a in intr.value.get("analysts", []):
        print(f"- {a.get('name')} | {a.get('role')} | {a.get('affiliation')}")
    fb = input("Feedback để tạo lại (Enter = duyệt & tiếp tục): ").strip()
    result = app.invoke(Command(resume=fb or "continue"), config)

report = result.get("final_report", "")
open("final_report.md", "w", encoding="utf-8").write(report)
print(f"\nĐã lưu final_report.md ({len(report)} ký tự).")
```

```bash
uv run python run_report.py "AI agents cho doanh nghiệp vừa và nhỏ 2026" 3
```

> Cùng script này (bản hoàn chỉnh hơn) đã có sẵn trong `USER_GUIDE.md` mục 4.2 — copy sang là chạy được.

**Điểm hay gặp khi chạy `deep_agent` bằng tay:**

| Hiện tượng | Lý do | Xử lý |
| --- | --- | --- |
| `interrupt` không dừng / chạy thẳng lỗi | graph không có checkpointer | dùng `builder.compile(checkpointer=MemorySaver())` hoặc chạy Studio |
| Lỗi 401 / `deepseek_api_key` | thiếu `.env` | kiểm tra `DEEPSEEK_API_KEY`, chạy trong đúng thư mục dự án |
| `tavily_api_key` thiếu | graph 2/3 có search web | thêm `TAVILY_API_KEY` |
| Chạy rất lâu / tốn tiền | mỗi analyst là 1 phiên phỏng vấn nhiều lượt LLM | hạ `max_analysts` (2–3) khi test |

---

## Phần 3 — Tóm tắt nhanh để khỏi nhầm

| | Graph 1 `create_analysts` | Graph 2 `asnwer_question` | Graph 3 `deep_agent` |
|---|---|---|---|
| File | `src/agent.py` | `src/answering_questions.py` | `src/deep_agent.py` |
| Làm gì | Sinh + duyệt analyst | 1 phiên phỏng vấn | Toàn pipeline → báo cáo |
| State | `GenerateAnalystsState` | `InterviewState` | `ResearchGraphState` |
| Có người duyệt (interrupt)? | ✅ | ❌ | ✅ (dùng lại edge Graph 1) |
| Search web? | ❌ | ✅ (Tavily) | ✅ (qua subgraph) |
| Chạy song song? | ❌ | 2 node search | ✅ `Send()` fan-out |
| Quan hệ | logic tái dùng ở Graph 3 | được nhúng làm **subgraph** `conduct_interview` | **graph mẹ**, dùng cả 2 |

**3 mẫu thiết kế (pattern) bạn nên nhớ, vì chúng lặp đi lặp lại:**

1. **Human-in-the-loop** → `interrupt(...)` + `compile(interrupt_before=[...])` (Graph 1 & 3).
2. **Looping / retry** → conditional edge quay lại node cũ (chê thì sinh lại; chưa đủ lượt thì hỏi tiếp).
3. **Map–Reduce** → `Send()` để chia nhỏ chạy song song (map), reducer `operator.add` + node gom để tổng hợp (reduce).

---

## Phụ lục — Ảnh xạ file

```
src/
├── agent.py                 → Graph 1
├── answering_questions.py   → Graph 2 (interview_builder)
├── deep_agent.py            → Graph 3 (dùng node "conduct_interview" = Graph 2)
└── utils/
    ├── states.py            → 3 state: GenerateAnalysts / Interview / ResearchGraph
    ├── nodes.py             → toàn bộ hàm node (create_analysts, generate_question, search_web, write_report, ...)
    ├── edges.py             → 3 router: should_continue (G1), route_messages (G2), initiate_all_interviews (G3 + Send)
    ├── models.py            → llm = ChatDeepSeek(...)
    ├── objects.py           → Analyst, Perspectives (Pydantic, ép kiểu structured output)
    └── prompts.py           → các prompt template
```

> ⚠️ Lưu ý khi chạy: `interrupt`/`resume` (Graph 1 & 3) **cần checkpointer** (LangGraph Studio / `langgraph dev` tự cung cấp; nếu gọi trực tiếp bằng `graph.invoke` phải compile kèm `MemorySaver()`). Ngoài ra code dùng `tool_choice="auto"` cho `with_structured_output` vì DeepSeek thinking model từ chối `tool_choice` dạng ép tên hàm (xem `nodes.py:29`).
