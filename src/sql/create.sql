/* User information table. */
CREATE TABLE IF NOT EXISTS user (
    name TEXT,
    email TEXT,
    alert BOOLEAN DEFAULT 1 NOT NULL,
    UNIQUE(email)
);

/* notification history information table. */
CREATE TABLE IF NOT EXISTS notif (
    time DATETIME,
    subject TEXT
);

/* RPi email info. */
CREATE TABLE IF NOT EXISTS email_info (
    user TEXT,
    pass TEXT
);

/* Recording reference. */
CREATE TABLE IF NOT EXISTS recording (
    ctime DATETIME,
    relpath TEXT
)