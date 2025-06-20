
/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
DROP TABLE IF EXISTS `admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `admin` (
  `username` varchar(20) NOT NULL,
  `email` varchar(30) NOT NULL,
  `password` varchar(100) NOT NULL,
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `admin` WRITE;
/*!40000 ALTER TABLE `admin` DISABLE KEYS */;
INSERT INTO `admin` VALUES ('jem','jem@admin.com','$2b$12$a20x8Hn1uiymEFVSrf.5zO4B3bZCWemh8WpuSVPKpbBVN.9RFkNUG');
/*!40000 ALTER TABLE `admin` ENABLE KEYS */;
UNLOCK TABLES;
DROP TABLE IF EXISTS `applications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `applications` (
  `application_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `job_id` bigint(20) unsigned NOT NULL,
  `seeker_id` bigint(20) unsigned NOT NULL,
  `resume_url` varchar(255) NOT NULL,
  `cover_letter` text DEFAULT NULL,
  `status` enum('applied','reviewed','shortlisted','rejected') DEFAULT 'applied',
  `applied_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`application_id`),
  KEY `idx_job_id` (`job_id`),
  KEY `idx_seeker_id` (`seeker_id`),
  KEY `idx_status` (`status`),
  CONSTRAINT `applications_ibfk_1` FOREIGN KEY (`job_id`) REFERENCES `jobs` (`job_id`) ON DELETE CASCADE,
  CONSTRAINT `applications_ibfk_2` FOREIGN KEY (`seeker_id`) REFERENCES `job_seekers` (`seeker_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=130 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `applications` WRITE;
/*!40000 ALTER TABLE `applications` DISABLE KEYS */;
INSERT INTO `applications` VALUES (123,1,139,'none','none','applied','2025-04-07 10:31:02'),(129,5,139,'','','applied','2025-06-15 13:36:18');
/*!40000 ALTER TABLE `applications` ENABLE KEYS */;
UNLOCK TABLES;
DROP TABLE IF EXISTS `employer_verification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `employer_verification` (
  `verification_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `employer_id` bigint(20) unsigned NOT NULL,
  `business_permit_url` varchar(255) NOT NULL,
  `tax_id_number` varchar(100) NOT NULL,
  `supporting_docs_urls` text DEFAULT NULL,
  `linkedin_profile` varchar(255) DEFAULT NULL,
  `facebook_profile` varchar(255) DEFAULT NULL,
  `submitted_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `status` enum('pending','approved','rejected') NOT NULL DEFAULT 'pending',
  `approved_at` timestamp NULL DEFAULT NULL,
  `admin_notes` text DEFAULT NULL,
  PRIMARY KEY (`verification_id`),
  UNIQUE KEY `unique_employer` (`employer_id`),
  CONSTRAINT `fk_verification_employer` FOREIGN KEY (`employer_id`) REFERENCES `employers` (`employer_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `employer_verification` WRITE;
/*!40000 ALTER TABLE `employer_verification` DISABLE KEYS */;
INSERT INTO `employer_verification` VALUES (6,3,'/files\\business_permits\\Screenshot 2025-06-01 201950.png','12312','/files\\supporting_docs\\Screenshot 2025-06-01 202726.png','https://fake.com','https://fake.com','2025-06-15 06:32:08','rejected',NULL,'asdasd'),(8,17,'/files\\business_permits\\Screenshot 2025-05-13 185447.png','123','/files\\supporting_docs\\Screenshot 2025-05-13 172553.png','https://fake.com','https://fake.com','2025-06-15 07:37:08','approved','2025-06-16 17:36:32','hahaha');
/*!40000 ALTER TABLE `employer_verification` ENABLE KEYS */;
UNLOCK TABLES;
DROP TABLE IF EXISTS `employers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `employers` (
  `employer_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `email` varchar(255) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `last_login` timestamp NULL DEFAULT NULL,
  `company_name` varchar(255) NOT NULL,
  `industry` varchar(100) DEFAULT NULL,
  `company_size` int(11) DEFAULT NULL CHECK (`company_size` > 0),
  `website` varchar(255) DEFAULT NULL,
  `logo_url` varchar(255) DEFAULT NULL,
  `register_id` varchar(100) NOT NULL,
  `field` varchar(255) NOT NULL,
  PRIMARY KEY (`employer_id`),
  UNIQUE KEY `email` (`email`),
  KEY `idx_email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `employers` WRITE;
/*!40000 ALTER TABLE `employers` DISABLE KEYS */;
INSERT INTO `employers` VALUES (2,'kamjijajajo@gmail.com','$2b$12$EmVDH7PYPLQSpKkBqN4Mterb9N5buSsJN9WvGOAWjFkscfIsryAA.','2025-03-21 09:01:05',NULL,'Innovatech','Programming',1,'','','0',''),(3,'kanjijajajo@gmail.com','$2b$12$hpw1pAYj1C96f4gtXtuhb.N3B/kVTbbNZLK4/zSJjohueFsuHV4Xm','2025-03-21 09:03:05','2025-06-20 03:26:13','company001','Programming',1,'','','0',''),(17,'test_employer@gmail.com','$2b$12$qKr1VuAdw7HuhfCcW9IrpeJ6/xek/qoolMwWpSnrix4NorqjMyHla','2025-06-15 07:36:53','2025-06-20 04:23:07','test_employer',NULL,51,'https:fake.com','/uploads/logos/Screenshot_2025-05-13_185459.png','616f99ef-9549-4078-a78d-5a7e21f7383c','we are a fucking morons');
/*!40000 ALTER TABLE `employers` ENABLE KEYS */;
UNLOCK TABLES;
DROP TABLE IF EXISTS `interviews`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `interviews` (
  `interview_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `seeker_id` bigint(20) unsigned NOT NULL,
  `status` enum('scheduled','confirmed','completed','cancelled') DEFAULT 'scheduled',
  `date` date NOT NULL,
  `time` time NOT NULL,
  `interview_type` varchar(50) NOT NULL,
  `location` varchar(50) DEFAULT NULL,
  `gmeet_link` varchar(255) DEFAULT NULL,
  `additional_notes` varchar(255) DEFAULT NULL,
  `employer_id` int(11) NOT NULL,
  PRIMARY KEY (`interview_id`),
  KEY `idx_seeker_id` (`seeker_id`),
  KEY `idx_employer_id` (`employer_id`),
  CONSTRAINT `interviews_ibfk_2` FOREIGN KEY (`seeker_id`) REFERENCES `job_seekers` (`seeker_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `interviews` WRITE;
/*!40000 ALTER TABLE `interviews` DISABLE KEYS */;
INSERT INTO `interviews` VALUES (4,139,'scheduled','2025-06-18','04:56:00','in-person','building 100',NULL,'find me',3);
/*!40000 ALTER TABLE `interviews` ENABLE KEYS */;
UNLOCK TABLES;
DROP TABLE IF EXISTS `job_alerts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `job_alerts` (
  `alert_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `seeker_id` bigint(20) unsigned NOT NULL,
  `search_terms` varchar(255) DEFAULT NULL,
  `location` varchar(100) DEFAULT NULL,
  `frequency` enum('daily','weekly','instant') DEFAULT NULL,
  PRIMARY KEY (`alert_id`),
  KEY `idx_seeker_id` (`seeker_id`),
  CONSTRAINT `job_alerts_ibfk_1` FOREIGN KEY (`seeker_id`) REFERENCES `job_seekers` (`seeker_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `job_alerts` WRITE;
/*!40000 ALTER TABLE `job_alerts` DISABLE KEYS */;
/*!40000 ALTER TABLE `job_alerts` ENABLE KEYS */;
UNLOCK TABLES;
DROP TABLE IF EXISTS `job_interest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `job_interest` (
  `interest_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) unsigned NOT NULL,
  `job_interest` varchar(255) NOT NULL,
  `job_type` enum('Full-time','Part-time','Freelance','Internship') NOT NULL,
  `preferred_location` varchar(255) NOT NULL,
  `expected_salary_range` varchar(100) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`interest_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `job_interest_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `job_seekers` (`seeker_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `job_interest` WRITE;
/*!40000 ALTER TABLE `job_interest` DISABLE KEYS */;
INSERT INTO `job_interest` VALUES (10,139,'programming','Freelance','On-site','20,000 - 35,000','2025-04-16 02:01:28'),(11,140,'programming','Full-time','Remote','50,000 - 75,000','2025-06-20 02:50:21'),(12,141,'programming','Full-time','Hybrid','50,000 - 75,000','2025-06-20 04:14:31'),(13,142,'programming','Full-time','Hybrid','75,000+','2025-06-20 04:39:35');
/*!40000 ALTER TABLE `job_interest` ENABLE KEYS */;
UNLOCK TABLES;
DROP TABLE IF EXISTS `job_seekers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `job_seekers` (
  `seeker_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `email` varchar(255) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `last_login` timestamp NULL DEFAULT NULL,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `province` varchar(100) DEFAULT NULL,
  `municipality` varchar(100) DEFAULT NULL,
  `degree` varchar(100) DEFAULT NULL,
  `portfolio_url` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`seeker_id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `phone` (`phone`),
  KEY `idx_email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=143 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `job_seekers` WRITE;
/*!40000 ALTER TABLE `job_seekers` DISABLE KEYS */;
INSERT INTO `job_seekers` VALUES (139,'jemcarlo46@gmail.com','$2b$12$jJsAP1.XiA4IFyrGxSCW0eeHEPop1rxc2Gz8XnKcUjDkthM1iwjRC','2025-03-25 02:49:13','2025-06-20 11:07:26','Jemcarlo','Austria','09207766194','Pangasinan','','bsit',''),(140,'jemcarlo49090@gmail.com','$2b$12$l12tcJ5fpMIfZHgS1WlkqOxYnwG.tPBOBvkTDSKZHQQade8v05x8m','2025-06-20 02:45:17','2025-06-20 03:47:31','Jemcarlo','Austria','0920776619455','Pangasinan','','bsit',''),(141,'test_jobseeker@gmail.com','$2b$12$PgRKyYYfQRJB6Hk2./027uwcduIt7kzNeEQrU1RvAzViLJHeYwiQq','2025-06-20 04:08:55','2025-06-20 04:09:10','Jem','Austria','09457323970','Pangasinan','','bsit','/uploads/portfolios/Screenshot_2025-05-12_060144.png'),(142,'maryjanedalas02@gmial.com','$2b$12$la1LTXRVnNrG/AR/JyW78uj91FXQoPG5Phcb8CGgyro8i/eR5YQNO','2025-06-20 04:34:39','2025-06-20 04:34:55','jjane','ali','090909027996','Pangasinan','Saaan carlos','bsit','/uploads/portfolios/Screenshot_2025-05-12_060144.png');
/*!40000 ALTER TABLE `job_seekers` ENABLE KEYS */;
UNLOCK TABLES;
DROP TABLE IF EXISTS `job_skills`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `job_skills` (
  `job_id` bigint(20) unsigned NOT NULL,
  `skill_id` bigint(20) unsigned NOT NULL,
  PRIMARY KEY (`job_id`,`skill_id`),
  KEY `idx_job_id` (`job_id`),
  KEY `idx_skill_id` (`skill_id`),
  CONSTRAINT `job_skills_ibfk_1` FOREIGN KEY (`job_id`) REFERENCES `jobs` (`job_id`) ON DELETE CASCADE,
  CONSTRAINT `job_skills_ibfk_2` FOREIGN KEY (`skill_id`) REFERENCES `skills` (`skill_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `job_skills` WRITE;
/*!40000 ALTER TABLE `job_skills` DISABLE KEYS */;
/*!40000 ALTER TABLE `job_skills` ENABLE KEYS */;
UNLOCK TABLES;
DROP TABLE IF EXISTS `job_submissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `job_submissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `recruiter_id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `description` text NOT NULL,
  `type` enum('full-time','part-time','contract','freelance') NOT NULL,
  `status` enum('new','pending','approved','rejected') NOT NULL DEFAULT 'new',
  `location` varchar(255) DEFAULT NULL,
  `salary_range` varchar(100) DEFAULT NULL,
  `submission_date` datetime DEFAULT current_timestamp(),
  `applicant_count` int(11) DEFAULT 0,
  `approved_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `recruiter_id` (`recruiter_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `job_submissions` WRITE;
/*!40000 ALTER TABLE `job_submissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `job_submissions` ENABLE KEYS */;
UNLOCK TABLES;
DROP TABLE IF EXISTS `jobs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `jobs` (
  `job_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `employer_id` bigint(20) unsigned NOT NULL,
  `title` varchar(255) NOT NULL,
  `description` text NOT NULL,
  `location` varchar(100) NOT NULL,
  `salary_range` varchar(50) DEFAULT NULL,
  `employment_type` enum('full_time','part_time','contract','internship') NOT NULL,
  `posted_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `expires_at` timestamp NULL DEFAULT NULL,
  `status` enum('active','paused','closed') DEFAULT 'active',
  `approved` tinyint(1) NOT NULL DEFAULT 1,
  PRIMARY KEY (`job_id`),
  KEY `idx_employer_id` (`employer_id`),
  KEY `idx_status` (`status`),
  CONSTRAINT `jobs_ibfk_1` FOREIGN KEY (`employer_id`) REFERENCES `employers` (`employer_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `jobs` WRITE;
/*!40000 ALTER TABLE `jobs` DISABLE KEYS */;
INSERT INTO `jobs` VALUES (1,3,'progamming','a programming job','manila','35,000 - 50,000','contract','2025-03-23 03:18:19','2025-04-22 16:00:00','active',1),(2,3,'junior dev 1','  a programming job 1',' manila',' 35,000 - 50,000','contract','2025-03-23 03:18:19','2025-04-22 16:00:00','closed',0),(3,2,'progamming','a programming job 1','manila','35,000 - 50,000','contract','2025-03-23 03:18:19','2025-04-22 16:00:00','active',3),(4,3,'web dev','web dec with reactjs','manila',' 35,000 - 50,000','part_time','2025-06-15 05:53:50','2025-07-10 16:00:00','active',0),(5,17,' backend deav','  must have experience in backend for atlest 40years','Hybrid','20,000 - 35,000','contract','2025-06-15 13:13:19','2025-09-16 16:00:00','active',0),(6,17,'designer','knowledge about figma and photoshop','Remote','20,000 - 35,000','part_time','2025-06-16 04:44:24','2025-06-30 16:00:00','active',3),(7,17,'java','proffesional pthon','On-site','75,000+','full_time','2025-06-20 03:43:17','2025-06-04 16:00:00','active',1),(8,17,'the city','jaaava','Hybrid','75,000+','full_time','2025-06-20 04:25:13','2025-06-19 16:00:00','active',1);
/*!40000 ALTER TABLE `jobs` ENABLE KEYS */;
UNLOCK TABLES;
DROP TABLE IF EXISTS `messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `messages` (
  `message_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `sender_id` bigint(20) unsigned NOT NULL,
  `conversation_id` varchar(50) NOT NULL,
  `sender_type` enum('employer','job_seeker') NOT NULL,
  `receiver_id` bigint(20) unsigned NOT NULL,
  `receiver_type` enum('employer','job_seeker') NOT NULL,
  `content` text NOT NULL,
  `sent_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `is_read` tinyint(1) DEFAULT 0,
  `is_message_deleted` enum('false','true') NOT NULL,
  `is_conversation_deleted_by_sender` enum('false','true') NOT NULL,
  `is_conversation_deleted_by_receiver` enum('false','true') NOT NULL,
  PRIMARY KEY (`message_id`),
  KEY `idx_sender_id` (`sender_id`),
  KEY `idx_receiver_id` (`receiver_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `messages` WRITE;
/*!40000 ALTER TABLE `messages` DISABLE KEYS */;
INSERT INTO `messages` VALUES (3,139,'575067013220190','job_seeker',3,'employer','hello','2025-05-05 02:06:30',0,'false','false','false'),(4,3,'575067013220190','employer',139,'employer','hey?','2025-05-05 02:06:41',0,'false','false','false'),(5,139,'975984132132786','job_seeker',17,'employer','hey','2025-06-15 22:06:41',0,'false','false','false');
/*!40000 ALTER TABLE `messages` ENABLE KEYS */;
UNLOCK TABLES;
DROP TABLE IF EXISTS `notifications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `notifications` (
  `notification_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) unsigned NOT NULL,
  `user_type` enum('employer','job_seeker') NOT NULL,
  `message` text NOT NULL,
  `is_read` tinyint(1) DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`notification_id`),
  KEY `idx_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `notifications` WRITE;
/*!40000 ALTER TABLE `notifications` DISABLE KEYS */;
/*!40000 ALTER TABLE `notifications` ENABLE KEYS */;
UNLOCK TABLES;
DROP TABLE IF EXISTS `otp_codes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `otp_codes` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `email` varchar(255) NOT NULL,
  `otp_code` varchar(6) NOT NULL,
  `expiry_time` datetime NOT NULL,
  `is_valid` tinyint(1) DEFAULT 1,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `idx_email` (`email`),
  KEY `idx_email_otp` (`email`,`otp_code`,`is_valid`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `otp_codes` WRITE;
/*!40000 ALTER TABLE `otp_codes` DISABLE KEYS */;
INSERT INTO `otp_codes` VALUES (1,'jemcarlo46@gmail.com','171150','2025-03-19 09:09:29',1,'2025-03-19 00:59:29');
/*!40000 ALTER TABLE `otp_codes` ENABLE KEYS */;
UNLOCK TABLES;
DROP TABLE IF EXISTS `password_reset_tokens`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `password_reset_tokens` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(255) NOT NULL,
  `token` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `expiry` timestamp NOT NULL DEFAULT current_timestamp(),
  `used` tinyint(1) DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_token` (`token`),
  KEY `idx_email` (`email`),
  KEY `idx_expiry` (`expiry`),
  KEY `idx_token` (`token`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `password_reset_tokens` WRITE;
/*!40000 ALTER TABLE `password_reset_tokens` DISABLE KEYS */;
/*!40000 ALTER TABLE `password_reset_tokens` ENABLE KEYS */;
UNLOCK TABLES;
DROP TABLE IF EXISTS `qualifications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `qualifications` (
  `qualification_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `seeker_id` bigint(20) unsigned NOT NULL,
  `degree` varchar(80) NOT NULL,
  `school_graduated` varchar(100) NOT NULL,
  `certifications` varchar(255) DEFAULT NULL,
  `specialized_training` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`qualification_id`),
  KEY `idx_seeker_id` (`seeker_id`),
  CONSTRAINT `qualifications_ibfk_1` FOREIGN KEY (`seeker_id`) REFERENCES `job_seekers` (`seeker_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `qualifications` WRITE;
/*!40000 ALTER TABLE `qualifications` DISABLE KEYS */;
INSERT INTO `qualifications` VALUES (10,139,'bsit','bcc','s','programming'),(12,141,'[\"Bachelor of Science in Information Technology\"]','bcc','none','programming'),(13,142,'[\"Bachelor of Science in Information Technology\"]','bcc','programming','programming');
/*!40000 ALTER TABLE `qualifications` ENABLE KEYS */;
UNLOCK TABLES;
DROP TABLE IF EXISTS `ratings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ratings` (
  `rating_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `rater_id` bigint(20) unsigned NOT NULL,
  `rater_type` enum('employer','job_seeker') NOT NULL,
  `ratee_id` bigint(20) unsigned NOT NULL,
  `ratee_type` enum('employer','job_seeker') NOT NULL,
  `job_id` bigint(20) unsigned NOT NULL,
  `score` tinyint(4) DEFAULT NULL CHECK (`score` between 1 and 5),
  `review` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`rating_id`),
  KEY `idx_rater_id` (`rater_id`),
  KEY `idx_ratee_id` (`ratee_id`),
  KEY `idx_job_id` (`job_id`),
  CONSTRAINT `ratings_ibfk_1` FOREIGN KEY (`job_id`) REFERENCES `jobs` (`job_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `ratings` WRITE;
/*!40000 ALTER TABLE `ratings` DISABLE KEYS */;
/*!40000 ALTER TABLE `ratings` ENABLE KEYS */;
UNLOCK TABLES;
DROP TABLE IF EXISTS `saved_jobs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `saved_jobs` (
  `saved_job_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `seeker_id` bigint(20) unsigned NOT NULL,
  `job_id` bigint(20) unsigned NOT NULL,
  `saved_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`saved_job_id`),
  KEY `seeker_id` (`seeker_id`),
  KEY `job_id` (`job_id`),
  CONSTRAINT `saved_jobs_ibfk_1` FOREIGN KEY (`seeker_id`) REFERENCES `job_seekers` (`seeker_id`) ON DELETE CASCADE,
  CONSTRAINT `saved_jobs_ibfk_2` FOREIGN KEY (`job_id`) REFERENCES `jobs` (`job_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `saved_jobs` WRITE;
/*!40000 ALTER TABLE `saved_jobs` DISABLE KEYS */;
INSERT INTO `saved_jobs` VALUES (2,139,5,'2025-06-15 13:15:27');
/*!40000 ALTER TABLE `saved_jobs` ENABLE KEYS */;
UNLOCK TABLES;
DROP TABLE IF EXISTS `seeker_profiles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `seeker_profiles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) unsigned NOT NULL,
  `about` text DEFAULT NULL,
  `experience_title` varchar(255) DEFAULT NULL,
  `company` varchar(255) DEFAULT NULL,
  `experience_date` varchar(255) DEFAULT NULL,
  `experience_description` text DEFAULT NULL,
  `resume` varchar(255) DEFAULT NULL,
  `linkedin` varchar(255) DEFAULT NULL,
  `github` varchar(255) DEFAULT NULL,
  `twitter` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `seeker_profiles_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `job_seekers` (`seeker_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `seeker_profiles` WRITE;
/*!40000 ALTER TABLE `seeker_profiles` DISABLE KEYS */;
INSERT INTO `seeker_profiles` VALUES (3,139,'im a student with some knowledgge about programming','some programming ','none','2025','im currently studing ','/files\\files/resumes\\Screenshot_2025-05-12_060800.png','https://fake.com','https://fake.com','https://fake.com'),(4,141,'python','programming','mentos company','jan 1 2023','nothing',NULL,'https://fake.com','https://pornhub.com','https://pornhub.com'),(5,142,'i dont have skill and ssshy person','programming','mentos company','jan 1 2023','i can programing ',NULL,'https://com','https://com','https://com');
/*!40000 ALTER TABLE `seeker_profiles` ENABLE KEYS */;
UNLOCK TABLES;
DROP TABLE IF EXISTS `seeker_skills`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `seeker_skills` (
  `seeker_id` bigint(20) unsigned NOT NULL,
  `skill_id` bigint(20) unsigned NOT NULL,
  `proficiency` enum('beginner','intermediate','expert') DEFAULT NULL,
  PRIMARY KEY (`seeker_id`,`skill_id`),
  KEY `idx_seeker_id` (`seeker_id`),
  KEY `idx_skill_id` (`skill_id`),
  CONSTRAINT `seeker_skills_ibfk_1` FOREIGN KEY (`seeker_id`) REFERENCES `job_seekers` (`seeker_id`) ON DELETE CASCADE,
  CONSTRAINT `seeker_skills_ibfk_2` FOREIGN KEY (`skill_id`) REFERENCES `skills` (`skill_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `seeker_skills` WRITE;
/*!40000 ALTER TABLE `seeker_skills` DISABLE KEYS */;
/*!40000 ALTER TABLE `seeker_skills` ENABLE KEYS */;
UNLOCK TABLES;
DROP TABLE IF EXISTS `skills`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `skills` (
  `skill_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`skill_id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `skills` WRITE;
/*!40000 ALTER TABLE `skills` DISABLE KEYS */;
/*!40000 ALTER TABLE `skills` ENABLE KEYS */;
UNLOCK TABLES;
DROP TABLE IF EXISTS `verified_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `verified_users` (
  `email` varchar(50) NOT NULL,
  PRIMARY KEY (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `verified_users` WRITE;
/*!40000 ALTER TABLE `verified_users` DISABLE KEYS */;
INSERT INTO `verified_users` VALUES ('jemcarlo46@gmail.com'),('kanjijajajo@gmail.com'),('maryjanedalas02@gmial.com'),('test_employer@gmail.com'),('test_jobseeker@gmail.com');
/*!40000 ALTER TABLE `verified_users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

