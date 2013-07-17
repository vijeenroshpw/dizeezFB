# ************************************************************
# Sequel Pro SQL dump
# Version 4096
#
# http://www.sequelpro.com/
# http://code.google.com/p/sequel-pro/
#
# Host: 127.0.0.1 (MySQL 5.5.27)
# Database: dizeez
# Generation Time: 2013-07-17 00:53:57 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table category
# ------------------------------------------------------------

DROP TABLE IF EXISTS `category`;

CREATE TABLE `category` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `text` varchar(240) DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table choice
# ------------------------------------------------------------

DROP TABLE IF EXISTS `choice`;

CREATE TABLE `choice` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `text` varchar(240) DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `choice` WRITE;
/*!40000 ALTER TABLE `choice` DISABLE KEYS */;

INSERT INTO `choice` (`id`, `text`, `created`)
VALUES
	(1,'AAAAA',NULL),
	(2,'BBBBBB',NULL),
	(3,'CCCCC',NULL),
	(4,'DDDDD',NULL),
	(5,'EEEEEEEEEE',NULL),
	(6,'F F F ',NULL);

/*!40000 ALTER TABLE `choice` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table qc_association
# ------------------------------------------------------------

DROP TABLE IF EXISTS `qc_association`;

CREATE TABLE `qc_association` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `question_id` int(11) DEFAULT NULL,
  `choice_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `question_id` (`question_id`),
  KEY `choice_id` (`choice_id`),
  CONSTRAINT `qc_association_ibfk_1` FOREIGN KEY (`question_id`) REFERENCES `question` (`id`),
  CONSTRAINT `qc_association_ibfk_2` FOREIGN KEY (`choice_id`) REFERENCES `choice` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `qc_association` WRITE;
/*!40000 ALTER TABLE `qc_association` DISABLE KEYS */;

INSERT INTO `qc_association` (`id`, `question_id`, `choice_id`)
VALUES
	(1,1,1),
	(2,1,2),
	(3,1,3),
	(4,1,4),
	(5,2,1),
	(6,2,2),
	(7,2,3),
	(8,2,4),
	(9,3,3),
	(10,3,4),
	(11,3,5),
	(12,3,6);

/*!40000 ALTER TABLE `qc_association` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table qcat_association
# ------------------------------------------------------------

DROP TABLE IF EXISTS `qcat_association`;

CREATE TABLE `qcat_association` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `category_id` int(11) DEFAULT NULL,
  `question_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `category_id` (`category_id`),
  KEY `question_id` (`question_id`),
  CONSTRAINT `qcat_association_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `category` (`id`),
  CONSTRAINT `qcat_association_ibfk_2` FOREIGN KEY (`question_id`) REFERENCES `question` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



# Dump of table question
# ------------------------------------------------------------

DROP TABLE IF EXISTS `question`;

CREATE TABLE `question` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `text` varchar(240) DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  `correct_choice_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

LOCK TABLES `question` WRITE;
/*!40000 ALTER TABLE `question` DISABLE KEYS */;

INSERT INTO `question` (`id`, `text`, `created`, `correct_choice_id`)
VALUES
	(1,'What is a good Question?',NULL,3),
	(2,'What is another good Question?',NULL,2),
	(3,'Let\'s mix it up!',NULL,6);

/*!40000 ALTER TABLE `question` ENABLE KEYS */;
UNLOCK TABLES;



/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
