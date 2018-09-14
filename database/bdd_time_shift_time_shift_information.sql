-- MySQL dump 10.13  Distrib 8.0.11, for Win64 (x86_64)
--
-- Host: localhost    Database: bdd_time_shift
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
-- Table structure for table `time_shift_information`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8 ;
CREATE TABLE `time_shift`.`time_shift_information` (
  `id` int(11) NOT NULL,
  `first_play_program_id` int(11) DEFAULT NULL,
  `time_shift_id` int(11) DEFAULT NULL,
  `parallel_machine_information` varchar(45)  DEFAULT NULL,
  `create_time` varchar(45)  DEFAULT NULL,
  `update_time` varchar(45)  DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `un_shift_info` (`first_play_program_id`,`time_shift_id`),
  KEY `FK_ID_first` (`time_shift_id`),
  CONSTRAINT `FK_ID_first` FOREIGN KEY (`time_shift_id`) REFERENCES `all_program_information` (`program_id`),
  CONSTRAINT `FK_ID_shift` FOREIGN KEY (`first_play_program_id`) REFERENCES `all_program_information` (`program_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `time_shift_information`
--


