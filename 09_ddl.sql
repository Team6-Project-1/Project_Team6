# DDL (Data Definition Language)
#  - 데이터베이스 스키마(객체)를
#    만들고(create), 수정하고(ALTER), 삭제(DROP)하는 구문
# - DDL 구문은 실행 시 바로 DB에 반영된다

# [주의사항]
#  **** 절대 DML과 DDL을 혼용해서 작성하지 말자 ****
# 1. DML 구문 수행 -> 트랜잭션에 담김
# 2. 중간에 DDL 구문 수행
# 3. 트랜잭션 내용이 자동 COMMIT

# ===========================================
### create table
/* [작성법]
    create table [if not exist] 테이블명(
        컬럼1 자료형 [제약조건 | auto increment] [default] [comment],
        컬럼2 자료형 [제약조건] [default] [comment],
        컬럼3 자료형 [제약조건] [default] [comment],
        ...
    );
 */
# auto_increment : 숫자 자동 증가 옵션
# 기본적으로 PK 컬럼에만 사용 가능

create table product(
    id int primary key auto_increment comment '상품식별코드',
    name varchar(100) not null comment '상품명', # not null == 값이 필수로 들어가야 한다
    price int not null default 0 comment '상품가격',
    created_at datetime default current_timestamp comment '상품등록일시'
);
/*CREATE TABLE `product` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '상품식별코드',
  `name` varchar(100) NOT NULL COMMENT '상품명',
  `price` int NOT NULL DEFAULT '0' COMMENT '상품가격',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '상품등록일시',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci*/


# 생성한 테이블 조회
select * from product;

# 생성한 테이블 DDL 구문 확인
show create table product;

# 생성한 테이블 설명 조회
desc product;

# 테이블의 메타정보를 조회하는 구문
select
    *
from
    information_schema.tables
where
    TABLE_SCHEMA = 'menudb'
and
    TABLE_NAME = 'product';

# product 테이블에 데이터 추가(INSERT)
insert into product(name) values ('텀블러');
insert into product(name, price) values ('머그컵', 5000);

select * from product;

commit;

# =========================================================
### 제약조건(constraint)
# - 테이블 컬럼에 붙어
#   INSERT, UPDATE 시 각 컬럼에 기록되는 값에 대한 조건을 설정하는 방법
# - 데이터 무결성을 보장하는 목적으로 사용
# - 종류 : NOT NULL, UNIQUE, PRIMARY KEY, FOREIGN KEY, CHECK

# 제약조건 확인 방법
select
    *
from
    information_schema.TABLE_CONSTRAINTS
where
    CONSTRAINT_SCHEMA = 'menudb'
and
    TABLE_NAME = 'product';

# NOTNULL : 지정된 컬럼은 NULL일 수 없다 == 값 필수
# UNIQUE : 지정된 컬럼에는 중복되는 값을 저장할 수 없다

DROP TABLE IF EXISTS user_unique;
CREATE TABLE IF NOT EXISTS user_unique (
    user_no INT NOT NULL,
    user_id VARCHAR(255) NOT NULL,
    user_pwd VARCHAR(255) NOT NULL,
    user_name VARCHAR(255) NOT NULL,
    gender VARCHAR(3),
    phone VARCHAR(255) NOT NULL UNIQUE,
    email VARCHAR(255)
    # , UNIQUE (phone)
) ENGINE=INNODB;

INSERT INTO user_unique
(user_no, user_id, user_pwd, user_name, gender, phone, email)
VALUES
(1, 'user01', 'pass01', '홍길동', '남', '010-1234-5678', 'hong123@gmail.com'),
(2,  'user02', 'pass02', '유관순', '여', '010-8888-8888', 'yu77@gmail.com');

SELECT * FROM user_unique;

# phone 값 변경 -> UNIQUE 제약조건 위배 해결
# unique 제약조건 위배
INSERT INTO user_unique
(user_no, user_id, user_pwd, user_name, gender, phone, email)
VALUES
(3, 'user03', 'pass03', '이순신', '남', '010-777-7777', 'lee222@gmail.com');

# 오류 해석
# [23000][1062] Duplicate entry '010-777-7777' for key 'user_unique.phone' == 중복된 값을 넣으려고 했다
# Column 'user_id' cannot be null == 빈칸을 넣을 수 없다

# PRIMARY KEY (중요) ⭐️⭐️⭐️⭐️⭐️
# - 테이블 내 행을 구별하기 위한
#   식별자 역할의 컬럼에 추가하는 제약 조건
# - NOT NULL + UNIQUE 특징을 가짐 : 중복되지 않는 값 필수
# - PRIMARY KEY는 테이블 내에 1개만 설정 가능
#   단 , PK 설정이 적용되는 컬럼은 1개 또는 여러개 묶음(복합키) 가능 / 2컬럼이 모두 일치하는지 봐야함
#  ex) 1 가, 1 나 or 2 가, 3 가는 2개 중 한개만 겹치니까 아님

DROP TABLE IF EXISTS user_primarykey;
CREATE TABLE IF NOT EXISTS user_primarykey (
--     user_no INT PRIMARY KEY,
    user_no INT,
    user_id VARCHAR(255) NOT NULL,
    user_pwd VARCHAR(255) NOT NULL,
    user_name VARCHAR(255) NOT NULL,
    gender VARCHAR(3),
    phone VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    PRIMARY KEY (user_no) # 테이블 레벨
) ENGINE=INNODB;

INSERT INTO user_primarykey
(user_no, user_id, user_pwd, user_name, gender, phone, email)
VALUES
(1, 'user01', 'pass01', '홍길동', '남', '010-1234-5678', 'hong123@gmail.com'),
(2, 'user02', 'pass02', '유관순', '여', '010-777-7777', 'yu77@gmail.com');

SELECT * FROM user_primarykey;

desc user_primarykey;

# primary key 제약조건 에러 발생(null값 적용)
INSERT INTO user_primarykey
(user_no, user_id, user_pwd, user_name, gender, phone, email)
VALUES
(null, 'user03', 'pass03', '이순신', '남', '010-777-7777', 'lee222@gmail.com');
# [23000][1048] Column 'user_no' cannot be null
# not null이라고 설정안해도 notnull의 성질을 띄고 있다


# primary key 제약조건 에러 발생(중복값 적용)
INSERT INTO user_primarykey
(user_no, user_id, user_pwd, user_name, gender, phone, email)
VALUES
(2, 'user03', 'pass03', '이순신', '남', '010-777-7777', 'lee222@gmail.com');
# [23000][1062] Duplicate entry '2' for key 'user_primarykey.PRIMARY'

### PK 복합기 확인
create table order_composite_pk (
    user_id int,
    prod_id int,
    count int default 1,
    ordered_at datetime default (current_timestamp),
    primary key(user_id, prod_id, ordered_at)
);
insert into order_composite_pk
values (1, 1, 10, now());

insert into order_composite_pk
values (2, 1, 5, now());

insert into order_composite_pk
values (3, 100, default, now());

# pk 컬럼 3개 값이 모두 일치하는 중복 데이터 삽입 == 오류
insert into  order_composite_pk
(select * from order_composite_pk where user_id = 3);
# [23000][1062] Duplicate entry '3-100-2026-06-12 11:31:45' for key 'order_composite_pk.PRIMARY'

## FOREIGN KEY
# - 참조(REFERENCES)된 다른 테이블에서 제공하는 값만 사용 가능
# - 참조 무결성을 위배하지 않기 위해 사용
#   -> 데이터의 결점을 제거해서 신뢰도를 높임
#   -> 중복 제거, 중복 값 필요 시 참조
# - 참조는 다른 테이블의 PK 또는 UNIQUE가 설정된 컬럼만 참조 가능

# - FK 제약조건 설정 시 두 테이블간의 관계(RELATIONSHIP)이 형성된다
#    - 부모 테이블 : 참조를 당해서 컬럼 값을 제공하는 테이블
#    - 자식 테이블 : 참조를 통해 다른 테이블의 값을 사용하는 테이블
# - 제공되는 값 외에 NULL 사용 가능

DROP TABLE IF EXISTS user_grade;
CREATE TABLE IF NOT EXISTS user_grade (
    grade_code INT NOT NULL UNIQUE,
    grade_name VARCHAR(255) NOT NULL
) ENGINE=INNODB;

INSERT INTO user_grade
VALUES
(10, '일반회원'),
(20, '우수회원'),
(30, '특별회원');

SELECT * FROM user_grade;


DROP TABLE IF EXISTS user_foreignkey1;
CREATE TABLE IF NOT EXISTS user_foreignkey1 (
    user_no INT PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    user_pwd VARCHAR(255) NOT NULL,
    user_name VARCHAR(255) NOT NULL,
    gender VARCHAR(3),
    phone VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    grade_code INT , # 10, 20, 30, NULL 삽입 가능
    FOREIGN KEY (grade_code)
		REFERENCES user_grade (grade_code)
) ENGINE=INNODB;

INSERT INTO user_foreignkey1
(user_no, user_id, user_pwd, user_name, gender, phone, email, grade_code)
VALUES
(1, 'user01', 'pass01', '홍길동', '남', '010-1234-5678', 'hong123@gmail.com', 10),
(2, 'user02', 'pass02', '유관순', '여', '010-777-7777', 'yu77@gmail.com', 20);


# 부모 테이블에서 제공하지 않는 값(50) 삽입
SELECT * FROM user_foreignkey1;
INSERT INTO user_foreignkey1
(user_no, user_id, user_pwd, user_name, gender, phone, email, grade_code)
VALUES
(3, 'user03', 'pass03', '이순신', '남', '010-777-7777', 'lee222@gmail.com', 50);
# [42000][1064] You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near '' at line 3

### FK 삭제옵션 설정제 삭제 불가능

# - UPDATE/DELETE SET NULL :
#   부모 컬럼 값을 자식이 참조 중이면 변경, 삭제 시
#   자식 컬럼 값을 NULL로 변경

# - UPDATE/DELETE CASCADE :
#   부모 컬럼 값을 자식이 참조 중이면 변경, 삭제 시
#   자식 테이블에서 참조 값이 포함된 모든 행을 삭

DROP TABLE IF EXISTS user_foreignkey2;
CREATE TABLE IF NOT EXISTS user_foreignkey2 (
    user_no INT PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    user_pwd VARCHAR(255) NOT NULL,
    user_name VARCHAR(255) NOT NULL,
    gender VARCHAR(3),
    phone VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    grade_code INT ,
    FOREIGN KEY (grade_code)
		REFERENCES user_grade (grade_code)
        ON UPDATE SET NULL
        ON DELETE SET NULL
) ENGINE=INNODB;

INSERT INTO user_foreignkey2
(user_no, user_id, user_pwd, user_name, gender, phone, email, grade_code)
VALUES
(1, 'user01', 'pass01', '홍길동', '남', '010-1234-5678', 'hong123@gmail.com', 10),
(2, 'user02', 'pass02', '유관순', '여', '010-777-7777', 'yu77@gmail.com', 20);

SELECT * FROM user_foreignkey2;

DROP TABLE IF EXISTS user_foreignkey1;

# 부모 테이블 컬럼 값 수정
UPDATE user_grade
SET grade_code = 50
WHERE grade_code = 10;

-- 자식 테이블의 grade_code가 10이 었던 회원의 grade_code값이 NULL이 된 것을 확인
SELECT * FROM user_foreignkey2;

DELETE FROM user_grade
WHERE grade_code = 20;

-- 자식 테이블의 grade_code가 20이 었던 회원의 grade_code값이 NULL이 된 것을 확인
SELECT * FROM user_foreignkey2;

## CHECK 제약 조건
# 컬럼에 삽입될 수 있는 값에 대한 조건 설정

DROP TABLE IF EXISTS user_check;
CREATE TABLE IF NOT EXISTS user_check (
    user_no INT AUTO_INCREMENT PRIMARY KEY,
    user_name VARCHAR(255) NOT NULL,
    gender VARCHAR(3) CHECK (gender IN ('남','여')),
    age INT CHECK (age >= 19)
) ENGINE=INNODB;

INSERT INTO user_check
VALUES
    (null, '홍길동', '남', 25),
    (null, '이순신', '남', 33);

SELECT * FROM user_check;

# gender 컬럼 값 check 위배
INSERT INTO user_check
VALUES (null, '안중근', '남성', 27);
# [HY000][3819] Check constraint 'user_check_chk_1' is violated.

# age 컬럼 값 check 위배
INSERT INTO user_check
VALUES (null, '유관순', '여', 17);
# [HY000][3819] Check constraint 'user_check_chk_2' is violated.
