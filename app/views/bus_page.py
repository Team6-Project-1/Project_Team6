import streamlit as st
import pandas as pd
from db.queries.route_query import (
    search_routes_by_name,
    get_route_info,
    get_route_operation,
    get_route_price,
    get_route_stations
)


class BusPage:
    def init_state(self):
        if "bus_search_input" not in st.session_state:
            st.session_state.bus_search_input = ""
        if "bus_search_results" not in st.session_state:
            st.session_state.bus_search_results = None
        if "bus_message" not in st.session_state:
            st.session_state.bus_message = ""
        if "selected_route_id" not in st.session_state:
            st.session_state.selected_route_id = None

    def search(self):
        name = st.session_state.bus_search_input.strip()
        if not name:
            st.session_state.bus_search_results = None
            st.session_state.bus_message = ""
            return

        df = search_routes_by_name(name)
        if df.empty:
            st.session_state.bus_search_results = None
            st.session_state.bus_message = "검색 결과가 없습니다."
        else:
            st.session_state.bus_search_results = df
            st.session_state.bus_message = f"{len(df)}개의 노선을 찾았습니다."
        st.session_state.selected_route_id = None

    def render_route_detail(self, route_id: int):
        route = get_route_info(route_id)
        if not route:
            st.error("노선 정보를 불러올 수 없습니다.")
            return

        route_ty = route.pop("route_ty", None)  # 쿼리용으로만 사용
        route.pop("노선ID", None)

        st.markdown("### 📋 노선 기본 정보")
        st.dataframe(pd.DataFrame([route]), use_container_width=True, hide_index=True)

        operation = get_route_operation(route_id)
        st.markdown("### 🕒 운행 및 배차 정보")
        if operation:
            st.dataframe(pd.DataFrame([operation]), use_container_width=True, hide_index=True)
        else:
            st.write("운행 정보가 없습니다.")

        st.markdown("### 💰 요금 정보")
        if route_ty:
            price_df = get_route_price(route_ty)
            if not price_df.empty:
                st.dataframe(price_df, use_container_width=True, hide_index=True)
            else:
                st.write("요금 정보가 없습니다.")

        st.markdown("### 🚏 경유 정류장")
        stations_df = get_route_stations(route_id)
        if not stations_df.empty:
            display_df = stations_df[["순번", "정류장명", "정류장ID"]].copy()
            display_df["구분"] = stations_df.apply(
                lambda r: "기점" if r["기점"] == "1" else ("종점" if r["종점"] == "1" else "경유"),
                axis=1
            )
            st.dataframe(display_df, use_container_width=True, hide_index=True)
        else:
            st.write("경유 정류장 정보가 없습니다.")

    def render(self):
        self.init_state()

        st.subheader("🚌 버스 조회")

        col1, col2, col3 = st.columns([5, 1, 1])
        with col1:
            st.text_input(
                "버스 번호",
                placeholder="노선명 또는 번호를 입력하세요 (예: 강남01)",
                label_visibility="collapsed",
                key="bus_search_input",
                on_change=self.search
            )
        with col2:
            if st.button("조회", use_container_width=True, key="bus_search_btn"):
                self.search()
        with col3:
            if st.button("초기화", use_container_width=True, key="bus_reset_btn"):
                st.session_state.bus_search_results = None
                st.session_state.bus_message = ""
                st.session_state.bus_search_input = ""
                st.session_state.selected_route_id = None
                st.rerun()

        if st.session_state.bus_message:
            if st.session_state.bus_search_results is not None:
                st.success(st.session_state.bus_message)
            else:
                st.error(st.session_state.bus_message)
        else:
            st.info("🔍 노선명 또는 버스 번호를 입력해 검색해보세요.")

        df = st.session_state.bus_search_results

        if df is not None and not df.empty:
            # 노선 목록 표시 + 선택
            st.markdown("#### 검색 결과")
            route_options = {
                f"{row['route_nm']} ({row['노선유형']})": row['route_id']
                for _, row in df.iterrows()
            }
            selected_label = st.selectbox(
                "노선 선택",
                options=list(route_options.keys()),
                label_visibility="collapsed"
            )
            selected_id = route_options[selected_label]

            st.divider()
            self.render_route_detail(selected_id)
