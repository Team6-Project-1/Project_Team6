import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
from app.sidebar import Sidebar
from app.views.map_page import MapPage
from app.views.station_page import StationPage
from app.views.bus_page import BusPage
from app.views.route_page import RoutePage
from app.views.faq_page import FAQPage

st.set_page_config(
    page_title="BUSKING",
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
    iframe { display: block; border: none; }
    section[data-testid="stSidebar"] a { text-decoration: none; }
    .nav-title {
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 0.75rem;
        color: #31333f;
    }
    .nav-link {
        display: flex;
        align-items: center;
        gap: 0.55rem;
        padding: 0.6rem 0.8rem;
        margin-bottom: 0.3rem;
        border-radius: 0.5rem;
        color: #4b5563;
        font-size: 1rem;
        font-weight: 500;
    }
    .nav-icon {
        font-size: 1.1rem;
        line-height: 1;
    }
    .nav-link:hover { background-color: #eef2f7; color: #111827; }
    .nav-link.active { background-color: #e1e7f0; color: #111827; font-weight: 700; }
    .sidebar-faq {
        position: fixed;
        left: 1.5rem;
        bottom: 1.5rem;
        z-index: 999;
    }
    .sidebar-faq a { color: #31333f; font-size: 1.05rem; font-weight: 700; }
    </style>
    """,
    unsafe_allow_html=True
)

sidebar = Sidebar()
current_page = sidebar.render()

pages = {
    "map": MapPage(),
    "station": StationPage(),
    "bus": BusPage(),
    "route": RoutePage(),
    "faq": FAQPage()
}

page = pages.get(current_page, pages["map"])
page.render()
