# Giai đoạn 2 — Thiết kế: Sơ đồ luồng, mô hình dữ liệu, schema Pydantic

> Sản phẩm giai đoạn **Thiết kế** theo mục 4.2 của Action Plan.
> Tài liệu này tự chứa (nộp riêng được), có tái dùng/chuẩn hóa sơ đồ từ `GRAPH_GUIDE.md`.

---

## 1. Mô hình dữ liệu (State)

Mọi graph dùng `StateGraph` với một **state chia sẻ**: node đọc state, trả về *phần thay đổi*, LangGraph gộp (merge) vào state chung.

### 1.1. `GenerateAnalystsState` — state cho graph persona
*(file `src/utils/states.py`)*

| Field | Kiểu | Vai trò | Ghi chú thiết kế |
|---|---|---|---|
| `topic` | `str` | chủ đề nghiên cứu | bắt buộc |
| `max_analysts` | `int` | số analyst mong muốn | bắt buộc |
| `human_analyst_feedback` | `NotRequired[Optional[str]]` | phản hồi người dùng | **tùy chọn** — lúc đầu chưa có |
| `analysts` | `NotRequired[List[Analyst]]` | kết quả danh sách analyst | do `create_analysts` ghi |

`NotRequired` = key không bắt buộc có ngay từ input đầu tiên (feedback, analysts sinh ra trong lúc chạy).

### 1.2. `InterviewState` — state cho subgraph phỏng vấn
*(kế thừa `MessagesState` → tự có key `messages`)*

| Field | Kiểu | Vai trò | Reducer? |
|---|---|---|---|
| `max_num_turns` | `int` | tối đa mấy lượt hỏi-đáp | ghi đè |
| `context` | `Annotated[list, operator.add]` | tài liệu search web | **cộng dồn** |
| `analyst` | `Analyst` | analyst đang phỏng vấn | ghi đè |
| `interview` | `str` | transcript đã lưu | ghi đè |
| `sections` | `list` | section rút ra (key để `Send` nhân bản sang state ngoài) | *(khai là list, reducer do graph mẹ)* |
| `messages` | `MessagesState` | hội thoại analyst↔expert | append (MessagesState mặc định) |

**Vì sao `context` cần `operator.add`:** hai node `search_web` và `search_web2` chạy **song song** và cùng ghi `context`. Reducer cộng dồn giúp **cái này không đè cái kia**.

### 1.3. `ResearchGraphState` — state "to" cho graph toàn trình

| Field | Kiểu | Vai trò | Reducer? |
|---|---|---|---|
| `topic`, `max_analysts`, `human_analyst_feedback`, `analysts` | như trên | pha persona | — |
| `sections` | `Annotated[list, operator.add]` | **gom section từ N analyst song song** | **cộng dồn** (chìa khóa fan-in) |
| `introduction` / `content` / `conclusion` | `str` | 3 mảnh của báo cáo | ghi đè (mỗi node 1 key) |
| `final_report` | `str` | kết quả cuối | `finalize_report` ghi |

---

## 2. Schema Pydantic (structured output)

*(file `src/utils/objects.py` và `states.py`)*

### `Analyst`
```python
class Analyst(BaseModel):
    affiliation: str  # tổ chức
    name: str         # tên
    role: str         # vai trò theo chủ đề
    description: str  # trọng tâm, lo ngại, động cơ
    @property
    def persona(self) -> str:  # chuỗi ghép đưa vào prompt
        ...
```

### `Perspectives`
```python
class Perspectives(BaseModel):
    analysts: List[Analyst]  # danh sách analyst — đích của create_analysts
```
→ `llm.with_structured_output(Perspectives, tool_choice="auto")` ép LLM trả đúng khung này (MT1).

### `SearchQuery`
```python
class SearchQuery(BaseModel):
    search_query: str  # một truy vấn tìm kiếm, đích của search_web
```
→ dùng ở node search; **phải xử lý trường hợp trả `None`** (xem §5.2).

---

## 3. Thiết kế node & edge — 3 graph

### 3.1. Graph 1 `create_analysts` (`src/agent.py`)
```
START ─▶ create_analysts ─▶ human_feedback ─(should_continue)─┬─▶ create_analysts (tạo lại)
                                                              └─▶ dummy ─▶ END
```
| Node | Loại | Vào → Ra |
|---|---|---|
| `create_analysts` | LLM structured | topic+feedback → `{"analysts": [...]}` |
| `human_feedback` | **interrupt** | pause, nhận giá trị resume → `{"human_analyst_feedback": ...}` |
| `dummy` | no-op | nối tới END |

Edge `should_continue` (`Literal["create_analysts","dummy"]`): feedback == `"perfect"` → `dummy` (chốt); feedback khác → về `create_analysts` (vòng lặp).
`compile(interrupt_before=['human_feedback'])` → graph tự dừng ở HITL (MT2).

### 3.2. Graph 2 `answer_question` / `interview_builder` (`src/answering_questions.py`)
```
                    ┌─▶ search_web ──┐
START ─▶ ask_question                ├─▶ answer_question ─(route_messages)─┬─▶ ask_question (vòng)
                   └─▶ search_web2 ──┘                                     └─▶ save_interview ─▶ write_section ─▶ END
```
| Node | Hàm | Vai trò |
|---|---|---|
| `ask_question` | `generate_question` | LLM (analyst) sinh câu hỏi |
| `search_web`, `search_web2` | search Tavily | **song song**, cộng dồn `context` |
| `answer_question` | `generate_answer` | LLM (expert) trả lời **dựa trên context** + citation (MT4) |
| `save_interview` | `save_interview` | dồn `messages` → `interview` |
| `write_section` | `write_section` | context → 1 section (append `sections`) |

Edge `route_messages`: đủ `max_num_turns` **hoặc** hỏi `"Thank you so much for your help"` → `save_interview`; ngược lại về `ask_question` (vòng hỏi-đáp + điều kiện thoát chống lặp vô hạn).

### 3.3. Graph 3 `deep_agent` (`src/deep_agent.py`) — graph mẹ
```
START ─▶ create_analysts ─▶ human_feedback ─(initiate_all_interviews)─┬─▶ create_analysts (bị chê)
                                                                       └─▶ conduct_interview ─┬─▶ write_report ─────┐
                                                            (nhúng Graph 2,          ├─▶ write_introduction ─┤
                                                             SONG SONG từng analyst)  └─▶ write_conclusion ───┤
                                                                                              finalize_report ─▶ END
```
Hai quyết định thiết kế then chốt:
1. **`conduct_interview` = subgraph** `interview_builder.compile()` — node không phải hàm mà là **một graph con** (MT3, pattern persona/agent lồng nhau).
2. **Fan-out bằng `Send()`** (edge `initiate_all_interviews`): mỗi analyst một `Send("conduct_interview", {...})` chạy độc lập; `sections` cộng dồn nhờ reducer (map). Ba node writer + `finalize_report` chạy rồi **giảm** về 1 báo cáo (reduce) (MT5).

→ **Toàn pipeline = Map (`Send`) → Reduce (`finalize_report`).**

---

## 4. Thiết kế prompt
Mỗi node LLM có prompt template riêng (`src/utils/prompts.py`), nhét tham số qua `.format(...)`:

| Prompt | Node dùng | Ý định thiết kế |
|---|---|---|
| `analyst_instructions` | create_analysts | sinh persona theo chủ đề + feedback, đúng `max_analysts` |
| `question_instructions` | generate_question | hỏi "thú vị + cụ thể", kết bằng "Thank you…" |
| `search_instructions` | search_web | chuyển hội thoại → 1 query retrieval |
| `answer_instructions` | generate_answer | **chỉ** trả lời theo context, cite [1][2], liệt kê nguồn |
| `section_writer_instructions` | write_section | memo có cấu trúc (## / ###, sources) |
| `report_writer_instructions` | write_report | hợp nhất memo → narrative, mở đầu `## Insights`, mục `## Sources` |
| `intro_conclusion_instructions` | write_introduction/conclusion | viết mở/kết ~100 từ |

**Thiết kế ngôn ngữ đầu ra:** vì prompt viết bằng tiếng Anh, nếu không chỉ định thì output dễ lẫn Anh/Việt dù nhập chủ đề tiếng Việt. → Các prompt sinh văn bản được chèn chỉ thị `{language}` (mặc định **Tiếng Việt**, đổi qua `REPORT_LANGUAGE`). Đây là một *quyết định thiết kế* để bảo đảm tính nhất quán đầu ra.

---

## 5. Thiết kế robustness (xử lý rủi ro đã biết khi khảo sát)

### 5.1. Routing thoát vòng lặp
`route_messages` và `should_continue` luôn có điều kiện dừng rõ (`max_num_turns`, từ khóa, `"perfect"`) → tránh deadlock/loop vô hạn (rủi ro mục 9.1).

### 5.2. Fallback cho structured output `None`
`with_structured_output(SearchQuery, tool_choice="auto")` trên `deepseek-chat` có thể **không gọi tool → trả `None`**, làm `None.search_query` crash node `search_web` (bug từng gặp ở `conduct_interview`).
**Thiết kế sửa:** hàm `_make_search_query` 3 tầng — (1) dùng structured output nếu có giá trị, (2) fallback gọi LLM lấy text thường, (3) dùng tin nhắn gần nhất / `analyst.description`. Không bao giờ trả `None` → node không crash.

### 5.3. Fan-in không mất dữ liệu
`sections`/`context` dùng reducer `operator.add`; `finalize_report` đọc `content`/`introduction`/`conclusion` đã gộp → MT5 "không mất dữ liệu".

---

## 6. Truy vết thiết kế ↔ mục tiêu
| MT | Cơ chế thiết kế ở tài liệu này |
|---|---|
| MT1 | `create_analysts` + `Perspectives` (§2, §3.1) |
| MT2 | `human_feedback` interrupt + `should_continue` (§3.1) |
| MT3 | `Send()` fan-out + subgraph `conduct_interview` (§3.3) |
| MT4 | `search_web`→`answer_question` + ràng buộc citation (§3.2, §4) |
| MT5 | 3 writer + `finalize_report` + reducer `sections` (§3.3, §5.3) |
| MT6 | module tách `states/objects/nodes/edges/models/prompts` + `langgraph.json` (§3, §4) |
