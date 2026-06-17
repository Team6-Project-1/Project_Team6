# 실행 파일
# 실행 명령어 : streamlit run ./app/demo.py

import app as st
from openpyxl.chart import layout
# from app import navigation

from ui.api_page import render_api_page
from ui.db_page import render_db_page

# 앱 전체에 공통으로 적용할 브라우저 제목, 화면 너비 설정
st.set_page_config(
    '버스 노선 조회',
    layout='wide',
)

# 페이지 등록 작업
api_page = st.Page(
    render_api_page,
    title='api 조회',
    default=True # 기본페이지(첫페이지)로 설정
)

db_page = st.Page(
    render_db_page,
    title='DB 버스 노선 조회'
)

# 사이드바 네비게이션 등록
navigation = st.navigation([api_page, db_page], position='sidebar')
navigation.run()
