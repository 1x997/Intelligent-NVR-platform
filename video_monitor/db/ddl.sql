create table vms_camera
(
  camera_id serial primary key,
  camera_name varchar(64) not null default '',
  is_active integer not null default 1,
  ord_id integer not null default 0,
  extend varchar(1024) not null default '',
  station_id integer not null default 0
);


create table vms_station
(
  station_id serial primary key,
  parent_id integer not null default 0,
  station_name varchar(64) not null default '',
  station_type integer not null default 0,  -- 0 变电站  1 集控站
  is_active integer not null default 1,
  ord_id integer not null default 0,
  extend varchar(1024) not null default ''
);


create table vms_alarm
(
  alarm_id serial primary key,
  station_id integer not null default 0,
  camera_id integer not null default 0,
  check_type varchar(64) not null default '',  -- 检测类型
  begin_time timestamp not null default now(),
  end_time timestamp not null default now()
);


create table vms_alarm_image
(
  image_id serial primary key,
  alarm_id integer not null default 0,
  image_time timestamp not null default now(),
  image_url varchar(128) not null default '',
  extend varchar(1024) not null default ''
);

