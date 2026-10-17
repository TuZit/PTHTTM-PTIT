# Giai đoạn 3 — Kiểm thử: Bộ test & biên bản kiểm thử

> Sản phẩm giai đoạn **Kiểm thử** theo mục 4.2 của Action Plan.
> Bộ test tự động: `tests/` (pytest) — **chạy offline bằng mock, không tốn API**;
> có 1 test e2e API thật (mark `live`). Ngày kiểm thử: **2026-10-16 → 2026-10-17**.
> Người thực hiện: [ĐIỀN HỌ TÊN].

---

## 1. Cách chạy

| Lệnh | Phạm vi | Thời gian đo được |
|---|---|---|
| `uv run pytest` | **38 test offline** (mock LLM + Tavily) — mặc định | **0.81s** |
| `uv run pytest -m live` | 1 test e2e `deep_agent` bằng **API thật** | **66s** |
| `uv run pytest -v` | xem tên từng test | — |

Cấu hình pytest nằm trong `pyproject.toml` (`[tool.pytest.ini_options]`, `pythonpath=["."]`,
mặc định deselect mark `live`). `tests/conftest.py` tự nạp `.env` (cho live) và đặt key giả
chốt dự phòng (cho offline).

**Kết quả lần chạy gần nhất:** `38 passed, 1 deselected` (offline) + `1 passed` (live) — **100% pass**.

---

## 2. Chiến lược kiểm thử (test plan)

| Tầng | File | Cách thực hiện | Ưu tiên |
|---|---|---|---|
| Unit — edge/routing | `tests/test_edges.py` | gọi thẳng 3 hàm router, assert nhãn node kế tiếp | **P0** |
| Unit — node | `tests/test_nodes.py` | mock `nodes.llm` / `nodes.tavily_search` / `nodes.interrupt` | **P0** |
| Unit — prompt | `tests/test_prompts.py` | format 6 prompt, kiểm placeholder + directive ngôn ngữ | **P0** |
| Integration — graph | `tests/test_graphs.py` | compile graph với `MemorySaver`, invoke/resume bằng mock | P1 |
| End-to-end | `tests/test_graphs.py::test_deep_agent_e2e_api_that` (`live`) | API DeepSeek + Tavily thật | **P0** |
| Đánh giá chất lượng | *(giai đoạn 4)* | bảng tiêu chí nhiều chủ đề | P1 |

---

## 3. Ma trận truy vết: Test ↔ Mục tiêu ↔ Tiêu chí nghiệm thu

| ID | Test case (tên pytest) | MT | Nghiệm thu 6.3 | Kết quả |
|---|---|---|---|---|
| TC-01 | `TestCreateAnalysts::test_tra_dung_schema_analyst` | MT1 | parse đúng Pydantic | ✅ PASS |
| TC-01b | `TestCreateAnalysts::test_prompt_chua_language` | MT1/6 | prompt chứa directive ngôn ngữ | ✅ PASS |
| TC-02 | `TestHumanFeedbackLogic::test_bang_quyet_dinh_feedback` (8 TH) | MT2 | duyệt/tạo lại đúng logic | ✅ PASS |
| TC-02b | `TestGraph1HITL::test_dung_dung_interrupt_va_resume_dung_nhanh` | MT2 | **dừng đúng interrupt, tiếp tục đúng nhánh** | ✅ PASS |
| TC-02c | `TestGraph1HITL::test_feedback_khac_tao_lai_persona` | MT2 | **feedback → tạo lại persona** | ✅ PASS |
| TC-03 | `TestInitiateAllInterviews::test_khong_feedback_fan_out_send` | MT3 | N analyst → N Send | ✅ PASS |
| TC-03b | `TestDeepAgentE2E::test_toan_trinh_voi_mock` (fan-in đủ 3 section) | MT3 | gom đủ khi fan-in | ✅ PASS |
| TC-04 | `TestSearchWebFallback` (6 TH: `None`, plain rỗng, OK, Tavily rỗng, thiếu url) | MT4/robust | **regression BUG-01, không crash** | ✅ PASS |
| TC-05 | `TestWriterNodes::test_write_section_tra_sections_khong_phai_str` | MT5 | sections là list, append đúng | ✅ PASS |
| TC-05b | `TestWriterNodes::test_finalize_report_gop_du_va_tach_sources` | MT5 | **đủ 4 phần + nguồn** | ✅ PASS |
| TC-06 | `test_deep_agent_e2e_api_that` (live) | MT5 | **e2e không lỗi, `final_report` > 500 ký tự** | ✅ PASS (66s) |
| TC-07 | `test_tc07_prompt_format_khong_loi_va_chi_dinh_ngon_ngu` (6 TH) + `test_tc07_tat_ca_nodes_truyen_du_language` | MT6 | prompt/nodes khớp placeholder | ✅ PASS |
| TC-09 | `TestDeepAgentE2E::test_subgraph_interview_doc_lap` | MT3/4 | 1 phiên interview độc lập (hỏi→search→đáp→section) | ✅ PASS |

> P0 offline (TC-01…05, 07): **đạt 100%** bằng `pytest` thường, không cần key.
> P0 e2e (TC-06): đạt với `.env` key hợp lệ.

---

## 4. Biên bản kiểm thử chi tiết

### 4.1. Phiên offline — `uv run pytest` (2026-10-17)
```
collected 39 items / 1 deselected / 38 selected
tests/test_edges.py .........        [ 23%]
tests/test_graphs.py ....            [ 34%]
tests/test_nodes.py ..................  [ 81%]
tests/test_prompts.py .......        [100%]
======================= 38 passed, 1 deselected in 0.81s =======================
```

### 4.2. Phiên live — `uv run pytest -m live` (2026-10-17)
```
tests/test_graphs.py::test_deep_agent_e2e_api_that PASSED   [100%]
================= 1 passed, 38 deselected in 66s =================
```
E2e thật: topic *"AI agent cho doanh nghiệp SME Việt Nam"*, `max_analysts=1`;
graph dừng đúng HITL → `Command(resume="continue")` → `final_report` đạt độ dài nghiệm thu.

### 4.3. Bằng chứng thủ công ghi nhận trong quá trình dev (không tự động hóa)
| # | Kiểm | Kết quả thực đo |
|---|---|---|
| 1 | `create_analysts` API thật, topic tiếng Việt | analyst mô tả **tiếng Việt** ("Nguyễn Minh Anh — Chuyên gia tư vấn chuyển đổi số…") |
| 2 | `write_section` API thật, **context đầu vào tiếng Anh** | đầu ra **tiếng Việt** (`## ROI của AI agent: Đầu tư thông minh…`) |
| 3 | Luồng Gradio `deep_agent` 2 bước | pause `⏸️ Đang chờ bạn duyệt` → resume → `final_report` **4703 ký tự**, ~51s, lưu file |

---

## 5. Nhật ký lỗi (defect log)

| ID | Mức | Mô tả | Nguyên nhân gốc | Trạng thái |
|---|---|---|---|---|
| BUG-01 | Cao | `AttributeError: 'NoneType' object has no attribute 'search_query'` khi chạy `deep_agent` → `conduct_interview` → `search_web` | `with_structured_output(tool_choice="auto")` trên `deepseek-chat` đôi khi bỏ qua function-calling → trả `None`; node giả định luôn có object | **ĐÃ SỬA** — `_make_search_query` 3 tầng fallback; TC-04 (6 TH) green |
| **BUG-02 (mới ghi nhận)** | Trung | `write_introduction` / `write_conclusion` truyền **chuỗi thô** vào message list: `llm.invoke([instructions] + [...])` thay vì `[SystemMessage(content=instructions)]` (nodes.py dòng 253 & 267) | LangChain tự convert `str` → **HumanMessage**, nên không crash (e2e live vẫn PASS) — nhưng prompt hệ thống bị gửi nhầm dạng *người dùng* thay vì *system*, sai ý thiết kế prompt và có thể làm model yếu hơn bám chỉ thị. Các node khác đều bọc `SystemMessage` đúng. | **MỞ** — sửa thành `[SystemMessage(content=instructions)]` |
| OBS-02 | Thấp | Cảnh báo `Deserializing unregistered type ...Analyst from checkpoint` | msgpack checkpointer + type Pydantic tùy biến | Mở — vô hại hôm nay, có thể bị chặn ở bản LangGraph sau |
| OBS-03 | Thấp | `intro_conclusion_instructions` **định nghĩa trùng 2 lần** trong `prompts.py` (dòng 137 và 162; bản sau đè bản trước — cả 2 đều đã có `{language}`) | lỗi soạn file | Mở — nên xóa bản trùng |
| OBS-04 | Thấp | `langgraph.json` đăng ký graph tên `"asnwer_question"` (thiếu chữ *w* → sai chính tả) | typo khi soạn cấu hình | Mở — Studio hiện tên này |
| OBS-05 | Thấp | `human_feedback_update()` (nodes.py dòng 69–72) lấy `GenerateAnalystsState["human_analyst_feedback"]` — subscript trên **class TypedDict** trả về *type annotation* (`Optional[str]`), không phải giá trị state → hàm không bao giờ hoạt động như tên | dead-code, không graph nào đăng ký node này | Mở — nên xóa |

---

## 6. Kết luận giai đoạn Kiểm thử

1. **Tự động hóa đạt**: 38 unit/integration test (mock, chạy <1s, không cần key) + 1 e2e live; **100% pass**. Đáp ứng mục 6.3 "100% test case P0 pass" cho các hạng mục đã phủ.
2. **Regression chốt**: BUG-01 (`NoneType.search_query`) giờ có TC-04 guarding — bug cũ không tái phạm được nữa.
3. **HITL chứng minh bằng test**: TC-02b/02c xác nhận cả 2 nhánh (duyệt → END; feedback → tạo lại persona).
4. **Fan-out/fan-in chứng minh**: TC-03 assert 3 `Send`; TC-03b assert `sections` gom đủ 3 (reducer hoạt động).
5. **Việc còn cho giai đoạn Đánh giá**: bảng chấm điểm theo tiêu chí (relevance/grounding/citation/completeness) trên **nhiều chủ đề**, so sánh có/không HITL.
6. **Việc nên làm trước khi nộp**: xử lý BUG-02 (đóng `SystemMessage` cho 2 node writer) và dọn OBS-03/05.
