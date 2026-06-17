"""
route_station_data.csv → MySQL ROUTE_STATION 테이블 INSERT 스크립트
"""
import importlib
import sys
sys.path = [p for p in sys.path if p not in ('', '.')]
csv = importlib.import_module('csv')
import csv
import os
import mysql.connector


# ── DB 연결 설정 ───────────────────────────────────────────
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'skn_ai',  # ← 본인 계정으로 수정
    'password': '1234',  # ← 비밀번호 입력
    'database': 'team6db',  # ← DB명 입력
}
# ───────────────────────────────────────────────────────────

CSV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'route_station_data.csv')


def insert_route_station():
    # CSV 읽기
    with open(CSV_PATH, 'r', encoding='utf-8-sig') as f:
        rows = list(csv.DictReader(f))
    print(f"CSV 행 수: {len(rows):,}")

    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # 기존 FK 체크 잠시 해제 (속도 향상)
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")

    # 유효한 route_id, station_id 목록 미리 조회
    cursor.execute("SELECT route_id FROM ROUTE")
    valid_routes = set(str(r[0]) for r in cursor.fetchall())

    cursor.execute("SELECT station_id FROM STATION")
    valid_stations = set(str(s[0]) for s in cursor.fetchall())

    print(f"DB ROUTE: {len(valid_routes):,}개, STATION: {len(valid_stations):,}개")

    # 필터링
    valid_rows = [
        r for r in rows
        if r['route_id'] in valid_routes and r['station_id'] in valid_stations
    ]
    skip = len(rows) - len(valid_rows)
    print(f"INSERT 대상: {len(valid_rows):,}행 (스킵 {skip:,}행)")

    # route_station_id 재부여 후 INSERT
    sql = """
          INSERT INTO ROUTE_STATION
              (route_station_id, station_seq, is_start, is_end, route_id, station_id)
          VALUES (%s, %s, %s, %s, %s, %s) \
          """

    data = [
        (
            idx + 1,
            int(r['station_seq']),
            r['is_start'],
            r['is_end'],
            int(r['route_id']),
            int(r['station_id']),
        )
        for idx, r in enumerate(valid_rows)
    ]

    cursor.executemany(sql, data)
    conn.commit()

    cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
    print(f"✅ INSERT 완료: {cursor.rowcount:,}행")

    cursor.close()
    conn.close()


if __name__ == '__main__':
    insert_route_station()
