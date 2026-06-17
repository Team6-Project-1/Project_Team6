import streamlit as st


FAQ_LIST = [
    {"category": "검색", "question": "노선 검색은 어떻게 하나요?", "answer": "버스 번호 또는 노선명을 입력하면 해당 노선 정보를 조회할 수 있습니다."},
    {"category": "검색", "question": "정류장 검색은 어떻게 하나요?", "answer": "정류장명의 일부만 입력해도 포함된 정류장이 모두 검색됩니다."},
    {"category": "검색", "question": "검색한 정류장이 없으면 어떻게 되나요?", "answer": "입력한 이름과 일치하는 정류장이 없으면 '검색 결과가 없습니다.'라고 표시됩니다."},
    {"category": "노선", "question": "노선 정보에는 어떤 내용이 포함되나요?", "answer": "노선 ID, 노선명, 약칭, 설명, 운행 거리, 노선 유형, 지역 정보가 포함됩니다."},
    {"category": "노선", "question": "운행하지 않는 버스도 조회되나요?", "answer": "조회는 가능하지만 운행 정보에서 미운행으로 표시됩니다."},
    {"category": "운행", "question": "운행 및 배차 정보에는 어떤 내용이 포함되나요?", "answer": "사용 여부, 운행 여부, 평균/최소/최대 배차 간격, 소요시간, 첫차·막차 시간이 포함됩니다."},
    {"category": "운행", "question": "배차 간격은 실시간 정보인가요?", "answer": "수집된 정적 데이터 기준이며, 실시간 운행 상황과 다를 수 있습니다."},
    {"category": "정류장", "question": "정류장 위치는 어떻게 표시되나요?", "answer": "정류장의 GPS 좌표를 활용해 지도 위에 마커로 표시됩니다."},
    {"category": "지도", "question": "경로 조회에서 지도에 무엇이 표시되나요?", "answer": "선택한 노선의 경유 정류장이 순서대로 선으로 연결되어 표시됩니다. 초록=기점, 파랑=중간, 빨강=종점입니다."},
    {"category": "요금", "question": "요금 정보는 어떻게 확인하나요?", "answer": "버스 조회 결과에서 성인, 청소년, 어린이 연령대별 요금을 확인할 수 있습니다."},
    {"category": "데이터", "question": "데이터는 어디에서 가져오나요?", "answer": "공공데이터포털, 서울시 열린데이터광장, 서울시 교통빅데이터플랫폼의 버스 데이터를 활용합니다."},
    {"category": "데이터", "question": "데이터가 실제와 다를 수 있나요?", "answer": "공공 API 수집 데이터 기준이므로 실제 운행 상황(우회, 공사, 사고 등)과 차이가 있을 수 있습니다."},
    {"category": "기능", "question": "FAQ도 검색할 수 있나요?", "answer": "FAQ 페이지 상단 검색창에 키워드를 입력하면 관련 항목만 필터링됩니다."},
]


CATEGORY_ICONS = {
    "검색": "🔍",
    "노선": "🚌",
    "운행": "🕒",
    "정류장": "📍",
    "지도": "🗺️",
    "요금": "💰",
    "데이터": "📊",
    "기능": "⚙️",
}


class FAQPage:
    def render(self):
        st.subheader("❓ FAQ")

        keyword = st.text_input(
            "FAQ 검색",
            placeholder="검색어를 입력하세요. 예: 요금, 정류장, 배차"
        )

        if keyword:
            filtered = [
                f for f in FAQ_LIST
                if keyword.lower() in f["question"].lower()
                or keyword.lower() in f["answer"].lower()
                or keyword.lower() in f["category"].lower()
            ]
        else:
            filtered = FAQ_LIST

        if not filtered:
            st.warning("검색 결과가 없습니다.")
            return

        st.caption(f"📄 총 {len(filtered)}개")

        for faq in filtered:
            icon = CATEGORY_ICONS.get(faq["category"], "❓")
            with st.expander(f"{icon} [{faq['category']}] {faq['question']}"):
                st.write(faq["answer"])
