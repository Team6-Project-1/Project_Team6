import streamlit as st
import folium
from streamlit_folium import st_folium
from db.queries.station_query import search_stations_by_name, get_routes_by_station


class StationPage:
    def init_state(self):
        if "station_search_input" not in st.session_state:
            st.session_state.station_search_input = ""
        if "station_results" not in st.session_state:
            st.session_state.station_results = None
        if "station_message" not in st.session_state:
            st.session_state.station_message = ""

    def search(self):
        name = st.session_state.station_search_input.strip()
        if not name:
            st.session_state.station_results = None
            st.session_state.station_message = ""
            return

        df = search_stations_by_name(name)
        if df.empty:
            st.session_state.station_results = None
            st.session_state.station_message = "검색 결과가 없습니다."
        else:
            st.session_state.station_results = df
            st.session_state.station_message = f"{len(df)}개의 정류장을 찾았습니다."
        st.session_state.pop("station_table", None)

    def render(self):
        self.init_state()

        st.subheader("📍 정류장 조회")

        col1, col2, col3 = st.columns([5, 1, 1])
        with col1:
            st.text_input(
                "정류장 이름",
                placeholder="정류장 이름을 입력하세요 (예: 강남역)",
                label_visibility="collapsed",
                key="station_search_input",
                on_change=self.search
            )
        with col2:
            if st.button("조회", use_container_width=True, key="station_search_btn"):
                self.search()
        with col3:
            if st.button("초기화", use_container_width=True, key="station_reset_btn"):
                st.session_state.station_results = None
                st.session_state.station_message = ""
                st.session_state.station_search_input = ""
                st.session_state.pop("station_table", None)
                st.rerun()

        if st.session_state.station_message:
            if st.session_state.station_results is not None:
                st.success(st.session_state.station_message)
            else:
                st.error(st.session_state.station_message)
        else:
            st.info("🔍 정류장 이름을 입력해 검색해보세요.")

        df = st.session_state.station_results

        if df is not None and not df.empty:
            # 테이블 표시 (정류장명만, 클릭으로 선택)
            display_df = df[["station_nm"]].copy()
            display_df.columns = ["정류장명"]

            event = st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True,
                on_select="rerun",
                selection_mode="single-row",
                key="station_table"
            )

            # 선택한 정류장만 지도에 표시
            st.markdown("#### 지도")
            selected_rows = event.selection.rows

            if selected_rows:
                row = df.iloc[selected_rows[0]]
                m = folium.Map(
                    location=[float(row["gps_y"]), float(row["gps_x"])],
                    zoom_start=17,
                    control_scale=True
                )
                folium.Marker(
                    location=[float(row["gps_y"]), float(row["gps_x"])],
                    popup=row["station_nm"],
                    tooltip=row["station_nm"]
                ).add_to(m)
                st_folium(m, use_container_width=True, height=500, returned_objects=[])

                st.markdown("#### 🚌 이 정류장을 지나는 노선")
                routes_df = get_routes_by_station(int(row["station_id"]))
                if not routes_df.empty:
                    display_routes = routes_df[["route_nm", "노선유형", "순번"]].copy()
                    display_routes["구분"] = routes_df.apply(
                        lambda r: "기점" if r["기점"] == "1" else ("종점" if r["종점"] == "1" else "경유"),
                        axis=1
                    )
                    display_routes.columns = ["노선명", "노선유형", "순번", "구분"]
                    st.dataframe(display_routes, use_container_width=True, hide_index=True)
                else:
                    st.write("이 정류장을 지나는 노선이 없습니다.")
            else:
                st.info("정류장을 선택하면 지도와 경유 노선이 표시됩니다.")
