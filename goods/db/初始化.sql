DROP DATABASE IF EXISTS db_good;
CREATE DATABASE db_good CHARACTER SET 'utf8' COLLATE 'utf8_general_ci';
USE db_good;

create table if not exists t_user
(
    f_id            bigint auto_increment comment '主键'
        primary key,
    f_username      varchar(64) default ''                not null comment '用户名',
    f_password_hash varchar(128) default ''                not null comment '密码',
    f_created_time  datetime    default CURRENT_TIMESTAMP not null comment '创建时间',
    f_modified_time datetime    default CURRENT_TIMESTAMP not null on update CURRENT_TIMESTAMP comment '修改时间'
)
    comment '用户表';
create table if not exists t_cart
(
    f_id            bigint auto_increment comment '主键'
        primary key,
    f_user_id       bigint                             not null comment '用户ID',
    f_product_id    bigint                             not null comment '产品ID',
    f_quantity      int      default 1                 not null comment '数量',
    f_status        int      default 1                 not null comment '0:失效 1:有效 2:已支付',
    f_created_time  datetime default CURRENT_TIMESTAMP not null comment '创建时间',
    f_modified_time datetime default CURRENT_TIMESTAMP not null on update CURRENT_TIMESTAMP comment '修改时间'
)
    comment '购物车表';

create table if not exists t_product
(
    f_id            bigint auto_increment comment '主键'
        primary key,
    f_name          varchar(64)    default ''                not null comment '产品名称',
    f_price         decimal(10, 2) default 0.00              not null comment '产品价格',
    f_created_time  datetime       default CURRENT_TIMESTAMP not null comment '创建时间',
    f_modified_time datetime       default CURRENT_TIMESTAMP not null on update CURRENT_TIMESTAMP comment '修改时间'
)
    comment '产品表';

-- 添加数据
INSERT INTO t_product (f_name, f_price) VALUES ('商品1', 150.59);
INSERT INTO t_product (f_name, f_price) VALUES ('商品2', 100);
INSERT INTO t_product (f_name, f_price) VALUES ('商品3', 200.45);
INSERT INTO t_product (f_name, f_price) VALUES ('商品4', 500);
INSERT INTO t_product (f_name, f_price) VALUES ('商品5', 100.23);
-- 用户名admin 密码123456
INSERT INTO t_user (f_username, f_password_hash)VALUES ('admin', 'pbkdf2:sha256:260000$eCw4zBkrnYj8C7hP$306650a1cecd84104f8d6e17dff485564b1f0fd997324ba3dddd04d9187372b0');