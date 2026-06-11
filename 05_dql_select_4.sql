# 내장 함수
# - mysql dbms에 이미 구현된 함수
# - 문자형, 숫자형, 날짜형별 함수가 따로 제공
# - 결과를 추출해야하다 보니 반드시 반환값을 갖는다

### 문자열 관련 함수
SELECT ASCII('A'), CHAR(65);

# 개발상식(개상 ㅋ)
# 1byte == 8bit
# 문자 인코딩 : 컴퓨터에서 문자를 표시하는 방법
# UTF-8 : ASCII코드 문자 == 1byte, 나머지는 3byte 표시
# -> 프로그래밍은 거의 영어, 숫자, 특수문자로 하기 때문에
# 1byte를 쓰는게 용량, 메모리적으로 이득
# UTF-16 : 모든 문자를 2byte(16bit)로 표시

# BIT_LENGTH: 할당된 비트 크기 반환
# CHAR_LENGTH: 문자열의 길이 반환
# LENGTH: 할당된 BYTE 크기 반환

SELECT
    BIT_LENGTH('pie'),
    CHAR_LENGTH('pie'),
    LENGTH('pie');

SELECT menu_name,
    CHAR_LENGTH(menu_name),
    LENGTH(menu_name),
    BIT_LENGTH(menu_name)
from
    tbl_menu;

# CONCAT: 문자열을 이어붙임
# CONCAT_WS: 구분자와 함께 문자열을 이어붙임
# WS == White Space == 공백문자라는 뜻(space, tab, enter)
SELECT CONCAT('호랑이', '기린', '토끼');
SELECT CONCAT_WS(',', '호랑이', '기린', '토끼');
SELECT CONCAT_WS('-', '2023', '05', '31');

# ELT: 해당 위치의 문자열 반환
# FIELD: 찾을 문자열 위치 반환
# FIND_IN_SET: 찾을 문자열의 위치 반환
# LOCATE: INSTR과 동일하고 순서는 반대
### INSTR(기준 문자열, 부분(검색) 문자열) == 많이 씀
# -> 기준 문자열에서 부분 문자열의 시작 위치 반환
select instr('사과딸기바나나', '딸기'); # == 3 (db는 거의 다 1부터 셈)
select instr('사과딸기바나나', '포도'); # == 0 (0이 없음 또는 틀림으로 반환)

# 메뉴 테이블에서 메뉴명에 '마늘'이 포함된 메뉴만 조회
select
    *
from
    tbl_menu
where
#   menu_name like '%마늘%';
    instr(menu_name, '마늘') > 0;


# LPAD(문자열, 길이, 채울 문자열), RPAD(문자열, 길이, 채울 문자열)

# LPAD: 문자열을 길이만큼 왼쪽으로 늘린 후에 빈 곳을 문자열로 채운다.
# RPAD: 문자열을 길이만큼 오른쪽으로 늘린 후에 빈 곳을 문자열로 채운다.

SELECT LPAD('왼쪽', 6, '@'), RPAD('오른쪽', 6 ,'@');

# SUBSTRING(문자열, 시작위치, 길이)
# SUBSTRING: 시작 위치부터 길이만큼의 문자를 반환(길이를 생략하면 시작 위치부터 끝까지 반환)
SELECT
    SUBSTRING('안녕하세요 반갑습니다.', 7, 2),
    SUBSTRING('안녕하세요 반갑습니다.', 7),
    substring('안녕하세요 반갑습니다.', instr('안녕하세요 반갑습니다', '반갑'))

# ======================================================
# 숫자 관련 함수

# `ABS: 절대값 반환`

    SELECT ABS(-123);


# CEILING(숫자), FLOOR(숫자), ROUND(숫자)
# CEILING: 올림값 반환
# FLOOR: 내림값 반환
# ROUND: 반올림값 반환
# TRUNCATE(숫자, 소수점자리): 버림
SELECT
    CEILING(1234.56),
    FLOOR(1234.56),
    ROUND(1234.56),
    TRUNCATE(1234.56, 0);

select
    ceiling(-1.5), # -1 == 커지는 쪽, 양수쪽으로 바꾸는 것
    FLOOR(-1.5), # -2 == 작아지는 쪽
    ROUND(-1.5), # -2 == 반대로 작용 소수점 뒤 9,8,7,6,5가 내려감
    TRUNCATE(-1.5, 0); # -1 == 소수점 아래로 지워버린다는 뜻

select
    truncate(1234.56, 1),
    truncate(1234.56, 0),
    truncate(1234.56, -1), # 1230 == 1의 자리의 수를 버려라
    truncate(1234.56, -2); # 1200 == 2의 자리의 수를 버려라

# RAND()
# RAND: 0이상 1 미만의 실수를 구한다
# 0.0 <= rand() < 1.0
# 'm <= 임의의 정수 < n'을 구하고 싶다면
# FLOOR((RAND() * (n - m) + m)을 사용한다.
# 1부터 10까지 난수 발생: FLOOR(RAND() * (11 - 1) + 1)
select
    rand(),
    rand(),
    rand();

# 1~45 사이 난수 1개 조회
# 0.0 <= x < 1.0
# 0.0 * 45 <= x * 45 < 1.0 * 45
# 0.0 * 45 + 1 <= x * 45 + 1< 1.0 * 45 + 1
# 1 <= floor(x * 45 + 1) < 46.0 -> 1 ~ 45사이 정수형 난수

select floor(rand() * 45 + 1);

# ========================================================
# 날짜 관련 함수

# now() : 현재시간
# adddate(date, 일수)
# subdate(date, 일수)
select
    now(),
    adddate(now(), 1),
    subdate(now(), 1),
    adddate(now(), interval 1 month), # day, month, year 등등
    subdate(now(), interval 1 month);

# DATEDIFF(날짜1, 날짜2) TIMEDIFF(날짜1 또는 시간1, 날짜1 또는 시간2)
# DATEDIFF: 날짜1 - 날짜2의 일수를 반환
# TIMEDIFF: 시간1 - 시간2의 결과를 구함

SELECT
    DATEDIFF('2026-11-20', NOW()),
    TIMEDIFF('17:07:11', '13:06:10');

# extract(단위 from date)
# - date에서 해당하는 단위 추출 -> 숫자 형태로 반환
# - 단위: year, quarter, month,
#    week, day, hour, minute, second, microsecond

select
    now(),
    extract(year from now()),
    extract(month from now()),
    extract(day from now());

# date_format(datetime, 형식문자열) -> 문자열
select
    date_format(now(), '%y/%m/%d'),
    date_format(now(), '%Y/%m/%d'),
    date_format(now(), '%h:%i');

# str_to_date(문자열, 형식문자열) -> datetime
select
    str_to_date('25/04/21', '%y/%m/%d'),
    str_to_date('2025/04/21', '%Y/%m/%d'),
    cast('2025/04/21' as date); -- 날짜시간형식 유추가 가능한 경우

# 기타함수
# null처리 함수 - if null(값, null일때 값)
select
    ifnull(ref_category_code, '미지정') ref_category_code
from
    tbl_category;

# 삼항연산처리 - if(조건식, 참일때 값, 거짓일때 값)
select
    isnull(category_code),
    if(isnull(category_code), '미지정', category_code) category_code
from
    tbl_menu;

select
    menu_name,
    menu_price,
    if(menu_price < 10000, '싼', '비싼') price_clf
from
    tbl_menu;

