import requests
import json

url = "http://t-data.seoul.go.kr/apig/apiman-gateway/tapi/BisTbisMsRoute/1.0"

params = {
    'apikey' : 'd8e0af2f-6a2f-49bd-9883-d3b6ee52eb4a'
}

response = requests.get(url, params=params)
data = response.json()

# result = []
#
# for row in data:
#     item = {
#         'routeId': row['routeId'],
#         'routeNm': row['routeNm'],
#         'routeAbrv': row['routeAbrv'],
#         'chrge': row['chrge'],
#         'fircarTm': row['fircarTm'],
#         'lstcarTm': row['lstcarTm'],
#         'caralc': row['caralc'],
#         'ssttnNm': row['ssttnNm'],
#         'esttnNm': row['esttnNm'],
#     }
#     result.append(item)
#
# print(result[0])
print(data)
#json 파일로 저장
with open("bus_route.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("JSON 파일 저장 완료 (bus_route.json)")