import pandas as pd
from db.connection import get_connection


def search_routes_by_name(name: str) -> pd.DataFrame:
    """노선명/약칭으로 검색 (부분 일치)"""
    sql = """
        SELECT r.route_id, r.route_nm, r.route_abrv, rt.ty_name AS 노선유형, r.dstnc AS 운행거리
        FROM route r
        JOIN route_ty rt ON r.route_ty = rt.route_ty
        WHERE r.route_nm LIKE %s OR r.route_abrv LIKE %s
        ORDER BY r.route_nm
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (f'%{name}%', f'%{name}%'))
            rows = cur.fetchall()
    return pd.DataFrame(rows)


def get_route_info(route_id: int) -> dict:
    """노선 기본 정보"""
    sql = """
        SELECT r.route_id AS 노선ID,
               r.route_nm AS 노선명,
               r.route_abrv AS 노선약칭,
               r.route_dc AS 노선설명,
               r.dstnc AS `운행거리(km)`,
               rt.ty_name AS 노선유형,
               an.area_name AS 지역명,
               r.route_ty
        FROM route r
        JOIN route_ty rt ON r.route_ty = rt.route_ty
        JOIN area a ON r.area_id = a.area_id
        JOIN area_name an ON a.area_code = an.area_code
        WHERE r.route_id = %s
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (route_id,))
            return cur.fetchone()


def get_route_operation(route_id: int) -> dict:
    """운행 및 배차 정보"""
    sql = """
        SELECT
            CASE use_at WHEN '1' THEN '사용' ELSE '미사용' END AS 사용여부,
            CASE oprat_at WHEN '1' THEN '운행' ELSE '미운행' END AS 운행여부,
            caralc AS `평균배차(분)`,
            mumm_caralc AS `최소배차(분)`,
            mxmm_caralc AS `최대배차(분)`,
            oprat_reqre_tm AS `소요시간(분)`,
            fircar_tm AS 첫차,
            lstcar_tm AS 막차,
            fircar_stm AS 첫차_토,
            lstcar_stm AS 막차_토,
            fircar_htm AS 첫차_공휴일,
            lstcar_htm AS 막차_공휴일
        FROM route_operation
        WHERE route_id = %s
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (route_id,))
            return cur.fetchone()


def get_route_price(route_ty: str) -> pd.DataFrame:
    """요금 정보 (노선 유형별)"""
    sql = """
        SELECT a.age AS 연령대, p.price AS 요금
        FROM price p
        JOIN age a ON p.age_code = a.age_code
        WHERE p.route_ty = %s
        ORDER BY a.age_code
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (route_ty,))
            rows = cur.fetchall()
    return pd.DataFrame(rows)


def search_direct_routes(origin_name: str, dest_name: str) -> pd.DataFrame:
    """출발지와 도착지를 모두 지나며 순서가 맞는 직행 노선 검색 (환승 미지원)"""
    sql = """
        SELECT r.route_id, r.route_nm, rt.ty_name AS 노선유형,
               s1.station_nm AS 출발정류장, s2.station_nm AS 도착정류장,
               rs1.station_seq AS 출발순번, rs2.station_seq AS 도착순번
        FROM route_station rs1
        JOIN route_station rs2
            ON rs1.route_id = rs2.route_id AND rs1.station_seq < rs2.station_seq
        JOIN station s1 ON rs1.station_id = s1.station_id
        JOIN station s2 ON rs2.station_id = s2.station_id
        JOIN route r ON rs1.route_id = r.route_id
        JOIN route_ty rt ON r.route_ty = rt.route_ty
        WHERE s1.station_nm LIKE %s AND s2.station_nm LIKE %s
        ORDER BY r.route_nm, 출발순번
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (f'%{origin_name}%', f'%{dest_name}%'))
            rows = cur.fetchall()
    return pd.DataFrame(rows)


def get_route_stations(route_id: int) -> pd.DataFrame:
    """노선 경유 정류장 목록 (순서대로)"""
    sql = """
        SELECT rs.station_seq AS 순번,
               s.station_nm AS 정류장명,
               s.station_id AS 정류장ID,
               s.gps_x AS 경도,
               s.gps_y AS 위도,
               rs.is_start AS 기점,
               rs.is_end AS 종점
        FROM route_station rs
        JOIN station s ON rs.station_id = s.station_id
        WHERE rs.route_id = %s
        ORDER BY rs.station_seq
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (route_id,))
            rows = cur.fetchall()
    return pd.DataFrame(rows)
