CREATE TABLE IF NOT EXISTS "users"
(
    "id"                UUID                NOT NULL    DEFAULT gen_random_uuid(),
    "login"             varchar(32)         NOT NULL,
    "password"          varchar(60)         NOT NULL,
    "role"              user_role           NOT NULL,
    "name"              varchar(255)        NOT NULL,
    "balance"           money,
    "scoring_system"    scoring_system,

    CONSTRAINT "pk_user_id"
        PRIMARY KEY ("id"),
    CONSTRAINT "unique_user_login"
        UNIQUE ("login")
);


CREATE TABLE IF NOT EXISTS "courses"
(
    "id"            UUID            NOT NULL    DEFAULT gen_random_uuid(),
    "author_id"     UUID            NOT NULL,
    "price"         money,
    "title"         varchar(255)    NOT NULL,
    "description"   text,

    CONSTRAINT "pk_course_id"
        PRIMARY KEY ("id"),
    CONSTRAINT "fk_course_author_id"
        FOREIGN KEY ("author_id") REFERENCES "users"("id") ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS "groups"
(
    "id"            UUID            NOT NULL    DEFAULT gen_random_uuid(),
    "course_id"     UUID            NOT NULL,
    "curator_id"    UUID            NOT NULL,
    "title"         varchar(255)    NOT NULL,

    CONSTRAINT "pk_group_id"
        PRIMARY KEY ("id"),
    CONSTRAINT "fk_group_course"
        FOREIGN KEY ("course_id") REFERENCES "courses"("id") ON DELETE CASCADE,
    CONSTRAINT "fk_group_curator_id"
        FOREIGN KEY ("curator_id") REFERENCES "users"("id") ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS "groups_members"
(
    "group_id"      UUID    NOT NULL,
    "student_id"    UUID    NOT NULL,

    CONSTRAINT "pk_groups_members_group_id_user_id"
        PRIMARY KEY ("group_id", "student_id"),
    CONSTRAINT "fk_groups_member_group_id"
        FOREIGN KEY ("group_id") REFERENCES "groups"("id") ON DELETE CASCADE,
    CONSTRAINT "fk_groups_member_student_id"
        FOREIGN KEY ("student_id") REFERENCES "users"("id") ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS "lessons"
(
    "id"            UUID            NOT NULL    DEFAULT gen_random_uuid(),
    "course_id"     UUID            NOT NULL,
    "teacher_id"    UUID            NOT NULL,
    "title"         varchar(255)    NOT NULL,
    "text"          text,

    CONSTRAINT "pk_lesson_id"
        PRIMARY KEY ("id"),
    CONSTRAINT "fk_lesson_course_id"
        FOREIGN KEY ("course_id") REFERENCES "courses"("id") ON DELETE CASCADE,
    CONSTRAINT "fk_lesson_teacher_id"
        FOREIGN KEY ("teacher_id") REFERENCES "users"("id") ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS "tasks"
(
    "id"            UUID            NOT NULL    DEFAULT gen_random_uuid(),
    "lesson_id"     UUID            NOT NULL,
    "title"         varchar(255)    NOT NULL,
    "description"   text,

    CONSTRAINT "pk_task_id"
        PRIMARY KEY ("id"),
    CONSTRAINT "fk_task_lesson_id"
        FOREIGN KEY ("lesson_id") REFERENCES "lessons"("id") ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS "hometasks"
(
    "id"            UUID            NOT NULL    DEFAULT gen_random_uuid(),
    "task_id"       UUID            NOT NULL,
    "student_id"    UUID            NOT NULL,
    "title"         varchar(255)    NOT NULL,
    "text"          text,
    "status"        task_status     NOT NULL,

    CONSTRAINT "pk_hometask_id"
        PRIMARY KEY ("id"),
    CONSTRAINT "fk_hometask_task_id"
        FOREIGN KEY ("task_id") REFERENCES "tasks"("id") ON DELETE CASCADE,
    CONSTRAINT "fk_hometask_student_id"
        FOREIGN KEY ("student_id") REFERENCES "users"("id") ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS "deadlines"
(
    "group_id"      UUID            NOT NULL,
    "lesson_id"     UUID            NOT NULL,
    "deadline"      timestamptz     NOT NULL,

    CONSTRAINT "pk_deadlines_group_id_lesson_id"
        PRIMARY KEY ("group_id", "lesson_id"),
    CONSTRAINT "fk_deadline_group_id"
        FOREIGN KEY ("group_id") REFERENCES "groups"("id") ON DELETE CASCADE,
    CONSTRAINT "fk_deadline_lesson_id"
        FOREIGN KEY ("lesson_id") REFERENCES "lessons"("id") ON DELETE CASCADE
);
