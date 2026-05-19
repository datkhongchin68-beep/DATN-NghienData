# Git Workflow Guide cho Data Team

Tài liệu này hướng dẫn cách làm việc với Git/GitHub trong dự án Data. Mục tiêu là giúp team làm việc thống nhất, tránh mất code và kiểm soát tốt thay đổi trước khi đưa lên production.

---

## 1. Cấu trúc branch

Dự án sử dụng mô hình branch theo vai trò.

```text
production
└── stagging
    └── develop
        ├── ba
        ├── da
        ├── de
        └── ae
```

Ý nghĩa:

| Branch | Mục đích |
|---|---|
| `production` | Bản chính thức, ổn định, dùng cho deploy thật |
| `stagging` | Nhánh kiểm thử cuối cùng trước khi lên production; Tester làm việc và xác nhận tại đây |
| `develop` | Nhánh tích hợp chung của team trước khi đưa sang `stagging` |
| `ba` | Business Analyst: requirement, business rules, acceptance criteria |
| `da` | Data Analyst: analysis, dashboard, report, metrics |
| `de` | Data Engineer: pipeline, ingestion, data warehouse |
| `ae` | Analytics Engineer: dbt, transformation, data models |

---

## 2. Luồng làm việc chuẩn

```text
ba / da / de / ae
        ↓ Pull Request
      develop
        ↓ Khi đã review xong
      stagging
        ↓ Tester xác nhận pass
    production
```

Quy trình:

1. BA, DA, DE, AE làm việc trên branch theo vai trò của mình.
2. Sau khi hoàn thành, push code lên branch của mình.
3. Tạo Pull Request vào `develop`.
4. Reviewer kiểm tra code/tài liệu/kết quả.
5. Khi `develop` ổn, Lead merge `develop` vào `stagging`.
6. Tester kiểm thử trên `stagging`.
7. Nếu test pass, Lead/PM merge `stagging` vào `production`.
8. Nếu test fail, tạo issue bug và yêu cầu người phụ trách sửa trên branch vai trò tương ứng.

---

## 3. Vai trò của Tester

Tester không làm việc trực tiếp trên branch `develop` hoặc `production`.

Tester kiểm thử trên nhánh:

```text
stagging
```

Tester chịu trách nhiệm:

```text
- Kiểm tra dữ liệu sau khi code đã được merge vào stagging.
- Kiểm tra dashboard/report/model/pipeline theo acceptance criteria.
- Ghi nhận bug nếu kết quả sai.
- Xác nhận pass trước khi release lên production.
```

Luồng kiểm thử:

```text
develop → stagging → Tester test → production
```

Nếu phát hiện lỗi:

```text
stagging test fail
        ↓
Tạo bug issue
        ↓
BA/DA/DE/AE sửa trên branch của mình
        ↓
Pull Request lại vào develop
        ↓
Merge lại sang stagging để Tester test lại
```

---

## 4. Quy tắc bắt buộc

```text
Không commit trực tiếp vào production.
Không commit trực tiếp vào stagging, trừ người được phân quyền release/test.
Không merge trực tiếp từ branch vai trò vào production.
Không merge trực tiếp từ branch vai trò vào stagging.
Không tự merge Pull Request của mình nếu chưa có review.
Luôn pull code mới nhất trước khi bắt đầu làm việc.
Mọi thay đổi quan trọng phải đi qua Pull Request.
```

Luồng đúng:

```text
ba → develop → stagging → production
da → develop → stagging → production
de → develop → stagging → production
ae → develop → stagging → production
```

Luồng sai:

```text
da → production
de → production
ae → production
ba → production

da → stagging
de → stagging
ae → stagging
ba → stagging
```

---

## 5. Cách làm việc hằng ngày cho BA/DA/DE/AE

### Bước 1: Lấy code mới nhất từ `develop`

```bash
git checkout develop
git pull origin develop
```

### Bước 2: Chuyển sang branch của mình

Ví dụ với DA:

```bash
git checkout da
git pull origin da
git merge develop
```

Các vai trò khác thay `da` bằng branch tương ứng:

```bash
git checkout ba
git checkout de
git checkout ae
```

### Bước 3: Làm việc và kiểm tra file thay đổi

```bash
git status
```

### Bước 4: Commit thay đổi

```bash
git add .
git commit -m "analysis(da): add weekly revenue analysis"
```

### Bước 5: Push lên branch của mình

```bash
git push origin da
```

### Bước 6: Tạo Pull Request trên GitHub

Trên GitHub, tạo Pull Request với cấu hình:

```text
Base: develop
Compare: branch của bạn
```

Ví dụ:

```text
Base: develop
Compare: da
```

---

## 6. Cách Tester kiểm thử trên `stagging`

### Bước 1: Lấy bản mới nhất của `stagging`

```bash
git checkout stagging
git pull origin stagging
```

### Bước 2: Chạy test hoặc kiểm tra kết quả

Tester kiểm tra theo tài liệu yêu cầu:

```text
- Acceptance criteria
- Test cases
- Data validation rules
- Dashboard/report output
- Pipeline output
- Data quality checks
```

### Bước 3: Nếu test pass

Comment vào Pull Request hoặc issue:

```text
Tester confirmed: PASS on stagging
```

Sau đó Lead/PM có thể merge:

```text
stagging → production
```

### Bước 4: Nếu test fail

Tạo bug issue với format:

```text
[BUG][STAGGING] Mô tả lỗi ngắn
```

Ví dụ:

```text
[BUG][STAGGING] Revenue dashboard shows incorrect total sales
```

Nội dung bug nên có:

```markdown
## Lỗi phát hiện
Mô tả lỗi.

## Môi trường
Branch: stagging

## Kết quả hiện tại
Kết quả đang sai là gì?

## Kết quả mong muốn
Kết quả đúng phải là gì?

## Bằng chứng
Ảnh chụp màn hình, query, log hoặc file liên quan.

## Người phụ trách sửa
BA/DA/DE/AE tương ứng.
```

---

## 7. Commit convention

Format commit:

```text
<type>(<role>): <message>
```

Ví dụ:

```text
docs(ba): add sales dashboard requirement
analysis(da): add customer retention analysis
feat(de): add orders ingestion pipeline
model(ae): add fct_orders model
test(tester): validate revenue dashboard on stagging
fix(de): handle null order timestamp
```

Danh sách `type` thường dùng:

| Type | Khi dùng |
|---|---|
| `feat` | Thêm tính năng mới |
| `fix` | Sửa lỗi |
| `docs` | Cập nhật tài liệu |
| `test` | Thêm/sửa test hoặc ghi nhận kiểm thử |
| `model` | Thêm/sửa data model hoặc dbt model |
| `analysis` | Notebook hoặc phân tích dữ liệu |
| `dashboard` | Dashboard hoặc report |
| `config` | Cấu hình |
| `chore` | Việc nhỏ, cleanup |

---

## 8. Pull Request convention

Tên Pull Request nên theo format:

```text
[ROLE][TYPE] Mô tả ngắn
```

Ví dụ:

```text
[BA][DOCS] Add revenue metric definition
[DA][DASHBOARD] Add weekly sales dashboard
[DE][FEATURE] Add orders ingestion pipeline
[AE][MODEL] Add fct_orders model
```

Nội dung Pull Request nên có:

```markdown
## Mục tiêu
Mô tả thay đổi này để làm gì.

## Thay đổi chính
- ...

## Ảnh hưởng dữ liệu
- Có thay đổi schema không?
- Có thay đổi metric không?
- Có cần backfill không?

## Cách test
- ...

## Checklist
- [ ] Đã pull code mới nhất từ develop
- [ ] Đã chạy test local nếu có
- [ ] Đã cập nhật tài liệu nếu cần
- [ ] Đã gắn issue liên quan nếu có
```

---

## 9. Quy định review và merge

| Nguồn | Đích | Người nên review/approve |
|---|---|---|
| `ba` | `develop` | PM/Data Lead |
| `da` | `develop` | BA hoặc AE |
| `de` | `develop` | Data Lead hoặc Tester |
| `ae` | `develop` | DE hoặc DA |
| `develop` | `stagging` | Data Lead/Tech Lead |
| `stagging` | `production` | PM/Data Lead/Tech Lead sau khi Tester pass |

---

## 10. Quy trình release

```text
1. BA/DA/DE/AE merge công việc vào develop qua Pull Request.
2. Lead kiểm tra develop đã ổn định.
3. Lead tạo Pull Request từ develop vào stagging.
4. Tester kiểm thử trên stagging.
5. Nếu pass, Lead/PM merge stagging vào production.
6. Nếu fail, tạo bug issue và quay lại bước sửa lỗi.
```

Release flow:

```text
develop → stagging → production
```

---

## 11. Khi bị conflict

Nếu Git báo conflict, không tự sửa nếu chưa chắc chắn.

Cách xử lý khuyến nghị:

1. Dừng lại, không push tiếp.
2. Báo cho Lead hoặc người phụ trách Git.
3. Gửi thông tin branch đang làm và file bị conflict.
4. Chỉ tiếp tục sau khi conflict đã được xử lý đúng.

---

## 12. Quy tắc 5 dòng cần nhớ

```text
1. Không làm trực tiếp trên production.
2. BA/DA/DE/AE làm trên branch riêng: ba, da, de, ae.
3. Làm xong thì tạo Pull Request vào develop.
4. Tester chỉ kiểm thử trên stagging.
5. Chỉ khi stagging đã test pass thì mới merge vào production.
```

---

## 13. Tóm tắt workflow

```text
Làm việc trên branch vai trò
        ↓
Commit thay đổi
        ↓
Push lên GitHub
        ↓
Tạo Pull Request vào develop
        ↓
Review
        ↓
Merge vào develop
        ↓
Merge develop vào stagging
        ↓
Tester kiểm thử
        ↓
Merge stagging vào production
```
