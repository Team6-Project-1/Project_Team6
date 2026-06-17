"""
ROUTE_STATION 테이블 데이터 생성 스크립트

[확인된 사실]
- CSV의 노드ID == bus_station.json의 sttnId == DB STATION.station_id (동일 ID 체계)
- CSV의 노선ID == bus_route.json의 route_id == DB ROUTE.route_id (동일 ID 체계)

[필터 조건]
1. 교차로구간ID == '0'  → 교차로 노드 제외, 정류장 노드만 유지
2. 노드ID 자릿수 == 9  → 10자리 비표준 ID 제외
3. (노선ID, 정류장순번) 중복 시 첫 번째 행만 유지

[출력]
- route_station_data.csv: ROUTE_STATION 테이블에 INSERT할 데이터
"""

import csv
import io
import os

# ── 경로 설정 ──────────────────────────────────────────────
BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
INPUT_CSV   = os.path.join(BASE_DIR, 'route_station_dat.csv')   # ← 실제 파일명으로 수정
OUTPUT_CSV  = os.path.join(BASE_DIR, 'route_station_data.csv')
# ───────────────────────────────────────────────────────────


def generate(input_path, output_path):
    print(f"[1/4] 읽는 중: {input_path}")
    with open(input_path, 'r', encoding='utf-8-sig') as f:
        content = f.read().replace('﻿', '')

    rows = list(csv.DictReader(io.StringIO(content)))
    print(f"      전체 행 수: {len(rows):,}")

    # ── 필터 ──────────────────────────────────────────────
    # 정류장 노드 조건:
    #   - 정류장구간ID != '0' (정류장 구간에 속하는 노드)
    #   - OR 교차로구간ID == '0' (기/종점처럼 구간ID가 없는 정류장)
    #   - AND 노드ID 9자리 (10자리는 별도 ID 체계)
    print("[2/4] 필터링 중 (정류장 노드 + 9자리 ID)...")
    stop_rows = [
        r for r in rows
        if (r['정류장구간ID'].strip() != '0' or r['교차로구간ID'].strip() == '0')
        and len(r['노드ID'].strip()) == 9
    ]
    print(f"      필터 후: {len(stop_rows):,}행")

    # ── 중복 제거 & 노선별 그룹화 ─────────────────────────
    print("[3/4] 중복 제거 및 is_start/is_end 계산 중...")
    seen = set()
    routes: dict[str, list] = {}

    for r in stop_rows:
        route_id    = r['노선ID'].strip()
        station_seq = int(r['정류장순번'].strip())
        node_id     = r['노드ID'].strip()
        key = (route_id, station_seq)

        if key in seen:
            continue
        seen.add(key)

        routes.setdefault(route_id, []).append((station_seq, node_id))

    print(f"      고유 노선 수: {len(routes):,}")

    # ── 결과 생성 ─────────────────────────────────────────
    print("[4/4] CSV 저장 중...")
    result = []
    rs_id = 1

    for route_id in sorted(routes.keys()):
        stops = sorted(routes[route_id], key=lambda x: x[0])
        min_seq = stops[0][0]
        max_seq = stops[-1][0]

        for station_seq, node_id in stops:
            result.append({
                'route_station_id': rs_id,
                'station_seq':      station_seq,
                'is_start':         '1' if station_seq == min_seq else '0',
                'is_end':           '1' if station_seq == max_seq else '0',
                'route_id':         route_id,
                'station_id':       node_id,
            })
            rs_id += 1

    fields = ['route_station_id', 'station_seq', 'is_start', 'is_end', 'route_id', 'station_id']
    with open(output_path, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(result)

    print(f"\n✅ 완료: {len(result):,}행 → {output_path}")
    print()
    print("=" * 55)
    print("DB INSERT 전 검증 쿼리 (FK 오류 방지)")
    print("=" * 55)
    print("""
-- 1. 임시 테이블 생성 & CSV 로드
CREATE TEMPORARY TABLE tmp_rs (
    route_station_id BIGINT,
    station_seq      INT,
    is_start         CHAR(1),
    is_end           CHAR(1),
    route_id         INT,
    station_id       INT
);

LOAD DATA INFILE '/path/to/route_station_data.csv'
INTO TABLE tmp_rs
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\\n'
IGNORE 1 ROWS;

-- 2. 매칭률 확인
SELECT
    COUNT(*)                                                     AS 전체,
    SUM(s.station_id IS NOT NULL AND r.route_id IS NOT NULL)    AS 매칭,
    SUM(s.station_id IS NULL)                                   AS station_없음,
    SUM(r.route_id IS NULL)                                     AS route_없음
FROM tmp_rs t
LEFT JOIN STATION s ON t.station_id = s.station_id
LEFT JOIN ROUTE   r ON t.route_id   = r.route_id;

-- 3. 매칭된 것만 INSERT (route_station_id 재부여)
INSERT INTO ROUTE_STATION
    (route_station_id, station_seq, is_start, is_end, route_id, station_id)
SELECT
    ROW_NUMBER() OVER (ORDER BY t.route_id, t.station_seq),
    t.station_seq, t.is_start, t.is_end, t.route_id, t.station_id
FROM tmp_rs t
INNER JOIN STATION s ON t.station_id = s.station_id
INNER JOIN ROUTE   r ON t.route_id   = r.route_id;
""")


if __name__ == '__main__':
    generate(INPUT_CSV, OUTPUT_CSV)
