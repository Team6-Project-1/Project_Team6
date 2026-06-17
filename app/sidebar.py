import streamlit as st


class Sidebar:
    def __init__(self):
        self.menu_items = [
            ("지도조회", "map", "🗺️"),
            ("정류장조회", "station", "📍"),
            ("버스조회", "bus", "🚌"),
            ("경로조회", "route", "🛣️"),
        ]

    def get_current_page(self):
        return st.query_params.get("page", "map")

    def render_link(self, label, page_key, icon, current_page):
        active = "active" if current_page == page_key else ""
        st.sidebar.markdown(
            f'<a class="nav-link {active}" href="?page={page_key}" target="_self">'
            f'<span class="nav-icon">{icon}</span>{label}</a>',
            unsafe_allow_html=True
        )

    def render(self):
        current_page = self.get_current_page()

        st.sidebar.markdown('<div class="nav-title">메뉴</div>', unsafe_allow_html=True)

        for label, page_key, icon in self.menu_items:
            self.render_link(label, page_key, icon, current_page)

        faq_active = "active" if current_page == "faq" else ""
        st.sidebar.markdown(
            f"""
            <div class="sidebar-faq">
                <a class="{faq_active}" href="?page=faq" target="_self">❓ FAQ</a>
            </div>
            """,
            unsafe_allow_html=True
        )

        return current_page
