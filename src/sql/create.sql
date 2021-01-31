/* User information table. */
CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT
);

/* notification history information table. */
CREATE TABLE IF NOT EXISTS notif (
    time DATETIME,
    subject TEXT
);