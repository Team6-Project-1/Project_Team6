
create database team6db;

show databases; # 데이터베이스 목록 조회

grant all privileges on team6db.* to skn_ai@'%';
show grants for skn_ai@'%'; # skn_ai 계정에 부여된 권한 목록 조회

