### **MÔN PHÁT TRIỂN HỆ THỐNG THÔNG MINH** 

# **CẤU TRÚC PHÂN RÃ CÔNG VIỆC (WBS)** 

_Trợ lý nghiên cứu đa tác tử sử dụng LangGraph_ 

|**Họ và tên**|[ĐIỀN HỌ TÊN]|
|---|---|
|**MSSV**|[ĐIỀN MSSV]|
|**Hình thức**|Bài tập lớn cá nhân — tự xây dựng và tự nghiên cứu|
|**Giảng viên hướng dẫn**|[ĐIỀN TÊN GIẢNG VIÊN]|
|**Thời lượng dự án**|04 tuần / 20 ngày làm việc|
|**Ngày lập**|[DD/MM/YYYY]|



## **1. Nguyên tắc xây dựng WBS** 

- **Quy tắc 100%:** toàn bộ phạm vi dự án (mã nguồn 3 graph, test, tài liệu, demo) được phân rã trọn vẹn trong cây WBS; công việc ngoài cây = ngoài phạm vi. 
- **Ba mức phân rã:** Mức 1 = giai đoạn (5 kiểm soát chính – control account); Mức 2 = gói công việc (work package, đóng gói theo hạng mục chuyên môn — tất cả do tác giả đảm nhiệm); Mức 3 = nhiệm vụ (task, ước lượng ≤ 1–2 ngày). 
- **Mỗi gói công việc có:** mã WBS, sản phẩm đầu ra (deliverable), người thực hiện (toàn bộ do tác giả đảm nhiệm), thời lượng, phụ thuộc và tiêu chí hoàn thành (Definition of Done). 
- **Điểm kiểm soát (checkpoint):** cuối mỗi tuần đối chiếu tiến độ với milestone M1–M4; gói chậm ≥ 2 ngày phải được xử lý trong buổi review cuối tuần bằng cách cắt phạm vi hoặc dồn buffer. 

## **2. Cấu trúc phân rã (cây WBS)** 

```text
1  Trợ lý nghiên cứu đa tác tử LangGraph 
├── 1  Khảo sát & Phân tích yêu cầu            [Tuần 1 | M1] 
│   ├── 1.1  Khảo sát công nghệ & bài toán 
│   │   ├── 1.1.1  Đọc tài liệu chính thức LangGraph/LangChain, paper agent/RAG 
│   │   └── 1.1.2  Bản phác họa kiến trúc 3 graph + danh mục file dự kiến 
│   ├── 1.2  Học công nghệ nền tảng 
│   │   ├── 1.2.1  LangGraph: state/node/edge, reducer, interrupt, Send 
│   │   └── 1.2.2  Tavily API; Pydantic structured output 
│   └── 1.3  Đặc tả yêu cầu 
│       ├── 1.3.1  Bảng yêu cầu chức năng FR1–FR6 
│       └── 1.3.2  Bảng yêu cầu phi chức năng NFR1–NFR6 
├── 2  Thiết kế hệ thống                       [Tuần 1–2 | M1] 
│   ├── 2.1  Thiết kế dữ liệu 
│   │   ├── 2.1.1  Sơ đồ state 3 graph (states.py) 
│   │   └── 2.1.2  Schema Pydantic objects.py 
│   ├── 2.2  Thiết kế luồng điều phối 
│   │   ├── 2.2.1  Sơ đồ node/edge + conditional routing 
│   │   ├── 2.2.2  Thiết kế điểm interrupt (HITL) 
│   │   └── 2.2.3  Thiết kế fan-out Send / fan-in reducer 
│   └── 2.3  Thiết kế prompt 
│       ├── 2.3.1  Khung prompt theo 5 quy tắc 
│       └── 2.3.2  Bản mẫu prompt v1 (persona/interview/report) 
├── 3  Triển khai                              [Tuần 2–3 | M2, M3] 
│   ├── 3.1  Hạ tầng & khung repo 
│   │   ├── 3.1.1  Khởi tạo repo, uv, .env, .gitignore 
│   │   ├── 3.1.2  models.py + langgraph.json (dev server/Studio) 
│   │   └── 3.1.3 CI nội bộ: branch, review trước merge 
│   ├── 3.2  Graph create_analysts + HITL 
│   │   ├── 3.2.1  Node sinh persona (structured output) 
│   │   ├── 3.2.2  Node human_feedback (interrupt) 
│   │   └── 3.2.3  Edge vòng phản hồi → tái sinh analyst 
│   ├── 3.3  Subgraph answer_question 
│   │   ├── 3.3.1  ask_question + ask_search_question 
│   │   ├── 3.3.2  search_web_task (Tavily, 2 node song song) 
│   │   ├── 3.3.3  answer_question (grounding + citation) 
│   │   ├── 3.3.4  should_continue (max_turns) 
│   │   └── 3.3.5  save_interview → memo + transcript 
│   ├── 3.4  Graph deep_agent (tích hợp toàn trình) 
│   │   ├── 3.4.1  Fan-out Send theo danh sách analyst 
│   │   ├── 3.4.2  write_section + reducer gom sections 
│   │   ├── 3.4.3  write_introduction / write_report / write_conclusion 
│   │   └── 3.4.4  finalize_report → Markdown + danh mục nguồn 
│   └── 3.5  Hardening 
│       ├── 3.5.1  Input validation (topic rỗng, giới hạn analyst/turn) 
│       ├── 3.5.2  Retry/backoff + timeout cho API lỗi 
│       └── 3.5.3  Log phiên chạy + telemetry token/độ trễ 
├── 4  Kiểm thử & Đánh giá                     [Tuần 3–4 | M3, M4] 
│   ├── 4.1  Kiểm thử 
│   │   ├── 4.1.1  Unit test node/edge trọng yếu 
│   │   ├── 4.1.2  Integration test từng graph 
│   │   ├── 4.1.3  E2E test kịch bản demo 
│   │   └── 4.1.4  Biên bản kiểm thử (ma trận test case) 
│   └── 4.2  Đánh giá chất lượng 
│       ├── 4.2.1  Bộ chủ đề thử nghiệm + chạy phiên thực nghiệm 
│       ├── 4.2.2  Bảng tiêu chí 7 chỉ số (relevance…UX) 
│       ├── 4.2.3  Tự chấm rubric + đối chiếu chéo + tổng hợp 
│       └── 4.2.4  Phân tích chi phí – độ trễ 
└── 5  Tài liệu & Demo                         [Tuần 1–4 | M4] 
    ├── 5.1  Tài liệu 
    │   ├── 5.1.1  README cài đặt/hướng dẫn chạy 
    │   ├── 5.1.2  Action Plan (WP đầu kỳ) 
    │   ├── 5.1.3  Báo cáo cuối kỳ + WBS + phụ lục demo 
    │   └── 5.1.4  Slide trình bày 
    └── 5.2  Demo & bảo vệ 
        ├── 5.2.1  Kịch bản demo end-to-end (kịch bản 4.4 BC) 
        ├── 5.2.2  Tổng duyệt nội bộ + fix phát sinh 
        └── 5.2.3  Nộp sản phẩm & trình bày trước lớp 
```

## **3. Từ điển WBS (chi tiết gói công việc)** 

### **3.1. WP1 – Khảo sát & Phân tích yêu cầu** 

|**Mã**|**Gói công việc**|**Sản phẩm đầu ra**|**Người thực hiện**|**Thời lượng**|**Phụ thuộc**|**Tiêu chí hoàn thành**|
|---|---|---|---|---|---|---|
|1.1|Khảo sát công nghệ & bài toán|Tài liệu khảo sát LangGraph/LangChain, paper agent/RAG; bản phác họa kiến trúc 3 graph|[ĐIỀN HỌ TÊN] (tự thực hiện)|2 ngày|—|Danh mục file `src/*` dự kiến + sơ đồ 3 graph, chỉ rõ điểm interrupt|
|1.2|Học công nghệ nền tảng [2][4][5]|Bộ ghi chú cơ chế (reducer, interrupt, Send, structured output, Tavily)|[ĐIỀN HỌ TÊN] (tự thực hiện)|3 ngày|—|Mỗi cơ chế có ghi chú tóm tắt riêng, hoàn tất trước khi code (W2)|
|1.3|Đặc tả yêu cầu|Tài liệu yêu cầu FR1–FR6, NFR1–NFR6|[ĐIỀN HỌ TÊN] (tự thực hiện)|2 ngày|1.1, 1.2|Giảng viên ghi nhận tại M1; mọi FR có chỉ tiêu đo được|

### **3.2. WP2 – Thiết kế hệ thống** 

|**Mã**|**Gói công việc**|**Sản phẩm đầu ra**|**Người thực hiện**|**Thời lượng**|**Phụ thuộc**|**Tiêu chí hoàn thành**|
|---|---|---|---|---|---|---|
|2.1|Thiết kế state & objects|Sơ đồ state 3 graph; schema `Analyst`, feedback, section|[ĐIỀN HỌ TÊN] (tự thực hiện)|2 ngày|1.3|Vẽ được trên giấy trước khi code; reducer khai báo rõ|
|2.2|Thiết kế luồng điều phối|Sơ đồ node/edge; thiết kế interrupt; thiết kế fan-out/fan-in|[ĐIỀN HỌ TÊN] (tự thực hiện)|3 ngày|2.1|Sơ đồ khớp kiến trúc Chương 3 báo cáo; đủ 2 vòng lặp (feedback, max_turns)|
|2.3|Thiết kế prompt v1|Khung 5 quy tắc + bản mẫu prompt các node|[ĐIỀN HỌ TÊN] (tự thực hiện)|2 ngày|2.1|Prompt persona sinh được ≥ 3 góc nhìn khác biệt khi thử thô|

### **3.3. WP3 – Triển khai** 

|**Mã**|**Gói công việc**|**Sản phẩm đầu ra**|**Người thực hiện**|**Thời lượng**|**Phụ thuộc**|**Tiêu chí hoàn thành**|
|---|---|---|---|---|---|---|
|3.1|Hạ tầng & khung repo|Repo `uv`-ready, `.env`, `langgraph.json`, dev server chạy được|[ĐIỀN HỌ TÊN] (tự thực hiện)|1 ngày|1.1|`uv run langgraph dev` mở được Studio với graph rỗng|
|3.2|Graph `create_analysts` + HITL|Persona sinh đúng schema; interrupt dừng/approve/feedback; vòng tái sinh|[ĐIỀN HỌ TÊN] (tự thực hiện)|4 ngày|2.2, 2.3, 3.1|Chạy được M2: sinh → duyệt → feedback → sinh lại trong Studio|
|3.3|Subgraph `answer_question`|Vòng ask↔search↔answer grounding + memo|[ĐIỀN HỌ TÊN] (tự thực hiện)|5 ngày|2.2, 2.3, 3.1|1 interview end-to-end với context + URL; thoát đúng `max_turns`|
|3.4|Graph `deep_agent` tích hợp|Fan-out N subgraph; sections; report 4 phần + nguồn|[ĐIỀN HỌ TÊN] (tự thực hiện)|5 ngày|3.2, 3.3|Demo topic thật ra Markdown đủ mở đầu–nội dung–kết luận–nguồn (M3)|
|3.5|Hardening|Validation, retry/timeout, log + telemetry|[ĐIỀN HỌ TÊN] (tự thực hiện)|2 ngày|3.4|Không kịch bản nào treo/lặp vô hạn; log đủ tính chỉ số 4.2 (BC)|

### **3.4. WP4 – Kiểm thử & Đánh giá** 

|**Mã**|**Gói công việc**|**Sản phẩm đầu ra**|**Người thực hiện**|**Thời lượng**|**Phụ thuộc**|**Tiêu chí hoàn thành**|
|---|---|---|---|---|---|---|
|4.1|Kiểm thử|Test suite + biên bản theo ma trận 9 nhóm|[ĐIỀN HỌ TÊN] (tự thực hiện)|4 ngày|3.5|100% test P0 pass; lỗi ghi issue, fix trong 48h|
|4.2|Đánh giá chất lượng|Bộ [≥6] phiên thực nghiệm; bảng 7 tiêu chí; phân tích cost/latency|[ĐIỀN HỌ TÊN] (tự thực hiện)|4 ngày|3.5, 4.1|Số liệu điền đủ vào Chương 4 báo cáo; tự chấm rubric + đối chiếu chéo|

### **3.5. WP5 – Tài liệu & Demo** 

|**Mã**|**Gói công việc**|**Sản phẩm đầu ra**|**Người thực hiện**|**Thời lượng**|**Phụ thuộc**|**Tiêu chí hoàn thành**|
|---|---|---|---|---|---|---|
|5.1|Tài liệu|README, Action Plan, Báo cáo cuối kỳ + WBS, phụ lục|**[ĐIỀN HỌ TÊN]** (tự thực hiện)|6 ngày (rải)|1.3, 4.2|Báo cáo đúng mẫu môn học, không còn placeholder `[ĐIỀN]` trước ngày nộp|
|5.2|Demo & bảo vệ|Kịch bản demo, video/ảnh chụp Studio, slide, buổi trình bày|[ĐIỀN HỌ TÊN] (tự thực hiện)|3 ngày|5.1, 4.1|Tổng duyệt pass; demo chạy live không lỗi ở 2 chủ đề đã chốt|

## **4. Lịch trình tổng hợp (Gantt theo tuần)** 

|**WBS**|**Hạng mục**|**W1**|**W2**|**W3**|**W4**|
|---|---|---|---|---|---|
|1|Khảo sát & phân tích|████| | | |
|2|Thiết kế|██|███| | |
|3.1–3.2|Hạ tầng + create_analysts| |████| | |
|3.3|Interview subgraph| |██|███| |
|3.4–3.5|Tích hợp + hardening| | |████|█|
|4.1|Kiểm thử| | |█|███|
|4.2|Đánh giá| | | |███|
|5.1|Tài liệu|█|█|█|██|
|5.2|Demo & nộp| | | |███|
|**Mốc**| |**M1**|**M2**|**M3**|**M4**|

## **5. Tổng hợp phân công theo hạng mục (thực hiện cá nhân)** 

|**Người thực hiện**|**Vai trò**|**Gói công việc đảm nhiệm**|**Tổng ngày**|
|---|---|---|---|
|[ĐIỀN HỌ TÊN]|Kiến trúc & tích hợp|1.1, 2.2, 3.2, 3.4|≈ 15 ngày|
|[ĐIỀN HỌ TÊN]|AI / Prompt Engineer|1.2, 2.1, 2.3, 4.2|≈ 13 ngày|
|[ĐIỀN HỌ TÊN]|Backend / Agent Developer|1.3, 3.1, 3.3, 3.5, 4.1|≈ 16 ngày|
|[ĐIỀN HỌ TÊN]|QA & Documentation|5.1, 5.2|≈ 9 ngày|

> Cân đối tải: toàn bộ ~53 người-ngày quy về một người thực hiện độc lập trong 20 ngày lịch, nhờ làm việc toàn thời gian cho đề tài và các hạng mục chạy song song được (test viết sớm, tài liệu rải đều); phần dè dặt (~15–20% quỹ thời gian) dành cho phát sinh fix bug. Không có cơ chế backup nội bộ — rủi ro single-point-of-failure được quản lý bằng cách cắt phạm vi (xem Mục 6). 

## **6. Điểm kiểm soát và cơ chế báo cáo tiến độ** 

|**Thời điểm**|**Kiểm tra**|**Người duyệt**|**Hành động nếu lệch**|
|---|---|---|---|
|Đầu tuần hằng tuần|Lập kế hoạch tuần, xác nhận phụ thuộc WP|[ĐIỀN HỌ TÊN] (tự review)|Dồn lịch, gói nguy cơ chậm làm trước|
|Cuối tuần|Đối chiếu deliverable với mức '% hoàn thành'|[ĐIỀN HỌ TÊN] + giảng viên (checkpoint)|Gói chậm ≥ 2 ngày: cut phạm vi, không tăng người (đề tài cá nhân)|
|Cuối W1 (M1)|Phạm vi + kiến trúc chốt|Giảng viên|Không code tiếp khi M1 chưa đạt|
|Cuối W2 (M2)|Persona + 1 interview chạy được|Tự nghiệm thu theo DoD|Dời fan-out sang W3|
|Cuối W3 (M3)|E2E + báo cáo mẫu đầu tiên|Tự nghiệm thu theo DoD|Hạn chế thêm tính năng, chỉ fix|
|Cuối W4 (M4)|Test pass, tài liệu, demo|Giảng viên|— (bàn giao)|

## **7. Ước lượng nguồn lực tổng thể** 

|**Hạng mục**|**Ước lượng**|**Ghi chú**|
|---|---|---|
|Nhân sự|01 người × 20 ngày làm việc tập trung|Phạm vi đã thiết kế tương ứng khối lượng bài tập cá nhân|
|Chi phí API|≈ 30–60 USD toàn dự án|[≥20] phiên thực nghiệm × 0,1–0,5 USD (Mục 5.3 Action Plan)|
|Hạ tầng|Máy cá nhân + LangGraph Studio (free tier)|Không cần server riêng|
|Dụng cụ|GitHub free, `uv`, VS Code|Chi phí 0|

--- 

*Tài liệu WBS này là một phần của hồ sơ dự án môn Phát triển hệ thống thông minh, thống nhất với mã gói công việc Mục 4.3 của Kế hoạch dự án (Action Plan) và Chương 3–4 của Báo cáo cuối kỳ.* 
