# Giai đoạn 1 — Khảo sát: Phân tích yêu cầu & kiến trúc hệ thống

> Sản phẩm giai đoạn **Khảo sát** theo mục 4.2 của Action Plan.
> Đề tài: *Trợ lý nghiên cứu đa tác tử sử dụng LangGraph* — Môn Phát triển hệ thống thông minh.
> Tài liệu tham chiếu nhanh cho code: xem `GRAPH_GUIDE.md`.

---

## 1. Bối cảnh và tính cấp thiết

Một lời gọi chat LLM đơn lẻ tồn tại ba hạn chế rõ rệt khi dùng cho nghiên cứu:

1. **Thiếu bao phủ góc nhìn** — một phiên chat khó đồng thời đại diện nhiều chuyên gia/phía nhìn trên cùng một chủ đề.
2. **Dễ "trông hợp lý nhưng không có căn cứ"** (hallucination) — vì không truy vết được nguồn khi mô hình suy đoán.
3. **Không duy trì được quy trình nhiều bước** — thiếu trạng thái, vòng lặp và điểm tương tác có kiểm soát của con người.

Hướng tiếp cận **đa tác tử (multi-agent)** kết hợp **điều phối theo đồ thị (graph orchestration)** giải quyết đúng ba hạn chế trên: mỗi "nhà phân tích" (analyst) ảo đảm nhận một persona chuyên biệt; trạng thái hội thoại được lưu có kiểm soát; luồng xử lý biểu diễn tường minh bằng node/edge cho phép quan sát, tạm dừng và thử lại.

**Đầu ra mong muốn:** từ một chủ đề nghiên cứu → một **báo cáo Markdown hoàn chỉnh, có trích dẫn nguồn**, với sự phê duyệt của con người ở bước trung gian.

---

## 2. Khảo sát công nghệ

### 2.1. Lựa chọn framework điều phối

| Tiêu chí | LangGraph | AutoGen | CrewAI |
|---|---|---|---|
| Mô hình điều phối | **StateGraph tường minh** (node/edge) | hội thoại nhóm (group chat) | phân vai theo "crew" |
| Vòng lặp (loop) | conditional edge — rõ ràng | có, qua hội thoại | hạn chế hơn |
| Fan-out song song | **`Send()` API** (map) | thủ công | một phần |
| Human-in-the-loop | **`interrupt` + checkpointer** (đúng điểm dừng) | qua hook | qua điều kiện |
| Debug trực quan | **LangGraph Studio** | ít | ít |
| Phù hợp bài toán có cả **vòng lặp + fan-out + HITL** | **✓ tốt nhất** | — | — |

**Quyết định: chọn LangGraph**, vì mô hình StateGraph với *reducer*, *conditional edge*, *interrupt*, *Send API* khớp nhất với yêu cầu nghiệp vụ, đồng thời có Studio hỗ trợ demo/bảo vệ.

### 2.2. Khảo sát cơ chế cốt lõi của LangGraph
- **StateGraph**: đồ thị state — các node đọc/ghi một state chia sẻ (TypedDict / `MessagesState`).
- **Node**: đơn vị xử lý (thường là hàm gọi LLM/tool), trả về *phần state thay đổi*.
- **Edge**: nối cứng (`add_edge`) hoặc rẽ nhánh theo điều kiện (`add_conditional_edges`).
- **Reducer** (`Annotated[list, operator.add]`): cho phép nhiều luồng **ghi cộng dồn** vào cùng một key mà không đè nhau → nền tảng cho fan-in.
- **`interrupt` + checkpointer**: dừng đồ thị tại một điểm để con người quyết, rồi `resume`.
- **`Send()`**: phóng nhiều luồng con chạy **độc lập, song song** (map), mỗi luồng một state riêng.
- **Subgraph**: một graph được nhúng như một node của graph lớn → tái sử dụng logic phỏng vấn.

### 2.3. Khảo sát grounding & citation (chống hallucination)
- **Retrieval lúc chạy (runtime)** bằng **Tavily Search API**: mỗi lượt phỏng vấn sinh một *search query* từ hội thoại, lấy tài liệu kèm URL, đưa vào ngữ cảnh.
- **Nguyên tắc trả lời**: expert *chỉ* trả lời dựa trên context retrieved, **trích dẫn đánh số [1], [2]…** và liệt kê nguồn — được ghi cứng trong prompt `answer_instructions`.
- Đây là cơ sở cho tiêu chí MT4 (mọi câu trả lời được grounding + có citation).

### 2.4. Mô hình nền và công thức sinh cấu trúc
- **LLM**: DeepSeek qua `langchain-deepseek` (`ChatDeepSeek`). `deepseek-chat` (V3, mặc định) cho demo; `deepseek-reasoner` (R1) khi cần lập luận sâu.
- **Structured output**: ép khuôn bằng Pydantic (`Perspectives`, `SearchQuery`) để `create_analysts` và `search_web` trả đúng schema.
- **Ràng buộc học được khi khảo sát**: (a) DeepSeek *thinking model* từ chối `tool_choice` dạng ép tên hàm (400) → phải dùng `tool_choice="auto"`; (b) nhưng `"auto"` trên `deepseek-chat` đôi khi **bỏ qua function-calling → trả `None`** → node phải có fallback. Hai phát hiện này ảnh hưởng trực tiếp thiết kế ở Giai đoạn 2.

---

## 3. Phân tích yêu cầu

### 3.1. Ánh xạ mục tiêu → yêu cầu → tiêu chí đo (KPI)

| MT | Mục tiêu cụ thể | Yêu cầu chức năng tương ứng | Tiêu chí đánh giá |
|---|---|---|---|
| MT1 | Sinh nhóm analyst persona từ chủ đề | Node `create_analysts` + schema `Perspectives` | Đúng số lượng ≤ `max_analysts`, parse đúng Pydantic 100% |
| MT2 | Human-in-the-loop duyệt/tạo lại | Node `human_feedback` + `interrupt` + edge `should_continue` | Dừng đúng interrupt; feedback đi đúng nhánh |
| MT3 | Phỏng vấn song song từng analyst | `Send()` fan-out tới subgraph `conduct_interview` | N analyst → N subgraph độc lập, gom đủ khi fan-in |
| MT4 | Câu trả lời grounding trên web search | `search_web` (Tavily) → `answer_question` kèm citation | Tỷ lệ câu trả lời có URL/citation đạt mục tiêu |
| MT5 | Tổng hợp báo cáo 4 phần | `write_report/introduction/conclusion` + `finalize_report` | Đủ mở đầu/nội dung/kết luận/nguồn, không mất dữ liệu |
| MT6 | Đóng gói mã + tài liệu chuẩn đồ án | `langgraph.json`, README, bộ test | Chạy được `uv run langgraph dev`, test pass, báo cáo đủ |

### 3.2. Yêu cầu phi chức năng
- **Chi phí kiểm soát được**: giới hạn `max_analysts`/`max_turns`; ước lượng ≈ 15–25 lời gọi LLM + 9–15 tìm kiếm, ≈ 0,1–0,5 USD/phiên (3 analyst/3 turn).
- **Bảo mật**: API key đặt `.env`, nằm trong `.gitignore`; không commit output chứa dữ liệu nhạy cảm.
- **Quan sát được**: mọi node/edge/state inspect qua LangGraph Studio (hoặc UI Gradio).
- **Ổn định luồng**: có điều kiện thoát (`max_turns`, chuỗi kết thúc "Thank you so much…") để tránh lặp vô hạn.

### 3.3. Yêu cầu dữ liệu

| Nhóm | Thành phần | Hình thức |
|---|---|---|
| Đầu vào | topic, `max_analysts`, phản hồi người dùng | text, số nguyên |
| Trung gian | analyst persona, câu hỏi, search query, tài liệu web + URL, hội thoại, memo, section | Pydantic object / message list / dict |
| Đầu ra | báo cáo Markdown final (mở đầu, nội dung, kết luận, nguồn) | text file |

---

## 4. Phạm vi

### 4.1. Trong phạm vi
- 03 graph: `create_analysts` (sinh & duyệt persona), `answer_question` (subgraph phỏng vấn đơn), `deep_agent` (điều phối toàn trình).
- Chỉ **sử dụng** mô hình nền qua API (không huấn luyện/fine-tune).
- Giao diện làm việc: LangGraph Studio/CLI; **bổ sung** UI Gradio local để tăng tính thân thiện (nằm trong phạm vi MT6/demo).
- Đầu ra: file Markdown.

### 4.2. Ngoài phạm vi
- Không xây web app thương mại, không quản lý tài khoản người dùng.
- Không dùng cơ sở dữ liệu tĩnh; nguồn là web search thời gian chạy.
- Không fine-tune mô hình.

---

## 5. Kiến trúc hệ thống tổng quan

Ba graph có quan hệ lồng nhau — `deep_agent` là graph "mẹ", dùng lại logic của `create_analysts` và **nhúng** `answer_question` làm subgraph:

```
┌───────────────────── deep_agent (graph toàn trình) ─────────────────────┐
│                                                                          │
│  create_analysts ─▶ human_feedback ─▶ [phỏng vấn SONG SONG] ─▶           │
│  (persona)         (HITL interrupt)   conduct_interview                  │
│                                          ▲ nhúng subgraph                │
│                                          └ = answer_question (graph 2)    │
│  ─▶ write_report / write_introduction / write_conclusion ─▶              │
│       finalize_report ─▶ END                                             │
└──────────────────────────────────────────────────────────────────────────┘
```

**Mẫu thiết kế (pattern) hệ thống minh họa:**
1. **Persona agent** — mỗi analyst một vai trò/chuyên môn riêng.
2. **Human-in-the-loop** — duyệt trước bước tốn chi phí.
3. **Supervisor/orchestrator** — `deep_agent` điều phối.
4. **Fan-out / fan-in** — `Send()` chia N luồng, reducer gom về.
5. **Map–Reduce synthesis** — map = từng section, reduce = hợp nhất + viết mở/kết.

→ **Kiến trúc này là căn cứ để thiết kế chi tiết ở Giai đoạn 2** (`docs/02_Thiet_ke.md`).

---

## 6. Tài liệu khảo sát đã dùng
- Tài liệu chính thức LangGraph / LangChain (StateGraph, Send, interrupt, checkpointer).
- Tài liệu DeepSeek API, Tavily Search API.
- Mã nguồn repo tham khảo `LangGraph_Research_Assistant_Agent` + README.
- Các công trình về multi-agent + RAG/grounding (tổng quan qua mục 2.4).
