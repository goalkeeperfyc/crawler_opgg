-- MySQL dump 10.13  Distrib 8.0.11, for Win64 (x86_64)
--
-- Host: localhost    Database: crawler_opgg
-- ------------------------------------------------------
-- Server version	8.0.11

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+08:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `user_performance`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8 ;
CREATE TABLE `crawler_opgg`.`user_performance` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_name` varchar(45)  DEFAULT NULL,
  `opgg_id` varchar(45)  DEFAULT NULL,
  `creat_time` DATETIME DEFAULT NULL,
  `solo_chicken` int(11) DEFAULT NULL,
  `solo_damage_per_match` float DEFAULT NULL,
  `solo_deaths_num` int(11) DEFAULT NULL,
  `solo_headshot_kills_sum` int(11) DEFAULT NULL,
  `solo_kills_max` int(11) DEFAULT NULL,
  `solo_kills_sum` int(11) DEFAULT NULL,
  `solo_play_times` int(11) DEFAULT NULL,
  `solo_rating` int(11) DEFAULT NULL,
  `solo_survived_second` float DEFAULT NULL,
  `double_chicken` int(11) DEFAULT NULL,
  `double_damage_per_match` float DEFAULT NULL,
  `double_deaths_num` int(11) DEFAULT NULL,
  `double_headshot_kills_sum` int(11) DEFAULT NULL,
  `double_kills_max` int(11) DEFAULT NULL,
  `double_kills_sum` int(11) DEFAULT NULL,
  `double_play_times` int(11) DEFAULT NULL,
  `double_rating` int(11) DEFAULT NULL,
  `double_survived_second` float DEFAULT NULL,
  `square_chicken` int(11) DEFAULT NULL,
  `square_damage_per_match` float DEFAULT NULL,
  `square_deaths_num` int(11) DEFAULT NULL,
  `square_headshot_kills_sum` int(11) DEFAULT NULL,
  `square_kills_max` int(11) DEFAULT NULL,
  `square_kills_sum` int(11) DEFAULT NULL,
  `square_play_times` int(11) DEFAULT NULL,
  `square_rating` int(11) DEFAULT NULL,
  `square_survived_second` float DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_performance`
--
