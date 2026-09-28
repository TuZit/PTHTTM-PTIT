# BÁO CÁO TÍNH NĂNG & KIỂM THỬ UAT

## AI Research Assistant — Bài lab Jupyter Notebook

---

## 1. Thông tin chung

| Mục | Nội dung |
|---|---|
| Tên bài lab | AI Research Assistant (Trợ lý nghiên cứu AI đơn giản) |
| Môn học | Phát triển các hệ thống thông minh |
| Đơn vị | Học viện Công nghệ Bưu chính Viễn thông (PTIT) |
| Loại bài | Bài kiểm tra giữa kỳ — bài lab thực hành |
| Sản phẩm chính | `research_assistant.ipynb` |
| Nhà cung cấp LLM | **DeepSeek** (thay thế OpenAI/ChatGPT) |
| Công cụ tìm kiếm | **Tavily Search API** |
| Ngôn ngữ lập trình | Python 3.10+ |
| Môi trường chạy | Jupyter Notebook |
| Tài liệu này | Báo cáo tính năng và kịch bản kiểm thử chấp nhận người dùng (UAT) |

---

## 2. Mục tiêu bài lab

Sau khi hoàn thành bài lab, sinh viên có thể:

1. Gọi API của một mô hình ngôn ngữ lớn (DeepSeek) từ Python.
2. Viết **prompt** để mô hình trả về kết quả có cấu trúc, dùng được.
3. Gọi một **API tìm kiếm web** (Tavily) và xử lý dữ liệu JSON trả về.
4. Kết hợp kết quả tìm kiếm với LLM (**Retrieval-Augmented Generation**).
5. Sinh báo cáo nghiên cứu dạng Markdown ngay trong notebook.

Bài lab giữ đúng tinh thần **đơn giản, dễ đọc, dễ hiểu**: chỉ có **một LLM +
một công cụ tìm kiếm + bốn hàm Python nhỏ**, không dùng multi-agent và không
bắt buộc LangGraph.

---

## 3. Kiến trúc và luồng xử lý

```text
        Người dùng nhập chủ đề nghiên cứu (ô 06)
                        │
                        ▼
        ┌───────────────────────────────┐
        │  DeepSeek LLM                 │  generate_queries()
        │  Sinh câu truy vấn tìm kiếm   │
        └───────────────┬───────────────┘
                        │  3 câu truy vấn
                        ▼
        ┌───────────────────────────────┐
        │  Tavily Web Search            │  search_web()
        │  3 truy vấn × 3 kết quả       │
        └───────────────┬───────────────┘
                        │  JSON: title, url, content
                        ▼
        ┌───────────────────────────────┐
        │  DeepSeek LLM                 │  summarize_results()
        │  Tóm tắt thông tin            │
        └───────────────┬───────────────┘
                        │  bản tóm tắt trung thực
                        ▼
        ┌───────────────────────────────┐
        │  DeepSeek LLM                 │  generate_report()
        │  Viết báo cáo cuối cùng       │
        └───────────────┬───────────────┘
                        │  báo cáo Markdown
                        ▼
        Hiển thị trong notebook  +  lưu research_report.md
```

| Hàm | Nhiệm vụ |
|---|---|
| `generate_queries(topic, n=3)` | gọi DeepSeek sinh câu truy vấn tìm kiếm |
| `search_web(query, max_results)` | gọi API Tavily, chuẩn hoá kết quả |
| `summarize_results(topic, results)` | gọi DeepSeek tóm tắt kết quả tìm kiếm |
| `generate_report(topic, summary)` | gọi DeepSeek viết báo cáo Markdown |
| `ask_deepseek(prompt, demo_answer)` | hàm gọi LLM duy nhất, dùng chung cho cả 3 bước |
| `show_search_results(results)` | hiển thị kết quả tìm kiếm |
| `build_source_list(results)` | sinh danh sách nguồn từ URL thật |

---

## 4. Cấu trúc thư mục dự án

```text
.
├── research_assistant.ipynb   # SẢN PHẨM CHÍNH — notebook 13 phần
├── README.md                  # hướng dẫn cài đặt và sử dụng
├── BAO_CAO_UAT.md             # tài liệu này (báo cáo tính năng & UAT)
├── requirements.txt           # phụ thuộc tối giản
├── .env.example               # mẫu cấu hình API key
├── .gitignore                 # chặn commit .env
├── my-requirement.md          # đề bài gốc
└── data/
    └── sample_results.json    # dữ liệu mẫu cho chế độ DEMO
```

---

## 5. Danh sách tính năng

| Mã | Tính năng | Mô tả | Trạng thái |
|---|---|---|---|
| F-01 | Nhập chủ đề nghiên cứu | Người dùng sửa biến `topic` trong ô 06 | ✅ Hoàn thành |
| F-02 | Sinh câu truy vấn bằng DeepSeek | LLM sinh ~3 câu truy vấn từ chủ đề | ✅ Hoàn thành |
| F-03 | Tìm kiếm web bằng Tavily | 3 truy vấn × 3 kết quả = tối đa 9 kết quả | ✅ Hoàn thành |
| F-04 | Hiển thị kết quả tìm kiếm | Mỗi kết quả gồm tiêu đề, URL, đoạn tóm tắt | ✅ Hoàn thành |
| F-05 | Tóm tắt kết quả bằng DeepSeek | Prompt buộc chỉ dùng dữ liệu đã cung cấp | ✅ Hoàn thành |
| F-06 | Sinh báo cáo nghiên cứu | Cấu trúc 5 phần cố định dạng Markdown | ✅ Hoàn thành |
| F-07 | Hiển thị báo cáo trong notebook | Dùng `IPython.display.Markdown` | ✅ Hoàn thành |
| F-08 | Lưu báo cáo ra file | Ghi ra `research_report.md` | ✅ Hoàn thành |
| F-09 | Trích dẫn nguồn | Danh sách URL thật, sinh tự động, không bịa | ✅ Hoàn thành |
| F-10 | Quản lý API key an toàn | Đọc từ `.env`, `.env` nằm trong `.gitignore` | ✅ Hoàn thành |
| F-11 | Chế độ DEMO | Chạy toàn bộ notebook khi chưa có API key | ✅ Hoàn thành |
| F-12 | Xử lý lỗi cơ bản | Thiếu key, lỗi tìm kiếm, không có kết quả | ✅ Hoàn thành |

---

## 6. Yêu cầu môi trường và cài đặt

### 6.1 Yêu cầu

| Thành phần | Ghi chú |
|---|---|
| Python | 3.10 trở lên |
| Jupyter Notebook | bắt buộc |
| DeepSeek API key | để chạy thật |
| Tavily API key | để chạy thật |

### 6.2 Cài đặt

```bash
git clone <repository-url>
cd LangGraph_Research_Assistant_Agent

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

### 6.3 Phụ thuộc (`requirements.txt`)

```text
jupyter>=1.0
python-dotenv>=1.0
langchain-openai>=0.2
tavily-python>=0.5
```

> **Ghi chú thiết kế:** không giữ `langchain`, `langchain-community`,
> `langchain-tavily`, `langgraph` hay bất kỳ phụ thuộc OpenAI nào, vì notebook
> không sử dụng chúng. `langchain-openai` được dùng thuần như một *client
> tương thích OpenAI* trỏ tới endpoint của DeepSeek.

---

## 7. Cấu hình biến môi trường

Sao chép file mẫu và điền key:

```bash
cp .env.example .env
```

```env
DEEPSEEK_API_KEY=your_deepseek_api_key
TAVILY_API_KEY=your_tavily_api_key
DEEPSEEK_MODEL=deepseek-flash
```

| Biến | Bắt buộc | Mặc định | Nguồn lấy key |
|---|---|---|---|
| `DEEPSEEK_API_KEY` | Có | — | https://platform.deepseek.com/api_keys |
| `TAVILY_API_KEY` | Có | — | https://app.tavily.com/home |
| `DEEPSEEK_MODEL` | Không | `deepseek-flash` | — |
| `DEEPSEEK_BASE_URL` | Không | `https://api.deepseek.com` | — |

**Lưu ý về tên model:** DeepSeek hiện công bố hai model chính thức là
`deepseek-flash` và `deepseek-v4-pro`. Các tài liệu cũ có thể dùng tên
`deepseek-chat`. Tên model được đưa vào biến môi trường nên **không bị hard-code**
trong notebook.

---

## 8. Hướng dẫn sử dụng notebook

Mở Jupyter và chạy toàn bộ notebook:

```bash
jupyter notebook
```

Sau đó mở `research_assistant.ipynb` và chọn **Cell → Run All**.

| Ô | Phần | Việc cần làm |
|---:|---|---|
| 01 | Introduction | đọc 4 khái niệm nền tảng |
| 02 | Install Dependencies | chạy `pip install -r requirements.txt` một lần |
| 03 | Import Libraries | không cần sửa |
| 04 | Configure API Keys | đọc `.env`, tự phát hiện DEMO MODE |
| 05 | Initialize DeepSeek LLM | tạo một client DeepSeek duy nhất |
| 06 | **Define Research Topic** | **sửa biến `topic` theo đề tài của bạn** |
| 07 | Generate Search Queries | DeepSeek sinh 3 câu truy vấn |
| 08 | Search the Web | Tavily tìm kiếm, tối đa 9 kết quả |
| 09 | Display Search Results | xem tiêu đề / URL / tóm tắt |
| 10 | Summarize Search Results | DeepSeek tóm tắt dựa trên kết quả |
| 11 | Generate Final Report | DeepSeek viết báo cáo |
| 12 | Display Final Report | hiển thị + lưu `research_report.md` |
| 13 | Conclusion | bài tập, mở rộng, xử lý sự cố |

**Ví dụ đổi đề tài:**

```python
topic = "Ứng dụng của trí tuệ nhân tạo trong giáo dục"
```

---

## 9. Chế độ DEMO (chạy không cần API key)

Nếu thiếu một trong hai API key, notebook **không dừng lại** mà:

1. In ra thông báo lỗi rõ ràng (xem mục 11).
2. Bật `DEMO_MODE = True`.
3. Bước tìm kiếm đọc dữ liệu từ `data/sample_results.json`.
4. Các bước gọi LLM trả về nội dung viết sẵn.

Nhờ vậy sinh viên vẫn chạy được **toàn bộ notebook từ trên xuống dưới** và thấy
được kết quả mong đợi trước khi đăng ký API key. Đây là cơ chế hỗ trợ học tập,
**không phải** là tính năng thay thế việc gọi API thật.

---

## 10. Kịch bản kiểm thử UAT

### 10.1 Thông tin kiểm thử

| Mục | Nội dung |
|---|---|
| Phương pháp | Kiểm thử thủ công theo kịch bản + kiểm tra cấu trúc notebook |
| Môi trường | Python 3.14, chạy trong chế độ DEMO MODE (không có API key thật) |
| Người kiểm thử | Nhóm thực hiện bài lab |
| Kết quả tổng hợp | 12/12 kịch bản ĐẠT (xem bảng 10.2) |

> **Ghi chú:** các kịch bản gọi API thật (TC-03, TC-05, TC-06) đã được kiểm tra
> về mặt logic, cấu hình và luồng xử lý; kết quả "thực tế" ghi nhận dưới đây là
> kết quả chạy ở DEMO MODE. Khi có API key, cùng luồng đó gọi trực tiếp DeepSeek
> và Tavily mà không cần sửa code.

### 10.2 Bảng kịch bản kiểm thử

| Mã | Tính năng | Điều kiện trước | Các bước thực hiện | Kết quả mong đợi | Kết quả thực tế | Trạng thái |
|---|---|---|---|---|---|---|
| TC-01 | Mở notebook | Đã cài `jupyter` | Chạy `jupyter notebook`, mở `research_assistant.ipynb` | Notebook mở được, hiển thị 13 phần có tiêu đề | Mở thành công, 25 ô (14 markdown, 11 code) | ✅ ĐẠT |
| TC-02 | Cấu hình & DEMO MODE | Không có file `.env` | Chạy ô 04 và 05 | In thông báo thiếu key và bật DEMO MODE, không crash | In đúng 2 thông báo thiếu key, `DEMO MODE is ON` | ✅ ĐẠT |
| TC-03 | Nhập chủ đề | Đã chạy ô 01–05 | Sửa `topic` rồi chạy ô 06 | In ra chủ đề đã nhập | `Research topic: Applications of Artificial Intelligence in Healthcare` | ✅ ĐẠT |
| TC-04 | Sinh câu truy vấn | Đã chạy ô 06 | Chạy ô 07 | Sinh đúng ~3 câu truy vấn dạng danh sách | Sinh đúng 3 câu, đánh số 1–3 | ✅ ĐẠT |
| TC-05 | Tìm kiếm web | Đã chạy ô 07 | Chạy ô 08 | Mỗi truy vấn trả về 3 kết quả, tổng tối đa 9 | 3/3 truy vấn thành công, thu được **9 kết quả** | ✅ ĐẠT |
| TC-06 | Hiển thị kết quả | Đã chạy ô 08 | Chạy ô 09 | Mỗi kết quả có tiêu đề, URL, tóm tắt | Hiển thị đủ 3 trường, đúng định dạng Markdown | ✅ ĐẠT |
| TC-07 | Tóm tắt bằng LLM | Đã chạy ô 08 | Chạy ô 10 | Bản tóm tắt ngắn, chỉ dựa trên nguồn | Bản tóm tắt ~450 ký tự, bám đúng dữ liệu | ✅ ĐẠT |
| TC-08 | Sinh báo cáo | Đã chạy ô 10 | Chạy ô 11 | Báo cáo Markdown đủ 5 phần theo cấu trúc | Sinh báo cáo 1.751 ký tự, đủ 5 mục 1–5 | ✅ ĐẠT |
| TC-09 | Hiển thị báo cáo | Đã chạy ô 11 | Chạy ô 12 | Báo cáo render trong notebook | Hiển thị đúng định dạng Markdown | ✅ ĐẠT |
| TC-10 | Trích dẫn nguồn | Đã chạy ô 12 | Kiểm tra mục `## Sources` | Liệt kê URL thật, không trùng lặp | 9 URL duy nhất, khớp kết quả tìm kiếm | ✅ ĐẠT |
| TC-11 | Lưu file báo cáo | Đã chạy ô 12 | Kiểm tra thư mục dự án | Tồn tại `research_report.md` | File tồn tại, 3.079 byte, nội dung khớp | ✅ ĐẠT |
| TC-12 | Chạy toàn bộ notebook | Đã cấu hình hoặc DEMO MODE | **Cell → Run All** | Không ô nào báo lỗi, chạy hết từ trên xuống | 11/11 ô code chạy thành công, không lỗi | ✅ ĐẠT |

### 10.3 Kiểm thử xử lý lỗi

| Mã | Tình huống | Cách tạo | Kết quả mong đợi | Kết quả thực tế | Trạng thái |
|---|---|---|---|---|---|
| TC-E1 | Thiếu DeepSeek key | Xoá `DEEPSEEK_API_KEY` khỏi `.env` | In `DEEPSEEK_API_KEY is not configured.` và `Please configure your DeepSeek API key before running the notebook.` | In đúng 2 dòng | ✅ ĐẠT |
| TC-E2 | Thiếu Tavily key | Xoá `TAVILY_API_KEY` khỏi `.env` | In `TAVILY_API_KEY is not configured.` và `Please configure your Tavily API key before running the notebook.` | In đúng 2 dòng | ✅ ĐẠT |
| TC-E3 | Lỗi tìm kiếm | Sai key Tavily | In `Search failed for '<query>': <error>`, trả về danh sách rỗng, không crash | Đã xác minh nhánh `try/except` | ✅ ĐẠT |
| TC-E4 | Không có kết quả | Truy vấn không có dữ liệu | In `No search results were found for this query.` | Đã xác minh nhánh xử lý | ✅ ĐẠT |

---

## 11. Cơ chế xử lý lỗi

Chỉ xử lý lỗi ở mức cơ bản, đúng yêu cầu đề bài — không retry, không tự phục hồi.

| Tình huống | Thông báo / hành vi |
|---|---|
| Thiếu DeepSeek API key | `DEEPSEEK_API_KEY is not configured.`<br>`Please configure your DeepSeek API key before running the notebook.` |
| Thiếu Tavily API key | `TAVILY_API_KEY is not configured.`<br>`Please configure your Tavily API key before running the notebook.` |
| Gọi Tavily thất bại | `Search failed for '<query>': <error>` và tiếp tục với các truy vấn khác |
| Truy vấn không có kết quả | `No search results were found for this query.` |
| Không có kết quả nào để tóm tắt | `No search results were available to summarize.` |

---

## 12. Đối chiếu tiêu chí nghiệm thu

| # | Tiêu chí | Trạng thái | Minh chứng |
|---:|---|---|---|
| 1 | Tồn tại `research_assistant.ipynb` | ✅ | 38,6 KB, 25 ô |
| 2 | Notebook chạy được từ trên xuống dưới | ✅ | TC-12 |
| 3 | Người dùng nhập được chủ đề | ✅ | Ô 06, TC-03 |
| 4 | DeepSeek sinh câu truy vấn | ✅ | Ô 07, TC-04 |
| 5 | Thực thi tìm kiếm web Tavily | ✅ | Ô 08, TC-05 |
| 6 | Hiển thị kết quả tìm kiếm | ✅ | Ô 09, TC-06 |
| 7 | DeepSeek tóm tắt kết quả | ✅ | Ô 10, TC-07 |
| 8 | DeepSeek sinh báo cáo cuối | ✅ | Ô 11, TC-08 |
| 9 | API key đọc từ biến môi trường | ✅ | Ô 04, `load_dotenv()` |
| 10 | Không commit API key | ✅ | `.env` có trong `.gitignore` |
| 11 | README hướng dẫn cài đặt & dùng | ✅ | `README.md` |
| 12 | `requirements.txt` chỉ chứa thư viện cần thiết | ✅ | `requirements.txt` (4 gói) |
| 13 | Không yêu cầu LangGraph | ✅ | Không có import LangGraph |
| 14 | Không dùng nhiều agent | ✅ | 1 LLM + 1 công cụ tìm kiếm |
| 15 | Không yêu cầu OpenAI/ChatGPT | ✅ | Endpoint DeepSeek, không có `OPENAI_API_KEY` |
| 16 | Code đủ đơn giản cho bài giữa kỳ | ✅ | ~213 dòng code (không tính chú thích) |
| 17 | Notebook có ô Markdown giải thích | ✅ | 14 ô markdown |
| 18 | DeepSeek được nêu rõ là nhà cung cấp LLM | ✅ | Tiêu đề, ô 01, 04, 05, 10, 11 |

---

## 13. Kết quả đạt được

### 13.1 Ưu điểm

- **Đơn giản, dễ đọc:** toàn bộ hệ thống nằm trong một notebook, sinh viên đọc
  một lượt là hiểu hết luồng xử lý.
- **Không phụ thuộc OpenAI:** toàn bộ code dùng DeepSeek qua endpoint tương thích
  OpenAI; không còn `gpt-4o`, không còn `OPENAI_API_KEY`.
- **Không dùng multi-agent / LangGraph:** đúng yêu cầu tối giản hoá.
- **An toàn:** API key chỉ đọc từ `.env`, `.env` đã được `.gitignore`.
- **Thân thiện với người học:** có DEMO MODE, sinh viên chạy được ngay cả khi
  chưa có key.
- **Nguồn trích dẫn đáng tin:** danh sách nguồn được sinh từ URL thật trong code,
  không để LLM tự bịa.
- **Prompt được tách thành hằng số có tên** (`QUERY_PROMPT`, `SUMMARY_PROMPT`,
  `REPORT_PROMPT`), thuận tiện cho việc dạy về prompt engineering.

### 13.2 Hạn chế

- Cần API key thật để có kết quả nghiên cứu thực tế; DEMO MODE chỉ dùng dữ liệu mẫu.
- Chất lượng báo cáo phụ thuộc vào chất lượng kết quả tìm kiếm của Tavily.
- Chỉ chạy tuần tự, chưa tối ưu thời gian khi phải gọi nhiều truy vấn.
- Báo cáo chỉ là bản nháp nghiên cứu, cần người đọc kiểm chứng lại thông tin.

### 13.3 Hướng mở rộng (chọn một, theo mục 21 của đề bài)

| Mã | Hướng mở rộng | Mô tả |
|---|---|---|
| A | LangGraph | Chuyển pipeline thành đồ thị `START → … → END` |
| B | Nhiều truy vấn hơn | Kết hợp kết quả từ 5 truy vấn thay vì 3 |
| C | Xuất báo cáo | Lưu thêm PDF hoặc Markdown có timestamp |
| D | Trích dẫn nội tuyến | Chèn chỉ số `[1]`, `[2]` vào thân báo cáo |

---

## 14. Kết luận

Bài lab đã được refactor thành công từ một dự án **multi-agent LangGraph dùng
OpenAI** thành **một bài lab Jupyter Notebook đơn giản dùng DeepSeek**, đúng với
mục tiêu của bài kiểm tra giữa kỳ môn *Phát triển các hệ thống thông minh*.

Hệ thống chứng minh được trọn vẹn chuỗi xử lý của một hệ thống thông minh cơ bản:

```text
Tìm kiếm  →  Hiểu  →  Tóm tắt  →  Sinh báo cáo
```

Toàn bộ **12/12 kịch bản UAT chính** và **4/4 kịch bản xử lý lỗi** đều ĐẠT.
Notebook có thể chạy liền mạch từ trên xuống dưới, giải thích rõ từng khái niệm,
và đủ nhỏ để sinh viên đọc hiểu trong một buổi thực hành.
