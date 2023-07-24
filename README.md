# --- HELUP ---
## _Upload unlimited file to helurl.com_
## Đặc điểm
- Dung lương lưu trữ 50 TB nhưng chưa ai kiểm chứng :v
- Download và upload với tốc độ bàn thờ
- Stream phim thì không cần phải biết đợi chờ
- Tool hỗ trợ upload mọi loại tệp (Dung lượng file < 10Gb)
- Tool hỗ trợ trên mọi nền tảng, và có thể chuyển từ cloud này sang cloud khác với tốc độ bàn thờ (Mình sẽ có video hướng dẫn sau nếu được mọi người ủng hộ)

## Chuẩn bị

Để có thể sử dụng mọi người cần phải có những thứ sau:

- [Helurl](https://helurl.com) - Tất nhiên rồi, một tài khoản healurl!
- [Cookie Editor](https://chrome.google.com/webstore/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm) - dùng để Export cookie
- [Helup.py](https://github.com/nguyenlamnghia/Helup/releases/download/v1.0.0/helup.py) - Yêu cầu phải có python 3.x để chạy, nếu bạn không có python ư, hãy tải cái bên dưới
- [Helup.zip](https://github.com/nguyenlamnghia/Helup/releases/download/v1.0.0/helup.zip) - Đã nén lại và chỉ cần tải xuống, giải nén và chạy

**Tất cả các file đều 100% không có virut các bạn có thể tải check tại [**đây**](https://www.virustotal.com/gui/file/22d46411ce864b5d5e6cd24ba4cbc2d8418e0bd29bdf43b90cef22e56b78ed2d?nocache=1)**

## Hướng dẫn sửa dụng

Bước 1: Mở cmd, chạy câu lệnh sau

```sh
helurl config
```

B2: Truy cập vào trang https://helurl.com và đăng nhập sau đó sử dụng Cookie Editor export cookie và dán vào file cookie.json lưu lại và thoát

B3: Lấy api token [**tại đây**](https://helurl.com/account-settings) sau đó dán vào cmd và nhấn enter

B4: Sử dụng câu lệnh để sau để copy file hoặc folder lên Helurl

```sh
helup copy <source> <target>
ex: helup copy "D:\Data\Ảnh người yêu cũ" "backup/anh"
``` 

> Note: `-thread=số luồng` để chỉnh số file upload lên cùng một lúc tối đa
>
> Vd: ```helup copy "D:\Data\Ảnh người yêu cũ" "backup/anh" -thread=8```

## Một số chú ý

1. File .exe có khác gì file .py không ?
- Chả khác gì chỉ là file chấm py có thể chạy được trên nhiều hệ điều hành hơn (Mình sẽ có video hướng dẫn sau nhé)
2. Upload được tất cả các file kể cả đuôi .mp4, mkv,... đúng không?
- Đúng có thể upload tất cả các file nhưng không được quá 10GB, do server nó cho có mỗi thế :v
3. Helurl có phải là nơi tốt và uy tín để lưu dữ liệu không?
- Hoàn toàn là nên đối với những bộ phim 🐖 còn dữ liệu quan trọng thì ae cứ chọn các nguồn uy tín như onedrive, gdrive. Chứ bản thân mình ngồi code cái này mà web sập lên sập xuống cay lắm :v. Cơ mà stream phim thì mượt như sunsilk
4. Nếu đường dẫn chứa dấu cách thì nhớ thêm dấu "" để không bị lỗi nhé


## Liên hệ

Email: lamnghia.hust@gmail.com

Facebook (clone): 

## License

NghiaNL

**Nguyen Lam Nghia**
