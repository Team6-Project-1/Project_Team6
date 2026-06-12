DROP TABLE IF EXISTS `product`;

CREATE TABLE `product` (
    `product_code`    int    NOT NULL    COMMENT '상품 고유 코드 번호',
    `product_name`    varchar(200)    NOT NULL    COMMENT '상품명',
    `product_price`    int    NOT NULL    COMMENT '상품 가격(원화 기준)',
    `created_at`    datetime    NOT NULL    DEFAULT current_timestamp    COMMENT '상품 등록일',
    `updated_at`    datetime    NULL    COMMENT '상품 정보 수정일',
    `prd_category_code`    int    NOT NULL    COMMENT '상품카테고리코드'
);

DROP TABLE IF EXISTS `prd_category`;

CREATE TABLE `prd_category` (
    `prd_category_code`    int    NOT NULL    COMMENT '상품카테고리코드',
    `prd_catetory_name`    varchar(100)    NOT NULL    COMMENT '상품카테고리명',
    `created_at`    datetime    NOT NULL    DEFAULT current_timestamp    COMMENT '카테고리 등록일',
    `updated_at`    datetime    NULL    COMMENT '카테고리 정보 수정일'
);


ALTER TABLE `product` ADD CONSTRAINT `PK_PRODUCT` PRIMARY KEY (
    `product_code`
);

ALTER TABLE `prd_category` ADD CONSTRAINT `PK_PRD_CATEGORY` PRIMARY KEY (
    `prd_category_code`
);


# AUTO_INCREMENT 추가
ALTER TABLE `product`
    MODIFY `product_code` int AUTO_INCREMENT;

ALTER TABLE `prd_category`
    MODIFY `prd_category_code` int AUTO_INCREMENT;



ALTER TABLE `product` ADD CONSTRAINT `FK_prd_category_TO_product_1` FOREIGN KEY (
    `prd_category_code`
)
REFERENCES `prd_category` (
    `prd_category_code`
);




