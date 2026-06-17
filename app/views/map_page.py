import streamlit as st
import folium
from streamlit_folium import st_folium
from db.queries.station_query import search_stations_by_name


class MapPage:
    def init_state(self):
        if "map_search_input" not in st.session_state:
            st.session_state.map_search_input = ""
        if "map_stations" not in st.session_state:
            st.session_state.map_stations = None
        if "map_message" not in st.session_state:
            st.session_state.map_message = ""

    def search(self):
        name = st.session_state.map_search_input.strip()
        if not name:
            st.session_state.map_stations = None
            st.session_state.map_message = ""
            return

        df = search_stations_by_name(name)
        if df.empty:
            st.session_state.map_stations = None
            st.session_state.map_message = "검색 결과가 없습니다."
        else:
            st.session_state.map_stations = df
            st.session_state.map_message = f"{len(df)}개의 정류장을 찾았습니다."

    def render(self):
        self.init_state()

        st.title("🚌 서울시 버스 노선 및 정류장 조회 시스템")

        col1, col2, col3 = st.columns([5, 1, 1])
        with col1:
            st.text_input(
                "정류장 이름",
                placeholder="정류장 이름을 입력하세요",
                label_visibility="collapsed",
                key="map_search_input",
                on_change=self.search
            )
        with col2:
            if st.button("조회", use_container_width=True):
                self.search()
        with col3:
            if st.button("취소", use_container_width=True):
                st.session_state.map_stations = None
                st.session_state.map_message = ""
                st.session_state.map_search_input = ""
                st.rerun()

        if st.session_state.map_message:
            if st.session_state.map_stations is not None:
                st.success(st.session_state.map_message)
            else:
                st.error(st.session_state.map_message)
        else:
            st.info("🔍 정류장 이름을 입력하면 지도에서 위치를 확인할 수 있습니다.")

        # 지도 중심 / 줌 설정
        df = st.session_state.map_stations
        if df is not None and not df.empty:
            center = [float(df["gps_y"].mean()), float(df["gps_x"].mean())]
            zoom = 15 if len(df) == 1 else 13
        else:
            center = [37.5665, 126.9780]
            zoom = 11

        m = folium.Map(location=center, zoom_start=zoom, control_scale=True)

        # 검색된 정류장 마커 표시
        if df is not None:
            for _, row in df.iterrows():
                folium.Marker(
                    location=[float(row["gps_y"]), float(row["gps_x"])],
                    popup=row["station_nm"],
                    tooltip=row["station_nm"]
                ).add_to(m)

        st_folium(m, use_container_width=True, height=700, returned_objects=[])
