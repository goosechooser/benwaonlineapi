CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL, 
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

-- Running upgrade  -> 22fda6090ace

CREATE TABLE likes_posts (
    user_id INTEGER, 
    posts_id INTEGER, 
    FOREIGN KEY(posts_id) REFERENCES post (id), 
    FOREIGN KEY(user_id) REFERENCES user (id)
);

INSERT INTO alembic_version (version_num) VALUES ('22fda6090ace');

