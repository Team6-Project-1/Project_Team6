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


# [2단계] 기현님이 만든 테이블 구조에 맞게 넣을수 있게 해당 컬럼만 뽑기
# STATION` ( # 3. 정류장
# 	`station_id`	VARCHAR(20)	NOT NULL	COMMENT '정류장 ID',
# 	`station_nm`	VARCHAR(100)	NOT NULL	COMMENT '정류장명',
# 	`gps_x`	DECIMAL(12,8)	NOT NULL	COMMENT '경도 X좌표',
# 	`gps_y`	DECIMAL(12,8)	NOT NULL	COMMENT '경도 Y좌표'

# 원하는 6가지 키값만 남긴 새로운 리스트를 만듭니다.
# (.get()을 사용하여 혹시 모를 누락 데이터(KeyError)를 방지합니다.)
#         cleaned_data = [
#             {
#                 "station_id": station.get("sttnId"),
#                 "station_nm": station.get("sttnNm"),
#                 "gps_x": station.get("crdntX"),
#                 "gps_y": station.get("crdntY"),
#                 "sttnNo": station.get("sttnNo"),
#                 "sttnUseAt": station.get("sttnUseAt"),
#             }
# #             for station in data
# #         ]
#
#     # 3. 잘 뽑혔나 프린트해보는 창
#     # print(f"추출된 데이터 -> ID: {station_id}, Name: {station_name}")
#
# # 결과 확인
# for db in data:
#     station_id = db.get({'sttnId'}.{})# (key, default)
#     station_nm = db.get({'sttnNm', []) # (key, default)
#     gps_x = db.get({'crdntX', []) # (key, default)
#     gps_y = db.get({'crdntY', []) # (key, default)
#     sttnNo = db.get({'sttnNo', []) # (key, default)
#     sttnUseAt = db.get({'sttnUseAt', []) # (key, default)

