-- auto-generated definition

USE zhihu;


-- auto-generated definition
-- auto-generated definition
CREATE TABLE zhihu_sub_topic
(
  id                    INT AUTO_INCREMENT
    PRIMARY KEY,
  sub_topic_id          VARCHAR(50)  NULL,
  sub_topic_name        TEXT         NULL,
  sub_topic_link        VARCHAR(100) NULL,
  sub_topic_description TEXT         NULL,
  parent_topic_id       VARCHAR(50)  NULL,
  UNIQUE (id)
);




-- auto-generated definition
CREATE TABLE zhihu_parent_topic
(
  id                INT AUTO_INCREMENT
    PRIMARY KEY,
  parent_topic_id   VARCHAR(50) NULL,
  parent_topic_name TEXT        NULL,
  CONSTRAINT zhihu_parent_topic_id_uindex
  UNIQUE (id),
  CONSTRAINT zhihu_parent_topic_parent_topic_id_uindex
  UNIQUE (parent_topic_id)
);