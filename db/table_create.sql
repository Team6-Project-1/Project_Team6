-- ============================================================
-- DROP (FK 의존성 역순)
-- price, ROUTE_OPERATION, ROUTE_STATION → ROUTE → ROUTE_TY, STATION, AREA
-- ============================================================

DROP TABLE IF EXISTS `price`;
DROP TABLE IF EXISTS `AGE`;
DROP TABLE IF EXISTS `ROUTE_OPERATION`;
DROP TABLE IF EXISTS `ROUTE_STATION`;
DROP TABLE IF EXISTS `ROUTE`;
DROP TABLE IF EXISTS `ROUTE_TY`;
DROP TABLE IF EXISTS `STATION`;
DROP TABLE IF EXISTS `AREA`;
DROP TABLE IF EXISTS `AREA_NAME`;

-- ============================================================
-- CREATE (FK 의존성 순서)
-- ============================================================

-- 1. 독립 테이블 (참조 없음)
CREATE TABLE `AGE` (
    `age_code` INT NOT NULL COMMENT '연령코드 (1: 일반, 2: 청소년, 3: 어린이)',
    `age` VARCHAR(10) NOT NULL COMMENT '연령대'
);

CREATE TABLE `AREA_NAME` (
    `area_code` INT NOT NULL COMMENT '지역코드',
    `area_name` VARCHAR(10) NOT NULL COMMENT '지역명'
);

CREATE TABLE `AREA` (
    `area_id`   VARCHAR(10)  NOT NULL COMMENT '지역 구분 ID',
    `area_code` INT  NOT NULL COMMENT '지역 코드'
);

CREATE TABLE `ROUTE_TY` (
    `route_ty` VARCHAR(10) NOT NULL COMMENT '1:공항2:마을3:간선4:지선5:순환6:광역7:인천8:경기10:관광',
    `ty_name`  VARCHAR(20) NOT NULL
);

CREATE TABLE `STATION` (
    `station_id`  INT           NOT NULL COMMENT '정류장 ID',
    `station_nm`  VARCHAR(100)  NOT NULL COMMENT '정류장명',
    `gps_x`       DECIMAL(12,8) NOT NULL COMMENT '경도 X좌표',
    `gps_y`       DECIMAL(12,8) NOT NULL COMMENT '경도 Y좌표',
    `sttn_no`     VARCHAR(10)   NULL     DEFAULT NULL,
    `sttn_use_at` CHAR(1)       NULL     DEFAULT NULL
);

-- 2. AREA, ROUTE_TY 참조
CREATE TABLE `ROUTE` (
    `route_id`   INT           NOT NULL COMMENT '노선 ID(PK)',
    `route_nm`   VARCHAR(50)   NOT NULL COMMENT '노선 이름',
    `route_abrv` VARCHAR(50)   NOT NULL COMMENT '노선 약칭',
    `route_dc`   VARCHAR(200)  NOT NULL COMMENT '노선 설명',
    `dstnc`      DECIMAL(5,1)  NOT NULL COMMENT '운행 거리(km)',
    `route_ty`   VARCHAR(10)   NOT NULL COMMENT '1:공항2:마을3:간선4:지선5:순환6:광역7:인천8:경기10:관광',
    `area_id`    VARCHAR(10)   NOT NULL COMMENT '지역 구분 ID'
);

-- 3. ROUTE, STATION 참조
CREATE TABLE `ROUTE_STATION` (
    `route_station_id` BIGINT   NOT NULL COMMENT '노선 정류장 ID',
    `station_seq`      INT      NOT NULL COMMENT '각 노선 별 정류장 순서 쿼리',
    `is_start`         CHAR(1)  NOT NULL COMMENT '기점 여부',
    `is_end`           CHAR(1)  NOT NULL COMMENT '종점 여부',
    `route_id`         INT      NOT NULL COMMENT '노선 ID',
    `station_id`       INT      NOT NULL COMMENT '정류장 ID'
    -- ❌ Key 컬럼 제거 (ERD의 PK 표시를 컬럼으로 잘못 해석한 것)
);

-- 4. ROUTE 참조
CREATE TABLE `ROUTE_OPERATION` (
    `operation_id`   BIGINT      NOT NULL COMMENT '운행 정보 ID',
    `route_id`       INT         NOT NULL COMMENT '노선 ID(PK)',
    `use_at`         CHAR(1)     NOT NULL COMMENT '사용 여부(0:미사용, 1:사용)',
    `oprat_at`       CHAR(1)     NOT NULL COMMENT '운행 여부(0:미운행, 1:운행)',
    `caralc`         INT         NOT NULL COMMENT '평균 배차 간격(분)',
    `mumm_caralc`    INT         NOT NULL COMMENT '최소 배차 간격',
    `mxmm_caralc`    INT         NOT NULL COMMENT '최대 배차 간격',
    `oprat_reqre_tm` INT         NOT NULL COMMENT '운행소요시간(분)',
    `fircar_tm`      VARCHAR(10) NOT NULL COMMENT '첫차 시간',
    `lstcar_tm`      VARCHAR(10) NOT NULL COMMENT '막차 시간',
    `fircar_stm`     VARCHAR(10) NOT NULL COMMENT '첫차시간(토요일)',
    `lstcar_stm`     VARCHAR(10) NOT NULL COMMENT '막차시간(토요일)',
    `fircar_htm`     VARCHAR(10) NOT NULL COMMENT '첫차시간(공휴일)',
    `lstcar_htm`     VARCHAR(10) NOT NULL COMMENT '막차시간(공휴일)'
);

-- 5. ROUTE_TY 참조
CREATE TABLE `price` (
    `age_code`      INT NOT NULL COMMENT '연령코드(1: 일반, 2: 청소년, 3: 어린이)',
    `route_ty` VARCHAR(10) NOT NULL COMMENT '1:공항2:마을3:간선4:지선5:순환6:광역7:인천8:경기10:관광',
    `price`    INT         NOT NULL COMMENT '요금'
);


-- ============================================================
-- PRIMARY KEY
-- ============================================================
ALTER TABLE `AREA`            ADD CONSTRAINT `PK_AREA`            PRIMARY KEY (`area_id`);
ALTER TABLE `ROUTE_TY`        ADD CONSTRAINT `PK_ROUTE_TY`        PRIMARY KEY (`route_ty`);
ALTER TABLE `STATION`         ADD CONSTRAINT `PK_STATION`         PRIMARY KEY (`station_id`);
ALTER TABLE `ROUTE`           ADD CONSTRAINT `PK_ROUTE`           PRIMARY KEY (`route_id`);
ALTER TABLE `ROUTE_STATION`   ADD CONSTRAINT `PK_ROUTE_STATION`   PRIMARY KEY (`route_station_id`);
ALTER TABLE `ROUTE_OPERATION` ADD CONSTRAINT `PK_ROUTE_OPERATION` PRIMARY KEY (`operation_id`, `route_id`);
ALTER TABLE `price`           ADD CONSTRAINT `PK_PRICE`           PRIMARY KEY (`age_code`, `route_ty`);
ALTER TABLE `AREA_NAME`       ADD CONSTRAINT `PK_AREA_NAME`       PRIMARY KEY (`area_code`);
ALTER TABLE `AGE`             ADD CONSTRAINT `PK_AGE`             PRIMARY KEY (`age_code`);

-- ============================================================
-- FOREIGN KEY
-- ============================================================

-- ROUTE → ROUTE_TY (수정 추가)
ALTER TABLE `ROUTE` ADD CONSTRAINT `FK_ROUTE_TY_TO_ROUTE_1`
    FOREIGN KEY (`route_ty`) REFERENCES `ROUTE_TY` (`route_ty`);

-- ROUTE → AREA (수정 추가)
ALTER TABLE `ROUTE` ADD CONSTRAINT `FK_AREA_TO_ROUTE_1`
    FOREIGN KEY (`area_id`) REFERENCES `AREA` (`area_id`);

-- ROUTE_STATION → ROUTE (수정 추가)
ALTER TABLE `ROUTE_STATION` ADD CONSTRAINT `FK_ROUTE_TO_ROUTE_STATION_1`
    FOREIGN KEY (`route_id`) REFERENCES `ROUTE` (`route_id`);

-- ROUTE_STATION → STATION (수정 추가)
ALTER TABLE `ROUTE_STATION` ADD CONSTRAINT `FK_STATION_TO_ROUTE_STATION_1`
    FOREIGN KEY (`station_id`) REFERENCES `STATION` (`station_id`);

-- ROUTE_OPERATION → ROUTE (기존)
ALTER TABLE `ROUTE_OPERATION` ADD CONSTRAINT `FK_ROUTE_TO_ROUTE_OPERATION_1`
    FOREIGN KEY (`route_id`) REFERENCES `ROUTE` (`route_id`);

-- price → ROUTE_TY (기존)
ALTER TABLE `price` ADD CONSTRAINT `FK_ROUTE_TY_TO_price_1`
    FOREIGN KEY (`route_ty`) REFERENCES `ROUTE_TY` (`route_ty`);

-- price → AGE (기존)
ALTER TABLE `price` ADD CONSTRAINT `FK_AGE_TO_price_1`
    FOREIGN KEY (`age_code`) REFERENCES `AGE`(`age_code`);

-- AREA → AREA_NAME (기존)
ALTER TABLE `AREA` ADD CONSTRAINT `FK_AREA_NAME_TO_AREA_1`
    FOREIGN KEY (`area_code`) REFERENCES `AREA_NAME`(`area_code`);