# [2단계]

import json
import pymysql

# ============================================
# 1. JSON 파일 로드
# ============================================
with open('./bus_station.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# ============================================
# 2. DB 연결
# ============================================
conn = pymysql.connect(
    host='localhost',
    user='skn_ai',
    password='1234',
    db='team6db',
    charset='utf8mb4'
)
cursor = conn.cursor()

# ============================================
# 3. ROUTE 테이블 INSERT
# ============================================
station_sql = """
    INSERT INTO STATION (station_id, station_nm, gps_x, gps_y, sttn_no, sttn_use_at)
    VALUES (%s, %s, %s, %s, %s, %s)
"""

station_count = 0
for row in data:
    values = (
        row['sttnId'],
        row['sttnNm'],
        row['crdntX'],
        row['crdntY'],
        row['sttnNo'],
        row['sttnUseAt']
    )
    cursor.execute(station_sql, values)
    station_count += 1

print(f"ROUTE 테이블 삽입 완료: {station_count}건")

# ============================================
# 4. 커밋 및 종료
# ============================================
conn.commit()
cursor.close()
conn.close()
print("전체 작업 완료")