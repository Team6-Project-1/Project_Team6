# 버스 노선 조회 프로젝트 정리

## 1. 프로젝트 방향

버스 노선 및 정류소 정보를 활용해 노선 조회 서비스를 구현한다.

API 또는 엑셀/CSV 파일에서 데이터를 수집한 뒤, 필요한 컬럼만 정제하여 DB에 저장한다. 이후 Streamlit을 활용해 노선 검색, 정류소 조회, 지도 시각화 기능을 구현하는 방향으로 진행한다.

## 2. 데이터 수집

### 노선정보 API

https://t-data.seoul.go.kr/dataprovide/trafficdataviewopenapi.do?data_id=1053

### 정류장 API

 https://t-data.seoul.go.kr/dataprovide/trafficdataviewopenapi.do?data_id=1064

### 추가 확인 데이터

서울시 교통빅데이터플랫폼 데이터도 함께 확인

- 노선 정보
- 정류장 정보
- 운수 회사 별 운행 노선
- 노선 별 경유 노드
- 노선 별 좌표 정보
- 배차 정보

## 3. 데이터 수집 방식

API가 정상적으로 동작하지 않을 가능성이 있어 API와 엑셀/CSV 파일을 함께 고려한다.

진행 방향:

1. API 사용 가능 여부 확인
2. API에서 필요한 데이터 수집
3. 부족한 데이터는 엑셀/CSV 파일 활용
4. 수집한 데이터에서 필요한 칼럼만 선별
5. DB 테이블 구조에 맞게 정제
6. 정제된 데이터를 DB에 저장

## 4. ERD 구성

현재 ERD는 버스 노선, 정류장, 경로 정보, 운행 정보, 지역, 노선 유형, 요금 정보를 기준으로 구성되어 있다.

```
route (1)                                  # 노선명
├─< route_operation (N)  # 운행 정보 및 배차
│    ├─< price (N)                # 요금 정보
│    │    └─< age (N)            # 연령 별 구분
│    └─ route_ty (1)               # 노선 타입
│
└─< route_station (N)        # 경로 정보
├─< area (N)                         # 위치
│    └─ area_name (1)          # 지역명
│
└─< station (N)                    # 정류장
```

---

### 주요 테이블

| 테이블명 | 설명 |
| --- | --- |
| `ROUTE` | 노선 기본 정보 |
| `STATION` | 정류장 정보 |
| `ROUTE_STATION` | 노선 별 정류장 경로 정보 |
| `ROUTE_OPERATION` | 운행 및 배차 정보 |
| `AREA` | 지역 정보 |
| `ROUTE_TY` | 노선 유형 정보 |
| `price` | 요금 정보 |

### 테이블 관계

- 하나의 노선은 여러 정류장을 경유한다.
- 하나의 정류장은 여러 노선에 포함될 수 있다.
- 따라서 `ROUTE`와 `STATION`은 N:M 관계이며, 이를 `ROUTE_STATION` 테이블로 연결한다.
- `ROUTE_OPERATION`은 노선별 운행 및 배차 정보를 가진다.
- `ROUTE`는 `AREA`를 통해 지역 정보를 참조한다.
- `ROUTE`는 `ROUTE_TY`를 통해 노선 유형 정보를 참조한다.
- `price`는 노선 유형과 연령대 기준으로 요금 정보를 관리한다.

## 5. ERD 테이블 상세

### ROUTE: 노선 기본 정보

노선의 기본 정보를 저장하는 테이블이다.

주요 컬럼:

- `route_id`: 노선 ID
- `route_nm`: 노선 이름
- `route_abrv`: 노선 약칭
- `route_dc`: 노선 설명
- `dstnc`: 운행 거리
- `route_ty`: 노선 유형
- `area_id`: 지역 구분 ID

### STATION: 정류장 정보

정류장의 기본 정보와 위치 정보를 저장한다.

주요 컬럼:

- `station_id`: 정류장 ID
- `station_nm`: 정류장명
- `gps_x`: 경도 X좌표
- `gps_y`: 위도 Y좌표
- `sttn_no`: 정류장 번호
- `sttn_use_at`: 이용 여부

정류장 좌표는 Streamlit 지도 시각화에 활용할 수 있다.

### ROUTE_STATION: 경로 정보

노선과 정류장을 연결하는 중간 테이블이다.

주요 컬럼:

- `route_station_id`: 노선 정류장 ID
- `station_seq`: 정류장 순번
- `is_start`: 기점 여부
- `is_end`: 종점 여부
- `route_id`: 노선 ID
- `station_id`: 정류장 ID

`route_id`, `station_id` 조합은 중복되지 않도록 관리한다.

### ROUTE_OPERATION: 운행 및 배차 정보

노선 별 운행 여부, 배차 간격, 첫차/막차 시간을 저장한다.

주요 칼럼:

- `operation_id`: 운행 정보 ID
- `route_id`: 노선 ID
- `use_at`: 사용 여부
- `oprat_at`: 운행 여부
- `caralc`: 평균 배차 간격
- `mumm_caralc`: 최소 배차 간격
- `mxmm_caralc`: 최대 배차 간격
- `oprat_reqre_tm`: 운행 소요 시간
- `fircar_tm`: 첫차 시간
- `lstcar_tm`: 막차 시간
- `fircar_stm`: 첫차 시간, 토요일
- `lstcar_stm`: 막차 시간, 토요일
- `fircar_htm`: 첫차 시간, 공휴일
- `lstcar_htm`: 막차 시간, 공휴일

### AREA: 지역 정보

노선이 속한 지역 정보를 저장한다.

주요 컬럼:

- `area_id`: 지역 구분 ID
- `area_name`: 지역명

### ROUTE_TY: 노선 유형

노선 유형 정보를 저장한다.

주요 컬럼:

- `route_ty`: 노선 유형 ID
- `ty_name`: 노선명

노선 유형 예시:

```
1: 공항
2: 마을
3: 간선
4: 지선
5: 순환
6: 광역
7: 인천
8: 경기
10: 관광
```

### price: 요금 정보

연령대와 노선 유형 기준으로 요금 정보를 저장한다.

주요 컬럼:

- `age`: 연령대
- `route_ty`: 노선 유형
- `price`: 요금

연령대 예시:

```
성인
청소년
어린이
```

## 6. 프로젝트 파일 구조 설계

프로젝트 파일은 기능 별로 분리하여 관리.

예상 구조:

```
Project_Team6/
├── api/                  # API 및 데이터 적재
│   ├── __init__.py
│   ├── _04_insert_station.py
│   ├── _05_insert_route.py
│   ├── create_station_api_json.py
│   ├── create_route_api_json.py
│   ├── api_run.py        # api 적재 실행
│   ├── api_json_run.py   # api json 변환 실행
│   ├── bus_route.json
│   └── bus_station.json
├── app/                  # Streamlit UI
│   ├── pages/
│   │   ├── bus_page.py
│   │   ├── faq_page.py
│   │   ├── map_pages.py
│   │   ├── route_page.py
│   │   └── station_page.py   
│   ├── views/
│   │   ├── __init__.py
│   │   ├── demo.py
│   │   ├── main.py
│   │   └── sidebar.py    
│   ├── __init__.py
│   └── demo.py
├── archive/               
│   └── demo.py
├── config/               # 설정 파일
│   └── __init__.py
├── csv/                   # 추가 데이터 csv
│   ├── _06_insert_route_station_data.py
│   ├── generate_route_station.py
│   ├── insert_route_station.py
│   └── route_station_data.csv
├── db/                   # DB 관련
│   ├── queris/
│   │   ├── __init__.py
│   │   ├── route_query.py
│   │   └── station_query.py
│   ├── __init__.py
│   ├── _01_project_init.sql
│   ├── _02_table_create.sql
│   ├── _03_insert_table.sql
│   └── connection.py
├── csv/                   # 데이터 README
│   ├── api.md
│   ├── app.md
│   └── db.md
├── .env_example                  # api 키 보관 .env 파일
├── .gitignore
├── README.md
├── requirements.txt                   
└── run.py                # 실행 파일
```

SQL 관련 파일은 우선 API 폴더에 배치할 예정이며, 이후 이름이나 위치는 변경 및 추가 칼럼, 테이블에 따라 변경 될 수 있다

## 7. GitHub 저장소

팀 GitHub 저장소:

Team6 Project GitHub

앞으로 commit/push는 해당 저장소 기준으로 진행한다.

## 8. DB 관련 메모

### 계정 생성 예시

```
CREATE USER skn_ai@'%' IDENTIFIED BY '1234';
ALTER USER skn_ai@'%' IDENTIFIED BY '1234';
```

### 데이터베이스/스키마 생성

MySQL에서는 database와 schema를 거의 같은 의미로 사용한다.

```
CREATE DATABASE ;
CREATE SCHEMA menudb;
SHOW DATABASES;
```

### 권한 부여

```
GRANT ALL PRIVILEGES ON menudb.* TO skn_ai@'%';
GRANT ALL PRIVILEGES ON employeedb.* TO skn_ai@'%';

SHOW GRANTS FOR skn_ai@'%';
```

## 9. API 호출 코드 예시

API 호출 후 JSON 파일로 저장하는 예시 코드.

```
import requests
import json

url = "http://t-data.seoul.go.kr/apig/apiman-gateway/tapi/BisTbisMsSttn/1.0"

params = {
    "apikey": "API_KEY"
}

response = requests.get(url, params=params)
response.raise_for_status()

data = response.json()
print(data)

with open("bus_route.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("JSON 파일 저장 완료 (bus_route.json)")
```

## 10. 앞으로 진행할 일

1. API 정상 동작 여부 확인 ✅
2. API와 CSV/엑셀 데이터 컬럼 비교 ✅
3. 필요한 컬럼 선별 ✅
4. API 데이터 수집 코드 작성 ✅
5. 수집 데이터 정제 ✅ 
6. DB insert 코드 작성 ✅
7. Streamlit 화면 구성 🔄 
8. 노선 조회 기능 구현 ✅
9. 정류장 조회 기능 구현 ✅ 
10. FAQ 조회 기능 주제 논의 ✅

## 11. 현재 결정된 핵심 사항

- 노선과 정류장은 N:M 구조로 설계한다.
- `ROUTE_STATION`을 중간 테이블로 사용한다.
- 정류장 좌표는 지도 시각화를 위해 저장한다.
- 정류장 번호와 이용 여부 컬럼을 포함한다.
- 운행 및 배차 정보는 `ROUTE_OPERATION`에서 관리한다.
- 요금 정보는 `price` 테이블에서 관리한다.
- 팀 GitHub 저장소는 `Team6-Project-1/Project_Team6`를 사용한다
- 커밋메세지는 뒤에 본인 이름 기입

## 12. FAQ 구성 방안

Q1. 노선 검색은 어떻게 하나요?

버스 번호 또는 노선명을 입력하면 해당 노선 정보를 조회할 수 있습니다.
예: 143, 서대문12, 버스번호

Q2. 정류장 검색은 어떻게 하나요?

정류장명 또는 정류장 번호를 입력해 정류소 정보를 조회할 수 있습니다.

Q3. 노선 정보에는 어떤 내용이 포함되나요?

노선명, 노선 유형, 기점, 종점, 운행 거리, 첫차 시간, 막차 시간, 배차 간격 등을 확인할 수 있습니다.

Q4. 첫차/막차와 배차 간격은 실시간 정보인가요?

정류장명, 정류장 번호, 정류장 ID, 위치 좌표, 이용 여부 등을 확인할 수 있습니다.

Q5. 지도에서는 어떤 정보를 볼 수 있나요?

정류장의 위치를 지도에서 확인할 수 있으며, 노선별 정류장 경유 순서를 시각적으로 확인할 수 있습니다.

Q6. 데이터 출처는 어디인가요?

노선별 첫차/막차 시간은 API에서 제공하는 운행 정보를 기준으로 표시됩니다.
평일, 토요일, 공휴일 시간이 구분될 수 있습니다.

Q7. 데이터가 실제와 다를 수 있나요?

배차 간격은 API 또는 수집 데이터에서 제공하는 평균/최소/최대 배차 간격 정보입니다.
실시간 도착 정보와는 다를 수 있습니다.

Q8. 원하는 노선이 검색되지 않으면 어떻게 하나요?

노선 유형과 연령대에 따라 성인, 청소년, 어린이 요금을 확인할 수 있습니다.

Q9. 조회 되는 데이터는 어디에서 가져오나요

공공데이터포털, 서울시 열린데이터광장, 서울시 교통빅데이터플랫폼의 버스 노선 및 정류장 데이터를 활용합니다.

CREATE TABLE FAQ (
faq_id INT AUTO_INCREMENT PRIMARY KEY,
question VARCHAR(255) NOT NULL,
answer TEXT NOT NULL,
category VARCHAR(50),
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

`