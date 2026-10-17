### **MÔN PHÁT TRIỂN HỆ THỐNG THÔNG MINH**

# **KẾ HOẠCH DỰ ÁN (ACTION PLAN)**

_Trợ lý nghiên cứu đa tác tử sử dụng LangGraph_

| **Họ và tên**            | [ĐIỀN HỌ TÊN]         |
| ------------------------ | --------------------- |
| **MSSV**                 | [ĐIỀN MSSV]           |
| **Giảng viên hướng dẫn** | [ĐIỀN TÊN GIẢNG VIÊN] |
| **Lớp / Mã lớp**         | [ĐIỀN LỚP]            |
| **Ngày nộp**             | [DD/MM/YYYY]          |

## **1. Thông tin dự án**

| **Hạng mục**        | **Nội dung**                                                                               |
| ------------------- | ------------------------------------------------------------------------------------------ |
| Tên đề tài          | Xây dựng Trợ lý Nghiên cứu Đa tác tử (Multi-Agent<br>Research Assistant) sử dụng LangGraph |
| Môn học             | Phát triển hệ thống thông minh                                                             |
| Mã môn học          | [ĐIỀN MÃ MÔN]                                                                              |
| Họ và tên / MSSV    | [ĐIỀN HỌ TÊN] / [ĐIỀN MSSV]                                                                |
| Loại bài tập        | Bài tập lớn cá nhân — tự xây dựng và tự nghiên cứu                                         |
| Kho mã nguồn        | LangGraph_Research_Assistant_Agent (repo cá nhân)                                          |
| Thời lượng dự kiến  | 04 tuần / 20 ngày làm việc                                                                 |
| Nền tảng phát triển | Python 3.12+, LangGraph CLI/Studio, uv                                                     |
| Công nghệ cốt lõi   | LangGraph, LangChain, DeepSeek API,<br>Tavily Search API, Pydantic                         |
| Hình thức làm việc  | Cá nhân, tự quản lý tiến độ<br>qua Git/GitHub                                              |

## **2. Mục tiêu**

### **2.1. Tính cấp thiết của đề tài**

Các mô hình ngôn ngữ lớn (LLM) ngày nay có khả năng đọc, tổng hợp và viết nội dung ở mức gần con người, nên được kỳ vọng trở thành công cụ hỗ trợ nghiên cứu khoa học và phân tích thông tin. Tuy nhiên, một lời gọi chat đơn lẻ tồn tại ba hạn chế rõ rệt: (i) khó bao phủ nhiều góc nhìn chuyên môn trên cùng một chủ đề; (ii) dễ sinh ra nội dung "trông hợp lý nhưng không có căn cứ" (hallucination) do không truy vết được nguồn; (iii) không duy trì được một quy trình nghiên cứu nhiều bước với trạng thái, vòng lặp và điểm tương tác của con người.

Hướng tiếp cận đa tác tử (multi-agent) kết hợp điều phối theo đồ thị (graph orchestration) giải quyết đúng ba hạn chế trên: mỗi "nhà phân tích" ảo đảm nhận một persona chuyên biệt, trạng thái hội thoại được lưu có kiểm soát, luồng xử lý biểu diễn tường minh bằng node/edge cho phép quan sát, tạm dừng và thử lại. Trong số các framework hiện có (AutoGen, CrewAI, LangGraph), LangGraph được lựa chọn vì mô hình StateGraph với reducer, conditional edge, interrupt và Send API phù hợp nhất với bài toán có both vòng lặp và fan-out song song, đồng thời có LangGraph Studio hỗ trợ debug trực quan — phù hợp yêu cầu báo cáo và demo của môn học.

Đề tài vì vậy vừa mang tính học thuật (nắm vững cơ chế hoạt động của hệ thống tác tử hiện đại) vừa mang tính thực hành (tạo ra sản phẩm chạy được, demo được), đáp ứng đúng chuẩn đầu ra của môn Phát triển hệ thống thông minh.

### **2.2. Mục tiêu tổng quát**

Xây dựng và đánh giá một trợ lý nghiên cứu tự động, đa tác tử, dựa trên LangGraph, có khả năng đi từ một chủ đề nghiên cứu đầu vào đến một báo cáo Markdown hoàn chỉnh có trích dẫn nguồn, với sự phê duyệt của con người ở bước trung gian.

### **2.3. Mục tiêu cụ thể và tiêu chí đo lường**

| **#** | **Mục tiêu cụ thể**                                                                  | **Tiêu chí đánh giá (KPI)**                                                |
| ----- | ------------------------------------------------------------------------------------ | -------------------------------------------------------------------------- |
| MT1   | Sinh tự động nhóm analyst persona (tên,<br>vai trò, affiliation, góc nhìn) từ chủ đề | Đúng số lượng yêu cầu (≤ max_analysts),<br>parse đúng Pydantic schema 100% |
| MT2   | Tích hợp human-in-the-loop: người dùng<br>duyệt hoặc phản hồi yêu cầu tạo lại        | Graph dừng đúng điểm interrupt,<br>tiếp tục đúng nhánh sau feedback        |
| MT3   | Triển khai luồng phỏng vấn song song<br>cho từng analyst qua Send API                | N analyst → N subgraph chạy độc lập,<br>kết quả gom đủ khi fan-in          |
| MT4   | Mỗi câu trả lời trong phỏng vấn được<br>grounding trên kết quả tìm kiếm web          | Tỷ lệ câu trả lời có citation/URL<br>đạt mục tiêu đề ra trong test         |
| MT5   | Tổng hợp transcript thành báo cáo Markdown<br>gồm mở đầu, nội dung, kết luận, nguồn  | Đủ 4 phần, đủ số section tương ứng<br>số analyst, không mất dữ liệu        |
| MT6   | Đóng gói mã nguồn, test và tài liệu<br>theo chuẩn đồ án sinh viên                    | Chạy được `uv run langgraph dev`,<br>bộ test pass, báo cáo hoàn tất        |

### **2.4. Đối tượng nghiên cứu**

- Kiến trúc và cơ chế của LangGraph: StateGraph, node, edge, conditional edge, reducer, `interrupt`, `Send`, checkpointer.
- Mẫu thiết kế hệ thống đa tác tử: persona agent, supervisor/orchestrator, fan-out/fan-in, map-reduce synthesis.
- Kỹ thuật prompt engineering và structured output (Pydantic) để kiểm soát hành vi LLM.
- Tích hợp retrieval theo thời gian chạy bằng Tavily Search API và sinh truy vấn từ ngữ cảnh hội thoại.

### **2.5. Phạm vi nghiên cứu**

- **Nội dung:** 03 graph đăng ký trong `langgraph.json` — `create_analysts` (sinh và duyệt persona), `answer_question` (subgraph phỏng vấn đơn), `deep_agent` (điều phối toàn trình). Không huấn luyện/fine-tune mô hình; chỉ sử dụng mô hình nền tảng qua API.
- **Không gian sản phẩm:** giao diện làm việc là LangGraph Studio/CLI; đầu ra là file Markdown. Không xây dựng web app thương mại, không quản lý tài khoản người dùng.
- **Thời gian:** 04 tuần, giới hạn tài nguyên là API key cá nhân với chi phí kiểm soát được.
- **Dữ liệu:** chủ đề nghiên cứu do người dùng nhập; nguồn là kết quả web search thời gian chạy, không dùng cơ sở dữ liệu tĩnh.

## **3. Tóm tắt**

Đề tài triển khai một trợ lý nghiên cứu dựa trên LangGraph và LangChain. Khi nhận chủ đề, hệ thống dùng mô hình ngôn ngữ để sinh nhóm analyst persona có chuyên môn và quan điểm bổ sung cho nhau (structured output theo schema Pydantic). Người dùng có thể duyệt hoặc yêu cầu tạo lại danh sách analyst thông qua điểm dừng `interrupt` — bảo đảm nguyên tắc human-in-the-loop trước bước tiêu tốn chi phí. Sau khi được phê duyệt, hệ thống dùng Send API để fan-out một phiên phỏng vấn độc lập cho mỗi analyst; trong mỗi phiên, agent tự đặt câu hỏi, sinh truy vấn tìm kiếm Tavily, thu thập tài liệu kèm URL, trả lời dựa trên ngữ cảnh retrieved và lặp tới khi đạt `max_turns`. Các transcript được chuyển thành section, rồi hợp nhất theo mô hình map-reduce (viết introduction, body, conclusion, nguồn) thành báo cáo Markdown cuối cùng có trích dẫn.

Sản phẩm minh họa đầy đủ các mẫu thiết kế agent quan trọng của hệ thống thông minh hiện đại và là cơ sở để đánh giá chất lượng hệ thống theo các tiêu chí: grounding, citation, coverage, độ ổn định luồng và trải nghiệm người dùng.

## **4. Phương pháp**

### **4.1. Cách tiếp cận tổng thể**

Tôi áp dụng mô hình phát triển **iterative prototype** (làm mẫu nhiều vòng), phù hợp với hệ thống AI phụ thuộc hành vi mô hình nền: khảo sát → thiết kế khung → dựng prototype từng phần → chạy thử với chủ đề thật → đo lường và tinh chỉnh prompt/schema → hoàn thiện. Mỗi vòng lặp ghi lại nhật ký phiên chạy để phục vụ phần đánh giá của báo cáo cuối kỳ.

### **4.2. Phương pháp theo giai đoạn**

| **Giai đoạn** | **Phương pháp**                                                                                                    | **Sản phẩm**                                     |
| ------------- | ------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------ |
| Khảo sát      | Tự nghiên cứu tài liệu chính thức<br>LangGraph/LangChain và các công trình<br>agent/RAG; phác họa kiến trúc từ đầu | Bản phân tích yêu cầu và<br>kiến trúc hệ thống   |
| Thiết kế      | Mô hình hóa state, node, edge,<br>routing, điểm interrupt, sơ đồ<br>fan-out/fan-in                                 | Sơ đồ luồng, mô hình dữ liệu,<br>schema Pydantic |
| Triển khai    | Python 3.12+, LangGraph,<br>LangChain, DeepSeek, Tavily;<br>quản lý nhánh trên Git                                 | Ứng dụng research assistant<br>chạy được 3 graph |
| Kiểm thử      | Unit test cho node/edge, integration<br>test từng graph, end-to-end test<br>kịch bản demo, đánh giá prompt/output  | Bộ test và biên bản kiểm thử                     |
| Đánh giá      | Ch chấm theo tiêu chí relevance,<br>grounding, citation, completeness<br>trên nhiều chủ đề; so sánh có/không HITL  | Bảng kết quả đánh giá,<br>báo cáo cuối kỳ        |

### **4.3. Phân rã công việc (WBS)**

| **Mã WP** | **Gói công việc**                    | **Sản phẩm chính**                     |
| --------- | ------------------------------------ | -------------------------------------- |
| 1         | Khảo sát và phân tích yêu cầu        | Tài liệu yêu cầu, bản vẽ lại kiến trúc |
| 1.1       | Đọc mã nguồn/README repo tham khảo   | Bảng ánh xạ file → chức năng           |
| 1.2       | Học tài liệu LangGraph/LangChain     | Ghi chú cơ chế state/reducer/interrupt |
| 2         | Thiết kế hệ thống                    | Sơ đồ graph, schema, prompt design     |
| 2.1       | Thiết kế states và objects           | `states.py`, `objects.py`              |
| 2.2       | Thiết kế node/edge và routing        | Sơ đồ luồng 3 graph                    |
| 3         | Triển khai                           | Source code chạy được                  |
| 3.1       | Graph `create_analysts` + HITL       | Persona + interrupt + feedback loop    |
| 3.2       | Subgraph `answer_question`           | ask ↔ search ↔ answer ↔ save           |
| 3.3       | Graph `deep_agent` + synthesis       | Fan-out, sections, final report        |
| 3.4       | Cấu hình env, models, langgraph.json | Repo dev-ready                         |
| 4         | Kiểm thử và đánh giá                 | Test suite, biên bản, bảng số liệu     |
| 5         | Tài liệu và demo                     | Báo cáo cuối kỳ, slide, kịch bản demo  |

### **4.4. Công cụ và môi trường phát triển**

| **Hạng mục**       | **Chi tiết**                                                                                                                   |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------ |
| Ngôn ngữ / runtime | Python 3.12+                                                                                                                   |
| Quản lý gói        | `uv` (`uv sync`, `uv run`)                                                                                                     |
| Orchestration      | LangGraph (`StateGraph`, `Send`, `interrupt`)                                                                                  |
| LLM & tooling      | LangChain, `ChatDeepSeek` (`langchain-deepseek`,<br>`deepseek-chat` / `deepseek-reasoner`), `langchain-tavily` hoặc Tavily API |
| Validation         | Pydantic (structured output)                                                                                                   |
| Bảo mật            | `python-dotenv`, `.env`, `.gitignore`                                                                                          |
| Dev/debug          | LangGraph CLI + LangGraph Studio, VS Code                                                                                      |
| VCS                | Git / GitHub (branch theo tính năng)                                                                                           |

### **4.5. Phương pháp bảo đảm chất lượng**

- Self-review theo checklist trước khi merge vào `main`; mỗi tuần đối chiếu tiến độ với kế hoạch WBS ít nhất một lần.
- Mỗi node có docstring mô tả input/output theo state; thay đổi prompt phải kèm kết quả chạy thử lưu vào thư mục `logs/`.
- Khóa API đặt tại `.env`, kiểm tra secret trước khi push; không commit output chứa thông tin nhạy cảm.

## **5. Dữ liệu**

### **5.1. Phân loại dữ liệu của hệ thống**

| **Nhóm**   | **Thành phần**                                                                                                     | **Hình thức**                            |
| ---------- | ------------------------------------------------------------------------------------------------------------------ | ---------------------------------------- |
| Đầu vào    | Topic nghiên cứu, `max_analysts`,<br>phản hồi người dùng                                                           | Text, số nguyên                          |
| Trung gian | Analyst persona có cấu trúc, câu hỏi<br>phỏng vấn, search query, tài liệu web<br>kèm URL, hội thoại, memo, section | Pydantic object /<br>message list / dict |
| Đầu ra     | Báo cáo Markdown final (mở đầu, nội<br>dung, kết luận, danh sách nguồn)                                            | Text file                                |

### **5.2. Nguyên tắc quản lý dữ liệu**

- Không huấn luyện mô hình mới; hệ thống dùng mô hình nền tảng qua API và xử lý dữ liệu ở thời điểm chạy (runtime retrieval).
- Khóa API quản lý qua biến môi trường, không đưa vào repository; báo cáo chỉ dùng số liệu ẩn danh của các phiên chạy thử.
- Mỗi phiên demo lưu transcript và final report làm phụ lục báo cáo, là căn cứ cho phần đánh giá.

### **5.3. Ước lượng chi phí tài nguyên**

| **Hạng mục**    | **Ước lượng 1 phiên (3 analyst, 3 turn)** | **Ghi chú**                                          |
| --------------- | ----------------------------------------- | ---------------------------------------------------- |
| Lời gọi LLM     | ≈ 15–25 calls                             | persona, question, answer,<br>section, report writer |
| Tìm kiếm Tavily | ≈ 9–15 calls                              | 1 query/turn/analyst                                 |
| Token           | ≈ 50–150K tokens                          | tùy độ dài context                                   |
| Chi phí API     | ≈ 0,1–0,5 USD/phiên                       | giới hạn bởi `max_analysts`,<br>`max_turns`          |

## **6. Đầu ra mong muốn**

### **6.1. Sản phẩm phần mềm**

- Mã nguồn chạy được cho cả 3 graph (`create_analysts`, `answer_question`, `deep_agent`), cấu hình `langgraph.json` cho môi trường phát triển/Studio.
- Báo cáo nghiên cứu có cấu trúc, có URL nguồn, phân biệt rõ các góc nhìn phân tích.
- Cơ chế duyệt persona qua `interrupt` và chạy lại khi có feedback của người dùng.
- Bộ test cho node/edge quan trọng và kịch bản demo end-to-end phục vụ buổi bảo vệ.

### **6.2. Sản phẩm tài liệu**

- Báo cáo cuối kỳ theo mẫu môn học, WBS, hướng dẫn cài đặt (README), biên bản kiểm thử và phần giới hạn hệ thống.
- Slide trình bày và video/ghi chú demo (nếu giảng viên yêu cầu).

### **6.3. Tiêu chí nghiệm thu**

| **Đầu ra**        | **Tiêu chí chấp nhận**                                |
| ----------------- | ----------------------------------------------------- |
| Graph hoạt động   | End-to-end chạy không lỗi với ≥ 2 chủ đề thử          |
| Human-in-the-loop | Dừng đúng interrupt; feedback dẫn tới tạo lại persona |
| Báo cáo           | Đủ 4 phần + danh sách nguồn, URL truy cập được        |
| Kiểm thử          | 100% test case nhóm P0 pass                           |
| Tài liệu          | Báo cáo, README, slide nộp trước deadline             |

## **7. Phân công vai trò**

### **7.1. Các vai trò kỹ thuật do một người đảm nhận**

Toàn bộ đề tài do tôi ([ĐIỀN HỌ TÊN]) thực hiện độc lập; các "vai trò" dưới đây là các hạng mục chuyên môn tôi lần lượt đảm nhiệm:

| **Hạng mục**            | **Người thực hiện** | **Trách nhiệm chính**                                                                                         |
| ----------------------- | ------------------- | ------------------------------------------------------------------------------------------------------------- |
| Kiến trúc & điều phối   | [ĐIỀN HỌ TÊN]       | Định phạm vi, thiết kế kiến trúc graph,<br>tích hợp `deep_agent`, quản lý tiến độ,<br>làm việc với giảng viên |
| AI / Prompt Engineering | [ĐIỀN HỌ TÊN]       | Thiết kế prompt, Pydantic schema,<br>đánh giá chất lượng output, bảng tiêu chí                                |
| Backend / Agent Dev     | [ĐIỀN HỌ TÊN]       | Cài đặt node/edge/state, tích hợp<br>DeepSeek và Tavily, fan-out Send API                                     |
| QA & Documentation      | [ĐIỀN HỌ TÊN]       | Lập test plan, chạy test, chuẩn bị<br>demo, tổng hợp báo cáo và tài liệu                                      |

### **7.2. Kế hoạch tự giám sát theo gói việc**

| **Gói việc**        | **Người thực hiện** | **Cơ chế tự giám sát**                                                |
| ------------------- | ------------------- | --------------------------------------------------------------------- |
| Yêu cầu & kiến trúc | [ĐIỀN HỌ TÊN]       | Decision log mỗi lần đổi phạm vi/thiết kế; chốt với giảng viên tại M1 |
| Prompt & schema     | [ĐIỀN HỌ TÊN]       | Nhật ký phiên chạy lưu `logs/` cho mỗi phiên bản prompt               |
| Graph & tích hợp    | [ĐIỀN HỌ TÊN]       | Demo nội bộ theo milestone M2–M4; checklist nghiệm thu từng graph     |
| Retrieval (Tavily)  | [ĐIỀN HỌ TÊN]       | Thống kê citation/độ phủ nguồn trên mỗi phiên chạy thử                |
| Kiểm thử & đánh giá | [ĐIỀN HỌ TÊN]       | Biên bản test cập nhật hằng tuần; lỗi ghi issue, hạn fix 48h          |
| Báo cáo & demo      | [ĐIỀN HỌ TÊN]       | Self-review slide và kịch bản demo trước buổi tổng duyệt              |

## **8. Tóm tắt lịch trình**

### **8.1. Theo tuần**

| **Tuần** | **Trọng tâm**                                                            | **Mốc hoàn thành**                  |
| -------- | ------------------------------------------------------------------------ | ----------------------------------- |
| W1       | Khảo sát tài liệu, phân tích repo,<br>chốt yêu cầu và thiết kế kiến trúc | M1: Scope và kiến trúc được chốt    |
| W2       | Triển khai graph `create_analysts`<br>và subgraph `answer_question`      | M2: Luồng đơn (1 analyst) chạy được |
| W3       | Fan-out song song, synthesis,<br>UI/Studio, kiểm thử và fix              | M3: End-to-end hoàn chỉnh           |
| W4       | Đánh giá theo tiêu chí, cải tiến,<br>viết báo cáo, tổng duyệt demo       | M4: Bàn giao sản phẩm + báo cáo     |

### **8.2. Chi tiết công việc theo tuần**

| **Tuần** | **Công việc**                                                                                                 | **Người chính** | **Sản phẩm kiểm chứng**        |
| -------- | ------------------------------------------------------------------------------------------------------------- | --------------- | ------------------------------ |
| W1       | Đọc tài liệu LangGraph; vẽ sơ đồ 3 graph; thống nhất schema state/object; dựng repo, cấu hình `.env`, `uv`    | [ĐIỀN HỌ TÊN]   | Sơ đồ kiến trúc, repo khởi tạo |
| W2       | Node sinh persona + structured output; điểm interrupt và logic feedback; vòng ask→search→answer của subgraph  | [ĐIỀN HỌ TÊN]   | Graph 1 chạy trong Studio      |
| W3       | Send API fan-out; reducer gom section; node writer (intro/body/conclusion/sources); retry/timeout; test suite | [ĐIỀN HỌ TÊN]   | Báo cáo demo đầu tiên          |
| W4       | Chạy bộ chủ đề đánh giá; hoàn thiện bảng số liệu; viết báo cáo, slide; tổng duyệt và nộp                      | [ĐIỀN HỌ TÊN]   | Báo cáo cuối kỳ + demo         |

### **8.3. Mốc và tiêu chí hoàn thành**

| **Mốc** | **Nội dung**         | **Tiêu chí hoàn thành**                      |
| ------- | -------------------- | -------------------------------------------- |
| M1      | Yêu cầu và kiến trúc | Sơ đồ graph/state được giảng viên ghi nhận   |
| M2      | Prototype            | Persona + một interview end-to-end           |
| M3      | Integration          | Interview song song + final report đủ 4 phần |
| M4      | Completion           | Test pass, demo đạt, tài liệu hoàn tất       |

## **9. Rủi ro và biện pháp**

### **9.1. Danh mục rủi ro**

| **Rủi ro**                                                        | **Khả năng** | **Tác động** | **Biện pháp phòng ngừa**                                                     | **Phương án dự phòng**                                                                               |
| ----------------------------------------------------------------- | ------------ | ------------ | ---------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| Nguồn web kém tin cậy,<br>thông tin trái chiều                    | Cao          | Cao          | Ưu tiên domain chính thống,<br>giữ URL, yêu cầu cross-check                  | Gắn nhãn độ tin cậy theo loại<br>nguồn, loại nguồn yếu                                               |
| Hallucination trong<br>câu trả lời                                | Cao          | Cao          | Bắt buộc trả lời theo context<br>và trích dẫn kèm URL                        | Thử lại truy vấn, siết prompt<br>"no context → say not found"                                        |
| Chi phí/giới hạn API<br>vượt dự kiến                              | Trung bình   | Trung bình   | Giới hạn `max_analysts`/<br>`max_turns`, cache, theo dõi<br>token từng phiên | Chạy demo bằng kịch bản<br>đã ghi sẵn, chuyển `deepseek-reasoner`<br>về `deepseek-chat` cho node phụ |
| Luồng graph lặp vô hạn,<br>deadlock routing                       | Trung bình   | Cao          | `max_turns`, điều kiện thoát,<br>test routing bằng unit test                 | Thêm hard-limit turn toàn cục                                                                        |
| Lộ khóa API                                                       | Thấp         | Cao          | `.env` + `.gitignore`,<br>secret scan trước push                             | Xoay (rotate) key ngay,<br>báo giảng viên nếu xảy ra                                                 |
| Mất tiến độ do làm việc đơn độc,<br>một người ôm toàn bộ hạng mục | Trung bình   | Trung bình   | Kế hoạch tuần có buffer 15–20%,<br>review tiến độ cuối tuần theo WBS         | Cắt phạm vi gói tùy chọn,<br>dời milestone trong 48h                                                 |
| Repo tham khảo thay đổi/<br>API breaking update                   | Thấp         | Trung bình   | Khóa version trong `uv`,<br>ghi changelog khi upgrade                        | Downgrade, cô lập bug,<br>báo cáo trong phụ lục                                                      |

### **9.2. Giám sát rủi ro**

Danh mục rủi ro được cập nhật mỗi buổi họp cuối tuần; rủi ro chuyển mức "đỏ" (khả năng cao × tác động cao) phải có hành động trong 48h và được báo cáo trong checkpoint gửi giảng viên.

## **10. Nhận xét của giáo viên**

[PHẦN DÀNH CHO GIẢNG VIÊN]

---

---
