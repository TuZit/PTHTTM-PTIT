# HƯỚNG DẪN CHẠY PROJECT BẰNG PYCHARM

> Tài liệu dành cho sinh viên môn **Phát triển các hệ thống thông minh — PTIT**
>
> Hướng dẫn chạy và tương tác với bài lab **AI Research Assistant**
> (`research_assistant.ipynb`) trên PyCharm, từ con số 0 đến khi có báo cáo.

---

## Mục lục

1. [Yêu cầu trước khi bắt đầu](#1-yêu-cầu-trước-khi-bắt-đầu)
2. [Cài đặt PyCharm](#2-cài-đặt-pycharm)
3. [Mở project đúng cách](#3-mở-project-đúng-cách)
4. [Tạo môi trường ảo (venv)](#4-tạo-môi-trường-ảo-venv)
5. [Cài đặt thư viện](#5-cài-đặt-thư-viện)
6. [Cấu hình API key (hoặc bỏ qua để chạy DEMO)](#6-cấu-hình-api-key-hoặc-bỏ-qua-để-chạy-demo)
7. [Mở notebook và chọn Jupyter server](#7-mở-notebook-và-chọn-jupyter-server)
8. [Chạy toàn bộ notebook](#8-chạy-toàn-bộ-notebook)
9. [Tương tác với notebook](#9-tương-tác-với-notebook)
10. [Kiểm tra kết quả đầu ra](#10-kiểm-tra-kết-quả-đầu-ra)
11. [Phím tắt và các nút cần biết](#11-phím-tắt-và-các-nút-cần-biết)
12. [Xử lý sự cố](#12-xử-lý-sự-cố)
13. [Cách dự phòng: chạy bằng Terminal / trình duyệt](#13-cách-dự-phòng-chạy-bằng-terminal--trình-duyệt)
14. [Checklist nhanh](#14-checklist-nhanh)

---

## 1. Yêu cầu trước khi bắt đầu

| Thành phần | Yêu cầu | Ghi chú |
|---|---|---|
| Python | **3.10 trở lên** | Kiểm tra: mở Terminal gõ `python --version` |
| PyCharm | **Community 2023.3+**, **Professional**, hoặc **PyCharm hợp nhất 2025.1+** | Xem mục 2 |
| Kết nối Internet | Có | Để cài thư viện và gọi API |
| DeepSeek API key | Không bắt buộc | Không có vẫn chạy được ở **DEMO MODE** |
| Tavily API key | Không bắt buộc | Không có vẫn chạy được ở **DEMO MODE** |

Kiểm tra Python đã cài chưa (Terminal của macOS/Linux, hoặc PowerShell của Windows):

```bash
python --version
# hoặc
python3 --version
```

Nếu chưa có Python, tải tại <https://www.python.org/downloads/> và **nhớ tick
"Add python.exe to PATH"** khi cài trên Windows.

---

## 2. Cài đặt PyCharm

Tải tại <https://www.jetbrains.com/pycharm/download/>. Cần biết về khả năng hỗ
trợ Jupyter của từng bản:

| Phiên bản PyCharm | Hỗ trợ Jupyter Notebook | Ghi chú |
|---|---|---|
| **Professional** | ✅ Đầy đủ | Bản trả phí; sinh viên có thể xin **free Educational license** |
| **Community 2023.3+** | ✅ Có hỗ trợ cơ bản | Chạy/chỉnh sửa ô, xem output, debug |
| **PyCharm hợp nhất 2025.1+** | ✅ Có (bản miễn phí cũng có Jupyter) | Từ 2025.1 JetBrains gộp Community + Professional |
| PyCharm cũ hơn 2023.3 | ❌ Không | Nếu không nâng cấp được, xem [mục 13](#13-cách-dự-phòng-chạy-bằng-terminal--trình-duyệt) |

> 💡 **Mẹo cho sinh viên:** đăng ký **PyCharm Professional miễn phí** bằng email
> sinh viên (`.edu` / email trường) tại
> <https://www.jetbrains.com/community/education/>.

---

## 3. Mở project đúng cách

> ⚠️ **Đây là bước quan trọng nhất.** Notebook đọc file
> `data/sample_results.json` bằng **đường dẫn tương đối**, nên thư mục làm việc
> phải là **thư mục gốc của project**. Nếu mở sai, bạn sẽ gặp lỗi
> `FileNotFoundError: 'data/sample_results.json'`.

**Cách mở:**

1. **File → Open…**
2. Trỏ tới **thư mục gốc** `LangGraph_Research_Assistant_Agent`
   (thư mục **chứa** `research_assistant.ipynb`), **không** mở file `.ipynb` lẻ.
3. PyCharm hỏi *"Open in new window / this window?"* → chọn tuỳ ý.
4. Nếu PyCharm hỏi **Trust Project** → chọn **Trust Project**.

**Kiểm tra đã mở đúng:** cây thư mục bên trái phải hiển thị:

```text
LangGraph_Research_Assistant_Agent
├── research_assistant.ipynb   ← file chính
├── README.md
├── requirements.txt
├── .env.example
└── data/
    └── sample_results.json
```

---

## 4. Tạo môi trường ảo (venv)

Môi trường ảo giúp thư viện của project **không lẫn** với Python hệ thống.

1. Mở **Settings** (Windows/Linux: `Ctrl + Alt + S`) hoặc
   **Preferences** (macOS: `⌘ + ,`).
2. Vào **Project: LangGraph_Research_Assistant_Agent → Python Interpreter**.
3. Bấm biểu tượng bánh răng ⚙️ → **Add Interpreter → Add Local Interpreter…**
4. Chọn **Virtualenv Environment** ở cột trái → chọn **New**.
5. Điền:
   - **Location:** `<đường-dẫn-project>/.venv`
   - **Base interpreter:** chọn Python **3.10+**
6. Bấm **OK**. PyCharm tạo `venv` và tự đặt làm interpreter của project.

> ✅ Sau bước này, góc dưới phải cửa sổ PyCharm phải hiện tên **`.venv`**.
> Nếu vẫn hiện `Python 3.x` khác, làm lại bước 2–6.

---

## 5. Cài đặt thư viện

Mở **Terminal** trong PyCharm: **View → Tool Windows → Terminal**
(`Alt + F12` trên Windows/Linux).

PyCharm tự kích hoạt `.venv` — bạn sẽ thấy tiền tố `(.venv)` ở đầu dòng lệnh.
Nếu **không** thấy, xem [mục 12](#12-xử-lý-sự-cố).

Chạy:

```bash
pip install -r requirements.txt
```

Cài thêm kernel cho Jupyter (bắt buộc để PyCharm chạy được notebook):

```bash
pip install ipykernel
```

Kiểm tra nhanh đã cài đủ:

```bash
python -c "import dotenv, tavily, langchain_openai; print('OK')"
```

Nếu in ra `OK` là môi trường đã sẵn sàng.

**Danh sách thư viện sẽ được cài:**

| Gói | Vai trò trong bài lab |
|---|---|
| `jupyter` | chạy notebook |
| `python-dotenv` | đọc API key từ file `.env` |
| `langchain-openai` | client gọi DeepSeek (endpoint tương thích OpenAI) |
| `tavily-python` | gọi API tìm kiếm Tavily |

---

## 6. Cấu hình API key (hoặc bỏ qua để chạy DEMO)

### 6.1. Cách 1 — Chạy thật với API key

1. Trong cây thư mục, bấm chuột phải vào `.env.example` → **Copy**.
2. Bấm chuột phải vào thư mục gốc → **Paste** → đổi tên thành `.env`.
3. Mở `.env` và điền key của bạn:

```env
DEEPSEEK_API_KEY=key_deepseek_cua_ban
TAVILY_API_KEY=key_tavily_cua_ban
DEEPSEEK_MODEL=deepseek-flash
```

| Biến | Lấy ở đâu |
|---|---|
| `DEEPSEEK_API_KEY` | <https://platform.deepseek.com/api_keys> |
| `TAVILY_API_KEY` | <https://app.tavily.com/home> |
| `DEEPSEEK_MODEL` | Không bắt buộc; mặc định `deepseek-flash` |

> 🔒 **Lưu ý bảo mật:** file `.env` đã có trong `.gitignore` nên sẽ **không** bị
> commit lên Git. Không bao giờ dán key trực tiếp vào notebook.

### 6.2. Cách 2 — Chạy DEMO MODE (không cần key)

**Bỏ qua bước 6.1.** Nếu thiếu một trong hai key, notebook sẽ:

1. In thông báo lỗi rõ ràng.
2. Tự bật **DEMO MODE**.
3. Đọc kết quả tìm kiếm từ `data/sample_results.json`.
4. Dùng nội dung viết sẵn cho các bước gọi LLM.

➡️ Notebook **vẫn chạy hết từ trên xuống dưới** và bạn thấy được output mẫu.
Đây là cách nhanh nhất để xem project hoạt động trước khi đăng ký API key.

---

## 7. Mở notebook và chọn Jupyter server

1. Trong cây thư mục, **nhấp đúp** vào `research_assistant.ipynb`.
   File sẽ có icon Jupyter (không mở dạng text).
2. Lần đầu chạy, PyCharm hiện hộp thoại chọn **Jupyter server**:
   - Chọn **Start managed server** (khuyến nghị) → PyCharm tự tạo một server
     Jupyter bằng interpreter `.venv`. Không cần làm gì thêm.
   - Hoặc chọn **Configure Jupyter Server** nếu bạn muốn dùng server có sẵn.
3. Chọn **kernel** ở thanh công cụ notebook (góc trên bên phải) → chọn kernel
   thuộc `.venv`.

**Cách kiểm tra đã đúng kernel:**

- Góc trên bên phải notebook hiển thị tên kernel/venv.
- Chạy ô **03. Import libraries** — nếu không báo `ModuleNotFoundError` là đúng.

### Bố cục notebook trong PyCharm

| Vùng | Ý nghĩa |
|---|---|
| **Thanh công cụ notebook** | Nút chạy ô, Run All, restart kernel, interrupt |
| **Thanh bên trái mỗi code cell** | Nút ▶ chạy riêng ô đó |
| **Cell menu** (menu trên cùng) | Run All, Clear Outputs, Cell Type… |
| **Jupyter Variables** (tool window) | Xem giá trị biến sau khi chạy |
| **Jupyter Server: Server Log** | Log của server, nút stop/start server |

---

## 8. Chạy toàn bộ notebook

**Cách 1 — Chạy tất cả (khuyến nghị cho lần đầu):**

- Bấm nút **Run All Cells** (▶▶) trên thanh công cụ notebook, hoặc
- Menu **Cell → Run All**, hoặc
- Phím tắt `Ctrl + Alt + Shift + Enter` (Windows/Linux).

**Cách 2 — Chạy tuần tự từng ô** (nên làm khi mới học):

- Chọn ô → bấm `Shift + Enter` để chạy và nhảy xuống ô dưới.

> ⏱️ Ở DEMO MODE, toàn bộ notebook chạy xong trong vài giây.
> Khi có API key thật, thời gian phụ thuộc tốc độ DeepSeek và Tavily (thường
> 20–60 giây cho toàn bộ 11 ô code).

**Thứ tự 13 phần của notebook:**

| Phần | Nội dung | Việc bạn cần làm |
|---:|---|---|
| 01 | Introduction | đọc |
| 02 | Install dependencies | chạy (đã cài ở bước 5) |
| 03 | Import libraries | chạy |
| 04 | Configure API keys | chạy, xem có bật DEMO MODE không |
| 05 | Initialize DeepSeek LLM | chạy |
| 06 | **Define research topic** | **sửa biến `topic`** |
| 07 | Generate search queries | chạy |
| 08 | Search the web | chạy |
| 09 | Display search results | chạy |
| 10 | Summarize search results | chạy |
| 11 | Generate final report | chạy |
| 12 | Display final report | chạy → sinh file báo cáo |
| 13 | Conclusion | đọc, làm bài tập |

---

## 9. Tương tác với notebook

Phần này trả lời câu hỏi *"làm sao để thực hiện tương tác"*.

### 9.1. Đổi đề tài nghiên cứu

Đây là tương tác chính. Tìm ô **06. Define the research topic**, sửa dòng:

```python
topic = "Applications of Artificial Intelligence in Healthcare"
```

thành đề tài của bạn, ví dụ:

```python
topic = "Ứng dụng của trí tuệ nhân tạo trong giáo dục"
```

Sau đó **chạy lại từ ô 06 trở xuống** (không cần chạy lại ô 02–05):

1. Bấm vào ô 06.
2. Menu **Cell → Run All Below** (hoặc `Ctrl + Shift + Enter` tuỳ keymap).

### 9.2. Chạy lại một ô đơn lẻ

- Bấm nút **▶** bên trái ô, hoặc chọn ô rồi `Shift + Enter`.
- Muốn chạy lại sạch sẽ: nút **Restart Kernel** (🔄) trên thanh công cụ, sau đó
  Run All. Dùng khi bạn nghi ngờ biến cũ còn sót lại trong bộ nhớ.

### 9.3. Chỉnh prompt (bài tập prompt engineering)

Ba prompt được đặt trong các hằng số có tên, rất dễ tìm và sửa:

| Hằng số | Ở ô | Tác dụng |
|---|---|---|
| `QUERY_PROMPT` | 07 | sinh câu truy vấn tìm kiếm |
| `SUMMARY_PROMPT` | 10 | tóm tắt kết quả tìm kiếm |
| `REPORT_PROMPT` | 11 | sinh báo cáo cuối cùng |

Ví dụ, thêm một mục mới vào báo cáo: sửa `REPORT_PROMPT` trong ô 11, thêm dòng

```text
6. Future Work
```

vào phần "Structure the report as:", rồi chạy lại ô 11 và 12.

### 9.4. Đổi số lượng truy vấn / số kết quả

```python
# ô 07: đổi số câu truy vấn
queries = generate_queries(topic, n=5)

# ô 04: đổi số kết quả mỗi truy vấn (cẩn thận dùng nhiều API credit hơn)
MAX_RESULTS_PER_QUERY = 5
```

Sau khi sửa, chạy lại các ô liên quan.

### 9.5. Xem giá trị biến khi đang chạy

Mở **View → Tool Windows → Jupyter Variables**. Sau khi chạy ô 08, bạn sẽ thấy:

| Biến | Ý nghĩa |
|---|---|
| `topic` | chủ đề đang nghiên cứu |
| `queries` | danh sách câu truy vấn |
| `search_results` | danh sách kết quả tìm kiếm |
| `summary` | bản tóm tắt của DeepSeek |
| `report` | báo cáo thô do DeepSeek viết |
| `final_report` | báo cáo cuối cùng (đã kèm nguồn) |
| `DEMO_MODE` | `True` nếu đang chạy bằng dữ liệu mẫu |

Đây là cách tốt để **hiểu dữ liệu chảy qua từng bước**.

### 9.6. Thử nghiệm nhanh trong Python Console

Mở **View → Tool Windows → Python Console**, chọn interpreter `.venv`, rồi thử:

```python
print(topic)
print(queries)
len(search_results)
print(search_results[0]["url"])
```

> ⚠️ Python Console là **phiên riêng**, không dùng chung biến với notebook.
> Muốn dùng biến của notebook, hãy chạy trực tiếp trong ô code.

### 9.7. Debug một ô (tính năng mạnh của PyCharm)

1. Bấm vào lề trái của dòng code để đặt **breakpoint** (chấm đỏ).
2. Bấm nút **Debug Cell** (🐞) trên thanh công cụ, hoặc chuột phải vào ô →
   **Debug Cell**.
3. Khi chương trình dừng, dùng panel **Debug** để xem biến, bước từng dòng
   (`F8`), chạy tiếp (`F9`).

Rất hữu ích để xem chính xác `search_results` được tạo ra như thế nào.

### 9.8. Dừng khi chạy quá lâu

- Bấm **Interrupt Kernel** (⏸) trên thanh công cụ để dừng ô đang chạy.
- Bấm **Restart Kernel** (🔄) để xoá sạch bộ nhớ và bắt đầu lại.

### 9.9. Lưu báo cáo

Ô 12 tự động ghi báo cáo ra file **`research_report.md`** ở thư mục gốc. Sau khi
chạy, file này xuất hiện trong cây thư mục — bấm đúp để mở và xem trước.

> 💡 File `research_report.md` nằm trong `.gitignore` vì đây là **kết quả sinh ra**,
> không phải mã nguồn.

---

## 10. Kiểm tra kết quả đầu ra

Sau khi **Run All** thành công, bạn phải thấy:

| Nơi | Kết quả mong đợi |
|---|---|
| Ô 04 | `DEMO MODE is ON...` (nếu chưa có key) hoặc `Configuration OK` |
| Ô 07 | 3 câu truy vấn được đánh số 1–3 |
| Ô 08 | `Total results collected: 9` |
| Ô 09 | Danh sách kết quả có **tiêu đề + URL + tóm tắt** |
| Ô 10 | Một đoạn tóm tắt ngắn |
| Ô 11 | `Report generated (xxxx characters).` |
| Ô 12 | Báo cáo Markdown hiển thị đẹp + dòng `saved to research_report.md` |
| Thư mục gốc | Xuất hiện file `research_report.md` |

Nếu mọi thứ khớp → project đã chạy đúng. 🎉

---

## 11. Phím tắt và các nút cần biết

| Thao tác | Phím tắt / Nút |
|---|---|
| Chạy ô hiện tại, nhảy xuống ô dưới | `Shift + Enter` |
| Chạy ô hiện tại, giữ nguyên vị trí | `Ctrl + Enter` |
| Chạy ô hiện tại và **tạo ô mới** bên dưới | `Alt + Enter` |
| Chạy toàn bộ notebook | `Ctrl + Alt + Shift + Enter` hoặc nút ▶▶ |
| Debug một ô | Nút 🐞 / chuột phải → Debug Cell |
| Dừng ô đang chạy | Nút ⏸ (Interrupt Kernel) |
| Khởi động lại kernel | Nút 🔄 (Restart Kernel) |
| Chuyển ô Code ↔ Markdown | Menu **Cell → Cell Type** |
| Mở Terminal | `Alt + F12` |
| Mở Settings | `Ctrl + Alt + S` (macOS: `⌘ + ,`) |

---

## 12. Xử lý sự cố

| Thông báo / Triệu chứng | Nguyên nhân | Cách khắc phục |
|---|---|---|
| `FileNotFoundError: 'data/sample_results.json'` | Working directory không phải thư mục gốc | Đóng project, **File → Open** lại **thư mục gốc**. Hoặc **Run → Edit Configurations → Jupyter**, đặt *Working directory* = thư mục gốc |
| `ModuleNotFoundError: No module named 'dotenv'` (hoặc `langchain_openai`, `tavily`) | Chưa cài thư viện, hoặc notebook dùng nhầm kernel hệ thống | Chạy `pip install -r requirements.txt` trong Terminal của project, rồi chọn lại kernel `.venv` |
| `Jupyter package is not installed` | Thiếu `jupyter` / `ipykernel` trong venv | `pip install jupyter ipykernel` |
| Không thấy kernel nào để chọn | Kernel chưa được đăng ký | `pip install ipykernel` → **Settings → Languages & Frameworks → Jupyter → Managed server** → chọn interpreter `.venv` |
| Notebook mở ra dạng file text, không có nút ▶ | PyCharm quá cũ (< 2023.3) hoặc tệp bị mở bằng chế độ text | Cập nhật PyCharm; chuột phải file → **Open With → Jupyter Notebook**; hoặc dùng [mục 13](#13-cách-dự-phòng-chạy-bằng-terminal--trình-duyệt) |
| Terminal không hiện `(.venv)` | Chưa kích hoạt venv | macOS/Linux: `source .venv/bin/activate` — Windows: `.venv\Scripts\activate` |
| `DEEPSEEK_API_KEY is not configured.` | Chưa tạo `.env` hoặc chưa điền key | Xem [mục 6](#6-cấu-hình-api-key-hoặc-bỏ-qua-để-chạy-demo) |
| Notebook vẫn ở DEMO MODE dù đã điền key | File `.env` sai vị trí (phải ở **thư mục gốc**), hoặc chưa **Restart Kernel** | Kiểm tra vị trí `.env`, lưu file, **Restart Kernel** rồi Run All |
| `Search failed for '...'` | Key Tavily sai hoặc mất mạng | Kiểm tra `TAVILY_API_KEY` và kết nối Internet |
| `401 Unauthorized` từ DeepSeek | Key DeepSeek sai/hết hạn/hết credit | Kiểm tra lại key tại <https://platform.deepseek.com> |
| Chạy mãi không xong | API chậm hoặc mạng lag | Bấm **Interrupt Kernel** ⏸ rồi chạy lại |
| Kết quả cũ vẫn còn sau khi sửa code | Biến cũ còn trong bộ nhớ kernel | **Restart Kernel** 🔄 rồi **Run All** |
| PyCharm báo "Trust Project?" | Cơ chế an toàn của PyCharm | Chọn **Trust Project** (đây là project của bạn) |

---

## 13. Cách dự phòng: chạy bằng Terminal / trình duyệt

Nếu PyCharm của bạn không hỗ trợ notebook (bản quá cũ), **project vẫn chạy được
bình thường** bằng Terminal ngay trong PyCharm (`Alt + F12`):

```bash
# đảm bảo đang ở thư mục gốc project
jupyter notebook
```

Trình duyệt sẽ tự mở. Sau đó:

1. Bấm vào `research_assistant.ipynb`.
2. Menu **Cell → Run All**.
3. Xem kết quả ngay trên trình duyệt.

Muốn dừng server: quay lại Terminal và bấm `Ctrl + C`.

Cách này dùng **chính xác cùng** file notebook, cùng `.env`, cùng `.venv` — không
có gì khác biệt về kết quả.

---

## 14. Checklist nhanh

Dán checklist này vào báo cáo nếu cần:

- [ ] Đã cài PyCharm (Community 2023.3+ / Professional / bản hợp nhất 2025.1+).
- [ ] Đã mở **đúng thư mục gốc** của project.
- [ ] Đã tạo virtual environment `.venv` với Python 3.10+.
- [ ] Đã chạy `pip install -r requirements.txt`.
- [ ] Đã chạy `pip install ipykernel`.
- [ ] (Tuỳ chọn) Đã tạo file `.env` với `DEEPSEEK_API_KEY` và `TAVILY_API_KEY`.
- [ ] Đã mở `research_assistant.ipynb` và chọn kernel `.venv`.
- [ ] Đã chạy **Run All** không có ô nào báo lỗi.
- [ ] Đã đổi `topic` ở ô 06 và chạy lại để thấy kết quả thay đổi.
- [ ] Đã xem biến trong **Jupyter Variables**.
- [ ] Đã kiểm tra file `research_report.md` được tạo ra.

---

## Phụ lục — Tài liệu tham khảo

- Hỗ trợ Jupyter Notebook trong PyCharm:
  <https://www.jetbrains.com/help/pycharm/ipython-notebook-support.html>
- Chạy ô notebook trong PyCharm:
  <https://www.jetbrains.com/help/pycharm/running-ipython-notebook-cells.html>
- Cấu hình Jupyter server & kernel:
  <https://www.jetbrains.com/help/pycharm/configuring-jupyter-notebook.html>
- PyCharm miễn phí cho sinh viên:
  <https://www.jetbrains.com/community/education/>
- DeepSeek API Docs: <https://api-docs.deepseek.com/>
- Tavily: <https://docs.tavily.com/>
