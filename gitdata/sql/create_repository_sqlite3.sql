---
--- gitdata repository schema - sqlite3
---

drop table if exists `facts`;
create table if not exists `facts` (
  `entity` char(32) not null,
  `attribute` varchar(100) not null,
  `value_type` varchar(30) not null,
  `value` mediumtext not null
);

drop table if exists 'remotes';
create table `remotes` (
  `name` varchar(100) not null primary key,
  `location` varchar(1000) not null
);
