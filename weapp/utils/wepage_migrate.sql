

--
-- update sql for table `webapp_project`
--
ALTER TABLE `webapp_project` ADD COLUMN `cover_name` varchar(50) DEFAULT "";
ALTER TABLE `webapp_project` ADD COLUMN `is_active` tinyint(1) DEFAULT 0;
ALTER TABLE `webapp_project` ADD COLUMN `is_enable` tinyint(1) DEFAULT 0;
ALTER TABLE `webapp_project` ADD COLUMN `site_title` varchar(50) DEFAULT "";
