BEGIN;
CREATE TABLE `followers` (`fs_id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `follower_id` integer NOT NULL, `since` datetime NOT NULL);
CREATE TABLE `following` (`fg_id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `following_id` integer NOT NULL, `since` datetime NOT NULL);
CREATE TABLE `hashtag` (`hid` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `hash_name` varchar(160) NOT NULL);
CREATE TABLE `tweets` (`tid` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `posted` datetime NOT NULL, `tweet` longtext NOT NULL);
CREATE TABLE `users` (`uid` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `fname` varchar(250) NOT NULL, `lname` varchar(250) NOT NULL, `email` varchar(500) NOT NULL, `handle` varchar(100) NOT NULL UNIQUE, `password` varchar(250) NOT NULL, `about` longtext NOT NULL);
ALTER TABLE `tweets` ADD COLUMN `uid_id` integer NOT NULL;
ALTER TABLE `tweets` ALTER COLUMN `uid_id` DROP DEFAULT;
ALTER TABLE `hashtag` ADD COLUMN `tid_id` integer NOT NULL;
ALTER TABLE `hashtag` ALTER COLUMN `tid_id` DROP DEFAULT;
ALTER TABLE `following` ADD COLUMN `uid_id` integer NOT NULL;
ALTER TABLE `following` ALTER COLUMN `uid_id` DROP DEFAULT;
ALTER TABLE `followers` ADD COLUMN `uid_id` integer NOT NULL;
ALTER TABLE `followers` ALTER COLUMN `uid_id` DROP DEFAULT;
CREATE INDEX tweets_71422c2d ON `tweets` (`uid_id`);
ALTER TABLE `tweets` ADD CONSTRAINT tweets_uid_id_10106c84ef125221_fk_users_uid FOREIGN KEY (`uid_id`) REFERENCES `users` (`uid`);
CREATE INDEX hashtag_64b9ff56 ON `hashtag` (`tid_id`);
ALTER TABLE `hashtag` ADD CONSTRAINT hashtag_tid_id_e33f406b4ff8899_fk_tweets_tid FOREIGN KEY (`tid_id`) REFERENCES `tweets` (`tid`);
CREATE INDEX following_71422c2d ON `following` (`uid_id`);
ALTER TABLE `following` ADD CONSTRAINT following_uid_id_546d7c1faa986ae1_fk_users_uid FOREIGN KEY (`uid_id`) REFERENCES `users` (`uid`);
CREATE INDEX followers_71422c2d ON `followers` (`uid_id`);
ALTER TABLE `followers` ADD CONSTRAINT followers_uid_id_14029ab2aa544e03_fk_users_uid FOREIGN KEY (`uid_id`) REFERENCES `users` (`uid`);

COMMIT;

