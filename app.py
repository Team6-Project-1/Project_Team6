import streamlit as st
import folium
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


def get_current_page():
    return st.query_params.get("page", "map")


def sidebar_link(label, page_key, current_page):
    active = "active" if current_page == page_key else ""
    st.sidebar.markdown(
        f'<a class="nav-link {active}" href="?page={page_key}" target="_self">{label}</a>',
        unsafe_allow_html=True
    )


def render_sidebar():
    current_page = get_current_page()

    st.sidebar.markdown('<div class="nav-title">메뉴</div>', unsafe_allow_html=True)

    sidebar_link("지도조회", "map", current_page)
    sidebar_link("정류장조회", "station", current_page)
    sidebar_link("버스조회", "bus", current_page)
    sidebar_link("경로조회", "route", current_page)

    faq_active = "active" if current_page == "faq" else ""
    st.sidebar.markdown(
        f"""
        <div class="sidebar-faq">
            <a class="{faq_active}" href="?page=faq" target="_self">FAQ</a>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_search_area():
    if "search_mode" not in st.session_state:
        st.session_state.search_mode = False

    if "selected_station" not in st.session_state:
        st.session_state.selected_station = None

    if "search_message" not in st.session_state:
        st.session_state.search_message = ""

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
            if station_name in stations:
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


def render_map_page():
    render_search_area()

    route = [
        [37.4979, 127.0276],
        [37.5007, 127.0365],
        [37.5045, 127.0490]
    ]

    if st.session_state.get("selected_station"):
        map_center = stations[st.session_state.selected_station]
        zoom_level = 16
    else:
        map_center = route[0]
        zoom_level = 14

    m = folium.Map(
        location=map_center,
        zoom_start=zoom_level,
        control_scale=True
    )

    for station_nm, point in stations.items():
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


def render_station_page():
    st.write("정류장조회 페이지")


def render_bus_page():
    st.write("버스조회 페이지")


def render_route_page():
    st.write("경로조회 페이지")


def render_faq_page():
    st.subheader("FAQ")

    with st.expander("노선 검색은 어떻게 하나요?"):
        st.write("버스 번호 또는 노선명을 입력하면 해당 노선 정보를 조회할 수 있습니다.")

    with st.expander("정류장 검색은 어떻게 하나요?"):
        st.write("정류장명을 정확히 입력하면 해당 정류장을 조회할 수 있습니다.")

    with st.expander("검색한 정류장이 없으면 어떻게 되나요?"):
        st.write("입력한 정류장명이 정확히 일치하지 않으면 '없는 정류장입니다.'라고 표시됩니다.")

    with st.expander("지도에서는 무엇을 볼 수 있나요?"):
        st.write("정류장의 위치를 지도에서 확인할 수 있습니다.")


render_sidebar()

current_page = get_current_page()

if current_page == "map":
    render_map_page()
elif current_page == "station":
    render_station_page()
elif current_page == "bus":
    render_bus_page()
elif current_page == "route":
    render_route_page()
elif current_page == "faq":
    render_faq_page()
else:
    render_map_page()

# 초기 파일 