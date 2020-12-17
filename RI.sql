DROP TRIGGER IF EXISTS IC_1_2 on transformer;


create or replace function match_voltage() returns trigger as
$$
declare
    bpv NUMERIC(7, 4);
    spv NUMERIC(7, 4);
begin
    -- Load corresponding busbar voltages into local variables
    select voltage from busbar where id = new.pbbid into bpv;
    select voltage from busbar where id = new.sbbid into spv;
    if new.pv <> bpv then -- If the primary voltages don't match
        raise exception 'Primary busbar %s voltage does not match with primary voltage', new.pbbid;
    elsif new.sv <> spv then -- If the secondary voltages don't match
        raise exception 'Secondary busbar %s voltage does not match with secondary voltage', new.sbbid;
    end if;
    return new; -- If everything is alright

end;
$$ language plpgsql;

create TRIGGER IC_1_2
    after -- Since an exception is raised everytime the condition is c«not checked before or after is irrelevant. The changes will always be rolled back
        update or insert
    on transformer
    for each row
execute procedure match_voltage();

DROP TRIGGER IF EXISTS IC_5 on analyses;

create or replace function check_substation() returns trigger as
$$
declare
    t_id VARCHAR(10); -- transformer id
    lat  NUMERIC(9, 6); -- latitude of transformer's substation
    long NUMERIC(8, 6); -- longitude of transformer's substation
    sn   VARCHAR(80); -- name of substation supervisor
    sa   VARCHAR(80); -- address of substation supervisor
begin
    if new.id IN (select id from transformer) then -- If the element is a transformer we need to check
        t_id := new.id; -- save element id
        -- Get the coordinates and supervisor data corresponding to the transformer in the incident
        select s.sname, s.saddress, t.gpslat, t.gpslong
        from transformer t
                 inner join substation s on s.gpslat = t.gpslat and s.gpslong = t.gpslong
        where t.id = t_id
        into sn,sa,lat,long;
        if new.name = sn and new.address=sa then -- If they are the same then the integrity constrsint was violated
            raise exception 'Analyst cannot analyse incident since it belongs to one of the substations he supervises';
        end if;
    end if;
    return new;

end;
$$ language plpgsql;

create TRIGGER IC_5
    after -- Similarly to before the after or before is irrelevant.
        update or insert
    on analyses
    for each row
execute procedure check_substation();

-- Just add a check to the coordinates of the substation so that there are no invalid coordinates
ALTER TABLE substation
ADD CONSTRAINT long_lat_range_check
CHECK (
	gpslong BETWEEN -90 AND 90
	AND gpslat BETWEEN -180 AND 180
);
-- Working with longitude and latitude ranges switched to not alter the schemaPart3.sql

