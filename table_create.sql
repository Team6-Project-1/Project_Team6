CREATE TABLE `ROUTE` ( # 1.노선 기본 정보
	`route_id`	VARCHAR(20)	NOT NULL	COMMENT '노선 ID(PK)',
	`route_nm`	VARCHAR(50)	NOT NULL	COMMENT '노선 이름',
	`route_abrv`	VARCHAR(50)	NOT NULL	COMMENT '노선 약칭',
	`area_id`	INT	NOT NULL	COMMENT '지역 구분 ID',
	`route_dc`	INT	NOT NULL	COMMENT '노선 설명',
	`dscnt`	DECIMAL(5,1)	NOT NULL	COMMENT '운행 거리(km)',
	`fare`	DECIMAL(10,2)	NULL	COMMENT '버스 운행 요금',
	`route_ty`	INT	NOT NULL	COMMENT '1:공항2:마을3:간선4:지선5:순환6:광역7:인천8:경기10:관광'
);

CREATE TABLE `ROUTE_STATION` ( # 2. 경로정보
	`route_station_id`	BIGINT	NOT NULL	COMMENT '노선 정류장 ID',
	`route_id`	VARCHAR(20)	NOT NULL	COMMENT '노선 ID(PK)',
	`station_id2`	VARCHAR(20)	NOT NULL	COMMENT '정류장 ID',
	`station_seq`	INT	NOT NULL	COMMENT '각 노선 별 정류장 순서 쿼리',
	`is_start`	CHAR(1)	NOT NULL	COMMENT '기점 여부',
	`is_end`	CHAR(1)	NOT NULL	COMMENT '종점 여부'
);

CREATE TABLE `STATION` ( # 3. 정류장
	`station_id`	VARCHAR(20)	NOT NULL	COMMENT '정류장 ID',
	`station_nm`	VARCHAR(100)	NOT NULL	COMMENT '정류장명',
	`gps_x`	DECIMAL(12,8)	NOT NULL	COMMENT '경도 X좌표',
	`gps_y`	DECIMAL(12,8)	NOT NULL	COMMENT '경도 Y좌표'
);

CREATE TABLE `ROUTE_OPERATION` ( # 4. 운행 및 배차 정보
	`operation_id`	BIGINT	NOT NULL	COMMENT '운행 정보 ID',
	`route_id`	VARCHAR(20)	NOT NULL	COMMENT '노선 ID(PK)',
	`use_at`	CHAR(1)	NOT NULL	COMMENT '사용 여부(0 : 미사용, 1: 사용)',
	`oprat_at`	CHAR(1)	NOT NULL	COMMENT '운행 여부(0 : 미운행, 1: 운행)',
	`caralc`	INT	NOT NULL	COMMENT '평균 배차  간격 (분)',
	`mumm_caralc`	INT	NOT NULL	COMMENT '최소 배차 간격',
	`mxmm_caralc`	INT	NOT NULL	COMMENT '최대 배치 간격',
	`oprat_reqre_tm`	INT	NOT NULL	COMMENT '운행소요시간(분)',
	`fircar_tm`	VARCHAR(10)	NOT NULL	COMMENT '첫차 시간',
	`lstcar_tm`	VARCHAR(10)	NOT NULL	COMMENT '막차 시간',
	`fircar_stm`	VARCHAR(10)	NOT NULL	COMMENT '기점 별 첫차 시간',
	`lstcar_stm`	VARCHAR(10)	NOT NULL	COMMENT '기점 별 막차 시간',
	`fircar_htm`	VARCHAR(10)	NOT NULL	COMMENT '종점 별 첫차 시간',
	`lstcar_htm`	VARCHAR(10)	NOT NULL	COMMENT '종점 별 막차 시간'
);

CREATE TABLE `price` ( # 5. 운행 요금
	`price_id`	INT	NOT NULL	COMMENT '운헹 요금',
	`route_id`	VARCHAR(20)	NOT NULL	COMMENT '노선 ID(PK)',
	`age`	INT	NOT NULL	COMMENT '나이대별',
	`price`	INT	NOT NULL	COMMENT '요금'
);

ALTER TABLE `ROUTE_OPERATION` ADD CONSTRAINT `PK_ROUTE_OPERATION` PRIMARY KEY (
	`operation_id`
);

ALTER TABLE `ROUTE_STATION` ADD CONSTRAINT `PK_ROUTE_STATION` PRIMARY KEY (
	`route_station_id`
);

ALTER TABLE `STATION` ADD CONSTRAINT `PK_STATION` PRIMARY KEY (
	`station_id`
);

ALTER TABLE `ROUTE` ADD CONSTRAINT `PK_ROUTE` PRIMARY KEY (
	`route_id`
);

ALTER TABLE `price` ADD CONSTRAINT `PK_PRICE` PRIMARY KEY (
	`price_id`,
	`route_id`
);

ALTER TABLE `price` ADD CONSTRAINT `FK_ROUTE_TO_price_1` FOREIGN KEY (
	`route_id`
)
REFERENCES `ROUTE` (
	`route_id`
);


