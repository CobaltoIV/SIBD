DROP TRIGGER IF EXISTS IC_1_2 on transformer;


create or replace function match_voltage() returns trigger as
$$
declare
    bpv NUMERIC(7, 4);
    spv NUMERIC(7, 4);
begin
    select voltage from busbar where id = new.pbbid into bpv;
    select voltage from busbar where id = new.sbbid into spv;
    if new.pv <> bpv then
        raise exception 'Primary busbar %s voltage does not match with primary voltage', new.pbbid;
    elsif new.sv <> spv then
        raise exception 'Secondary busbar %s voltage does not match with secondary voltage', new.sbbid;
    end if;
    return new;

end;
$$ language plpgsql;

create TRIGGER IC_1_2
    after
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
    if new.id IN (select id from transformer) then
        t_id := new.id;
        select s.sname, s.saddress, t.gpslat, t.gpslong
        from transformer t
                 inner join substation s on s.gpslat = t.gpslat and s.gpslong = t.gpslong
        where t.id = t_id
        into sn,sa,lat,long;
        if new.name = sn and new.address=sa then
            raise exception 'Analyst cannot analyse incident since it belongs to one of the substations he supervises';
        end if;
    end if;
    return new;

end;
$$ language plpgsql;

create TRIGGER IC_5
    after
        update or insert
    on analyses
    for each row
execute procedure check_substation();
