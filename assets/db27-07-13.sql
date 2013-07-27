-- MySQL dump 10.13  Distrib 5.5.28, for debian-linux-gnu (i686)
--
-- Host: localhost    Database: fbintegrated
-- ------------------------------------------------------
-- Server version	5.5.28-0ubuntu0.12.04.3

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `category`
--

DROP TABLE IF EXISTS `category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `category` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `text` varchar(240) DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `category`
--

LOCK TABLES `category` WRITE;
/*!40000 ALTER TABLE `category` DISABLE KEYS */;
INSERT INTO `category` VALUES (1,'cat1',NULL),(2,'cat2',NULL);
/*!40000 ALTER TABLE `category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `choice`
--

DROP TABLE IF EXISTS `choice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `choice` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `text` varchar(240) DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `choice`
--

LOCK TABLES `choice` WRITE;
/*!40000 ALTER TABLE `choice` DISABLE KEYS */;
INSERT INTO `choice` VALUES (1,' Choice 1',NULL),(2,' Choice 2',NULL),(3,' Choice 3',NULL),(4,' Choice 4',NULL),(5,' Choice 5',NULL),(6,' Choice 6',NULL);
/*!40000 ALTER TABLE `choice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `game`
--

DROP TABLE IF EXISTS `game`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `game` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `player_id` varchar(30) DEFAULT NULL,
  `player_name` varchar(50) DEFAULT NULL,
  `start_timestamp` datetime DEFAULT NULL,
  `category` int(11) DEFAULT NULL,
  `questions` varchar(100) DEFAULT NULL,
  `num_questions` int(11) DEFAULT NULL,
  `user_agent` varchar(150) DEFAULT NULL,
  `player_ip` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `game`
--

LOCK TABLES `game` WRITE;
/*!40000 ALTER TABLE `game` DISABLE KEYS */;
INSERT INTO `game` VALUES (1,'1','','2013-07-27 00:56:58',1,'[1L, 3L, 2L]',3,'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.56 Safari/537.17','127.0.0.1'),(2,'2','','2013-07-27 01:15:10',2,'[3L, 2L]',2,'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.56 Safari/537.17','127.0.0.1'),(3,'2','','2013-07-27 01:18:08',2,'[3L, 2L]',2,'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.56 Safari/537.17','127.0.0.1'),(4,'2','','2013-07-27 01:18:13',2,'[3L, 2L]',2,'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.56 Safari/537.17','127.0.0.1'),(5,'2','','2013-07-27 01:18:16',2,'[2L, 3L]',2,'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.56 Safari/537.17','127.0.0.1'),(6,'2','','2013-07-27 01:19:58',1,'[2L, 3L, 1L]',3,'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.56 Safari/537.17','127.0.0.1'),(7,'2','','2013-07-27 01:20:29',1,'[2L, 3L, 1L]',3,'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.56 Safari/537.17','127.0.0.1'),(8,'2','','2013-07-27 01:20:30',2,'[3L, 2L]',2,'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.56 Safari/537.17','127.0.0.1'),(9,'2','','2013-07-27 01:25:10',2,'[2L, 3L]',2,'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.56 Safari/537.17','127.0.0.1'),(10,'3','Vijeenrosh Vijeen','2013-07-27 01:33:11',2,'[2L, 3L]',2,'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.56 Safari/537.17','127.0.0.1'),(11,'3','Vijeenrosh Vijeen','2013-07-27 01:34:05',2,'[2L, 3L]',2,'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.56 Safari/537.17','127.0.0.1'),(12,'3','Vijeenrosh Vijeen','2013-07-27 01:34:11',1,'[1L, 2L, 3L]',3,'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.56 Safari/537.17','127.0.0.1'),(13,'3','Vijeenrosh Vijeen','2013-07-27 01:51:53',1,'[2L, 3L, 1L]',3,'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:11.0) Gecko/20100101 Firefox/11.0','127.0.0.1'),(14,'3','Vijeenrosh Vijeen','2013-07-27 19:15:06',2,'[2L, 3L]',2,'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.56 Safari/537.17','127.0.0.1');
/*!40000 ALTER TABLE `game` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `log`
--

DROP TABLE IF EXISTS `log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `choice_id` int(11) DEFAULT NULL,
  `choice_text` varchar(100) DEFAULT NULL,
  `parent_question` int(11) DEFAULT NULL,
  `correct` int(11) DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL,
  `game_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `game_id` (`game_id`),
  CONSTRAINT `log_ibfk_1` FOREIGN KEY (`game_id`) REFERENCES `game` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `log`
--

LOCK TABLES `log` WRITE;
/*!40000 ALTER TABLE `log` DISABLE KEYS */;
INSERT INTO `log` VALUES (1,1,' Choice 1',1,0,'2013-07-27 00:59:29',1),(2,2,' Choice 2',1,1,'2013-07-27 00:59:31',1),(3,3,' Choice 3',1,0,'2013-07-27 01:45:58',12),(4,2,' Choice 2',1,1,'2013-07-27 01:45:59',12),(5,1,' Choice 1',1,0,'2013-07-27 01:46:00',12),(6,3,' Choice 3',1,0,'2013-07-27 01:46:01',12),(7,4,' Choice 4',1,0,'2013-07-27 01:46:02',12),(8,3,' Choice 3',1,0,'2013-07-27 01:46:03',12),(9,2,' Choice 2',1,1,'2013-07-27 01:46:04',12),(10,1,' Choice 1',1,0,'2013-07-27 01:46:04',12),(11,4,' Choice 4',2,0,'2013-07-27 01:51:57',13),(12,5,' Choice 5',2,0,'2013-07-27 01:51:58',13),(13,3,' Choice 3',2,1,'2013-07-27 01:51:59',13);
/*!40000 ALTER TABLE `log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `qc_association`
--

DROP TABLE IF EXISTS `qc_association`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `qc_association` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `question_id` int(11) DEFAULT NULL,
  `choice_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `question_id` (`question_id`),
  KEY `choice_id` (`choice_id`),
  CONSTRAINT `qc_association_ibfk_1` FOREIGN KEY (`question_id`) REFERENCES `question` (`id`),
  CONSTRAINT `qc_association_ibfk_2` FOREIGN KEY (`choice_id`) REFERENCES `choice` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `qc_association`
--

LOCK TABLES `qc_association` WRITE;
/*!40000 ALTER TABLE `qc_association` DISABLE KEYS */;
INSERT INTO `qc_association` VALUES (1,1,1),(2,1,2),(3,1,3),(4,1,4),(5,2,4),(6,2,5),(7,2,3),(10,3,3),(11,3,4);
/*!40000 ALTER TABLE `qc_association` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `qcat_association`
--

DROP TABLE IF EXISTS `qcat_association`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `qcat_association` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `category_id` int(11) DEFAULT NULL,
  `question_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `category_id` (`category_id`),
  KEY `question_id` (`question_id`),
  CONSTRAINT `qcat_association_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `category` (`id`),
  CONSTRAINT `qcat_association_ibfk_2` FOREIGN KEY (`question_id`) REFERENCES `question` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `qcat_association`
--

LOCK TABLES `qcat_association` WRITE;
/*!40000 ALTER TABLE `qcat_association` DISABLE KEYS */;
INSERT INTO `qcat_association` VALUES (1,1,1),(2,1,2),(3,1,3),(4,2,2),(5,2,3);
/*!40000 ALTER TABLE `qcat_association` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `question`
--

DROP TABLE IF EXISTS `question`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `question` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `text` varchar(240) DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  `correct_choice_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `question`
--

LOCK TABLES `question` WRITE;
/*!40000 ALTER TABLE `question` DISABLE KEYS */;
INSERT INTO `question` VALUES (1,'Question 1',NULL,2),(2,'Question 2',NULL,3),(3,'Question 3',NULL,3);
/*!40000 ALTER TABLE `question` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fb_id` varchar(100) DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `api_key` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (3,'100002023991153','Vijeenrosh Vijeen','zRecJYEntjV3WtCrGGjvuOJ2xPccHWZ4fTlOJurjWZM');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2013-07-27 19:29:13
