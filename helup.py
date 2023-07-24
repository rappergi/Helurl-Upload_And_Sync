import os
import sys
# import thư viện tách dấu \ và dấu / thành mảng
import re
import json
import requests
import mimetypes
import argparse
# Kiểm tra hệ điều hành
import platform

VERSION = '1.0.0'

chunk_size = 50 * 1024 * 1024
batch_size = 10
etags = []
counter = 1

# Hàm đếm tổng số file có trong folder

def save_cookie():
    with open('cookie.json', 'a+', encoding='utf-8') as f:
        f.write('')
    if platform.uname().system == 'Windows':
        os.system('cookie.json')
    else:
        input("[+] We just created cookie.json, please open to config, and hit ENTER!")
    print("[+] Cookie is saved")

def save_key(key):
    with open('key.txt', 'w', encoding='utf-8') as f:
        f.write(key)
    print("[+] Key is saved")

def count_files_in_folder(local_path):
    total_files = 0

    def count_files_recursively(folder_path):
        nonlocal total_files

        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)

            if os.path.isfile(item_path):
                total_files += 1
            elif os.path.isdir(item_path):
                # Đệ quy để duyệt qua tất cả các tệp và thư mục con
                count_files_recursively(item_path)

    # Gọi hàm đệ quy để đếm số lượng tệp trong thư mục gốc và các thư mục con
    count_files_recursively(local_path)

    return total_files

# Hàm kiểm tra xem một đường dẫn là tệp (file) hay thư mục (folder)
def is_file_or_folder(path):
    return os.path.isfile(path), os.path.isdir(path)

# Hàm tải lên một tệp (file) lên server với đường dẫn tương ứng trên server
def upload_file(local_file_path, server_file_id):
    global counter
    print(f"[+] UPLOADING {local_file_path}")
    # Thực hiện tải lên tệp lên server với đường dẫn tương ứng trên server bằng cách gọi API
    # hoặc sử dụng các phương thức tương ứng của dịch vụ lưu trữ. (Bạn cần thay thế phần này
    # bằng code thực tế cho việc tải lên tệp.)
    with open('cookie.json', 'r', encoding='utf-8') as file:
        read_cookie = json.load(file)
    dirOfFile = local_file_path
    nameOfFile = os.path.basename(dirOfFile)
    # print(f"[+] Standarding ...")
    # print("[+] Hold Ctrl and press C to stop...")
    # print(f"[+] Uploading {nameOfFile} ...")
    headers1 = {
        'X-Xsrf-Token': read_cookie[2]["value"].replace("%3D","="),
        'Cookie':f'activeWorkspaceId=0; {read_cookie[1]["name"]}={read_cookie[1]["value"]}; XSRF-TOKEN={read_cookie[2]["value"]}; helurlcom_free_file_upload_and_sharing_session={read_cookie[0]["value"]}',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Referer':'https://helurl.com/drive'
    }

    clientMime = str(mimetypes.guess_type(nameOfFile))[2:-8]
    file_stats = os.stat(dirOfFile).st_size
    split_tup = os.path.splitext(nameOfFile)[1]

    payload1 = {
        "workspaceId":0,
        "parentId": server_file_id,
        "relativePath":"",
        "disk":"uploads",
        "mime": clientMime,
        "filename":nameOfFile,
        "size": file_stats,
        "extension":split_tup[1:]
    }

    with requests.Session() as s:
        s.headers = headers1
        html = s.post('https://helurl.com/api/v1/s3/multipart/create', data=payload1)
        create_download = html.json()

        with open(dirOfFile, 'rb') as file:
            part_number = 1
            while True:
                chunk = file.read(chunk_size)
                if not chunk:
                    break
                payload2 = {
                    "partNumbers": [part_number],
                    "uploadId": create_download['uploadId'],
                    "key": create_download['key']
                }
                payload2_json = json.dumps(payload2)
                headers2 = {
                    'Referer':'https://helurl.com/drive',
                    'Origin':'https://helurl.com',
                    'Sec-Ch-Ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
                    'Sec-Fetch-Mode':'cors',
                    'Sec-Ch-Ua-Platform':"Windows",
                    'Sec-Fetch-Dest':'empty',
                    'Sec-Fetch-Site':'same-origin',
                    'Accept-Encoding':'gzip, deflate, br',
                    'Sec-Ch-Ua-Mobile':'?0',
                    'Accept':'application/json, text/plain, */*',
                    'Accept-Language':'vi,en;q=0.9,fr;q=0.8',
                    'Content-Length':'174',
                    'Content-Type':'application/json',
                    'Connection': 'keep-alive'
                }
                html = s.post('https://helurl.com/api/v1/s3/multipart/batch-sign-part-urls', data=payload2_json, headers=headers2)
                list_urls = html.json()
                signed_urls = html.json()['urls']
                url = signed_urls[0]['url']
                headers_put = {'Content-Length': str(len(chunk))}
                response = requests.put(url, data=chunk, headers=headers_put)
                etags.append(response.headers.get('Etag'))
                # Check the response status and handle any errors if needed
                if response.status_code != 200:
                    # Handle the error, for example, abort the upload, retry, or raise an exception
                    print(f"Error uploading chunk {part_number}: {response.text}")
                    break
                part_number += 1

        # print("[+] Finishing upload ...")
        payload = {
            "uploadId": create_download['uploadId'],
            "key": create_download['key'],
            "parts": [{"PartNumber": i, "ETag": etags[i - 1]} for i in range(1, part_number)]
        }
        payload = json.dumps(payload)
        response = s.post('https://helurl.com/api/v1/s3/multipart/complete', data=payload, headers=headers2)
        payload3 = {
            "workspaceId":0,
            "parentId": server_file_id,
            "relativePath":"",
            "disk":"uploads",
            "clientMime":clientMime,
            "clientName": nameOfFile,
            "filename":create_download['key'][-36:],
            "size": file_stats,
            "clientExtension":split_tup[1:]
        }
        payload3 = json.dumps(payload3)
        response = s.post('https://helurl.com/api/v1/s3/entries', data=payload3, headers=headers2)
        print(f"[{counter}/{total_files}] SUCCESSFUL UPLOAD | {local_file_path}")
        counter += 1
    pass

# Hàm tải lên một thư mục và tất cả các tệp con bên trong
def upload_folder_contents(local_folder_path, server_folder_path, server_folder_id,thread):
    import concurrent.futures
    with concurrent.futures.ThreadPoolExecutor(max_workers=thread) as executor:
        futures = []
        for item in os.listdir(local_folder_path):
            item_path = os.path.join(local_folder_path, item)
            item_server_path = os.path.join(server_folder_path, item)

            if os.path.isfile(item_path):
                # Lấy tên folder cua server tai file
                future = executor.submit(upload_file, item_path, server_folder_id)
                # Upload tệp lên máy chủ với đường dẫn tương ứng trên server
                futures.append(future)

            elif os.path.isdir(item_path):
                # Đệ quy để duyệt qua các tệp và thư mục con trong thư mục con hiện tại
                upload_folder_contents(item_path, item_server_path,get_id_folder(item_server_path),thread)
        for future in futures:
            future.result()

# Lấy toàn bộ name_subfolder và id_subfolder trên id_folder và trả về một mảng dạng
# [{
# "name" : "the name",
# "id": "1"
# }]

def create_folder(name,parentId):
    with open('cookie.json', 'r', encoding='utf-8') as file:
        read_json = json.load(file)
    headers = {
        'X-Xsrf-Token': read_json[2]["value"].replace("%3D","="),
        'Cookie':f'activeWorkspaceId=0; {read_json[1]["name"]}={read_json[1]["value"]}; XSRF-TOKEN={read_json[2]["value"]}; helurlcom_free_file_upload_and_sharing_session={read_json[0]["value"]}',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Referer':'https://helurl.com/drive',
        'Referer':'https://helurl.com/drive',
        'Origin':'https://helurl.com',
        'Sec-Ch-Ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'Sec-Fetch-Mode':'cors',
        'Sec-Ch-Ua-Platform':"Windows",
        'Sec-Fetch-Dest':'empty',
        'Sec-Fetch-Site':'same-origin',
        'Accept-Encoding':'gzip, deflate, br',
        'Sec-Ch-Ua-Mobile':'?0',
        'Accept':'application/json, text/plain, */*',
        'Accept-Language':'vi,en;q=0.9,fr;q=0.8',
        'Content-Length':'174',
        'Content-Type':'application/json',
        'Connection': 'keep-alive'
    }
    payload = {"name": name,"parentId":parentId}
    html = requests.post('https://helurl.com/api/v1/folders',headers=headers,json=payload)
    data = html.json()
    return(data['folder']['id'])

def get_subfolder(id_folder):
    with open('key.txt', 'r', encoding='utf-8') as file:
        KEY = file.read()

    headers = {
        'Authorization': f'Bearer {KEY}'
    }
    if id_folder == None:
        id_folder = ''
    html = requests.get(f'https://helurl.com/api/v1/drive/file-entries?perPage=10000&parentIds={id_folder}&workspaceId=0', headers=headers)
    dict_folder_data = html.json()
    list_subfolder = []
    for item in dict_folder_data['data']:
        if item['type'] == 'folder':
            list_subfolder.append({
                'name': item['name'],
                'id': item['id']
            })
    return list_subfolder
# Lấy id của thư mục
def get_id_folder(server_folder_path):
    all_folders = re.split(r'\\|/',server_folder_path)
    id_folder = None
    for folder in all_folders:
        if folder == "" or folder == ".":
            continue
        # Lấy toàn bộ name_subfolder và id_subfolder trên id_folder
        list_subfolder = get_subfolder(id_folder)
        # Đặt biến is_exists để kiểm tra xem subfolder có nằm trong folder cha không
        is_exists = False
        # Kiểm tra trên server có folder nào trùng với folder cần tìm
        for subfolder in list_subfolder:
            if subfolder['name'] == folder:
                id_folder = subfolder["id"]
                is_exists = True
                break
        # Nếu không nằm trong folder cha thì tiến hành tạo folder mới
        if is_exists == False:
            # Tạo folder mới dựa vào id_folder
            # Lấy id folder mới tạo gán vào biến id_folder
            id_folder = create_folder(folder,id_folder)
    return id_folder

# Hàm xử lý việc tải lên file hoặc folder dựa trên loại đường dẫn người dùng đã nhập
def upload_file_or_folder(path, server_folder_path, thread):
    is_file, is_folder = is_file_or_folder(path)

    if is_file:
        # Nếu là tệp (file), thực hiện tải lên tệp
        upload_file(path, get_id_folder(server_folder_path))
        
    elif is_folder:
        # Nếu là thư mục (folder), thực hiện tải lên thư mục và các tệp con
        upload_folder_contents(path, server_folder_path, get_id_folder(server_folder_path),thread)
    else:
        print("Đường dẫn không tồn tại hoặc không phải là tệp hoặc thư mục!")

def main():
    # Tạo một đối tượng ArgumentParser với hỗ trợ subparser
    parser = argparse.ArgumentParser(description='Mô tả của chương trình')

    # Tạo một subparser cho chức năng 'config'
    subparsers = parser.add_subparsers(title='commands', dest='command', help='Chọn một trong các chức năng')
    parser.add_argument('-v', '--version', action='version', version=f'Helup {VERSION}')
    # Định nghĩa subparser cho chức năng 'config'
    config_parser = subparsers.add_parser('config', help='Thực hiện chức năng config')

    # Tạo một subparser cho chức năng 'copy'
    copy_parser = subparsers.add_parser('copy', help='Thực hiện chức năng copy')
    copy_parser.add_argument('source', help='Tập tin nguồn')
    copy_parser.add_argument('target', nargs='?', default='', help='Tập tin đích')
    copy_parser.add_argument('-thread', type=int, default=4, help='Số luồng')

    # Tùy chọn -h hoặc --help sẽ hiển thị hướng dẫn
    args = parser.parse_args()

    # Kiểm tra lựa chọn chức năng và gọi các hàm tương ứng
    if args.command == 'config':
        save_cookie()
        try:
            with open('key.txt', 'r', encoding='utf-8') as f:
                key = f.read()
            answer = input(f"[+] Your API Key: {key}\n[+] Do you want to edit your key (y/n): ").lower()
            if answer == 'y':
                save_key()
        except:
            save_key(input("[+] Please input your api key: "))
        print('[+] Config succeed')
    elif args.command == 'copy':
        source = args.source
        target = args.target
        thread = args.thread
        
        global total_files 
        is_file, is_folder = is_file_or_folder(source)
        if is_file:
            total_files = 1
        else:
            total_files = count_files_in_folder(source)
        
        print("""
____________________________________________________
|                                                   |
| █░░█ █▀▀ █░░ █░░█ █▀▀█   ▀█░█▀ ▄█░ ░ █▀▀█ ░ █▀▀█  |
| █▀▀█ █▀▀ █░░ █░░█ █░░█   ░█▄█░ ░█░ ▄ █▄▀█ ▄ █▄▀█  |
| ▀░░▀ ▀▀▀ ▀▀▀ ░▀▀▀ █▀▀▀   ░░▀░░ ▄█▄ █ █▄▄█ █ █▄▄█  |
|                                                   |
|       UPLOAD UNLIMITED FILE TO HELURL.COM         |
|              -- MADE BY NGHIANL --                |
|                                                   |
|             FROM NGHIEN WITH LOVE                 |
|___________________________________________________|\n""")
        # Gọi hàm để tải lên thư mục hoặc tệp
        print(f"""
***************************************** 
TỔNG SỐ FILE {total_files} 
*****************************************
              """)
        upload_file_or_folder(source, target, thread)

if __name__ == "__main__":
    main()


