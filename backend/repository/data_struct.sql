drop schema if  exists decision_engine cascade;
create schema if not exists decision_engine;

create table decision_engine.combat_task
(
    id               bigserial primary key,
    name             varchar(64),
    status           varchar(16),  -- create已创建，init已初始化，running进程中，end已结束
    description      varchar(256),
    init_situation   json,
    flow_json        json,
    limit_att_ck     text[],
    tendency         varchar(64),  -- hide隐蔽，max_destruction最大化破坏
    create_time      bigint default extract(epoch from now())::bigint,
    update_time      bigint default extract(epoch from now())::bigint
);
