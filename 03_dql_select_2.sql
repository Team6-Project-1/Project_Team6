-- =============================
-- JOIN
-- =============================
-- 두개 이상의 테이블의 레코드를 연결해서 가상테이블(relation) 생성
-- 연관성을 가지고 있는 컬럼을 기준(데이터)으로 조합

# relation을 생성하는 2가지 방법
-- 1. join : 특정컬럼 기준으로 행과 행을 연결한다. (가로)
-- 2. union : 컬럼과 컬럼을 연결한다.(세로)
-- join은 두 테이블의 행사이의 공통된 데이터를 기준으로 **선을 연결해서** 새로운 하나의 행을 만든다.

# JOIN 구분
-- 1. Equi JOIN : 일반적으로 사용하는 Equality Condition(=)에 의한 조인
-- 2. Non-Equi JOIN : 동등조건(=)이 아닌 BETWEEN AND, IS NULL, IS NOT NULL, IN, NOT IN, !=  등으로 사용.

# EQUI JOIN 구분
-- 1. INNER JOIN(내부 조인) : 교집합 (일반적으로 사용하는 JOIN)
-- 2. OUTER JOIN(외부 조인) : 합집합
        -- LEFT (OUTER) JOIN (왼쪽 외부 조인)
        -- RIGHT (OUTER) JOIN (오른쪽 외부 조인)
-- 3. CROSS JOIN
-- 4. SELF JOIN(자가 조인)
-- 5. MULTIPLE JOIN(다중 조인)

## inner join(내부 조인)
# - 두 테이블의 교집합을 반환하는 SQL JOIN
# - == 조인에 사용될 두 테이블의 특정 컬럼 값이 같은 행만 JOIN

# tbl_menu, tbl_category 두 테이블을 inner join
# 조인 조건 : category_code 값이 같은 행 끼리 join
# select
#     *
# from
#     tbl_menu a # 별칭을 a로 지정
# inner join # inner는 생략 가능 == inner가 기본값
#     tbl_category b # 별칭을 b로 지정
# on
#     a.category_code = b.category_code;
#
# # 메뉴명, 가격, 카테고리명 가격 내림차순 조회
# select
#     b.menu_name,
#     b.menu_price,
#     a.category_name
# from
#     tbl_category a
# join
#     tbl_menu b
# on
#     a.category_code = b.category_code
# order by
#     b.menu_price desc;

# ================================================
# outer join
# - 좌/우측 기준 테이블의 모든 행을 relation에 포함하는 join
# - left  [outer] join
# - right [outer] join

# employeedb로 변경
# employee 테이블 조회
select
    emp_name, dept_code
from
    employee;

# department 테이블 조회
select
    *
from
    DEPARTMENT;

# employee 테이블과 department 테이블 inner join
# -> employee(23행), department(9행)
# -> join 결과 : 21행
# 원인 : employee.dept_code에 값이 없는(NULL) 행
#       하동운, 이오리 두 행이 조인 결과(relation) 포함되지 않음

## left outer join ##
# join 구문 기준 왼쪽에 작성된 테이블의 모든 행이
# relation에 포함되게 하기
# - inner join 결과 21행 + employee join 안된 2행 = 23행

select
    a.EMP_ID,
    a.EMP_NAME,
    a.DEPT_CODE,
    b.DEPT_id,
    b.DEPT_TITLE
from
    employee a
left outer join
    department b
on
    a.dept_code = b.DEPT_ID
order by
    a.EMP_ID asc;

## right outer join ##
# join 구문 기준 오른쪽에 작성된 테이블의 모든 행이
# relation에 포함되게 하기
# - inner join 결과 21행 + department join 안된 3행 = 24행

select
    a.EMP_ID,
    a.EMP_NAME,
    a.DEPT_CODE,
    b.DEPT_id,
    b.DEPT_TITLE
from
    employee a
right outer join
    department b
on
    a.dept_code = b.DEPT_ID
order by
    a.EMP_ID asc;


### menudb 계정
# cross join(카테시안곱, 곱집합)
# 조인 되는 두 테이블의 모든 경우수를 처리한것
select count(*) from tbl_menu; # 24행(초콜릿을 3번 누름)
select count(*) from tbl_category; # 12행

# 22 * 12 = 264

select
    *
from
    tbl_menu
cross join
    tbl_category;

# self join
# - 하나의 테이블에서
#   한 행이 다른 행을 참조하는 관계가 있는 경우
#   같은 테이블 끼리 조인하는 것
# [tip] 똑같은 테이블이 2개 있다고 생각하면 쉬움
select *from tbl_category;

select
    child.category_code,
    child.category_name,
    parent.category_name as "상위카테고리"
from
    tbl_category child
join
    tbl_category parent
on
    child.ref_category_code = parent.category_code
where
    parent.category_name = '식사';

# multiple join(다중 조인)
# - 3개 이상의 테이블을 조인하는 것
# - join의 순서가 매우 중요함
# ex) a join b join c
#  -> (a+b) join c
#  -> (a+b+c)

select * from tbl_order;
select * from tbl_order_menu;
select * from tbl_menu;

select
    *
from
    tbl_order o
join
    tbl_order_menu om
on
    o.order_code = om.order_code # o, om 합쳐진 reation 생성
join
    tbl_menu m
on
    m.menu_name = om.menu_code;

# employeedb로 변경
select * from EMPLOYEE;
select * from DEPARTMENT;
select * from LOCATION;

select
    *
from
    EMPLOYEE e
join
    DEPARTMENT d
on
    e.DEPT_CODE = d.DEPT_ID
join
    LOCATION l
on
    d.LOCATION_ID = l.LOCAL_CODE;



