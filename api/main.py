# [1단계]

import requests
import json

url = "http://t-data.seoul.go.kr/apig/apiman-gateway/tapi/BisTbisMsSttn/1.0"

params = {
    'apikey': 'd8e0af2f-6a2f-49bd-9883-d3b6ee52eb4a'
}

response = requests.get(url, params=params)

response.raise_for_status()

#json 파싱
data = response.json()
print(data)

#json 파일로 저장
# with open("bus_station.json", "w", encoding="utf-8") as f:
#     json.dump(data, f, ensure_ascii=False, indent=4)

print("JSON 파일 저장 완료 (bus_station.json)")
