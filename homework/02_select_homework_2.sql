# 재직 중이고 휴대폰 마지막 자리가 2인 직원 중 입사일이 가장 최근인
# 직원 3명의 사원번호, 직원명, 전화번호, 입사일, 퇴직여부를 출력하세요.
# - 참고. 퇴사한 직원은 퇴직여부 컬럼값이 ‘Y’이고, 재직 중인 직원의 퇴직여부 컬럼값은 ‘N’
select
    EMP_ID,
    EMP_NAME,
    PHONE,
    HIRE_DATE,
    ENT_YN
from
    employee
where
    ENT_YN = 'N'
    and
    PHONE like '%2'
order by
    HIRE_DATE desc
limit
    3;
