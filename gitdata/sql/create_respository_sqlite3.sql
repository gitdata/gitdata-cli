---
--- gitdata repository schema - sqlite3
---

drop table if exists `subjects`;
create table `subjects` (
  `id` integer not null primary key autoincrement,
  `kind` varchar(100) NOT NULL
);

drop table if exists `facts`;
create table `facts` (
  `id` integer not null primary key autoincrement,
  `kind` varchar(100) NOT NULL,
  `entity` integer  not null,
  `attribute` varchar(100),
  `datatype` varchar(30),
  `value` mediumtext
);
