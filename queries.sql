-- 3 - View   --
CREATE VIEW supp(sname,saddress,num_subs)
AS
SELECT sname,saddress, COUNT(*) AS num_subs
FROM  substation
GROUP BY sname, saddress;

-- 4 - SQL Queries --
-- 1 --
select a.name, a.address
from analyst a
where not exists(select id, instant
                 from incident
                 where id = 'B-789'
                     except
                 select id, instant
                 from analyses an
                 where an.name = a.name and an.address = a.address)
;
-- 2 --
SELECT DISTINCT sname, saddress
FROM substation
WHERE (sname,saddress) NOT IN(
    SELECT sname, saddress
    FROM substation
    WHERE gpslat <= 39.336775);
-- 3 --

SELECT id , COUNT(id)
FROM incident 
GROUP BY id
HAVING COUNT(id) <= ALL(
        SELECT COUNT(i2.id)
        FROM  incident i2 
        GROUP BY i2.id);

-- 4 --

SELECT name,address, COALESCE(num_subs,0)
FROM supervisor s LEFT OUTER JOIN supp ON s.name = supp.sname AND s.address = supp.saddress;

