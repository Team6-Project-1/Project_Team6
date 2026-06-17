import json
import pymysql

# ============================================
# 1. JSON 파일 로드
# ============================================
with open('./../bus_route.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# ============================================
# 2. DB 연결
# ============================================
conn = pymysql.connect(
    host='localhost',
    user='skn_ai',
    password='1234',
    db='seoul_bus',
    charset='utf8mb4'
)
cursor = conn.cursor()

# ============================================
# 3. ROUTE 테이블 INSERT
# ============================================
route_sql = """
    INSERT INTO ROUTE (route_id, route_nm, route_abrv, route_dc, dstnc, route_ty, area_id)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

route_count = 0
for row in data:
    # area_id는 여전히 INT 컬럼이라 '-' 같은 비숫자 값은 0으로 처리 필요

    values = (
        row['route_id'],
        row['route_nm'],
        row['route_abrv'],
        row['route_dc'],   # VARCHAR(50)로 변경되어 '-' 그대로 삽입 가능
        row['dstnc'],
        row['route_ty'],
        row['area_id']
    )
    cursor.execute(route_sql, values)
    route_count += 1

print(f"ROUTE 테이블 삽입 완료: {route_count}건")

# ============================================
# 4. ROUTE_OPERATION 테이블 INSERT
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
    operation_count += 1
    operation_id = operation_count  # JSON에 없는 값이라 순번으로 직접 생성

    values = (
        operation_id,
        row['route_id'],
        row['use_at'],
        row['oprat_at'],
        row['caralc'],
        row['mumm_caralc'],
        row['mxmm_caralc'],
        row['oprat_reqre_tm'],
        row['fircar_tm'],
        row['lstcar_tm'],
        row['fircar_stm'],
        row['lstcar_stm'],
        row['fircar_htm'],
        row['lstcar_htm'],
    )
    cursor.execute(operation_sql, values)

print(f"ROUTE_OPERATION 테이블 삽입 완료: {operation_count}건")

# ============================================
# 5. 커밋 및 종료
# ============================================
conn.commit()
cursor.close()
conn.close()
print("전체 작업 완료")
