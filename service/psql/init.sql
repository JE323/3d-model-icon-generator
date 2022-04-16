-----------------------------
-- CREATE TABLE STRUCTURES --
-----------------------------

create table if not exists jobStatus
(
    id   uuid not null,
    name text
);

create unique index if not exists jobStatus_id_uindex
    on jobStatus (id);

create table if not exists jobs
(
    id        uuid not null,
    name      text not null,
    modelId uuid,
    statusId    uuid,
    constraint jobs_pk
        primary key (id),
    constraint jobStatus_fk
        foreign key (statusId) references jobStatus(id)
);

create unique index if not exists jobs_id_uindex
    on jobs (id);


-----------------
-- CREATE DATA --
-----------------

 insert into jobStatus (id, name)
 values  ('f586550c-d38d-4471-a8e8-5b308ffaae2e', 'Created'),
         ('36cd2e5b-cb01-42cc-bf5e-c0f76884a7ae', 'AwaitingModel'),
         ('40cbae8d-747b-453f-a77c-cef0ee812af7', 'Processing'),
         ('8b57d835-78a3-4929-9189-ee39b3dc5065', 'Finished');