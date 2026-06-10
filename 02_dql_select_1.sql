/* SQL(Structured Query Language)
   - 구조화된(조건을 넣을 수 있다) 질의 언어
   - RDBMS에서 저장된 데이터를 관리, 조작하거나
     DB구조를 제어할때 사용하는 언어

   ## SQL 종류
   - DQL(Data Query Language)
     - 데이터 질의어
     - 테이블의 데이터를 검색/조회
     - SELECT

   - DML(Data Manipulation Language)
     - 데이터 조작 언어
     - 테이블에 저장된 값을 삽입, 수정, 삭제
     - INSERT, UPDATE, DELETE

   - DDL(Data Definition Language) - 데이터 정의 언어
   - DCL(Data Control Language) - 데이터 제어 언어
   - TCL(Transaction Control Language) - 트랙잭션 제어 언어
 */

 # DQL구조
/* (n) == 괄호 안에 숫자는 7개의 구문다 쓰였을때 해석 순서
    select 컬럼명 (5)  -- 필수
    from 테이블 (1)  -- 필수
    where 조건절(필터링) (2)
    group by 그룹핑 (3)
    having 조건절(그룹핑에 대해 필터링) (4)
    order by 정렬기준 (6)
    limit 행수제한 (7)

    1. SELECT : 조회하고자 하는 컬럼명을 기술함. 여러개를 기술하고자 하면 쉼표(,)로 구분하고 모든 컬럼 조회시 '*'을 사용
    2. FROM : 조회 대상 컬럼이 포함된 테이블명을 기술
    3. WHERE :
        행을 선택하는 조건을 기술함.
        여러 개의 제한 조건을 포함할 수 있으며, 각각의 제한 조건은 논리 연산자로 연결함
        제한조건을 만족시키는 행들만 Result Set에 포함됨
    4. ORDER BY : 정렬할 컬럼을 기준으로 오름/내림차순 지정
    5. GROUP BY : 행을 그룹핑함
    6. HAVING : 그룹핑된 행을 선택하는 조건을 기술함
*/

# tbl_menu(메뉴 테이블)의 모든(*) 컬럼 조회
select
    *
from
    tbl_menu;

# 메뉴 테이블에서 메뉴명, 가격 조회
select
    menu_name, menu_price
from
    tbl_menu;

## 조회되는 컬럼에 연산 가능
# 메뉴 테이블에서 메뉴명, 가격, 부가세(10%), 부가세 포함 전체 가격
select
    menu_name,
    menu_price,
    menu_price * 0.1,
    menu_price + (menu_price * 0.1)
from
    tbl_menu;

# ==================================================
# ResultSet : SELECT 조회 결과행의 집합
# 컬럼명 as 별칭 : ResultSet에 표기되는 컬럼명에 별칭(alias) 부여가능
# ==================================================

select
    menu_name as 메뉴명,
    menu_price as "메뉴 가격", # " "를 이용해서 띄어쓰기된 컬럼 묶기
    menu_price * 0.1 부가세, # as 생략
    menu_price + (menu_price * 0.1) "부가세 포함 가격"
from
    tbl_menu;

# 산술 연산
select
    10 + 3,
    10 - 3,
    10 * 3,
    10 / 3,
    10 div 3, # python == //(몫)
    10 % 3,
    10 mod 3; # % == modulo (나머지)

# 문자열 연결 처리(이어쓰기)
# concat('abc' 'def') == 'abcdef'
# 메튜 테이블에서 메뉴명, 메뉴가격(원) 조회
select
    menu_name as 메뉴명,
    concat(menu_price, '원') as '메뉴 가격(원)' # ' ' 이 문자열이라는 뜻
#     menu_price || '원' == oracle 문법 || = or 이라는 뜻
from
    tbl_menu;

# DISTINCT 컬럼 값 중복 제거
# - 지정된 컬럼의 값이 중복되는 행을 제거해서 조회
SELECT
    distinct category_code
from
    tbl_menu;

# =====================================================
# order by 절
# - 조회 결과(ResultSet)의 정렬 순서를 지정하는 구문
# - 특정 컬럼을 기준으로 삼아서 오름차순(ASC), 내림차순(DESC) 지정
# - 기준으로 삼은 컬럼이 여러 개 존재하면 그룹화된 정렬이 수행된

# 메뉴 테이블을 조회(가격 오름차순)
select
    menu_name,
    menu_price
from
    tbl_menu
order by
    menu_price asc;

# 메뉴 테이블을 조회(가격 내림차순)
select
    menu_name,
    menu_price
from
    tbl_menu
order by
    menu_price desc;

# 문자열(유니코드 순서), 날짜(과거~미래)도 정렬 기준이 될 수 있다
# 메뉴명 오름차순 정렬
select
    menu_name
from
    tbl_menu
order by
    menu_name asc;

# select절에 작성되지 않은 컬럼도 정렬 기준이 될 수 있다
select
    menu_name
from
    tbl_menu
order by
    menu_price asc;

# 기준으로 삼은 컬럼이 여러개 존재하면 그룹화된 정렬이 수행
# 메뉴 테이블에서
# 메뉴명, 카테고리코드, 가격을 조회
# 단, 카테고리 코드 오름차순, 가격 내림차순으로 조회
# 1) 카테고리 코드로 오름차순 정렬을 먼저 수행
# 2) 같은 카테고리 코드를 지닌 행들끼리 붙어있게됨
# 3) 같은 카테고리 코드를 지닌 행 내에서 가격 내림차순 정렬 수행

select
    menu_name,
    category_code,
    menu_price
from
    tbl_menu
order by
    category_code asc, # 같은 값을 가진 것끼리 그룹이 형성된다 볼 수 있음
    menu_price desc;

# ===================================================

# WHERE 행 필터링
# - 각 행별로 제시한 조건을 검사하고, TRUE인 행만 결과집합에 포함시킨다.
#  select 실행 -> cursor 객체 생성 -> 1행씩 접근 -> where가 필터링 하는 역할

# WHERE 비교 연산자
-- 표현식 사이의 관계를 비교하기 위해 사용하고, 비교 결과는 논리 결과중에 하나 (TRUE/FALSE/NULL)가 됨
-- 단, 비교하는 두 컬럼 값/표현식은 서로 동일한 데이터 타입이어야 함

-- --------------------------------------------------------------------------------
-- 연산자                    설명
-- --------------------------------------------------------------------------------
-- =                        같다(sql은 == 이 아닌 = 로 사용)
-- >,<                      크다/작다
-- >=,<=                    크거나 같다/작거나 같다
-- <>,!=                    같지 않다 (^= 없음)
-- BETWEEN AND                특정 범위에 포함되는지 비교
-- LIKE / NOT LIKE            문자 패턴 비교
-- IS NULL / IS NOT NULL    NULL 여부 비교
-- IN / NOT IN                비교 값 목록에 포함/미포함 되는지 여부 비교

-- --------------------------------------------------------------------------------

# WHERE 논리 연산자
-- 여러 개의 제한 조건 결과를 하나의 논리결과로 만들어 줌 (&&,|| 사용불가)
-- AND &&    여러 조건이 동시에 TRUE일 경우에만 TRUE 값 반환
-- OR ||    여러 조건들 중에 어느 하나의 조건만 TRUE이면 TRUE값 반환
-- NOT !    조건에 대한 반대값으로 반환(NULL은 예외)
-- XOR        두 값이 같으면 거짓, 두 값이 다르면 참

# 메뉴 테이블에서 가격이 13000원 이상인 메뉴의
# 메뉴코드, 메뉴명, 가격 조회
# 가격 내림차순 정렬
select # select가 제일 어렵고 복잡
    menu_code,
    menu_name,
    menu_price
from
    tbl_menu
where
    menu_price >= 13000
order by
    menu_price desc;

# 메뉴 테이블에서 카테고리 코드가 10번인 메뉴만 조회
# 카테코리 코드, 메뉴명, 메뉴 가격 컬럼
# 메뉴명 오름차순
select
    category_code,
    menu_name,
    menu_price
from
    tbl_menu
where
    category_code = 10
order by
    menu_name asc;

# 메뉴 테이블에서 가격이 10,000원 이상, 20,000 이하인
# 메뉴의 메뉴명, 가격, 카테고리 코드를
# 가격 내림차순으로 조회
select
    menu_name,
    menu_price,
    category_code
from
    tbl_menu
where
#   menu_price >= 10000 and menu_price <= 20000
    menu_price between 10000 and 20000 # 10000 ~ 20000 사이
order by
    menu_price desc;

# 반대 -> 10,000 미만 또는 20,000원 초과
# 10,0000원 이상, 20,000원 이상

select
    menu_name,
    menu_price,
    category_code
from
    tbl_menu
where
#     menu_price < 10000 or menu_price > 20000
    menu_price not between 10000 and 20000
order by
    menu_price desc;

# 메뉴 테이블에서
# 카테고리 코드가 4,6,10 인 메뉴의
# 메뉴명, 카테고리 코드 조회
select
    menu_name,
    category_code
from
    tbl_menu
where
#   category_code = 4 or category_code = 6 or category_code = 10
    category_code in (4, 6, 10) # 4, 6, 10 제외는 in 앞에 not만 붙이면 됨
order by
    category_code asc;

# like
# - 문자열 패턴 검사 연산자
# - 패턴을 나타내는 기호(와일드카드)로 %, _ 를 사용
# '%' : 포함, 0개 이상
# '_' : 문자 1개(한 칸)
select
    menu_name
from
    tbl_menu
where
#   menu_name like '아%'; '아'로 시작하는 메뉴 조회
#   menu_name like '%밥'; '밥'으로 끝나는 메뉴 조회
#   menu_name like '%마늘%'; '마늘'이 포함된 메뉴 조회
    menu_name like '_____'; #메뉴명이 5글자인 메뉴만 조회

-- =============================================================

# DB에서 NULL == 저장된 데이터가 없음을 의미

# 비교 연산 '=' : 비교하는 두 값(data)dl 같으면 True
# null은 빈칸의 상태를 의미 / 기호같은 거임 실제로는 아무것도 안써있는것
# = 는 실제의 값을 의미하기 때문에 조회되지 않음
# 카테고리 테이블에서 ref_category_code가 null인 행 조회
select
    *
from
    tbl_category
where
#   ref_category_code 컬럼 안에 null이란 값이 있으면 True
#   -> null은 값(data)가 아님. 컬럼이 비었음을 나타내는 기호
#   ref_category_code = null; == 모든 행 False

#   ref_category_code 컬럼 값이 비어있으면 True
#   ref_category_code is null

    ref_category_code is not null;

# =====================================================
# limit
# - 조회 결과(Resultset)에서 지정된 크기만큼의 행만 조회
# limit n : 0번 인덱스(1행) 부터 n행 만큼 조회
# limit start, n : start 인덱스부터 n행 만큼 조회
# limit offset, n : offset행 만큼 건너뛰고 n행 만큼 조회

select * from tbl_menu;
select * from tbl_menu limit 5;
select * from tbl_menu limit 1, 5;
select * from tbl_menu limit 5, 10;
select * from tbl_menu limit 10, 3;

# 페이징 처리 시 limit를 사용

# 메뉴 테이블을 이용해서 메뉴판을 만든다고 하였을 대
# 한 페이지당 메뉴 4개씩만
# 순서는 메뉴코드 역순

# 1페이지
select * from tbl_menu
order by menu_code desc
limit 0, 4;

# 2페이지
select * from tbl_menu
order by menu_code desc
limit 4, 4;

# 3페이지
select * from tbl_menu
order by menu_code desc
limit 8, 4;

# 4페이지
select * from tbl_menu
order by menu_code desc
limit 12, 4;

# 5페이지
select * from tbl_menu
order by menu_code desc
limit 16, 4;