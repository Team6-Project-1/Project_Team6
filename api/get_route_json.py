import requests
import json
import time

url = "http://t-data.seoul.go.kr/apig/apiman-gateway/tapi/BisTbisMsRoute/1.0"
API_KEY = 'd8e0af2f-6a2f-49bd-9883-d3b6ee52eb4a'

all_data = []
start_row = 1
row_cnt = 1000

print("노선 데이터 수집 시작...")

while True:
    params = {
        'apikey': API_KEY,
        'startRow': start_row,
        'rowCnt': row_cnt
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    if not data or len(data) == 0:
        break

    all_data.extend(data)
    print(f"  {start_row} ~ {start_row + len(data) - 1}번째 수집 완료 (누적: {len(all_data)}개)")

    if len(data) < row_cnt:
        break

    start_row += row_cnt
    time.sleep(0.3)

print(f"\n총 {len(all_data)}개 수집 완료")

with open("bus_route.json", "w", encoding="utf-8") as f:
    json.dump(all_data, f, ensure_ascii=False, indent=4)

print("bus_route.json 저장 완료")