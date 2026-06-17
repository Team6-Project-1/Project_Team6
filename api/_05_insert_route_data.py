import json
import pymysql

# ============================================
# 1. JSON 파일 로드
# ============================================
with open('./bus_route.json', 'r', encoding='utf-8') as f:
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
# 3. DB에 존재하는 FK 값 사전 로드 (필터링용)
# ============================================
cursor.execute("SELECT area_id FROM AREA")
valid_area_ids = set(str(r[0]) for r in cursor.fetchall())

cursor.execute("SELECT route_ty FROM ROUTE_TY")
valid_route_tys = set(str(r[0]) for r in cursor.fetchall())

print(f"유효 area_id: {len(valid_area_ids)}개, 유효 route_ty: {len(valid_route_tys)}개")

# ============================================
# 4. ROUTE 테이블 INSERT
# ============================================
route_sql = """
    INSERT INTO ROUTE (route_id, route_nm, route_abrv, route_dc, dstnc, route_ty, area_id)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

route_count = 0
route_skip = 0
valid_route_ids = set()

for row in data:
    area_id  = str(row.get('areaId', '-'))
    route_ty = str(row.get('routeTy', ''))

    # FK 검증: area_id, route_ty 모두 DB에 있어야 INSERT
    if area_id not in valid_area_ids or route_ty not in valid_route_tys:
        route_skip += 1
        continue

    values = (
        row['routeId'],
        row['routeNm'],
        row['routeAbrv'],
        row['routeDc'],
        row['dstnc'],
        route_ty,
        area_id,
    )
    cursor.execute(route_sql, values)
    valid_route_ids.add(str(row['routeId']))
    route_count += 1

print(f"ROUTE 테이블 삽입 완료: {route_count}건 (스킵: {route_skip}건)")

# ============================================
# 5. ROUTE_OPERATION 테이블 INSERT (삽입된 route만)
# ============================================
operation_sql = """
    INSERT INTO ROUTE_OPERATION (
        operation_id, route_id, use_at, oprat_at, caralc,
        mumm_caralc, mxmm_caralc, oprat_reqre_tm,
        fircar_tm, lstcar_tm, fircar_stm, lstcar_stm, fircar_htm, lstcar_htm
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

operation_count = 0
for row in data:
    if str(row.get('routeId', '')) not in valid_route_ids:
        continue

    operation_count += 1

    values = (
        operation_count,
        row['routeId'],
        row['useAt'],
        row['opratAt'],
        row['caralc'],
        row['mummCaralc'],
        row['mxmmCaralc'],
        row['opratReqreTm'],
        row['fircarTm'],
        row['lstcarTm'],
        row['fircarStm'],
        row['lstcarStm'],
        row['fircarHtm'],
        row['lstcarHtm'],
    )
    cursor.execute(operation_sql, values)

print(f"ROUTE_OPERATION 테이블 삽입 완료: {operation_count}건")

# ============================================
# 6. 커밋 및 종료
# ============================================
conn.commit()
cursor.close()
conn.close()
print("전체 작업 완료")
