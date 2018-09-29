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
-- Table structure for table `match_info`
--

Drop table if exists `crawler_opgg`.`match_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `crawler_opgg`.`match_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `match_id` varchar(300) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `season` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `match_info`
--

LOCK TABLES `crawler_opgg`.`match_info` WRITE;
/*!40000 ALTER TABLE `crawler_opgg`.`match_info` DISABLE KEYS */;
INSERT INTO `crawler_opgg`.`match_info` VALUES (1,'Svg7Thpx__N3LAxphviehxEU16RTyT07LuYv1_7hewCtxbDuTKs3ZYXx-qtK0eQrDg_HP87G1QBMB9Bv7EBGFW9JMLdpUXy_JA0oFE0IkiDCis5oBykytzHJcqTajvESIQCHu-h2Isw=','2018-09-29 10:09:32','2018-09'),(2,'Svg7Thpx__N3LAxphvieh5pnXNvTgKsWnHBWjZavu7scNWw7wVzHQce_nTojN53-bPXOIkJPjtRYIg8SrXrkJYjI2JK6lVB9ebQfukirKQeGJL-xVCgp9TQaaW6RR5LjXU5z6ISLiUA=','2018-09-29 10:09:32','2018-09'),(3,'Svg7Thpx__N3LAxphvieh0Q9MqKuOoXWl-h_QCRMLiV6-zV5JaBet9FuSEhbDzITP56urCr9PtJZsdF3tTrvmmEbOVM3XhZc4teKAb2vFLrbLTOM0sPVWzETx5C3-XQFEMBgMSKTolY=','2018-09-29 10:09:32','2018-09'),(4,'Svg7Thpx__N3LAxphvieh5yWrfVF6gT7EwJABsFaDwKdFJUar0eOO_h1IEvzNJEl8pP5gM2LnpSqVYVlmBSkyGdNczHCEYI89i1NSbyiCNxHU4WQ_cY7BamWpV0NFl_4KuEJWTmgooc=','2018-09-29 10:09:32','2018-09'),(5,'Svg7Thpx__N3LAxphvieh2PfrITkBj2MK6DnBfTLHgxYJAuezkIfxbwXrtviNwk3n6ldS0tbeYws8cVe602o09ql1xXbHJCJF4r8KSxIaOkzMBuaPbz6X4z3hvMI1_UISTW82k4wOIA=','2018-09-29 10:09:32','2018-09'),(6,'Svg7Thpx__N3LAxphvieh8X70YmPtjChIGdzMl7OcRMHfsN_xu0Lcq7RbDfG2txa3U1NBv3zwaiNNz_kUYniRaPZd0uNHSb5-ySAd22Ond5GefsXvpX-x_iMHjMBdKMLbf270oAZs3w=','2018-09-29 10:09:32','2018-09'),(7,'Svg7Thpx__N3LAxphvieh9wV4R00L9-0odeq1OTDARsUbfFo5NCO22TxMjyp9E5dd3-5ELIRtVCpoXPo2TcFPbQaf8bFOIfxwWsSbraXWALQR8K0BC4RTyf_wtgVsuZ5aYKAymIjD9U=','2018-09-29 10:09:32','2018-09'),(8,'Svg7Thpx__N3LAxphvieh8EFcHhSfFBeDoyDrimSr3fcpW34e0NX3nxrbE7OeNMTWX1hnTYDs955Lfu7dfSA8Lw67Y2Ac1UzuqMrvRUUlBxFo9s_bxjl4W_I96GEa_R7NQhDtK-0xsY=','2018-09-29 10:09:32','2018-09'),(9,'Svg7Thpx__N3LAxphvieh5EgQo5Afzham3D10RnE56NkjVv4kJ7fWKNB7hr4nIn7Jt6zXpy8fJybi2Pp4PaxfychzfwgWYEFmtRwN02JPw4zbo01qnnVBn21FP6T2pmc244xtfbjTDE=','2018-09-29 10:09:32','2018-09'),(10,'Svg7Thpx__N3LAxphviehynSIrfNis60IR7ulT6V5ug3kNrwrO_TMaEB_dzmTRE1JpNKJ8V0RZkJyXWBtSV_zxAUvJIH4sBn2DwWf56UkLAbkcn1t-mRPYsHqdkadDzTE-IZ40mjyVk=','2018-09-29 10:09:32','2018-09'),(11,'Svg7Thpx__N3LAxphviehwG3KEaRIcQrCGQYTxDIzxCbMGfi-F7Pvr0aPH5tzchFMzP1K9xEPqAdKOc6t2Pp0WiN7Yif9jkN_erdKXtbZsOJ6TqrYy5d3i2VXXSif4JIQP4cMgJvQTU=','2018-09-29 10:09:32','2018-09'),(12,'Svg7Thpx__N3LAxphviehwdXSsHiQtupT8kPY12sWfftLa7WYkZFOHOw5uagMXtQMIrP4mQPJB5_jzKSK6sqKhhOMFj08_n7FbokVul-IqzsHl_0vrPQQOOpxVBM6tsoWo8fnhpHKpQ=','2018-09-29 10:09:32','2018-09'),(13,'Svg7Thpx__N3LAxphvieh8MAh1mYq-ys80QgH_Sli5c6fV7fW0Y6QAQ-FjkiXDXwEzFqZ3Yb8qGgr_kpbmFQjVMJOMDEo4wPPr_C4zJF5OiculTeZTWPLCOXGzCi8Mq4UOu-mMmLmOs=','2018-09-29 10:09:32','2018-09'),(14,'Svg7Thpx__N3LAxphviehydyBV__-P_pdh_cd-ej-KIBaoM7UERpKZUX5iN2fD7JHPWEHVYIk_HCGi8VSz_Pi-0GmYyGIxrxT1TxAlA8hrhqh22lXpQeYNYMdFmbrBORfVaQdivlOnM=','2018-09-29 10:09:32','2018-09'),(15,'Svg7Thpx__N3LAxphvieh8brqdMqECVS69iokqSkV7BBF8Ufd0hIfQ5EiqMymqf_PfcQa3Xct8YJRc8iOjV-YYdQbp8d7vtXMAIKJk2MEPMbJh40KF0fqBgJl7BgavwTM4JLFZQZrlg=','2018-09-29 10:09:32','2018-09'),(16,'Svg7Thpx__N3LAxphvieh_OZp3ilrDtw5qxL-6dVct89qAqpH9BYXmKr7Ws28yyXDmeTYL3rdYgibALKBNKl3QplyXjXemU3x0HYNQrhPVOZVXI4cDdSBho5huPLwN-NuL43csBTapY=','2018-09-29 10:09:32','2018-09'),(17,'Svg7Thpx__N3LAxphviehzQ9BeEuBHf5VWUNUCsiHJkzcQi1cg_wX90A3pLgGLh6_bd-pIp-UjpMO49JgBZwsVzTutPPhxzAeFT1TBdfTcBxsmeEk6hAjC0b8bNo957ugR0bS3d2QXs=','2018-09-29 10:09:32','2018-09'),(18,'Svg7Thpx__N3LAxphviehxCpavE4lw0GEDb2CHdzsp_Hp6tlrZzDcqEmp3tp5tc9kbUqLyYnYDy6jTZvprqovQ8aObkoV4IaJqocMb1T-OTQO6NyUxz_yo67HSfrVYnoFALyvrLFt7w=','2018-09-29 10:09:32','2018-09'),(19,'Svg7Thpx__N3LAxphvieh2tu1SSw6S_gG1AwatcwMxHI-VO345pigGqFPgyNYfab_eRHnEo_5RrQJi7vtdmKwSQ68sM_MdVEEdOyXXP8SVCEgnzcuJdo8LEiPcA2yNTLPSIyQfFyh5c=','2018-09-29 10:09:32','2018-09'),(20,'Svg7Thpx__N3LAxphvieh8eyeFu6IK_3wkjTeEQlGIp2LaWcGCTA4Nk-sXgULF1Do9gNJVVHZR-4BRPyEorZRlqnO9Inwi8xgxbc9E3xjmwc5cAmKGtFKp4K3bHXXPkfz5MpDdE4Tzs=','2018-09-29 10:09:32','2018-09');
/*!40000 ALTER TABLE `crawler_opgg`.`match_info` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-09-29 10:43:16
