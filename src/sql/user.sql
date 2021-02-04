/* User information table. */
DROP TABLE IF EXISTS user;
CREATE TABLE user (
    name TEXT,
    email TEXT,
    alert BOOLEAN DEFAULT 1 NOT NULL,
    UNIQUE(email)
);

/* notification history information table. */
DROP TABLE IF EXISTS notif;
CREATE TABLE notif (
    time DATETIME,
    subject TEXT
);

/* RPi email info. */
CREATE TABLE IF NOT EXISTS email_info (
    user TEXT,
    pass TEXT
);

/* Recording reference. */
DROP TABLE IF EXISTS recording;
CREATE TABLE recording (
    ctime DATETIME,
    relpath TEXT
)