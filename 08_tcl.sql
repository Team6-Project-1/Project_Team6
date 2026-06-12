# TCL(Transaction Control Language)
# - 트랜잭션 제어 언어
# - COMMIT, ROLLBACK, SAVEPOINT 등이 있음

# Transaction이란?
# - 한번에 수행될 DML 논리적 작업 단위
# - 하나의 트랜잭션을 이용해서 관련 작업을
#   한번에 완료 또는 취소할 수 있게하기 위해서 사용

### Atomicity, 원자성
# - 원자성은 트랜잭션에 포함된 작업이 전부 성공하거나 전부 실패해야 한다는 원칙이다.
# - 예를 들어 계좌이체는 다음 두 작업이 함께 처리되어야 한다.
# 1. 내 계좌에서 금액 차감
# 2. 상대방 계좌에 금액 증가

# =========================================

# MySQL은 기본적으로 Autocommit 활성화 상태

# set autocommit = ON; # 활성화
set autocommit = OFF; # 비활성화

# COMMIT : DML로 인한 변경 사항(Transaction)을 DB에 반영
# ROLLBACK : DML 변경 사항을 취소(Transaction 내부 내용 폐기)

# 트랜잭션 시작 == 이후 실행되는 DML 구문을 트랜잭션에 저장
# 트랜잭션 종료 == COMMIT, ROLLBACK
start TRANSACTION; # autocommit이 활성화 되어도 사용 가능

select
    *
from
    tbl_menu
where
    menu_code = 21;

# 판매 가능 여부 Y -> N 수정
update
    tbl_menu
set
    orderable_status = 'N'
where
    menu_code = 21;

delete
from tbl_menu
where menu_code = 20;

insert into
    tbl_menu
values (
        null,
        'TX테스트',
        3000,
        5,
        'N'
       );

# 수정 후 commit을 수행하지 않았는데
# 조회 시 수정 내용이 반영된 것 처럼 보이는 이유
# -> 실제 DB에 반영은 안됐지만, 조회 시
#    트랜잭션에 저장된 DML 구문을 반영해서 보여줌
# == 미리보기, preview 같은 느낌
select * from tbl_menu;

ROLLBACK; # 변경사항 폐기

select * from tbl_menu;


# menu_code = 100 삭제후 DB 반영
delete
from tbl_menu
where menu_code = 100;

commit;
select * from tbl_menu;

ROLLBACK;
 # commit된 내용은 rollback X
select * from tbl_menu;