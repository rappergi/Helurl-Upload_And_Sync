# --- HELUP ---
## _Upload unlimited file to helurl.com_
## Đặc điểm
- Dung lương lưu trữ 50 TB nhưng chưa ai kiểm chứng :v
- Download và upload với tốc độ bàn thờ
- Stream phim thì không cần phải biết đợi chờ
- Tool cho phép upload mọi loại tệp không cần đổi đuôi file
- Tool hỗ trợ upload với tốc độ siêu nhanh và đa luồng, có thể tuỳ chỉnh.
- Tool tương thích trên mọi nền tảng, và có thể chuyển từ cloud này sang cloud khác với tốc độ bàn thờ (Em sẽ có video hướng dẫn sau sync từ bằng google colab hoặc vps với tốc độ bét tè lè nhè sau)

Do sản phẩm đang trong quá trình hoàn thiện nên chắc chắn không thể thiếu bug, nếu các bác thấy thì có thể liên hệ với em ở dưới phần liên hệ nhé.

***Nếu thấy hay thì các bác hãy ủng hộ cho em một sao để em có động lực tối ưu hoá và ra thêm những thứ hay ho ở những version sau nhé***
## Chuẩn bị

Để có thể sử dụng mọi người cần phải có những thứ sau:

- [Helurl](https://helurl.com) - Tất nhiên rồi, một tài khoản healurl!
- [Cookie Editor](https://chrome.google.com/webstore/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm) - dùng để Export cookie
- [Helup.py](https://github.com/nguyenlamnghia/Helup/releases/download/v1.0.0/helup.py) - Yêu cầu phải có python 3.x để chạy, nếu bạn không có python ư, hãy tải cái bên dưới
- [Helup.zip](https://github.com/nguyenlamnghia/Helup/releases/download/v1.0.0/helup.zip) - Đã nén lại và chỉ cần tải xuống, giải nén và chạy

**Tất cả các file đều 100% không có virut các bạn có thể tải check tại [**đây**](https://www.virustotal.com/gui/file-analysis/MWYyOTQyODkxZjgwZjBiM2QxMDI4ZTBlY2JhOTM4ODU6MTY5MDE5MjAxOQ==)**

## Hướng dẫn sửa dụng

***WINDOWS***

Bước 1: Mở cmd, chạy câu lệnh sau

```sh
helup config
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

***Video dành cho mấy bác lười đọc :v***

[![Watch the video](https://img.youtube.com/vi/wUMCu4r8wIA/hqdefault.jpg)](https://www.youtube.com/embed/wUMCu4r8wIA)

***UBUNTU***

B1: Tải file helup về máy bằng lệnh
```sh
wget https://github.com/nguyenlamnghia/Helup/releases/download/v1.0.0/helup.py
```

B2: Config helup bằng lệnh
```sh
python3 helup.py config
```
Nhấn enter, nhập token. Và sử dụng câu lệnh
```sh
sudo nano cookie.json
```
Để nhập cookie helurl vào, sau đó nhấp ctrl + o và nhấn enter để lưu, nhấn ctrl + x để thoát

B4: Chạy thôi


```sh
python3 helup.py copy <source> <target>
ex: python3 helup.py copy "D:\Data\Ảnh người yêu cũ" "backup/anh"
```


> Note: `-thread=số luồng` để chỉnh số file upload lên cùng một lúc tối đa
>
> Vd: ```python3 helup.py copy "D:\Data\Ảnh người yêu cũ" "backup/anh" -thread=8```

## Một số chú ý

1. File .exe có khác gì file .py không ?
- Chả khác gì chỉ là file chấm py có thể chạy được trên nhiều hệ điều hành hơn (Mình sẽ có video hướng dẫn sau nhé)
2. Upload được tất cả các file kể cả đuôi .mp4, mkv,... đúng không?
- Đúng có thể upload tất cả các file nhưng không được quá 10GB, do server nó cho có mỗi thế :v
3. Helurl có phải là nơi tốt và uy tín để lưu dữ liệu không?
- Hoàn toàn là nên đối với những bộ phim 🐖 còn dữ liệu quan trọng thì ae cứ chọn các nguồn uy tín như onedrive, gdrive. Chứ bản thân mình ngồi code cái này mà web sập lên sập xuống cay lắm :v. Cơ mà stream phim thì mượt như sunsilk
4. Nếu đường dẫn chứa dấu cách thì nhớ thêm dấu "" để không bị lỗi nhé
5. Đường dẫn phải có dạng "D:/xxx/yyy/zzz" hoặc "xxx/yyy/zzz" (Với file thì tương tự nhưng thêm tên file vào sau vd D:/xxx/yyy/zzz/ttt.zip)
6. Nếu file zip xảy ra lỗi các bác có thể thử cài đặt python 3.x và chạy file helup.py nhé 


## Liên hệ

Email: lamnghia.hust@gmail.com

Facebook (clone): [**Nguyễn Lâm Nghĩa**](https://www.facebook.com/nguyenlamnghia2003/)

## License

NghiaNL

**Nguyen Lam Nghia**
