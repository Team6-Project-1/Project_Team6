import pandas as pd
from db.connection import get_connection


def search_stations_by_name(name: str) -> pd.DataFrame:
    """정류장명으로 검색 (부분 일치)"""
    sql = """
        SELECT station_id, station_nm, gps_x, gps_y, sttn_no, sttn_use_at
        FROM station
        WHERE station_nm LIKE %s
        ORDER BY station_nm
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (f'%{name}%',))
            rows = cur.fetchall()
    return pd.DataFrame(rows)


def get_routes_by_station(station_id: int) -> pd.DataFrame:
    """해당 정류장을 지나는 노선 목록"""
    sql = """
        SELECT r.route_id, r.route_nm, rt.ty_name AS 노선유형,
               rs.station_seq AS 순번, rs.is_start AS 기점, rs.is_end AS 종점
        FROM route_station rs
        JOIN route r ON rs.route_id = r.route_id
        JOIN route_ty rt ON r.route_ty = rt.route_ty
        WHERE rs.station_id = %s
        ORDER BY r.route_nm
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (station_id,))
            rows = cur.fetchall()
    return pd.DataFrame(rows)


def get_station_by_id(station_id: int) -> dict:
    """정류장 ID로 단건 조회"""
    sql = """
        SELECT station_id, station_nm, gps_x, gps_y, sttn_no, sttn_use_at
        FROM station
        WHERE station_id = %s
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (station_id,))
            return cur.fetchone()
