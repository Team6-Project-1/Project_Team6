import streamlit as st
import folium
import pandas as pd
from streamlit_folium import st_folium


st.set_page_config(
    page_title="Bus System",
    page_icon="🚌",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 3rem;
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: 100%;
    }

    iframe {
        display: block;
        border: none;
    }

    section[data-testid="stSidebar"] a {
        text-decoration: none;
    }

    .nav-title {
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 0.75rem;
        color: #31333f;
    }

    .nav-link {
        display: block;
        padding: 0.6rem 0.8rem;
        margin-bottom: 0.3rem;
        border-radius: 0.5rem;
        color: #4b5563;
        font-size: 1rem;
        font-weight: 500;
    }

    .nav-link:hover {
        background-color: #eef2f7;
        color: #111827;
    }

    .nav-link.active {
        background-color: #e1e7f0;
        color: #111827;
        font-weight: 700;
    }

    .sidebar-faq {
        position: fixed;
        left: 1.5rem;
        bottom: 1.5rem;
        z-index: 999;
    }

    .sidebar-faq a {
        color: #31333f;
        font-size: 1.05rem;
        font-weight: 700;
    }
    </style>
    """,
    unsafe_allow_html=True
)


stations = {
    "강남역": [37.4979, 127.0276],
    "역삼역": [37.5007, 127.0365],
    "선릉역": [37.5045, 127.0490]
}


bus_data = {
    "서대문12": {
        "route": {
            "노선 ID": 112900002,
            "노선 이름": "서대문12",
            "노선 약칭": "서대12",
            "노선 설명": "-",
            "운행 거리(km)": 4.5,
            "노선 유형": "마을버스",
            "지역 ID": "523"
        },
        "operation": {
            "사용 여부": "사용",
            "운행 여부": "운행",
            "평균 배차 간격(분)": 12,
            "최소 배차 간격(분)": 8,
            "최대 배차 간격(분)": 20,
            "운행 소요 시간(분)": 27,
            "첫차 시간": "06:00",
            "막차 시간": "23:00",
            "첫차 시간(토요일)": "06:00",
            "막차 시간(토요일)": "23:00",
            "첫차 시간(공휴일)": "06:00",
            "막차 시간(공휴일)": "23:00"
        },
        "price": [
            {"연령대": "성인", "노선 유형": "마을버스", "요금": 1200},
            {"연령대": "청소년", "노선 유형": "마을버스", "요금": 600},
            {"연령대": "어린이", "노선 유형": "마을버스", "요금": 400}
        ],
        "route_station": [
            {
                "정류장 순번": 1,
                "정류장 ID": 1001,
                "정류장명": "유원아파트",
                "기점 여부": "Y",
                "종점 여부": "N"
            },
            {
                "정류장 순번": 2,
                "정류장 ID": 1002,
                "정류장명": "홍제역",
                "기점 여부": "N",
                "종점 여부": "Y"
            }
        ]
    },
    "강남01": {
        "route": {
            "노선 ID": 113000001,
            "노선 이름": "강남01",
            "노선 약칭": "강남01",
            "노선 설명": "-",
            "운행 거리(km)": 5.2,
            "노선 유형": "마을버스",
            "지역 ID": "321"
        },
        "operation": {
            "사용 여부": "사용",
            "운행 여부": "운행",
            "평균 배차 간격(분)": 10,
            "최소 배차 간격(분)": 7,
            "최대 배차 간격(분)": 15,
            "운행 소요 시간(분)": 30,
            "첫차 시간": "05:40",
            "막차 시간": "23:30",
            "첫차 시간(토요일)": "05:50",
            "막차 시간(토요일)": "23:20",
            "첫차 시간(공휴일)": "06:00",
            "막차 시간(공휴일)": "23:10"
        },
        "price": [
            {"연령대": "성인", "노선 유형": "마을버스", "요금": 1200},
            {"연령대": "청소년", "노선 유형": "마을버스", "요금": 600},
            {"연령대": "어린이", "노선 유형": "마을버스", "요금": 400}
        ],
        "route_station": [
            {
                "정류장 순번": 1,
                "정류장 ID": 2001,
                "정류장명": "강남역",
                "기점 여부": "Y",
                "종점 여부": "N"
            },
            {
                "정류장 순번": 2,
                "정류장 ID": 2002,
                "정류장명": "역삼역",
                "기점 여부": "N",
                "종점 여부": "N"
            },
            {
                "정류장 순번": 3,
                "정류장 ID": 2003,
                "정류장명": "선릉역",
                "기점 여부": "N",
                "종점 여부": "Y"
            }
        ]
    },
    "테스트00": {
        "route": {
            "노선 ID": 999999999,
            "노선 이름": "테스트00",
            "노선 약칭": "테스트00",
            "노선 설명": "-",
            "운행 거리(km)": 0.0,
            "노선 유형": "마을버스",
            "지역 ID": "000"
        },
        "operation": {
            "사용 여부": "사용",
            "운행 여부": "미운행",
            "평균 배차 간격(분)": 0,
            "최소 배차 간격(분)": 0,
            "최대 배차 간격(분)": 0,
            "운행 소요 시간(분)": 0,
            "첫차 시간": "-",
            "막차 시간": "-",
            "첫차 시간(토요일)": "-",
            "막차 시간(토요일)": "-",
            "첫차 시간(공휴일)": "-",
            "막차 시간(공휴일)": "-"
        },
        "price": [],
        "route_station": []
    }
}


class Sidebar:
    def __init__(self):
        self.menu_items = {
            "지도조회": "map",
            "정류장조회": "station",
            "버스조회": "bus",
            "경로조회": "route"
        }

    def get_current_page(self):
        return st.query_params.get("page", "map")

    def render_link(self, label, page_key, current_page):
        active = "active" if current_page == page_key else ""
        st.sidebar.markdown(
            f'<a class="nav-link {active}" href="?page={page_key}" target="_self">{label}</a>',
            unsafe_allow_html=True
        )

    def render(self):
        current_page = self.get_current_page()

        st.sidebar.markdown(
            '<div class="nav-title">메뉴</div>',
            unsafe_allow_html=True
        )

        for label, page_key in self.menu_items.items():
            self.render_link(label, page_key, current_page)

        faq_active = "active" if current_page == "faq" else ""
        st.sidebar.markdown(
            f"""
            <div class="sidebar-faq">
                <a class="{faq_active}" href="?page=faq" target="_self">FAQ</a>
            </div>
            """,
            unsafe_allow_html=True
        )

        return current_page


class MapPage:
    def __init__(self, stations):
        self.stations = stations

    def init_state(self):
        if "search_mode" not in st.session_state:
            st.session_state.search_mode = False

        if "selected_station" not in st.session_state:
            st.session_state.selected_station = None

        if "search_message" not in st.session_state:
            st.session_state.search_message = ""

    def render_search_area(self):
        self.init_state()

        if not st.session_state.search_mode:
            if st.button("검색"):
                st.session_state.search_mode = True
                st.session_state.search_message = ""
                st.rerun()
        else:
            col1, col2, col3 = st.columns([5, 1, 1])

            with col1:
                station_name = st.text_input(
                    "정류장 이름",
                    placeholder="정확한 정류장 이름을 입력하세요",
                    label_visibility="collapsed"
                )

            with col2:
                search_clicked = st.button("조회", use_container_width=True)

            with col3:
                cancel_clicked = st.button("취소", use_container_width=True)

            if search_clicked:
                if station_name in self.stations:
                    st.session_state.selected_station = station_name
                    st.session_state.search_message = f"{station_name} 정류장을 찾았습니다."
                else:
                    st.session_state.selected_station = None
                    st.session_state.search_message = "없는 정류장입니다."

            if cancel_clicked:
                st.session_state.search_mode = False
                st.session_state.selected_station = None
                st.session_state.search_message = ""
                st.rerun()

        if st.session_state.search_message:
            if st.session_state.selected_station:
                st.success(st.session_state.search_message)
            else:
                st.error(st.session_state.search_message)

    def render(self):
        self.render_search_area()

        route = [
            [37.4979, 127.0276],
            [37.5007, 127.0365],
            [37.5045, 127.0490]
        ]

        if st.session_state.get("selected_station"):
            map_center = self.stations[st.session_state.selected_station]
            zoom_level = 16
        else:
            map_center = route[0]
            zoom_level = 14

        m = folium.Map(
            location=map_center,
            zoom_start=zoom_level,
            control_scale=True
        )

        for station_nm, point in self.stations.items():
            folium.Marker(
                location=point,
                popup=station_nm,
                tooltip=station_nm
            ).add_to(m)

        st_folium(
            m,
            use_container_width=True,
            height=750,
            returned_objects=[]
        )


class BusPage:
    def __init__(self, bus_data):
        self.bus_data = bus_data

    def init_state(self):
        if "bus_search_message" not in st.session_state:
            st.session_state.bus_search_message = ""

        if "selected_bus" not in st.session_state:
            st.session_state.selected_bus = None

        if "bus_operation_message" not in st.session_state:
            st.session_state.bus_operation_message = ""

    def render(self):
        self.init_state()

        st.subheader("버스조회")

        col1, col2 = st.columns([5, 1])

        with col1:
            bus_number = st.text_input(
                "버스 번호",
                placeholder="정확한 버스 번호를 입력하세요. 예: 서대문12",
                label_visibility="collapsed"
            )

        with col2:
            search_clicked = st.button("조회", use_container_width=True)

        if search_clicked:
            if bus_number in self.bus_data:
                st.session_state.selected_bus = bus_number
                st.session_state.bus_search_message = f"{bus_number}번 버스를 찾았습니다."

                operation_status = self.bus_data[bus_number]["operation"]["운행 여부"]

                if operation_status == "운행":
                    st.session_state.bus_operation_message = f"운행 여부: {operation_status}"
                else:
                    st.session_state.bus_operation_message = "운행하지 않는 버스입니다."
            else:
                st.session_state.selected_bus = None
                st.session_state.bus_search_message = "없는 버스 번호입니다."
                st.session_state.bus_operation_message = ""

        if st.session_state.bus_search_message:
            if st.session_state.selected_bus:
                st.success(st.session_state.bus_search_message)
            else:
                st.error(st.session_state.bus_search_message)

        if st.session_state.bus_operation_message:
            if st.session_state.bus_operation_message == "운행하지 않는 버스입니다.":
                st.warning(st.session_state.bus_operation_message)
            else:
                st.info(st.session_state.bus_operation_message)

        if st.session_state.selected_bus:
            selected_data = self.bus_data[st.session_state.selected_bus]

            st.markdown("### 노선 기본 정보")
            st.dataframe(
                pd.DataFrame([selected_data["route"]]),
                use_container_width=True,
                hide_index=True
            )

            st.markdown("### 운행 및 배차 정보")
            st.dataframe(
                pd.DataFrame([selected_data["operation"]]),
                use_container_width=True,
                hide_index=True
            )

            st.markdown("### 요금 정보")
            if selected_data["price"]:
                st.dataframe(
                    pd.DataFrame(selected_data["price"]),
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.write("요금 정보가 없습니다.")

            st.markdown("### 경로 정류장 정보")
            if selected_data["route_station"]:
                st.dataframe(
                    pd.DataFrame(selected_data["route_station"]),
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.write("경로 정류장 정보가 없습니다.")


class StationPage:
    def render(self):
        st.subheader("정류장조회")
        st.write("정류장조회 페이지")


class RoutePage:
    def render(self):
        st.subheader("경로조회")
        st.write("경로조회 페이지")


class FAQPage:
    def render(self):
        st.subheader("FAQ")

        with st.expander("노선 검색은 어떻게 하나요?"):
            st.write("버스 번호 또는 노선명을 입력하면 해당 노선 정보를 조회할 수 있습니다.")

        with st.expander("정류장 검색은 어떻게 하나요?"):
            st.write("정류장명을 정확히 입력하면 해당 정류장을 조회할 수 있습니다.")

        with st.expander("검색한 정류장이 없으면 어떻게 되나요?"):
            st.write("입력한 정류장명이 정확히 일치하지 않으면 '없는 정류장입니다.'라고 표시됩니다.")

        with st.expander("지도에서는 무엇을 볼 수 있나요?"):
            st.write("정류장의 위치를 지도에서 확인할 수 있습니다.")


sidebar = Sidebar()
current_page = sidebar.render()

pages = {
    "map": MapPage(stations),
    "station": StationPage(),
    "bus": BusPage(bus_data),
    "route": RoutePage(),
    "faq": FAQPage()
}

page = pages.get(current_page, pages["map"])
page.render()

# streamlit edit & add
# Class 목록

# Sidebar
# → 사이드바 네비게이션 담당

# MapPage
# → 지도조회 + 정류장 검색 담당

# BusPage
# → 버스번호 검색 + 상세 테이블 출력 담당

# StationPage
# → 정류장조회 페이지 담당

# RoutePage
# → 경로조회 페이지 담당

# FAQPage
# → FAQ 페이지 담당

# sidebar = Sidebar()
# current_page = sidebar.render()

# 서대문12 → 운행 여부: 운행
# 강남01 → 운행 여부: 운행
# 테스트00 → 운행하지 않는 버스입니다.

# pages = {
#     "map": MapPage(stations),
#     "station": StationPage(),
#     "bus": BusPage(bus_data),
#     "route": RoutePage(),
#     "faq": FAQPage()
# }

# page = pages.get(current_page, pages["map"])
# page.render()

# == 사이드바에서 고른 페이지 키에 따라 해당 클래스의 render()가 실행되는 구조