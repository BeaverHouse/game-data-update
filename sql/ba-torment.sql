CREATE TABLE students (
    student_id              VARCHAR(20) NOT NULL,
    name                    VARCHAR(50) NOT NULL,
    created_at              TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at              TIMESTAMP,
    deleted_at              TIMESTAMP,
    CONSTRAINT ba_students_pk PRIMARY KEY (student_id)
);

CREATE TABLE raids (
    raid_id                 VARCHAR(20) NOT NULL,
    name                    VARCHAR(200) NOT NULL,
    status                  VARCHAR(20) NOT NULL,
    created_at              TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at              TIMESTAMP,
    deleted_at              TIMESTAMP,
    CONSTRAINT ba_raids_pk PRIMARY KEY (raid_id)
);

CREATE TABLE named_users (
    user_id                 VARCHAR(20) NOT NULL,
    raid_id                 VARCHAR(20),
    description             VARCHAR(200) NOT NULL,
    youtube_url             VARCHAR(200) NOT NULL,
    created_at              TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at              TIMESTAMP,
    deleted_at              TIMESTAMP,
    UNIQUE (user_id, raid_id)
);