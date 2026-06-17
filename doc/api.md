## API 데이터 적재

### 데이터 적재 파일

* `_04_insert_station_data.py` : 버스 정류장 정보 수집 및 DB 저장
* `_05_insert_route_data.py` : 버스 노선 정보 수집 및 DB 저장

### 실행 방법

* `api_run.py` 실행
* 정류장 정보 및 노선 정보를 수집하여 데이터베이스에 저장

---

## JSON 데이터 생성

### JSON 생성 파일

* `create_station_api_json.py` : 정류장 정보를 JSON 파일로 변환 및 저장
* `create_route_api_json.py` : 노선 정보를 JSON 파일로 변환 및 저장

### 실행 방법

* `api_json_run.py` 실행
* 데이터베이스 또는 API 데이터를 JSON 파일로 생성 및 저장

---

## 실행 순서

1. DB 초기화

   * `_01_project_init.sql`
   * `_02_table_create.sql`
   * `_03_insert_table.sql`

2. API 데이터 적재

   * `api_run.py`

3. JSON 파일 생성

   * `api_json_run.py`

4. 서비스 실행

   * `run.py`
