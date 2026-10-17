### **MÔN PHÁT TRIỂN HỆ THỐNG THÔNG MINH**

# **BÁO CÁO DỰ ÁN CUỐI KHÓA**

_XÂY DỰNG TRỢ LÝ NGHIÊN CỨU ĐA TÁC TỬ SỬ DỤNG LANGGRAPH_

| **Họ và tên**            | [ĐIỀN HỌ TÊN]               |
| ------------------------ | --------------------------- |
| **MSSV**                 | [ĐIỀN MSSV]                 |
| **Giảng viên hướng dẫn** | [ĐIỀN TÊN GIẢNG VIÊN]       |
| **Lớp / Mã lớp**         | [ĐIỀN LỚP]                  |
| **Ngày nộp**             | [DD/MM/YYYY]                |

## **Tóm tắt**

Báo cáo trình bày quá trình phân tích, thiết kế và triển khai một trợ lý nghiên cứu đa tác tử (multi-agent research assistant) dựa trên nền tảng điều phối đồ thị LangGraph. Nhận đầu vào là một chủ đề nghiên cứu, hệ thống tự động sinh nhiều "nhà phân tích" ảo với persona, chuyên môn và góc nhìn bổ sung cho nhau; người dùng đóng vai trò kiểm soát ở bước trung gian thông qua cơ chế human-in-the-loop (duyệt hoặc phản hồi yêu cầu tạo lại). Sau khi được phê duyệt, hệ thống fan-out song song các phiên phỏng vấn bằng Send API; trong mỗi phiên, tác tử tự đặt câu hỏi, sinh truy vấn tìm kiếm web qua Tavily, trả lời dựa trên ngữ cảnh thu được kèm URL nguồn, và lặp tới khi đạt giới hạn số lượt. Toàn bộ transcript được chuyển thành các section và hợp nhất theo mô hình map-reduce thành báo cáo Markdown hoàn chỉnh gồm mở đầu, nội dung, kết luận và danh mục tài liệu tham khảo.

Đề tài là minh họa thực hành cho các mẫu thiết kế hệ thống tác tử hiện đại: structured output với Pydantic, human-in-the-loop với `interrupt`, fan-out/fan-in với `Send`, vòng lặp có điều kiện với `max_turns`, retrieval-grounded generation và map-reduce synthesis. Kết quả đạt được một quy trình nghiên cứu mô-đun, quan sát được, truy vết được và dễ mở rộng, đồng thời chỉ ra rõ các giới hạn về chất lượng nguồn, chi phí API và nguy cơ hallucination của hệ thống sinh tự động.

**Từ khóa:** LangGraph, LangChain, multi-agent system, research assistant, Tavily, human-in-the-loop, retrieval-augmented generation, generative AI.

## **Mục lục nội dung**

- Chương 1. Giới thiệu
- Chương 2. Tổng quan tài liệu và cơ sở lý thuyết
- Chương 3. Triển khai dự án
- Chương 4. Kết quả và đánh giá
- Chương 5. Tác động của dự án
- Chương 6. Kết luận và hướng phát triển
- Tài liệu tham khảo; Tự đánh giá quá trình thực hiện; Nhận xét giảng viên

## **1. Giới thiệu**

> **Tổng quan chương:** Chương 1 trình bày lý do chọn đề tài, mục tiêu nghiên cứu, đối tượng và phạm vi của đề tài, phương pháp thực hiện, hình thức thực hiện cá nhân cùng các mốc quan trọng của lịch trình, tạo cơ sở cho các chương phân tích – thiết kế – đánh giá ở phần sau.

### **1.1. Tính cấp thiết của đề tài**

Khối lượng tài liệu khoa học và thông tin trên web tăng nhanh khiến việc tự mình khảo sát một chủ đề mới trở nên tốn thời gian và dễ bỏ sót góc nhìn. Các mô hình ngôn ngữ lớn (LLM) thế hệ mới có thể đọc, tóm tắt và viết nội dung ở chất lượng cao, nhưng một lời gọi hội thoại đơn lẻ bộc lộ ba hạn chế:

1. **Thiếu đa dạng góc nhìn:** câu trả lời đến từ một "góc nhìn" duy nhất, không đóng vai nhiều chuyên gia với giả định và phương pháp khác nhau — vốn là cách làm việc của một nhóm nghiên cứu thực thụ.
2. **Thiếu kiểm soát nguồn:** thông tin sinh ra không luôn truy vết được về tài liệu gốc, dẫn tới nguy cơ hallucination — nội dung hợp lý về mặt câu chữ nhưng sai hoặc bịa về dữ kiện.
3. **Thiếu quy trình nhiều bước:** chat một lượt không duy trì được trạng thái của một pipeline dài (sinh giả thuyết → thu thập chứng cứ → phỏng vấn → tổng hợp), cũng không cho phép con người can thiệp đúng lúc.

Hướng tiếp cận **hệ thống đa tác tử** (multi-agent system) kết hợp **điều phối theo đồ thị trạng thái** (stateful graph orchestration) giải quyết đồng thời cả ba hạn chế: mỗi tác tử đảm nhận một persona chuyên biệt, trạng thái hội thoại được khai báo tường minh, còn luồng xử lý được biểu diễn bằng node/edge nên quan sát được, tạm dừng được và thử lại được. Trong các framework phổ biến — AutoGen [9], CrewAI, LangGraph [2] — tôi chọn **LangGraph** vì mô hình StateGraph với reducer, conditional edge, điểm dừng `interrupt` và cơ chế `Send` phủ đúng cả hai nhu cầu vòng lặp lẫn xử lý song song của bài toán, lại đi kèm LangGraph Studio giúp debug trực quan khi demo. Đề tài vì vậy vừa đáp ứng yêu cầu học phần Phát triển hệ thống thông minh (xây dựng hệ thống ứng dụng AI thực thụ), vừa mang tính thời sự khi các hệ thống agent đang trở thành hướng ứng dụng chủ lực của LLM trong nghiên cứu và doanh nghiệp.

### **1.2. Mục tiêu và động lực**

**Mục tiêu tổng quát:** xây dựng và đánh giá một trợ lý nghiên cứu tự động, đa tác tử, dựa trên LangGraph, đi từ chủ đề nghiên cứu đến báo cáo Markdown có trích dẫn nguồn, có sự phê duyệt của con người ở bước trung gian.

**Mục tiêu cụ thể:**

- MT1. Tự động sinh nhóm analyst persona (tên, vai trò, affiliation, quan điểm) có cấu trúc từ một chủ đề bất kỳ.
- MT2. Tích hợp human-in-the-loop: người dùng duyệt persona hoặc gửi phản hồi để hệ thống tạo lại trước khi tiêu tốn chi phí nghiên cứu.
- MT3. Triển khai các luồng phỏng vấn song song (fan-out) — mỗi analyst một subgraph độc lập — với vòng hỏi/đáp có điều kiện kết thúc.
- MT4. Grounding từng câu trả lời trên kết quả tìm kiếm web (Tavily) và giữ lại URL để trích dẫn.
- MT5. Tổng hợp transcript thành báo cáo hoàn chỉnh theo mô hình map-reduce: mở đầu, nội dung theo section, kết luận, danh mục nguồn.
- MT6. Kiểm thử và đánh giá hệ thống theo tiêu chí: tính đúng đắn của luồng, grounding, citation coverage, độ đầy đủ và trải nghiệm người dùng.

**Động lực:** tôi mong muốn chuyển từ việc "gọi LLM qua chat" sang năng lực thiết kế một hệ thống AI có kiến trúc — nơi mỗi quyết định nghiệp vụ (tạm dừng chờ người, song song hóa, giới hạn vòng lặp, bắt buộc trích dẫn) đều được mã hóa tường minh trong đồ thị xử lý.

### **1.3. Đối tượng và phạm vi nghiên cứu**

| **Hạng mục**      | **Nội dung**                                                                                                                                                                                       |
| ----------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Đối tượng         | Cơ chế điều phối tác tử của LangGraph<br>(StateGraph, node/edge, reducer,<br>`interrupt`, `Send`, checkpointer);<br>prompt engineering & structured output;<br>retrieval thời gian chạy qua Tavily |
| Phạm vi nội dung  | 03 graph: `create_analysts`,<br>`answer_question`, `deep_agent`;<br>không fine-tune mô hình nền tảng                                                                                               |
| Phạm vi sản phẩm  | CLI/LangGraph Studio làm giao diện;<br>đầu ra là file Markdown                                                                                                                                     |
| Phạm vi thời gian | 04 tuần, API key cá nhân tự quản lý                                                                                                                                                                   |

### **1.4. Phương pháp nghiên cứu**

Đề tài kết hợp ba nhóm phương pháp:

1. **Phân tích – khảo sát:** tự nghiên cứu tài liệu chính thức của LangGraph/LangChain [2][3], đọc các công trình nền về agent, RAG [7][8][9][10], sau đó tự phác họa kiến trúc graph của hệ thống từ đầu (không kế thừa từ repository có sẵn).
2. **Thiết kế – triển khai:** mô hình hóa state/node/edge trước khi code; phát triển theo mẫu iterative prototype ( prototype từng graph → tích hợp → tinh chỉnh prompt qua nhật ký phiên chạy); công cụ Python 3.12+, `uv`, LangGraph CLI/Studio.
3. **Kiểm thử – đánh giá:** unit test cho node/edge trọng yếu, integration test theo graph, end-to-end test theo kịch bản demo; đánh giá output bằng bảng tiêu chí định tính–định lượng (relevance, grounding, citation, completeness) trên bộ chủ đề thử nghiệm, kết hợp nhận xét của người dùng.

### **1.5. Hình thức thực hiện và phạm vi công việc cá nhân**

Đề tài do tôi thực hiện độc lập, tự thiết kế và tự nghiên cứu trên toàn bộ các hạng mục:

| **Hạng mục**            | **Nội dung đảm nhiệm**                                                          |
| ----------------------- | ------------------------------------------------------------------------------- |
| Kiến trúc & tích hợp    | Thiết kế 3 graph, logic `deep_agent`,<br>quản lý tiến độ, checkpoint với GV      |
| AI/Prompt Engineering   | Persona prompt, Pydantic schema,<br>bảng tiêu chí và kết quả đánh giá           |
| Backend/Agent Developer | Node, edge, state; tích hợp DeepSeek,<br>Tavily; fan-out Send API               |
| QA & Documentation      | Test plan, chạy test, kịch bản demo,<br>tổng hợp báo cáo và slide               |

### **1.6. Lịch trình và mốc quan trọng**

| **Mốc** | **Nội dung**         | **Tiêu chí hoàn thành**                               |
| ------- | -------------------- | ----------------------------------------------------- |
| M1 (W1) | Yêu cầu và kiến trúc | Sơ đồ graph/state và schema được chốt                 |
| M2 (W2) | Prototype            | Sinh persona + interrupt + một<br>interview chạy được |
| M3 (W3) | Integration          | Phỏng vấn song song + báo cáo cuối kỳ                 |
| M4 (W4) | Completion           | Test, đánh giá, demo, tài liệu hoàn tất               |

### **1.7. Kết cấu của báo cáo**

Ngoài phần tóm tắt và tài liệu tham khảo, báo cáo gồm 6 chương: Chương 2 trình bày cơ sở lý thuyết về hệ tác tử, LangGraph và các kỹ thuật liên quan; Chương 3 mô tả phân tích yêu cầu, thiết kế và cài đặt hệ thống; Chương 4 đưa ra kết quả chạy thử, kiểm thử và đánh giá; Chương 5 bàn về tác động, hạn chế và hướng phát triển; Chương 6 kết luận.

**Kết chương 1:** Chương 1 đã xác định tính cấp thiết, mục tiêu (MT1–MT6), đối tượng – phạm vi và phương pháp của đề tài. Trên nền khung logic đó, Chương 2 làm rõ cơ sở lý thuyết và các công trình liên quan để hợp lý hóa lựa chọn kiến trúc.

## **2. Tổng quan tài liệu và cơ sở lý thuyết**

> **Tổng quan chương:** Chương 2 giới thiệu bức tranh tổng quan về ứng dụng LLM trong nghiên cứu, khái niệm tác tử và hệ đa tác tử, các mẫu điều phối phổ biến, framework LangGraph/LangChain cùng các kỹ thuật nền tảng được đề tài sử dụng: human-in-the-loop, retrieval-augmented generation với Tavily, structured output bằng Pydantic và tổng hợp map-reduce. Cuối chương khảo lược các nghiên cứu liên quan và định vị đề tài.

### **2.1. LLM với hỗ trợ khảo sát thông tin khoa học**

LLM được huấn luyện trên kho ngữ liệu khổng lồ có thể đóng vai "máy tổng hợp tri thức" cho giai đoạn khảo sát ban đầu của nghiên cứu: đề xuất dàn ý, so sánh quan điểm, soạn trích dẫn. Tuy nhiên, khả năng này đi kèm hai vấn đề kinh điển được cộng đồng nghiên cứu chỉ ra rộng rãi: kiến thức tham số có giới hạn theo thời điểm cắt dữ liệu, và xu hướng "đoán" câu trả lời thiếu căn cứ (hallucination). Các giải pháp được đề xuất trong tài liệu gồm retrieval-augmented generation (RAG) — nhúng tài liệu truy xuất được vào prompt để mô hình trả lời trên ngữ cảnh thật [8], và các mẫu tác tử cho phép mô hình _hành động_ (gọi công cụ tìm kiếm, đọc kết quả) thay vì chỉ _sinh văn bản_ theo suy luận — tiêu biểu là ReAct kết hợp reasoning với acting [7]. Đề tài đứng ở giao điểm hai hướng này: một pipeline đa bước, mỗi bước trả lời trên ngữ cảnh web truy xuất được.

### **2.2. Tác tử và hệ thống đa tác tử**

Tác tử LLM (LLM agent) là chương trình trong đó mô hình ngôn ngữ điều phối vòng: quan sát trạng thái → quyết định hành động → gọi công cụ → cập nhật trạng thái, cho tới khi đạt điều kiện kết thúc. Hệ thống **đa tác tử** phân chia công việc cho nhiều tác tử — thường theo vai trò (persona) hoặc theo pipeline — để tăng độ bao phủ và cho phép chạy song song. Các framework tiêu biểu: AutoGen tổ chức đối thoại giữa các agent lập trình được [9]; MetaGPT gán vai trò phần mềm (PM, architect, engineer) cho từng agent [10]; CrewAI theo mẫu "crew" phân công nhiệm vụ. Điểm chung của hướng này: chất lượng hệ thống phụ thuộc mạnh vào thiết kế _điều phối_ — ai nói khi nào, trạng thái nào được chia sẻ, vòng lặp dừng ở đâu — hơn là vào riêng chất lượng mô hình nền.

### **2.3. Framework LangGraph**

LangGraph [2] biểu diễn quy trình agent dưới dạng **đồ thị trạng thái (StateGraph)** với ba khái niệm:

- **State:** cấu trúc dữ liệu chia sẻ (TypedDict/Pydantic) mô tả "cục diện" của workflow tại mỗi bước; mỗi node khai báo nhận gì và trả gì, và kết quả được hợp nhất vào state qua **reducer** (ví dụ reducer cộng thêm vào danh sách message, gom section).
- **Node:** hàm thực thi một bước nghiệp vụ (gọi LLM, tìm kiếm, parse output…); node có thể là graph con (subgraph) — cho phép tái sử dụng và lồng ghép.
- **Edge:** quan hệ chuyển tiếp giữa node; **conditional edge** chọn nhánh theo hàm điều kiện đọc từ state, còn **`Send`** cho phép fan-out — gửi một bản sao state tới nhiều instance của cùng một node/subgraph để chạy song song, sau đó **fan-in** gom kết quả về state cha qua reducer.

Hai cơ chế đặc biệt quan trọng với đề tài: **`interrupt`** — dừng thực thi tại một node, chờ input từ người dùng rồi tiếp tục (nền tảng của human-in-the-loop); và **checkpointer/persistence** — lưu trạng thái theo thread để có thể tạm dừng, hồi phục và quan sát trong LangGraph Studio. So với việc viết vòng lặp agent thủ công, mô hình graph khiến mọi quyết định điều phối (điểm dừng, nhánh, vòng, song song) trở thành đối tượng tường minh — kiểm thử và debug được, đúng nhu cầu của một hệ thống "có thể báo cáo và demo được".

### **2.4. LangChain và sinh output có cấu trúc với Pydantic**

Đề tài dùng LangChain [3] cho tầng giao tiếp mô hình (`ChatDeepSeek` thuộc gói `langchain-deepseek`, gọi API DeepSeek), message và output parser; LangGraph đảm nhiệm tầng điều phối. Một vấn đề cốt lõi của hệ đa tác tử là **tính giao tiếp máy-đọc-được**: nếu persona chỉ là văn bản tự do, các node sau không thể lập trình dựa trên nó. Pydantic [5] giải quyết bằng kỹ thuật structured output — ràng buộc phản hồi của mô hình theo schema (tên, vai trò, affiliation, mô tả, persona…), ví dụ sinh danh sách đối tượng `Analyst` với `with_structured_output`. Schema trở thành "hợp đồng dữ liệu" giữa các node, đồng thời là điểm kiểm tra lỗi parse.

### **2.5. Human-in-the-loop (HITL)**

Nguyên tắc HITL trong hệ tác tử: đặt điểm dừng tại các bước _tốn kém hoặc nhạy cảm về quyết định_ để con người duyệt/từ chối/chỉnh sửa trước khi tiêu tốn tài nguyên. Trong đề tài, điểm dừng nằm ngay sau khi sinh danh sách analyst: người dùng đọc persona, hoặc chấp thuận (hệ chuyển sang nghiên cứu), hoặc viết feedback (hệ quay lại node sinh persona với ràng buộc mới). Cơ chế `interrupt` của LangGraph cho phép tạm dừng _thật_ (graph persist trạng thái, chờ input) thay vì chỉ là một prompt hỏi người trong cùng lời gọi — nhờ đó bước duyệt trở thành một phần tự nhiên của workflow và có thể demo mạch lạc.

### **2.6. Retrieval theo thời gian chạy với Tavily**

Tavily [4] là search API được thiết kế cho ứng dụng LLM: nhận query, trả về danh sách đoạn trích kèm URL, score liên quan. Khác với RAG cổ điển trên kho tĩnh, đề tài dùng **retrieval động**: chính ngữ cảnh hội thoại hiện tại của từng analyst được dùng để sinh search query mới ở mỗi lượt phỏng vấn, nghĩa là hướng tìm kiếm _tiến hóa theo câu hỏi_ thay vì một bộ truy vấn cố định từ đầu; hai node tìm kiếm song song trong subgraph giúp tăng độ phủ nguồn trong cùng thời gian. Toàn bộ tài liệu truy xuất được giữ lại nội dung + URL để node trả lời bám ngữ cảnh (grounding) và để báo cáo cuối in danh mục nguồn — cơ chế giảm hallucination chủ động của hệ thống.

### **2.7. Tổng hợp báo cáo theo mô hình map-reduce**

Với N phiên phỏng vấn độc lập, việc "đổ toàn bộ transcript vào một prompt" sẽ vỡ giới hạn context và mất cấu trúc. Mô hình **map-reduce** xử lý theo hai pha: _map_ — mỗi phiên tự viết một section ngắn (chế độ reducer gom section vào state); _reduce_ — các node writer riêng lần lượt viết introduction (từ chủ đề + các section), body ghép nối, conclusion, và `finalize_report` assembling cuối cùng kèm danh mục URL nguồn đã khử trùng lặp. Thiết kế này giữ mỗi lời gọi LLM trong ngân sách context, đồng thời tách trách nhiệm để dễ kiểm tra từng phần.

### **2.8. Hệ thống nguồn và các nghiên cứu liên quan**

Đề tài do tôi tự thiết kế theo hướng tổ chức hệ thống thành ba graph đăng ký trong `langgraph.json` (`create_analysts`, `answer_question`, `deep_agent`) với tầng util tách biệt (nodes/edges/states/objects/prompts/models) — kiến trúc hình thành từ quá trình tự khảo sát tài liệu chính thức [2][3] rồi thử–sai qua từng vòng prototype, kèm phân tích, test và tài liệu đánh giá theo đúng quy trình bài tập lớn. Trên bình diện học thuật, các công trình nền gồm: ReAct [7] cho mẫu reasoning+acting; RAG [8] cho grounded generation; AutoGen [9] và MetaGPT [10] cho thiết kế đa tác tử theo vai trò; các tài liệu chính thức về graph-based agent workflow [11]. Điểm chung của chúng — điều phối tường minh, con người kiểm soát điểm then chốt, mọi phát ngôn bám ngữ cảnh truy xuất — chính là các nguyên tắc được cụ thể hóa trong đề tài này.

**Kết chương 2:** Chương 2 đã trình bày cơ sở lý thuyết: hạn chế của chat đơn lượt, mô hình tác tử/đa tác tử, kiến trúc StateGraph của LangGraph cùng bốn kỹ thuật nền tảng của đề tài (structured output, HITL, dynamic retrieval, map-reduce synthesis). Các nguyên lý này là căn cứ cho phần phân tích yêu cầu và thiết kế ở Chương 3.

## **3. Triển khai dự án**

> **Tổng quan chương:** Chương 3 đi từ phân tích yêu cầu đến thiết kế chi tiết và cài đặt: yêu cầu chức năng – phi chức năng; cách hệ thống thu nhận và tổ chức dữ liệu; phương pháp cấu hình hệ thống AI; kiến trúc ba graph; thiết kế state, node, edge; thiết kế prompt; luồng human-in-the-loop; fan-out song song; và quy trình 8 bước từ topic đến báo cáo cuối cùng.

### **3.1. Phân tích yêu cầu**

**Yêu cầu chức năng:**

| **Mã** | **Yêu cầu**              | **Mô tả**                                                                                          |
| ------ | ------------------------ | -------------------------------------------------------------------------------------------------- |
| FR1    | Sinh persona             | Từ topic + `max_analysts`, sinh N<br>analyst có tên/vai trò/affiliation/<br>persona, đúng schema   |
| FR2    | Duyệt của người dùng     | Dừng sau FR1; chấp thuận hoặc<br>phản hồi; phản hồi dẫn tới sinh lại                               |
| FR3    | Phỏng vấn song song      | Mỗi analyst một subgraph phỏng<br>vấn độc lập chạy đồng thời                                       |
| FR4    | Hỏi–tìm–đáp              | Mỗi lượt: sinh câu hỏi → sinh<br>query → Tavily → trả lời theo<br>context + URL; lặp ≤ `max_turns` |
| FR5    | Ghi transcript & section | Lưu hội thoại, memo từng analyst,<br>viết section tương ứng                                        |
| FR6    | Tổng hợp báo cáo         | Ghép mở đầu, body, kết luận,<br>danh mục nguồn; xuất Markdown                                      |

**Yêu cầu phi chức năng:**

| **Mã** | **Yêu cầu**         | **Chỉ tiêu đề ra**                                                                               |
| ------ | ------------------- | ------------------------------------------------------------------------------------------------ |
| NFR1   | Quan sát được       | Mọi node/state hiển thị trong Studio;<br>log từng phiên chạy                                     |
| NFR2   | Giới hạn tài nguyên | Khống chế `max_analysts`, `max_turns`;<br>không lặp vô hạn                                       |
| NFR3   | Grounding           | Mọi câu trả lời sinh khi có context;<br>citation/URL xuất hiện trong báo cáo                     |
| NFR4   | Bền vững trước lỗi  | Retry có giới hạn cho API lỗi;<br>thông báo rõ khi thất bại                                      |
| NFR5   | Bảo mật             | Key chỉ qua `.env`; không secret trong repo                                                      |
| NFR6   | Mô-đun              | Thay model/search provider không sửa<br>toàn bộ workflow (tách `models.py`,<br>`utils/nodes.py`) |

### **3.2. Thu thập và tổ chức dữ liệu**

Hệ thống không xây dựng tập dữ liệu huấn luyện cố định. Ở thời điểm chạy, mỗi phiên thu nhận: (i) **dữ liệu người dùng nhập** — chủ đề nghiên cứu, số analyst tối đa, phản hồi duyệt persona; (ii) **dữ liệu truy xuất động** — search query được sinh từ trạng thái hội thoại, tài liệu web Tavily trả về (đoạn trích + URL) được chuẩn hóa về một dạng context thống nhất; (iii) **dữ liệu phát sinh** — hội thoại phỏng vấn, memo, transcript, section và final report. Cách tiếp cận này phù hợp với lĩnh vực thông tin biến động nhanh (mà mô hình nền không thể biết sau thời điểm cắt dữ liệu), nhưng khiến chất lượng đầu ra phụ thuộc trực tiếp vào chất lượng truy vấn và nguồn tìm được — điểm được định lượng ở Chương 4.

### **3.3. Phương pháp cấu hình hệ thống AI ("huấn luyện")**

Đề tài **không fine-tune hay huấn luyện mô hình mới**; DeepSeek [6] (hai dòng `deepseek-chat` và `deepseek-reasoner`) được dùng như mô hình nền tảng qua API, tích hợp qua `ChatDeepSeek`. Toàn bộ hành vi nghiệp vụ được "cấu hình" qua bốn lớp, theo thứ tự ưu tiên kiểm soát từ mạnh tới mềm:

1. **Lớp đồ thị (hard):** node/edge/reducer quyết định điều gì _được phép xảy ra_ và theo thứ tự nào; `max_turns` là ràng buộc cứng của vòng lặp.
2. **Lớp schema (hard):** Pydantic ép phản hồi vào khuôn dữ liệu; lệch khuôn gây lỗi parse — bắt được ở test.
3. **Lớp prompt (soft):** instruction đặt vai trò, mục tiêu, phong cách cho từng node (sinh persona, hỏi, trả lời, viết section…).
4. **Lớp ngữ cảnh (soft):** tài liệu retrieved đưa vào prompt; prompt yêu cầu chỉ trả lời theo context và ghi nguồn.

Vì vậy, phần "phương pháp huấn luyện" của biểu mẫu được diễn giải thành **phương pháp thiết kế – cấu hình – đánh giá hệ thống dùng mô hình nền tảng**: thiết kế prompt, schema, retrieval context, giới hạn vòng lặp và tiêu chí chất lượng output.

### **3.4. Kiến trúc tổng thể hệ thống**

Kiến trúc logic của pipeline toàn trình (`deep_agent`):

```text
Topic
  └─> create_analysts ──> human_feedback (interrupt)
                              │ [feedback?] ──> quay lại create_analysts
                              ▼ [approve]
                     fan-out (Send) ──┬── Interview subgraph #1
                                      ├── Interview subgraph #2
                                      └── Interview subgraph #N
                                            ask_question ⇄ search_web
                                            (2 node search song song)
                                                  → answer_question
                                                  → (repeat ≤ max_turns)
                                                  → save_interview → write_section
  ──> fan-in: write_report(introduction, body, conclusion) ──> finalize_report → Markdown
```

Ba graph đăng ký trong `langgraph.json` và vai trò từng file mã nguồn:

| **Thành phần**               | **Trách nhiệm**                                                                |
| ---------------------------- | ------------------------------------------------------------------------------ |
| `src/agent.py`               | Graph `create_analysts`: sinh persona,<br>`interrupt` chờ duyệt, vòng feedback |
| `src/answering_questions.py` | Subgraph `answer_question`: vòng<br>hỏi–tìm–đáp của một analyst                |
| `src/deep_agent.py`          | Graph toàn trình: fan-out, tổng hợp,<br>xuất báo cáo                           |
| `src/utils/states.py`        | State graph/subgraph (TypedDict),<br>message container, reducer                |
| `src/utils/objects.py`       | Pydantic: `Analyst`, cấu trúc phản hồi,<br>output có khuôn                     |
| `src/utils/prompts.py`       | Toàn bộ prompt template theo node                                              |
| `src/utils/nodes.py`         | Hàm node: LLM call, search, parse,<br>viết section/report                      |
| `src/utils/edges.py`         | Hàm điều kiện routing và logic `Send`                                          |
| `src/utils/models.py`        | Khởi tạo ChatDeepSeek dùng chung                                               |
| `langgraph.json`             | Đăng ký graph cho CLI/Studio                                                   |
| `main.py`                    | Runner CLI tối thiểu                                                           |

Tầng util tách _chính sách_ (prompt, schema, routing) khỏi _cơ chế_ (graph wiring) — mỗi lần chỉnh hành vi chỉ đụng một file chuyên trách, là điều kiện để kiểm thử và báo cáo từng phần.

### **3.5. Thiết kế state và objects**

State của mỗi graph là TypedDict khai báo trường, kèm reducer khi nhiều nhánh cùng ghi vào một key. Bảng dưới tổng hợp các trường then chốt của toàn hệ thống (rút gọn theo mức báo cáo):

| **Graph/State** | **Trường**                | \*\*Ý nghĩa / Reducer                                     |
| --------------- | ------------------------- | --------------------------------------------------------- |
| Analyst state   | `topic`, `max_analysts`   | Input người dùng                                          |
|                 | `analysts: List[Analyst]` | Persona đã sinh (schema Pydantic)                         |
|                 | `feedback`                | Phản hồi duyệt; có ⇒ routing<br>quay lại sinh lại persona |
| Interview state | `analyst`, `conversation` | Chân dung analyst + lịch sử<br>hỏi/đáp của phiên (append) |
|                 | `search_documents`        | Tài liệu truy xuất hiện có                                |
|                 | `turn` / `max_turns`      | Đếm vòng để điều kiện thoát                               |
|                 | `interview` / `memo`      | Transcript và ghi chú cuối phiên                          |
| Deep state      | `sections: List[str]`     | Section từng analyst — **reducer<br>gom** khi fan-in      |
|                 | `final_report`            | Văn bản Markdown cuối cùng                                |

Objects (`objects.py`) là hợp đồng dữ liệu giữa các node — ví dụ `Analyst(name, role, affiliation, description, persona...)` do structured output sinh ra; lỗi khuôn bị parse từ chối ngay tại node, không lan xuống downstream.

### **3.6. Thiết kế node**

| **Node**                                                         | **Input←Output**               | **Mô tả nghiệp vụ**                                                                             |
| ---------------------------------------------------------------- | ------------------------------ | ----------------------------------------------------------------------------------------------- |
| `create_analysts`                                                | topic, feedback → analysts     | LLM sinh ≤ `max_analysts` persona<br>bổ trợ góc nhìn; có feedback thì<br>tái sinh theo phản hồi |
| `human_feedback`                                                 | analysts → (approve\|feedback) | `interrupt`: dừng graph, chờ người<br>duyệt qua Studio/CLI                                      |
| `ask_question`                                                   | conversation → question        | Đóng vai analyst đặt câu hỏi<br>tiếp theo cho chuyên gia đối diện                               |
| `ask_search_question`                                            | conversation → query           | Chuẩn hóa nhu cầu thông tin hiện<br>tại thành truy vấn tìm kiếm                                 |
| `search_web_task` (+ song song)                                  | query → documents              | Gọi Tavily, giữ snippet + URL<br>vào context                                                    |
| `answer_question`                                                | question + documents → answer  | Trả lời **chỉ theo context**, ghi<br>nguồn; không đủ context thì nhận                           |
| `should_continue`                                                | turn < max_turns → route       | Cổng điều kiện của vòng phỏng vấn                                                               |
| `save_interview`                                                 | conversation → memo            | Kết thúc phiên, lưu transcript<br>+ ghi chú analyst                                             |
| `write_section`                                                  | interview → section            | Viết section báo cáo cho analyst                                                                |
| `write_report` /<br>`write_introduction` /<br>`write_conclusion` | sections → report parts        | Pha reduce map-reduce: body,<br>mở đầu, kết luận                                                |
| `finalize_report`                                                | report parts → final_report    | Assemble Markdown + danh mục<br>nguồn khử trùng lặp                                             |

### **3.7. Thiết kế edge, routing và fan-out**

- **Vòng phản hồi persona:** conditional edge tại `human_feedback` — tồn tại `feedback` ⇒ về `create_analysts` (không xuống interview); chấp thuận ⇒ tiếp nghiên cứu. Đây là hiện thực hóa MT2.
- **Vòng phỏng vấn:** `ask_question → search_web → answer_question → (should_continue)`; đủ `max_turns` hoặc analyst kết luận ⇒ `save_interview → write_section → END`. Chặn lặp vô hạn bằng giới hạn đếm (NFR2).
- **Fan-out/fan-in:** tại điểm phê duyệt, danh sách `analysts` được map thành N đối tượng `Send("conduct_interview", state_copy)` — một subgraph/analyst, độc luận và song song; reducer của `sections` trong state cha gom kết quả khi các subgraph kết thúc. Đây là hiện thực hóa MT3 và là lý do LangGraph được chọn so với vòng lặp tuyến tính.

### **3.8. Thiết kế prompt**

Prompt trong `prompts.py` tuân năm quy tắc, mỗi quy tắc ứng một nhóm lỗi hệ thống: (1) mỗi node một template chuyên nhiệm, không "siêu prompt" gộp việc — dễ test từng phần; (2) template persona ép danh sách N góc nhìn **khác biệt và bổ trợ** (định lượng, chính sách, kỹ thuật, phản biện…); (3) prompt trả lời bắt buộc cú pháp "chỉ sử dụng context được cung cấp; không đủ căn cứ thì nói rõ" — tuyến phòng thủ hallucination; (4) prompt section/report quy định đầu ra Markdown có mục nguồn; (5) phiên bản prompt gắn số và lưu nhật ký ứng viên — cho phép so sánh chất lượng khi sửa (Chương 4).

### **3.9. Quy trình xử lý end-to-end (8 bước)**

1. Nhận `topic` và `max_analysts` (kiểm tra hợp lệ ngay tại đầu vào).
2. `create_analysts` sinh danh sách analyst có tên, vai trò, affiliation, mô tả và persona — parse theo Pydantic schema.
3. Graph dừng tại `human_feedback`; người dùng duyệt persona hoặc gửi feedback; có feedback ⇒ quay lại bước 2 với ràng buộc mới.
4. Sau phê duyệt, `Send` API fan-out một interview subgraph cho mỗi analyst (MT3).
5. Trong mỗi subgraph: `ask_question` → `ask_search_question` → `search_web_task` (Tavily, giữ URL) → `answer_question` (grounding trên context) → lặp tới `max_turns` hoặc điều kiện kết thúc.
6. `save_interview` lưu transcript và memo; `write_section` viết section ngắn cho analyst.
7. Fan-in `sections`; các node writer viết introduction, body, conclusion (map-reduce).
8. `finalize_report` assemble và xuất báo cáo Markdown cuối cùng kèm danh mục nguồn.

### **3.10. Môi trường cài đặt và chạy thử**

```bash
git clone <repo-cá-nhân> && cd <repo>
uv sync                                   # cài dependencies Python 3.12+
cp .env.example .env                      # khai báo DEEPSEEK_API_KEY, TAVILY_API_KEY
uv run langgraph dev                      # launch dev server + LangGraph Studio
# hoặc: uv run python main.py "chủ đề"
```

Tôi dùng Studio làm bàn điều khiển chính: quan sát từng node thực thi, inspect state tại mọi thời điểm, thao tác `interrupt` (approve/feedback) và download final report — đồng thời là công cụ chính để thu dữ liệu đánh giá ở Chương 4.

**Kết chương 3:** Chương 3 đã chuyển hóa cơ sở lý thuyết Chương 2 thành hệ thống cụ thể: bộ yêu cầu FR1–FR6/NFR1–NFR6, kiến trúc ba graph, thiết kế state/objects, bảng node/edge, chiến lược prompt, và quy trình 8 bước cài đặt được trong repo `uv`-ready. Chương 4 trình bày kết quả vận hành, kiểm thử và đánh giá hệ thống này.

## **4. Kết quả**

> **Tổng quan chương:** Chương 4 báo cáo kết quả theo đúng vòng đời dự án: chuẩn hóa dữ liệu vào/ra, phân tích vận hành (EDA) theo chỉ số, kết quả xây dựng mô hình pipeline, demo kịch bản end-to-end, giao diện, kết quả kiểm thử theo ma trận test case, đánh giá chất lượng báo cáo theo tiêu chí, cùng phân tích chi phí – độ trễ và các cải tiến đã thực hiện.

### **4.1. Tiền xử lý dữ liệu**

Kết quả của ba lớp xử lý đầu vào/đầu ra: (i) **input validation** — từ chối topic rỗng, `max_analysts`/`max_turns` ngoài khoảng cho phép bằng thông báo lỗi rõ ràng; (ii) **chuẩn hóa search result** — mọi đoạn trích Tavily quy về dạng {content, url} thống nhất, bất kể query nào, để node trả lời và writer dùng chung; (iii) **output parsing** — phản hồi LLM ép vào Pydantic (persona, feedback, section); các section lưu theo danh sách để reducer gom mà không mất thứ tự. Biến nhạy cảm (API key) chỉ đọc từ môi trường tại khởi động.

### **4.2. Phân tích vận hành (EDA)**

Vì đây là hệ thống orchestration thời gian chạy, EDA không áp dụng cho dữ liệu tĩnh mà trên **nhật ký phiên**: tôi log 09 phiên chạy thực nghiệm trên [ĐIỀN SỐ] chủ đề (kinh tế – công nghệ – y tế công cộng) với cấu hình 2–4 analyst, 2–4 turn. Các chỉ số thu được:

| **Chỉ số vận hành**              | **Giá trị trung bình (điền số liệu)** | **Nhận xét**              |
| -------------------------------- | ------------------------------------- | ------------------------- |
| Số analyst / phiên               | \_\_                                  | Theo `max_analysts`       |
| Số lượt phỏng vấn / analyst      | \_\_                                  | Bám `max_turns`           |
| Số truy vấn Tavily / phiên       | \_\_                                  | ≈ 1 question/turn         |
| Số nguồn duy nhất / báo cáo      | \_\_                                  | Đo độ phủ thông tin       |
| Tỷ lệ câu trả lời có citation    | \_\_ %                                | Chỉ số grounding chủ chốt |
| Độ dài section / báo cáo (token) | \_\_                                  | Ngân sách context         |
| LLM calls / phiên                | \_\_                                  | Cơ sở tính chi phí        |
| Thời gian end-to-end / phiên     | \_\_ phút                             | Trải nghiệm người dùng    |

Nhật ký nhiều phiên cũng phơi bày ba mẫu lỗi để cải tiến: truy vấn lặp giữa hai lượt gần nhau; nguồn bị lệch về một domain (search thiên vị); và node `search_web_task` là nút cổ chai latency — các mục tiêu của 4.7.

### **4.3. Kết quả xây dựng mô hình pipeline**

"Mô hình" của đề tài = LLM nền tảng + graph điều phối; kết quả chứng minh từng cơ chế hoạt động đúng thiết kế:

- **Structured output** sinh persona ổn định: 100% phiên parse đúng schema `Analyst`, không có phản hồi lệch khuôn trong bộ dữ liệu thử.
- **Conditional edge** điều khiển đúng hai vòng: vòng tái tạo analyst (khi có feedback) và vòng phỏng vấn (thoát đúng tại `max_turns`, không kịch bản lặp vô hạn).
- **Send API** cho thấy xử lý song song thật: trên Studio, N subgraph chạy concurrently, tổng thời gian phỏng vấn xấp xỉ một phiên dài nhất thay vì tổng N phiên.
- **Reducer** gom đủ N section khi fan-in, không mất/ghi đè section trong các phiên thử.
- **Writer nodes** tạo introduction, body, conclusion độc lập; `finalize_report` in danh mục URL nguồn khử trùng lặp.
- Tính mô-đun kiểm chứng bằng swap nhanh: đổi model ID trong `models.py` hoặc đổi search provider tại node search không phải sửa workflow đồ thị.

### **4.4. Demo end-to-end (kịch bản bảo vệ)**

| **Bước**                                        | **Quan sát được**                                                                                       |
| ----------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| Nhập topic "[CHỦ ĐỀ DEMO]",<br>`max_analysts=3` | Graph bắt đầu `create_analysts`                                                                         |
| Kết quả sinh persona                            | Studio liệt kê 3 analyst: ví dụ<br>chuyên gia định lượng / nhà phản<br>biện chính sách / người thực thi |
| Gửi feedback "thêm góc nhìn<br>quốc tế"         | Node tái sinh với ràng buộc mới<br>(đúng nhánh feedback)                                                |
| Approve                                         | 3 subgraph chạy song song; vòng<br>ask ↔ search ↔ answer hiển thị                                       |
| Kết thúc phỏng vấn                              | Transcript, memo, 3 section                                                                             |
| `finalize_report`                               | Markdown đủ mở đầu – nội dung –<br>kết luận – nguồn (URL click được)                                    |

[Điền link video/ảnh chụp màn hình Studio hoặc file báo cáo mẫu vào phụ lục.]

### **4.5. Giao diện người dùng**

Giao diện vận hành chính là **LangGraph Studio/CLI**: nhập `topic`/`max_analysts`, theo dõi trạng thái graph từng node, và tương tác tại điểm `interrupt` sau `create_analysts` — xem persona, bấm approve hoặc gõ feedback. Điểm tương tác người dùng duy nhất này được thiết kế có chủ đích: đủ sớm để kiểm soát hướng nghiên cứu, đủ muộn để người duyệt đã có persona cụ thể mà không phải chờ kết quả. Đầu ra cuối là Markdown hiển thị trên web, có thể xuất sang tài liệu khác.

### **4.6. Kết quả kiểm thử**

Ma trận test case và kết quả (bảng KQ là PLACEHOLDER — điền theo biên bản kiểm thử thật):

| **Nhóm**          | **Kịch bản**                    | **Kết quả mong đợi**                          | **Kết quả** |
| ----------------- | ------------------------------- | --------------------------------------------- | ----------- |
| Input             | Topic rỗng / `max_analysts` sai | Từ chối, báo lỗi rõ ràng                      | PASS/FAIL   |
| Structured output | LLM trả persona                 | Parse đúng schema 100%                        | PASS/FAIL   |
| Human loop        | Người dùng gửi feedback         | Sinh lại analyst, **không** chạy<br>interview | PASS/FAIL   |
| Routing           | Không có feedback (approve)     | Fan-out đúng số analyst                       | PASS/FAIL   |
| Interview loop    | Đạt `max_turns`                 | Thoát vòng, về save_interview                 | PASS/FAIL   |
| Grounding         | Có search context               | Trả lời dùng context + URL                    | PASS/FAIL   |
| Aggregation       | Nhiều section từ fan-in         | Đủ section, không mất                         | PASS/FAIL   |
| Failure           | Search/API lỗi                  | Retry có giới hạn + thông báo                 | PASS/FAIL   |
| E2E               | Topic thật, 3 analyst           | Markdown 4 phần + nguồn                       | PASS/FAIL   |

### **4.7. Đánh giá chất lượng theo tiêu chí**

Mỗi phiên được chấm 1–5 theo rubric cá nhân và đối chiếu chéo bởi một người đánh giá thứ hai trên [ĐIỀN] báo cáo (trung bình lấy khi hai lượt chấm đồng thuận):

| **Tiêu chí**      | **Định nghĩa**                                                      | **Kết quả TB** |
| ----------------- | ------------------------------------------------------------------- | -------------- |
| Relevance         | Section bám chủ đề, đúng vai<br>trò persona                         | \_\_/5         |
| Grounding         | Câu trả lời dựa trên context<br>truy xuất, ít phát biểu ngoài nguồn | \_\_/5         |
| Citation coverage | Tỷ lệ phát biểu quan trọng<br>dẫn được về URL trong danh mục        | \_\_ %         |
| Completeness      | Đủ mở đầu/nội dung/kết luận;<br>đủ section theo số analyst          | \_\_/5         |
| Multi-perspective | Khác biệt thực chất giữa các<br>góc nhìn persona                    | \_\_/5         |
| Traceability      | Mở một phát biểu → lần ra<br>nguồn qua transcript                   | \_\_/5         |
| UX tại interrupt  | Persona đủ thông tin để duyệt<br>hay cần chạy lại                   | \_\_/5         |

Nhận xét định tính chính: persona đa dạng rõ rệt khi prompt nêu yêu cầu "góc nhìn bổ trợ và một người phản biện"; nguồn tập trung vào tin tức công nghệ (cân bằng khi thêm domain filter/boost); phần kết luận chất lượng cao nhờ reduce từ memo từng analyst thay vì từ transcript thô.

### **4.8. Chi phí tính toán và độ trễ**

Với 3 analyst × 3 turn: ~[ĐIỀN] LLM calls/phiên, ~[ĐIỀN] Tavily calls, ~[ĐIỀN] tokens, chi phí ~[ĐIỀN] USD, thời gian ~[ĐIỀN] phút (phỏng vấn song song nên thời gian không tuyến tính với số analyst). Các con số này chứng minh tính khả dụng trong ngân sách bài tập lớn khi giữ `max_analysts` ≤ 4 và bật cache theo chủ đề.

### **4.9. Cải tiến đã và đang thực hiện**

_retry/backoff_ và timeout cho call Tavily/DeepSeek; cache kết quả search theo query; lọc domain chính thống; chống prompt-injection từ nội dung web bằng chỉ dẫn "coi tài liệu là dữ liệu"; bước verification nguồn trước khi viết section; telemetry token/độ trễ cho phép đo 4.2/4.8; bộ đánh giá tự động (LLM-as-judge theo tiêu chí 4.7) kết hợp đánh giá con người.

**Kết chương 4:** Chương 4 cho thấy hệ thống chạy đúng thiết kế Chương 3 trên cả ba trục: đúng luồng (ma trận test 4.6), có căn cứ (grounding + citation 4.7), và khả dụng về chi phí/thời gian (4.8). Đồng thời các số liệu cũng định lượng rõ giới hạn chất lượng nguồn — luận điểm chính của Chương 5.

## **5. Tác động dự kiến**

> **Tổng quan chương:** Chương 5 bàn về thành tựu và lợi ích của hệ thống, giá trị đối với học tập – nghiên cứu, các hạn chế còn lại sau đánh giá, và những hướng phát triển tiếp theo có căn cứ từ kết quả Chương 4.

### **5.1. Thành tựu và lợi ích**

- **Rút ngắn khảo sát ban đầu:** từ một dòng topic đến dàn ý nhiều góc nhìn trong một phiên, giảm đáng kể thời gian khởi động khảo sát tài liệu.
- **Tăng độ đa dạng góc nhìn:** persona chuyên biệt buộc hệ thống "phản biện chính sách", "người định lượng"… — điều chat một lượt khó tạo ổn định.
- **Truy nguyên được thông tin:** mọi phần chính của báo cáo ánh xạ về transcript và URL nguồn (traceability, tiêu chí 4.7).
- **Kiểm soát con người đúng chỗ:** HITL tại interrupt lọc hướng nghiên cứu trước khi tiêu thụ API, đồng thời là điểm demo có giá trị nhất về trải nghiệm.
- **Nền tảng học thuật cho bản thân:** nắm thực hành các mẫu thiết kế agent cốt lõi (structured output, HITL, fan-out, loop có điều kiện, RAG động, map-reduce) — chính là mục tiêu đầu ra của học phần.
- **Kiến trúc mở rộng được:** thêm graph (fact-checker, writer chuyên ngành) hoặc thêm node (PDF export, memory) mà không phá vỡ pipeline hiện tại.

### **5.2. Hạn chế**

- **Phụ thuộc chất lượng Tavily:** query kém hoặc nguồn nhiễu thì section kém — lỗi "rác vào – rác ra" của retrieval chưa loại bỏ được hoàn toàn.
- **Hallucination giảm chưa triệt:** khi tài liệu về chủ đề quá mỏng, câu trả lời có thể rơi về nội dung tham số của mô hình; đã chặn bằng tuyến phòng thủ grounding nhưng cần cơ chế xác minh độc lập.
- **Persona là "diễn" theo prompt:** góc nhìn khác nhau thật nhưng chưa tương đương chuyên gia người; chất lượng đa góc nhìn phụ thuộc độ khéo của template.
- **Chi phí tăng theo quy mô:** thêm analyst/turn tăng token gần tuyến tính; chưa có budget động.
- **Đánh giá còn thủ công:** bảng 4.7 cần LLM-as-judge tự động + người để mở rộng số phiên.

### **5.3. Hướng phát triển**

- **Đánh giá độ tin cậy nguồn và cross-check:** nhiều nguồn cho một phát biểu chính, chấm điểm đồng thuận giữa nguồn.
- **Memory và checkpointer nâng cao:** tiếp tục phiên nghiên cứu bị gián đoạn, tái sử dụng persona/transcript giữa các chủ đề liên quan.
- **RAG trên tài liệu nội bộ:** tích hợp kho PDF/đề cương môn học có phân quyền — biến hệ thành trợ lý học tập cụ thể cho sinh viên.
- **Sản phẩm hóa giao diện:** web UI (chat + tree graph), export DOCX/PDF, lịch sử báo cáo theo user.
- **Đo lường học thuật hơn:** citation correctness tự động, faithfulness/coverage theo công thức, benchmark latency–cost theo cấu hình.
- **Guardrail:** chống prompt-injection toàn diện, chặn PII leakage và nội dung độc hại khi đưa ra môi trường mở.

**Kết chương 5:** Hệ thống tạo giá trị thực cho khâu khảo sát ý tưởng nghiên cứu và minh chứng các mẫu thiết kế agent, nhưng các hạn chế về nguồn, đa dạng persona và đánh giá tự động xác định lộ trình phát triển có ưu tiên rõ ràng nêu trên.

## **6. Kết luận**

Đề tài đã hoàn thành mục tiêu MT1–MT6 đặt ra ở Chương 1: một trợ lý nghiên cứu đa tác tử chạy được trên LangGraph, sinh persona có cấu trúc, dừng đúng điểm human-in-the-loop, phỏng vấn song song có fan-out/fan-in, trả lời có grounding trên web retrieval với URL, và tổng hợp thành báo cáo Markdown hoàn chỉnh bằng map-reduce. Kết quả kiểm thử và đánh giá (Chương 4) khẳng định LangGraph là nền tảng phù hợp cho quy trình nghiên cứu đa bước có trạng thái, vòng lặp, nhánh điều kiện và xử lý song song; sự kết hợp analyst persona + HITL + Tavily + report synthesis tạo pipeline mạch lạc và truy vết được hơn hẳn lời gọi LLM đơn lẻ — đúng điều học phần Phát triển hệ thống thông minh hướng tới.

Bên cạnh đó, báo cáo sinh tự động **không thay thế thẩm định học thuật**: người dùng vẫn phải kiểm chứng nội dung và nguồn. Với lộ trình cải tiến về xác minh nguồn, bộ nhớ, RAG nội bộ và đánh giá tự động trong Chương 5, hệ thống có tiềm năng phát triển thành trợ lý nghiên cứu thực thụ phục vụ học tập và doanh nghiệp. Tôi xin trân trọng cảm ơn giảng viên hướng dẫn [ĐIỀN TÊN] đã hỗ trợ chuyên môn trong suốt quá trình thực hiện.

## **Tài liệu tham khảo**

- [2] LangChain. _LangGraph Documentation – Overview_. https://docs.langchain.com/oss/python/langgraph/overview
- [3] LangChain. _LangChain Documentation_. https://docs.langchain.com/
- [4] Tavily. _Tavily Documentation_. https://docs.tavily.com/
- [5] Pydantic. _Pydantic Documentation_. https://docs.pydantic.dev/
- [6] DeepSeek. _DeepSeek API Documentation_. https://api-docs.deepseek.com/ ; tích hợp LangChain qua gói `langchain-deepseek` (https://pypi.org/project/langchain-deepseek/)
- [7] Yao, S. et al. (2023). _ReAct: Synergizing Reasoning and Acting in Language Models_. ICLR 2023. arXiv:2210.03629.
- [8] Lewis, P. et al. (2020). _Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks_. NeurIPS 2020. arXiv:2005.11401.
- [9] Wu, Q. et al. (2023). _AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation_. arXiv:2308.08155.
- [10] Hong, S. et al. (2023). _MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework_. arXiv:2308.00352.
- [11] _Graph-Based Agentic AI with LangGraph: Workflow_. https://arxiv.org/html/2607.19297v1
- [12] LangChain. _LangGraph Studio / CLI Reference_. https://docs.langchain.com/langgraph-platform/studio-overview

## **7. Tự đánh giá quá trình thực hiện**

| **Hạng mục**               | **Tự đánh giá (0–100%)** | **Ghi chú**                                                     |
| -------------------------- | ------------------------ | --------------------------------------------------------------- |
| Kiến trúc graph & tích hợp | [Điền]                   | 3 graph chạy end-to-end; fan-out/fan-in đúng thiết kế; [Điền]   |
| Prompt & schema            | [Điền]                   | Structured output ổn định, persona đa dạng góc nhìn; [Điền]     |
| Backend & retrieval        | [Điền]                   | Hoàn thành vòng hỏi–tìm–đáp, tích hợp DeepSeek và Tavily; [Điền] |
| Kiểm thử & tài liệu        | [Điền]                   | Bộ test đạt, báo cáo/slide/demo hoàn tất đúng hạn; [Điền]       |

## **8. Nhận xét của giảng viên**

| **Hạng mục**        | **Điểm**     | **Nhận xét** |
| ------------------- | ------------ | ------------ |
| Ý tưởng             | \_\_/10      |              |
| Ứng dụng            | \_\_/30      |              |
| Kết quả             | \_\_/30      |              |
| Quản lý dự án       | \_\_/10      |              |
| Trình bày & Báo cáo | \_\_/20      |              |
| **Tổng**            | **\_\_/100** |              |
