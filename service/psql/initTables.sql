create table if not exists status
(
    id   uuid not null,
    name text
);

create table if not exists jobs
(
    id        uuid not null,
    name      text not null,
    "modelId" uuid,
    status    uuid,
    constraint jobs_pk
        primary key (id),
    constraint status_fk
        foreign key (id) references status (id)
);

create unique index if not exists jobs_id_uindex
    on jobs (id);

create unique index if not exists status_id_uindex
    on status (id);


