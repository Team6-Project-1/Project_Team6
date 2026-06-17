import streamlit as st
import folium
from streamlit_folium import st_folium
from db.queries.route_query import search_direct_routes, get_route_stations


class RoutePage:
    def init_state(self):
        if "route_origin_input" not in st.session_state:
            st.session_state.route_origin_input = ""
        if "route_dest_input" not in st.session_state:
            st.session_state.route_dest_input = ""
        if "route_search_results" not in st.session_state:
            st.session_state.route_search_results = None
        if "route_message" not in st.session_state:
            st.session_state.route_message = ""

    def search(self):
        origin = st.session_state.route_origin_input.strip()
        dest = st.session_state.route_dest_input.strip()
        if not origin or not dest:
            st.session_state.route_search_results = None
            st.session_state.route_message = ""
            return

        df = search_direct_routes(origin, dest)
        if df.empty:
            st.session_state.route_search_results = None
            st.session_state.route_message = "직행으로 갈 수 있는 노선을 찾을 수 없습니다."
        else:
            st.session_state.route_search_results = df
            st.session_state.route_message = f"{len(df)}개의 노선을 찾았습니다."

    def render_route_map(self, route_id: int, start_seq: int, end_seq: int):
        stations_df = get_route_stations(route_id)
        if stations_df.empty:
            st.warning("경유 정류장 정보가 없습니다.")
            return

        segment_df = stations_df[
            (stations_df["순번"] >= start_seq) & (stations_df["순번"] <= end_seq)
        ].sort_values("순번").reset_index(drop=True)

        if segment_df.empty:
            st.warning("경유 정류장 정보가 없습니다.")
            return

        coords = list(zip(
            segment_df["위도"].astype(float),
            segment_df["경도"].astype(float)
        ))

        center = [segment_df["위도"].astype(float).mean(),
                  segment_df["경도"].astype(float).mean()]

        m = folium.Map(location=center, zoom_start=13, control_scale=True)

        folium.PolyLine(
            locations=coords,
            color="#0066CC",
            weight=4,
            opacity=0.8
        ).add_to(m)

        last_idx = len(segment_df) - 1
        for idx, row in segment_df.iterrows():
            lat = float(row["위도"])
            lon = float(row["경도"])

            if idx == 0:
                color, icon = "green", "play"
            elif idx == last_idx:
                color, icon = "red", "stop"
            else:
                color, icon = "blue", "info-sign"

            folium.Marker(
                location=[lat, lon],
                popup=f"{row['순번']}. {row['정류장명']}",
                tooltip=f"{row['순번']}. {row['정류장명']}",
                icon=folium.Icon(color=color, icon=icon)
            ).add_to(m)

        st_folium(m, use_container_width=True, height=650, returned_objects=[])

        with st.expander("🚏 탑승 구간 정류장 보기"):
            display_df = segment_df[["순번", "정류장명"]]
            st.dataframe(display_df, use_container_width=True, hide_index=True)

    def render(self):
        self.init_state()

        st.subheader("🛣️ 경로 조회")

        col1, col2, col3, col4 = st.columns([3, 3, 1, 1])
        with col1:
            st.text_input(
                "출발지",
                placeholder="출발 정류장 (예: 강남역)",
                label_visibility="collapsed",
                key="route_origin_input",
                on_change=self.search
            )
        with col2:
            st.text_input(
                "도착지",
                placeholder="도착 정류장 (예: 역삼역)",
                label_visibility="collapsed",
                key="route_dest_input",
                on_change=self.search
            )
        with col3:
            if st.button("조회", use_container_width=True, key="route_search_btn"):
                self.search()
        with col4:
            if st.button("초기화", use_container_width=True, key="route_reset_btn"):
                st.session_state.route_search_results = None
                st.session_state.route_message = ""
                st.session_state.route_origin_input = ""
                st.session_state.route_dest_input = ""
                st.rerun()

        if st.session_state.route_message:
            if st.session_state.route_search_results is not None:
                st.success(st.session_state.route_message)
            else:
                st.error(st.session_state.route_message)
        else:
            st.info("🔍 출발지와 도착지를 입력하면 직행으로 갈 수 있는 노선을 찾아드립니다.")

        df = st.session_state.route_search_results

        if df is not None and not df.empty:
            route_options = {
                f"{row['route_nm']} ({row['노선유형']}) · {row['출발정류장']} → {row['도착정류장']}":
                    (row['route_id'], row['출발순번'], row['도착순번'])
                for _, row in df.iterrows()
            }
            selected_label = st.selectbox(
                "노선 선택",
                options=list(route_options.keys()),
                label_visibility="collapsed"
            )
            selected_id, start_seq, end_seq = route_options[selected_label]

            st.divider()
            self.render_route_map(selected_id, start_seq, end_seq)
