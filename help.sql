delete
from supervisor
where name = 'Arly Klawi';
delete
from analyst
where name = 'Arly Klawi';
delete
from person
where name = 'Arly Klawi';

insert into person
values ('Purcell Abadam', '53 Northwestern Park');
insert into analyst
values ('Purcell Abadam', '53 Northwestern Park');
insert into person
values ('Purcell Abadam', '53 Northwestern Park');

delete
from analyses
where instant = '2020-07-10 00:02:48'
  and id = 'B-789';

select *
from incident
         left join analyses a on incident.instant = a.instant and incident.id = a.id
where incident.id in (select id from transformer)
;

select Distinct id
from incident;

DROP TABLE IF EXISTS analyses cascade;
DROP TABLE IF EXISTS lineincident cascade;
DROP TABLE IF EXISTS incident cascade;
DROP TABLE IF EXISTS transformer cascade;
DROP TABLE IF EXISTS line cascade;
DROP TABLE IF EXISTS busbar cascade;
DROP TABLE IF EXISTS element cascade;
DROP TABLE IF EXISTS substation cascade;
DROP TABLE IF EXISTS analyst cascade;
DROP TABLE IF EXISTS supervisor cascade;
DROP TABLE IF EXISTS person cascade;
drop table if exists borrower cascade;
drop table if exists loan cascade;
drop table if exists depositor cascade;
drop table if exists account cascade;
drop table if exists customer cascade;
drop table if exists branch cascade;

select id
from busbar
where id not in (select pbbid from transformer t)
  and id not in (select pbbid from line l)
  and id not in (select sbbid from transformer t)
  and id not in (select sbbid from line l);

select id
from element
where id not in (select id from transformer t)
  and id not in (select id from line l)
  and id not in (select id from busbar);

select gpslat,gpslong
from substation
where (gpslat,gpslong) not in (select t.gpslat,t.gpslong from transformer t)

select id from transformer
union
select id from busbar;