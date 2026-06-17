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

    div[data-testid="stVerticalBlock"] {
        gap: 0.5rem;
    }

    iframe {
        display: block;
        border: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.sidebar.title("메뉴")


def render_api_page():
    route = [
        [37.4979, 127.0276],  # 강남역
        [37.5007, 127.0365],  # 역삼역
        [37.5045, 127.0490]   # 선릉역
    ]

    m = folium.Map(
        location=route[0],
        zoom_start=14,
        control_scale=True
    )

    for idx, point in enumerate(route, start=1):
        folium.Marker(
            location=point,
            popup=f"정류장 {idx}",
            tooltip=f"정류장 {idx}"
        ).add_to(m)

    st.write("")

    st_folium(
        m,
        use_container_width=True,
        height=750,
        returned_objects=[]
    )


def render_db_page():
    st.write("정류장조회 페이지")


api_page = st.Page(
    render_api_page,
    title="지도조회",
    default=True
)

db_page = st.Page(
    render_db_page,
    title="정류장조회"
)

navigation = st.navigation([api_page, db_page], position="sidebar")
navigation.run()

# 초기 파일