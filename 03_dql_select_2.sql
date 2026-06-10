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
select
    *
from
    tbl_menu a # 별칭을 a로 지정
inner join # inner는 생략 가능 == inner가 기본값
    tbl_category b # 별칭을 b로 지정
on
    a.category_code = b.category_code;

# 메뉴명, 가격, 카테고리명 가격 내림차순 조회
select
    b.menu_name,
    b.menu_price,
    a.category_name
from
    tbl_category a
join
    tbl_menu b
on
    a.category_code = b.category_code
order by
    b.menu_price desc;

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


# cross join

# multiple join