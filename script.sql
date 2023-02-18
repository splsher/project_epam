create table if not exists user(
id INT AUTO_INCREMENT PRIMARY KEY,
username VARCHAR(45) NOT NULL,
password VARCHAR(160) NOT NULL,
photo BLOB NULL,
city VARCHAR(45) NOT NULL,
email VARCHAR(45) NOT NULL
);


CREATE TABLE IF NOT EXISTS wall(
id INT AUTO_INCREMENT PRIMARY KEY,
user_id INT NOT NULL,
username VARCHAR(45) NOT NULL,
photo BLOB NULL,
datetime DATETIME NOT NULL,
text TEXT NOT NULL,
photo_wall longblob NULL,
);

INSERT INTO wall (username, photo)
SELECT username, photo
FROM user;

