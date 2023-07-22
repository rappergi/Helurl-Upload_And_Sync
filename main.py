import requests
import mimetypes
import os
import json
from concurrent.futures import ThreadPoolExecutor
from time import sleep

"""
MADE BY NGHIANL
FROM NGHIEN WITH LOVE
"""


chunk_size = 50 * 1024 * 1024
batch_size = 10
etags = []

def upload_chunk(s, url, chunk, part_number):
    headers = {'Content-Length': str(len(chunk))}
    response = s.put(url, data=chunk, headers=headers)
    etags.append(response.headers.get('Etag'))
    if response.status_code != 200:
        print(f"Error uploading chunk {part_number}: {response.text}")

def main():
    with open('cookie.json', 'r', encoding='utf-8') as file:
        read_cookie = json.load(file)
    with open('config.json', 'r', encoding='utf-8') as file:
        read_config = json.load(file)
    dirOfFile = read_config["Dir_Of_File"]
    nameOfFile = os.path.basename(dirOfFile)
    print("___________________________________")
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

    print(f"[+] Standarding ...")
    print("[+] Hold Ctrl and press C to stop...")
    print(f"[+] Uploading {nameOfFile} ...")
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
        "parentId": read_config["Id_Upload"],
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
            with ThreadPoolExecutor(max_workers=2) as executor:
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
                    executor.submit(upload_chunk, s, url, chunk, part_number)
                    part_number += 1

        print("[+] Finishing upload ...")
        payload = {
            "uploadId": create_download['uploadId'],
            "key": create_download['key'],
            "parts": [{"PartNumber": i, "ETag": etags[i - 1]} for i in range(1, part_number)]
        }
        payload = json.dumps(payload)
        response = s.post('https://helurl.com/api/v1/s3/multipart/complete', data=payload, headers=headers2)
        payload3 = {
            "workspaceId":0,
            "parentId":read_config["Id_Upload"],
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
        print(f"[+] {nameOfFile} - UPLOADED:")
        sleep(3)

if __name__ == "__main__":
    main()
