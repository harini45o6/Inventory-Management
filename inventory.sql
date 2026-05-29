-- MySQL dump 10.13  Distrib 8.1.0, for macos13 (x86_64)
--
-- Host: localhost    Database: shopstock
-- ------------------------------------------------------
-- Server version	8.1.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `activity_log`
--

DROP TABLE IF EXISTS `activity_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `activity_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `sku` varchar(50) DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `action` varchar(50) DEFAULT NULL,
  `qty_change` int DEFAULT '0',
  `stock_before` int DEFAULT '0',
  `stock_after` int DEFAULT '0',
  `note` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=274 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `activity_log`
--

LOCK TABLES `activity_log` WRITE;
/*!40000 ALTER TABLE `activity_log` DISABLE KEYS */;
INSERT INTO `activity_log` VALUES (6,'2026-05-12 15:56:22','PRD003','LED Monitor 24 Inch','Restock IN',32,8,40,'Restocked by admin'),(7,'2026-05-12 16:55:52','PRD001','Wireless Mouse','Restock OUT',-5,25,20,'Stock removed by admin'),(8,'2026-05-12 16:56:08','PRD013','Women Handbag','Price Change',0,9,9,'Price changed by admin: 1299.00 -> 1000.00'),(9,'2026-05-12 16:56:23','PRD014','Sports Shoes','Price Change',0,14,14,'Price changed by admin: 2199.00 -> 1499.00'),(10,'2026-05-12 16:56:32','PRD017','Office File Folder','Restock OUT',-6,26,20,'Stock removed by admin'),(11,'2026-05-12 16:57:17','PRD003','LED Monitor 24 Inch','Restock OUT',-20,40,20,'Stock removed by admin'),(12,'2026-05-12 17:30:27','PRD021','Micro Fiber Towel','Add Item',25,0,25,'New item added by admin'),(13,'2026-05-12 17:44:26','PRD022','Salt 1kg','Add Item',50,0,50,'New item added by admin'),(14,'2026-05-13 10:42:22','PRD023','Cargo Jean','Add Item',25,0,25,'Added via supplier #11 by admin'),(15,'2026-05-13 15:51:39','PRD005','Basmati Rice 5KG','Sale OUT',-1,20,19,'Sale INV011 by admin'),(16,'2026-05-13 15:51:39','PRD022','Salt 1kg','Sale OUT',-1,50,49,'Sale INV011 by admin'),(17,'2026-05-13 15:51:39','PRD006','Sunflower Oil 1L','Sale OUT',-2,35,33,'Sale INV011 by admin'),(18,'2026-05-13 16:26:18','PRD010','Detergent Powder 2KG','Sale OUT',-2,17,15,'Sale INV012 by admin'),(19,'2026-05-13 16:26:18','PRD020','Knife Set','Sale OUT',-1,7,6,'Sale INV012 by admin'),(20,'2026-05-13 16:26:18','PRD021','Micro Fiber Towel','Sale OUT',-1,25,24,'Sale INV012 by admin'),(21,'2026-05-13 16:27:52','PRD005','Basmati Rice 5KG','Sale OUT',-1,19,18,'Sale INV013 by admin'),(22,'2026-05-13 16:27:52','PRD016','Blue Pen Pack','Sale OUT',-1,45,44,'Sale INV013 by admin'),(23,'2026-05-13 16:27:52','PRD012','Men T-Shirt','Sale OUT',-1,12,11,'Sale INV013 by admin'),(24,'2026-05-13 17:25:59','PRD001','Wireless Mouse','Restock IN',5,20,25,'Restocked by admin'),(25,'2026-05-13 17:26:13','PRD002','Mechanical Keyboard','Restock OUT',-5,15,10,'Stock removed by admin'),(26,'2026-05-13 17:26:42','PRD002','Mechanical Keyboard','Restock OUT',-7,10,3,'Stock removed by admin'),(27,'2026-05-13 17:26:53','PRD002','Mechanical Keyboard','Restock IN',7,3,10,'Restocked by admin'),(28,'2026-05-13 17:27:06','PRD002','Mechanical Keyboard','Restock IN',7,10,17,'Restocked by admin'),(29,'2026-05-13 17:30:17','PRD024','Keybroad','Add Item',15,0,15,'Added via supplier #12 by admin'),(30,'2026-05-15 10:56:01','PRD016','Blue Pen Pack','Sale OUT',-1,44,43,'Sale INV014 by admin'),(31,'2026-05-15 10:56:01','PRD024','Keybroad','Sale OUT',-1,15,14,'Sale INV014 by admin'),(32,'2026-05-15 11:42:34','PRD008','Toor Dal 1KG','Sale OUT',-1,18,17,'Sale INV015 by admin'),(33,'2026-05-15 11:42:34','PRD007','Sugar 1KG','Sale OUT',-1,40,39,'Sale INV015 by admin'),(34,'2026-05-15 12:04:41','PRD006','Sunflower Oil 1L','Sale OUT',-1,33,32,'Sale INV016 by admin'),(35,'2026-05-15 12:04:41','PRD022','Salt 1kg','Sale OUT',-1,49,48,'Sale INV016 by admin'),(36,'2026-05-15 12:04:41','PRD009','Floor Cleaner 1L','Sale OUT',-1,22,21,'Sale INV016 by admin'),(37,'2026-05-15 12:04:41','PRD010','Detergent Powder 2KG','Sale OUT',-1,15,14,'Sale INV016 by admin'),(38,'2026-05-15 12:22:06','PRD005','Basmati Rice 5KG','Sale OUT',-1,18,17,'Sale INV017 by admin'),(39,'2026-05-15 12:22:06','PRD006','Sunflower Oil 1L','Sale OUT',-2,32,30,'Sale INV017 by admin'),(40,'2026-05-15 12:22:06','PRD020','Knife Set','Sale OUT',-1,6,5,'Sale INV017 by admin'),(41,'2026-05-15 12:22:09','PRD005','Basmati Rice 5KG','Sale OUT',-1,17,16,'Sale INV018 by admin'),(42,'2026-05-15 12:22:09','PRD006','Sunflower Oil 1L','Sale OUT',-2,30,28,'Sale INV018 by admin'),(43,'2026-05-15 12:22:09','PRD020','Knife Set','Sale OUT',-1,5,4,'Sale INV018 by admin'),(44,'2026-05-15 12:23:27','PRD005','Basmati Rice 5KG','Sale OUT',-1,16,15,'Sale INV019 by admin'),(45,'2026-05-15 12:23:27','PRD006','Sunflower Oil 1L','Sale OUT',-2,28,26,'Sale INV019 by admin'),(46,'2026-05-15 12:23:27','PRD020','Knife Set','Sale OUT',-1,4,3,'Sale INV019 by admin'),(47,'2026-05-15 12:23:41','PRD005','Basmati Rice 5KG','Sale OUT',-1,15,14,'Sale INV020 by admin'),(48,'2026-05-15 12:23:41','PRD006','Sunflower Oil 1L','Sale OUT',-2,26,24,'Sale INV020 by admin'),(49,'2026-05-15 12:23:41','PRD020','Knife Set','Sale OUT',-1,3,2,'Sale INV020 by admin'),(50,'2026-05-15 12:32:09','PRD001','Wireless Mouse','Sale OUT',-1,25,24,'Sale INV018 by admin'),(51,'2026-05-15 12:32:09','PRD019','Non-stick Frying Pan','Sale OUT',-1,11,10,'Sale INV018 by admin'),(52,'2026-05-15 12:32:09','PRD021','Micro Fiber Towel','Sale OUT',-2,24,22,'Sale INV018 by admin'),(53,'2026-05-15 12:33:20','PRD020','Knife Set','Restock IN',15,2,17,'Restocked by admin'),(54,'2026-05-15 16:47:38','PRD015','Notebook A4','Sale OUT',-1,50,49,'Sale INV019 by admin'),(55,'2026-05-15 16:47:38','PRD018','Steel Water Bottle','Sale OUT',-1,19,18,'Sale INV019 by admin'),(56,'2026-05-15 16:47:38','PRD020','Knife Set','Sale OUT',-1,17,16,'Sale INV019 by admin'),(57,'2026-05-16 13:00:40','PRD007','Sugar 1KG','Restock OUT',-9,39,30,'Stock removed by admin'),(58,'2026-05-16 13:00:58','PRD008','Toor Dal 1KG','Restock IN',8,17,25,'Restocked by admin'),(59,'2026-05-16 13:04:48','PRD003','LED Monitor 24 Inch','Sale OUT',-1,20,19,'Sale INV020 by admin'),(60,'2026-05-16 13:04:48','PRD002','Mechanical Keyboard','Sale OUT',-1,17,16,'Sale INV020 by admin'),(61,'2026-05-19 10:47:08','PRD008','Toor Dal 1KG','Refund IN',1,25,26,'Refund of INV015 by admin'),(62,'2026-05-19 10:47:08','PRD007','Sugar 1KG','Refund IN',1,30,31,'Refund of INV015 by admin'),(63,'2026-05-19 10:47:25','PRD006','Sunflower Oil 1L','Refund IN',1,24,25,'Refund of INV016 by admin'),(64,'2026-05-19 10:47:25','PRD022','Salt 1kg','Refund IN',1,48,49,'Refund of INV016 by admin'),(65,'2026-05-19 10:47:25','PRD009','Floor Cleaner 1L','Refund IN',1,21,22,'Refund of INV016 by admin'),(66,'2026-05-19 10:47:25','PRD010','Detergent Powder 2KG','Refund IN',1,14,15,'Refund of INV016 by admin'),(67,'2026-05-19 10:56:21','PRD015','Notebook A4','Refund IN',3,49,52,'Refund of INV006 by admin'),(68,'2026-05-19 10:56:21','PRD016','Blue Pen Pack','Refund IN',2,43,45,'Refund of INV006 by admin'),(69,'2026-05-19 11:17:35','PRD001','Wireless Mouse','Restock IN',5,24,29,'Restocked by admin'),(70,'2026-05-19 11:18:02','PRD002','Mechanical Keyboard','Price Change',0,16,16,'Price changed by admin: 2499.00 -> 2000.00'),(71,'2026-05-19 11:18:12','PRD003','LED Monitor 24 Inch','Delete',0,19,0,'Product deleted by admin'),(72,'2026-05-19 11:19:15','PRD025','Wireles Speaker','Add Item',15,0,15,'New item added by admin'),(73,'2026-05-19 11:21:42','PRD001','Wireless Mouse','Refund IN',1,29,30,'Refund of INV018 by admin'),(74,'2026-05-19 11:21:42','PRD019','Non-stick Frying Pan','Refund IN',1,10,11,'Refund of INV018 by admin'),(75,'2026-05-19 11:21:42','PRD021','Micro Fiber Towel','Refund IN',2,22,24,'Refund of INV018 by admin'),(76,'2026-05-19 13:14:30','PRD002','Mechanical Keyboard','Refund IN',1,16,17,'Refund of INV020 by admin'),(77,'2026-05-19 13:28:14','PRD016','Blue Pen Pack','Refund IN',1,45,46,'Refund of INV014 by admin'),(78,'2026-05-19 13:28:14','PRD024','Keybroad','Refund IN',1,14,15,'Refund of INV014 by admin'),(79,'2026-05-19 13:28:30','PRD015','Notebook A4','Refund IN',1,52,53,'Refund of INV019 by admin'),(80,'2026-05-19 13:28:30','PRD018','Steel Water Bottle','Refund IN',1,18,19,'Refund of INV019 by admin'),(81,'2026-05-19 13:28:30','PRD020','Knife Set','Refund IN',1,16,17,'Refund of INV019 by admin'),(82,'2026-05-19 13:38:16','PRD026','Mango Juice 1L','Add Item',60,0,60,'New item added by admin'),(83,'2026-05-19 13:38:16','PRD027','Cold Coffee Tetra 200ml','Add Item',90,0,90,'New item added by admin'),(84,'2026-05-19 13:38:16','PRD028','Mineral Water 1L Pack','Add Item',120,0,120,'New item added by admin'),(85,'2026-05-19 13:38:16','PRD029','Green Tea Box 25 Bags','Add Item',40,0,40,'New item added by admin'),(86,'2026-05-19 13:38:16','PRD030','Potato Chips 150g','Add Item',75,0,75,'New item added by admin'),(87,'2026-05-19 13:38:16','PRD031','Biscuit Pack Assorted','Add Item',65,0,65,'New item added by admin'),(88,'2026-05-19 13:38:16','PRD032','Roasted Peanuts 250g','Add Item',50,0,50,'New item added by admin'),(89,'2026-05-19 13:38:16','PRD033','Namkeen Mix 200g','Add Item',55,0,55,'New item added by admin'),(90,'2026-05-19 13:38:16','PRD034','Full Cream Milk 500ml','Add Item',80,0,80,'New item added by admin'),(91,'2026-05-19 13:38:16','PRD035','Curd 400g','Add Item',70,0,70,'New item added by admin'),(92,'2026-05-19 13:38:16','PRD036','Paneer 200g','Add Item',35,0,35,'New item added by admin'),(93,'2026-05-19 13:38:16','PRD037','Butter 100g','Add Item',45,0,45,'New item added by admin'),(94,'2026-05-19 13:38:16','PRD038','Baby Diapers Pack of 20','Add Item',30,0,30,'New item added by admin'),(95,'2026-05-19 13:38:16','PRD039','Baby Shampoo 200ml','Add Item',25,0,25,'New item added by admin'),(96,'2026-05-19 13:38:16','PRD040','Baby Powder 300g','Add Item',28,0,28,'New item added by admin'),(97,'2026-05-19 13:38:16','PRD041','Baby Wipes 80 Sheets','Add Item',35,0,35,'New item added by admin'),(98,'2026-05-19 13:38:16','PRD042','Shampoo 400ml','Add Item',40,0,40,'New item added by admin'),(99,'2026-05-19 13:38:16','PRD043','Conditioner 200ml','Add Item',35,0,35,'New item added by admin'),(100,'2026-05-19 13:38:16','PRD044','Face Wash 100ml','Add Item',42,0,42,'New item added by admin'),(101,'2026-05-19 13:38:16','PRD045','Toothpaste 150g','Add Item',60,0,60,'New item added by admin'),(102,'2026-05-19 13:38:16','PRD046','Paracetamol 500mg Strip','Add Item',80,0,80,'New item added by admin'),(103,'2026-05-19 13:38:16','PRD047','Antacid Syrup 170ml','Add Item',40,0,40,'New item added by admin'),(104,'2026-05-19 13:38:16','PRD048','Vitamin C Tablets 10s','Add Item',55,0,55,'New item added by admin'),(105,'2026-05-19 13:38:16','PRD049','Bandage Roll 5m','Add Item',45,0,45,'New item added by admin'),(106,'2026-05-19 13:38:16','PRD050','Frozen Peas 500g','Add Item',30,0,30,'New item added by admin'),(107,'2026-05-19 13:38:16','PRD051','Frozen Corn 500g','Add Item',28,0,28,'New item added by admin'),(108,'2026-05-19 13:38:16','PRD052','Frozen French Fries 1kg','Add Item',20,0,20,'New item added by admin'),(109,'2026-05-19 13:38:16','PRD053','Ice Cream Vanilla 500ml','Add Item',22,0,22,'New item added by admin'),(110,'2026-05-19 13:38:16','PRD054','White Bread Loaf','Add Item',40,0,40,'New item added by admin'),(111,'2026-05-19 13:38:16','PRD055','Brown Bread Loaf','Add Item',35,0,35,'New item added by admin'),(112,'2026-05-19 13:38:16','PRD056','Croissant Pack of 4','Add Item',20,0,20,'New item added by admin'),(113,'2026-05-19 13:38:16','PRD057','Pav Bun Pack of 6','Add Item',45,0,45,'New item added by admin'),(116,'2026-05-19 13:38:16','PRD058','Organic Chia Seeds 500g','+ NEW',40,0,40,'New item added by admin'),(117,'2026-05-19 13:38:16','PRD059','Ergonomic Wireless Keyboard','+ NEW',15,0,15,'New item added by admin'),(118,'2026-05-21 10:20:35','PRD050','Frozen Peas 500g','Refund IN',1,30,31,'Refund of INV025 by admin'),(119,'2026-05-21 10:20:35','PRD051','Frozen Corn 500g','Refund IN',1,28,29,'Refund of INV025 by admin'),(120,'2026-05-21 10:20:35','PRD053','Ice Cream Vanilla 500ml','Refund IN',2,22,24,'Refund of INV025 by admin'),(121,'2026-05-21 10:20:35','PRD054','White Bread Loaf','Refund IN',1,40,41,'Refund of INV025 by admin'),(122,'2026-05-21 10:20:35','PRD057','Pav Bun Pack of 6','Refund IN',1,45,46,'Refund of INV025 by admin'),(123,'2026-05-21 10:20:55','PRD046','Paracetamol 500mg Strip','Refund IN',2,80,82,'Refund of INV024 by admin'),(124,'2026-05-21 10:20:55','PRD047','Antacid Syrup 170ml','Refund IN',1,40,41,'Refund of INV024 by admin'),(125,'2026-05-21 10:20:55','PRD048','Vitamin C Tablets 10s','Refund IN',2,55,57,'Refund of INV024 by admin'),(126,'2026-05-21 10:20:55','PRD049','Bandage Roll 5m','Refund IN',2,45,47,'Refund of INV024 by admin'),(127,'2026-05-21 10:24:33','PRD054','White Bread Loaf','Refund IN',2,41,43,'Refund of INV022 by admin'),(128,'2026-05-21 10:24:33','PRD034','Full Cream Milk 500ml','Refund IN',3,80,83,'Refund of INV022 by admin'),(129,'2026-05-21 10:24:33','PRD035','Curd 400g','Refund IN',2,70,72,'Refund of INV022 by admin'),(130,'2026-05-21 10:24:33','PRD057','Pav Bun Pack of 6','Refund IN',1,46,47,'Refund of INV022 by admin'),(131,'2026-05-21 10:33:45','PRD058','Organic Chia Seeds 500g','Restock OUT',-20,40,20,'Stock removed by admin'),(133,'2026-05-21 10:36:46','PRD013','Women Handbag','Sale OUT',-2,9,7,'Sale INV028 by admin'),(135,'2026-05-21 10:36:46','PRD039','Baby Shampoo 200ml','Sale OUT',-1,25,24,'Sale INV028 by admin'),(137,'2026-05-21 10:36:46','PRD055','Brown Bread Loaf','Sale OUT',-1,35,34,'Sale INV028 by admin'),(139,'2026-05-25 11:32:32','PRD035','Curd 400g','Sale OUT',-1,72,71,'Sale INV029 by cashier1'),(141,'2026-05-25 11:32:32','PRD040','Baby Powder 300g','Sale OUT',-10,28,18,'Sale INV029 by cashier1'),(143,'2026-05-25 11:32:32','PRD020','Knife Set','Sale OUT',-2,17,15,'Sale INV029 by cashier1'),(145,'2026-05-25 12:40:13','PRD015','Notebook A4','Sale OUT',-1,53,52,'Sale INV030 by cashier1'),(147,'2026-05-25 12:40:13','PRD011','Bathroom Brush','Sale OUT',-1,28,27,'Sale INV030 by cashier1'),(149,'2026-05-25 12:40:13','PRD022','Salt 1kg','Sale OUT',-1,49,48,'Sale INV030 by cashier1'),(151,'2026-05-25 12:40:13','PRD001','Wireless Mouse','Sale OUT',-1,30,29,'Sale INV030 by cashier1'),(153,'2026-05-25 12:40:13','PRD014','Sports Shoes','Sale OUT',-1,14,13,'Sale INV030 by cashier1'),(155,'2026-05-25 14:52:20','PRD058','Organic Chia Seeds 500g','Sale OUT',-1,20,19,'Sale INV031 by cashier1'),(157,'2026-05-25 14:52:20','PRD006','Sunflower Oil 1L','Sale OUT',-1,25,24,'Sale INV031 by cashier1'),(159,'2026-05-25 14:52:20','PRD035','Curd 400g','Sale OUT',-1,71,70,'Sale INV031 by cashier1'),(161,'2026-05-25 14:52:20','PRD036','Paneer 200g','Sale OUT',-1,35,34,'Sale INV031 by cashier1'),(163,'2026-05-25 14:52:20','PRD055','Brown Bread Loaf','Sale OUT',-1,34,33,'Sale INV031 by cashier1'),(165,'2026-05-25 14:52:20','PRD044','Face Wash 100ml','Sale OUT',-1,42,41,'Sale INV031 by cashier1'),(167,'2026-05-25 15:32:38','PRD052','Frozen French Fries 1kg','Sale OUT',-1,20,19,'Sale INV032 by cashier1'),(169,'2026-05-25 15:32:39','PRD053','Ice Cream Vanilla 500ml','Sale OUT',-1,24,23,'Sale INV032 by cashier1'),(171,'2026-05-25 15:32:39','PRD009','Floor Cleaner 1L','Sale OUT',-1,22,21,'Sale INV032 by cashier1'),(173,'2026-05-25 15:32:39','PRD019','Non-stick Frying Pan','Sale OUT',-1,11,10,'Sale INV032 by cashier1'),(174,'2026-05-25 15:41:45','PRD057','Pav Bun Pack of 6','Restock OUT',-7,47,40,'Stock removed by admin'),(176,'2026-05-25 15:43:08','PRD037','Butter 100g','Sale OUT',-1,45,44,'Sale INV033 by cashier1'),(178,'2026-05-25 15:43:08','PRD050','Frozen Peas 500g','Sale OUT',-1,31,30,'Sale INV033 by cashier1'),(180,'2026-05-25 15:43:08','PRD043','Conditioner 200ml','Sale OUT',-1,35,34,'Sale INV033 by cashier1'),(182,'2026-05-25 15:43:08','PRD047','Antacid Syrup 170ml','Sale OUT',-1,41,40,'Sale INV033 by cashier1'),(184,'2026-05-25 15:43:08','PRD016','Blue Pen Pack','Sale OUT',-1,46,45,'Sale INV033 by cashier1'),(186,'2026-05-25 15:48:39','PRD045','Toothpaste 150g','Sale OUT',-1,60,59,'Sale INV034 by cashier1'),(188,'2026-05-25 15:48:39','PRD042','Shampoo 400ml','Sale OUT',-1,40,39,'Sale INV034 by cashier1'),(190,'2026-05-25 15:48:39','PRD011','Bathroom Brush','Sale OUT',-1,27,26,'Sale INV034 by cashier1'),(192,'2026-05-25 15:48:39','PRD013','Women Handbag','Sale OUT',-1,7,6,'Sale INV034 by cashier1'),(194,'2026-05-25 15:48:39','PRD012','Men T-Shirt','Sale OUT',-1,11,10,'Sale INV034 by cashier1'),(196,'2026-05-25 15:50:30','PRD037','Butter 100g','Sale OUT',-2,44,42,'Sale INV035 by cashier1'),(197,'2026-05-25 15:53:26','PRD035','Curd 400g','Sale OUT',-2,70,68,'Sale INV036 by cashier1'),(198,'2026-05-25 15:53:26','PRD034','Full Cream Milk 500ml','Sale OUT',-1,83,82,'Sale INV036 by cashier1'),(199,'2026-05-26 10:50:24','PRD021','Micro Fiber Towel','Sale OUT',-1,24,23,'Sale INV037 by cashier1'),(200,'2026-05-26 10:50:24','PRD023','Cargo Jean','Sale OUT',-1,25,24,'Sale INV037 by cashier1'),(201,'2026-05-26 10:50:24','PRD024','Keybroad','Sale OUT',-1,15,14,'Sale INV037 by cashier1'),(202,'2026-05-26 11:06:15','PRD056','Croissant Pack of 4','Sale OUT',-1,20,19,'Sale INV038 by cashier1'),(203,'2026-05-26 11:06:15','PRD036','Paneer 200g','Sale OUT',-1,34,33,'Sale INV038 by cashier1'),(204,'2026-05-26 11:06:15','PRD053','Ice Cream Vanilla 500ml','Sale OUT',-1,23,22,'Sale INV038 by cashier1'),(205,'2026-05-26 11:06:15','PRD058','Organic Chia Seeds 500g','Sale OUT',-1,19,18,'Sale INV038 by cashier1'),(206,'2026-05-26 11:06:15','PRD006','Sunflower Oil 1L','Sale OUT',-1,24,23,'Sale INV038 by cashier1'),(207,'2026-05-26 11:06:44','PRD007','Sugar 1KG','Sale OUT',-1,31,30,'Sale INV039 by cashier1'),(208,'2026-05-26 11:06:44','PRD008','Toor Dal 1KG','Sale OUT',-1,26,25,'Sale INV039 by cashier1'),(209,'2026-05-26 11:06:44','PRD045','Toothpaste 150g','Sale OUT',-1,59,58,'Sale INV039 by cashier1'),(210,'2026-05-26 11:08:18','PRD057','Pav Bun Pack of 6','Sale OUT',-2,40,38,'Sale INV040 by cashier1'),(211,'2026-05-26 11:08:18','PRD037','Butter 100g','Sale OUT',-1,42,41,'Sale INV040 by cashier1'),(212,'2026-05-26 12:06:36','PRD059','Ergonomic Wireless Keyboard','Sale OUT',-2,15,13,'Sale INV041 by cashier1'),(213,'2026-05-26 12:06:36','PRD018','Steel Water Bottle','Sale OUT',-1,19,18,'Sale INV041 by cashier1'),(214,'2026-05-26 12:12:54','PRD041','Baby Wipes 80 Sheets','Sale OUT',-1,35,34,'Sale INV042 by cashier1'),(215,'2026-05-26 12:12:54','PRD039','Baby Shampoo 200ml','Sale OUT',-1,24,23,'Sale INV042 by cashier1'),(216,'2026-05-26 12:12:54','PRD010','Detergent Powder 2KG','Sale OUT',-1,15,14,'Sale INV042 by cashier1'),(217,'2026-05-26 12:13:50','PRD056','Croissant Pack of 4','Sale OUT',-1,19,18,'Sale INV043 by cashier1'),(218,'2026-05-26 12:13:50','PRD001','Wireless Mouse','Sale OUT',-1,29,28,'Sale INV043 by cashier1'),(219,'2026-05-26 12:25:09','PRD039','Baby Shampoo 200ml','Sale OUT',-1,23,22,'Sale INV044 by cashier1'),(220,'2026-05-26 12:25:09','PRD037','Butter 100g','Sale OUT',-1,41,40,'Sale INV044 by cashier1'),(221,'2026-05-26 12:25:09','PRD005','Basmati Rice 5KG','Sale OUT',-1,14,13,'Sale INV044 by cashier1'),(222,'2026-05-26 12:25:09','PRD013','Women Handbag','Sale OUT',-1,6,5,'Sale INV044 by cashier1'),(223,'2026-05-26 12:25:09','PRD008','Toor Dal 1KG','Sale OUT',-1,25,24,'Sale INV044 by cashier1'),(224,'2026-05-26 12:28:33','PRD056','Croissant Pack of 4','Refund IN',1,18,19,'Refund of INV043 by cashier1'),(225,'2026-05-26 12:28:33','PRD001','Wireless Mouse','Refund IN',1,28,29,'Refund of INV043 by cashier1'),(226,'2026-05-26 12:38:54','PRD034','Full Cream Milk 500ml','Sale OUT',-1,82,81,'Sale INV045 by cashier1'),(227,'2026-05-26 12:38:54','PRD059','Ergonomic Wireless Keyboard','Sale OUT',-1,13,12,'Sale INV045 by cashier1'),(228,'2026-05-26 13:03:49','PRD058','Organic Chia Seeds 500g','Restock IN',5,18,23,'Restocked by admin'),(229,'2026-05-26 13:03:59','PRD059','Wireless Keyboard','Restock OUT',-2,12,10,'Stock removed by admin'),(230,'2026-05-26 13:08:17','PRD035','Curd 400g','Sale OUT',-1,68,67,'Sale INV046 by cashier1'),(231,'2026-05-26 13:08:17','PRD024','Keybroad','Sale OUT',-1,14,13,'Sale INV046 by cashier1'),(232,'2026-05-26 13:08:17','PRD025','Wireless Speaker','Sale OUT',-1,15,14,'Sale INV046 by cashier1'),(233,'2026-05-27 11:10:16','PRD055','Brown Bread Loaf','Sale OUT',-1,33,32,'Sale INV047 by cashier2'),(234,'2026-05-27 11:10:16','PRD054','White Bread Loaf','Sale OUT',-1,43,42,'Sale INV047 by cashier2'),(235,'2026-05-27 11:11:01','PRD059','Wireless Keyboard','Sale OUT',-1,10,9,'Sale INV048 by cashier1'),(236,'2026-05-27 11:11:01','PRD023','Cargo Jean','Sale OUT',-1,24,23,'Sale INV048 by cashier1'),(237,'2026-05-27 11:11:01','PRD012','Men T-Shirt','Sale OUT',-1,10,9,'Sale INV048 by cashier1'),(238,'2026-05-27 11:25:46','PRD006','Sunflower Oil 1L','Sale OUT',-1,23,22,'Sale INV049 by cashier1'),(239,'2026-05-27 11:25:46','PRD018','Steel Water Bottle','Sale OUT',-5,18,13,'Sale INV049 by cashier1'),(240,'2026-05-27 11:25:46','PRD046','Paracetamol 500mg Strip','Sale OUT',-1,82,81,'Sale INV049 by cashier1'),(241,'2026-05-27 11:25:46','PRD049','Bandage Roll 5m','Sale OUT',-2,47,45,'Sale INV049 by cashier1'),(242,'2026-05-27 11:25:46','PRD051','Frozen Corn 500g','Sale OUT',-1,29,28,'Sale INV049 by cashier1'),(243,'2026-05-27 11:26:35','PRD010','Detergent Powder 2KG','Sale OUT',-1,14,13,'Sale INV050 by cashier1'),(244,'2026-05-27 11:26:35','PRD021','Micro Fiber Towel','Sale OUT',-1,23,22,'Sale INV050 by cashier1'),(245,'2026-05-27 11:26:35','PRD009','Floor Cleaner 1L','Sale OUT',-1,21,20,'Sale INV050 by cashier1'),(246,'2026-05-27 11:26:35','PRD024','Keybroad','Sale OUT',-1,13,12,'Sale INV050 by cashier1'),(247,'2026-05-27 11:26:35','PRD014','Sports Shoes','Sale OUT',-1,13,12,'Sale INV050 by cashier1'),(248,'2026-05-27 11:29:04','PRD035','Curd 400g','Sale OUT',-2,67,65,'Sale INV051 by cashier2'),(249,'2026-05-27 11:29:04','PRD036','Paneer 200g','Sale OUT',-1,33,32,'Sale INV051 by cashier2'),(250,'2026-05-27 11:29:04','PRD043','Conditioner 200ml','Sale OUT',-1,34,33,'Sale INV051 by cashier2'),(251,'2026-05-27 11:29:04','PRD045','Toothpaste 150g','Sale OUT',-2,58,56,'Sale INV051 by cashier2'),(252,'2026-05-27 12:46:35','PRD021','Micro Fiber Towel','Sale OUT',-1,22,21,'Sale INV052 by cashier1'),(253,'2026-05-27 12:46:35','PRD054','White Bread Loaf','Sale OUT',-1,42,41,'Sale INV052 by cashier1'),(254,'2026-05-27 12:46:36','PRD019','Non-stick Frying Pan','Sale OUT',-1,10,9,'Sale INV053 by cashier2'),(255,'2026-05-27 12:46:36','PRD047','Antacid Syrup 170ml','Sale OUT',-1,40,39,'Sale INV053 by cashier2'),(256,'2026-05-28 14:29:49','PRD055','Brown Bread Loaf','stock_in',10,32,42,'Supplier purchase: 18'),(257,'2026-05-28 14:29:49','PRD051','Frozen Corn 500g','stock_in',10,28,38,'Supplier purchase: 18'),(258,'2026-05-28 14:57:34','PRD013','Women Handbag','Restock IN',15,5,20,'Restocked by admin'),(259,'2026-05-28 14:58:43','PRD018','Steel Water Bottle','Restock IN',12,13,25,'Restocked by admin'),(260,'2026-05-28 15:00:55','PRD024','Keybroad','Restock IN',10,12,22,'Restocked by admin'),(261,'2026-05-28 15:21:18','PRD046','Paracetamol 500mg Strip','Restock OUT',-25,81,56,'Stock removed by admin'),(262,'2026-05-28 15:22:34','PRD039','Baby Shampoo 200ml','Restock OUT',-15,22,7,'Stock removed by admin'),(263,'2026-05-28 15:22:52','PRD020','Knife Set','Restock OUT',-10,15,5,'Stock removed by admin'),(264,'2026-05-28 15:23:52','PRD035','Curd 400g','Sale OUT',-1,65,64,'Sale INV054 by cashier2'),(265,'2026-05-28 15:23:52','PRD036','Paneer 200g','Sale OUT',-1,32,31,'Sale INV054 by cashier2'),(266,'2026-05-28 15:23:52','PRD012','Men T-Shirt','Sale OUT',-1,9,8,'Sale INV054 by cashier2'),(267,'2026-05-28 15:23:52','PRD050','Frozen Peas 500g','Sale OUT',-1,30,29,'Sale INV054 by cashier2'),(268,'2026-05-28 15:24:18','PRD050','Frozen Peas 500g','Sale OUT',-2,29,27,'Sale INV055 by cashier2'),(269,'2026-05-28 15:24:18','PRD053','Ice Cream Vanilla 500ml','Sale OUT',-1,22,21,'Sale INV055 by cashier2'),(270,'2026-05-28 15:24:18','PRD039','Baby Shampoo 200ml','Sale OUT',-1,7,6,'Sale INV055 by cashier2'),(271,'2026-05-29 10:30:18','PRD039','Baby Shampoo 200ml','Restock IN',15,6,21,'Restocked by admin'),(272,'2026-05-29 10:30:40','PRD020','Knife Set','Restock IN',15,5,20,'Restocked by admin'),(273,'2026-05-29 10:30:56','PRD057','Pav Bun Pack of 6','Restock OUT',-8,38,30,'Stock removed by admin');
/*!40000 ALTER TABLE `activity_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cashier_alerts`
--

DROP TABLE IF EXISTS `cashier_alerts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cashier_alerts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `cashier_id` int NOT NULL,
  `cashier_name` varchar(100) NOT NULL,
  `sku` varchar(50) DEFAULT NULL,
  `product_name` varchar(200) DEFAULT NULL,
  `current_stock` int DEFAULT '0',
  `message` text NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `dismissed` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `idx_dismissed` (`dismissed`),
  KEY `idx_cashier` (`cashier_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cashier_alerts`
--

LOCK TABLES `cashier_alerts` WRITE;
/*!40000 ALTER TABLE `cashier_alerts` DISABLE KEYS */;
INSERT INTO `cashier_alerts` VALUES (1,2,'cashier1','PRD013','Women Handbag',5,'Women Handbag is running low – only 5 units left. Please restock!','2026-05-28 14:54:15',1),(2,3,'cashier2','PRD039','Baby Shampoo 200ml',6,'Baby Shampoo 200ml is running low – only 6 units left. Please restock!','2026-05-28 15:25:02',1),(3,2,'cashier1','PRD039','Baby Shampoo 200ml',6,'Baby Shampoo 200ml is running low – only 6 units left. Please restock!','2026-05-28 17:02:15',1),(4,2,'cashier1','PRD020','Knife Set',5,'Knife Set is running low – only 5 units left. Please restock!','2026-05-28 17:02:20',1);
/*!40000 ALTER TABLE `cashier_alerts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customers`
--

DROP TABLE IF EXISTS `customers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customers`
--

LOCK TABLES `customers` WRITE;
/*!40000 ALTER TABLE `customers` DISABLE KEYS */;
INSERT INTO `customers` VALUES (1,'Ravi Kumar','9876543210','ravi@gmail.com','2026-05-13 16:11:13'),(2,'Priya Sharma','9876543211','priya@gmail.com','2026-05-13 16:11:13'),(3,'Arun Vel','9876543212','arun@gmail.com','2026-05-13 16:11:13'),(4,'Meena Devi','9876543213','meena@gmail.com','2026-05-13 16:11:13'),(5,'Karthik R','9876543214','karthik@gmail.com','2026-05-13 16:11:13'),(6,'Lakshmi S','9876543215','lakshmi@gmail.com','2026-05-13 16:11:13'),(7,'Suresh P','9876543216','suresh@gmail.com','2026-05-13 16:11:13'),(8,'Divya N','9876543217','divya@gmail.com','2026-05-13 16:11:13'),(9,'Vijay M','9876543218','vijay@gmail.com','2026-05-13 16:11:13'),(10,'Anitha B','9876543219','anitha@gmail.com','2026-05-13 16:11:13'),(11,'Harini','9876543220','harini@gmail.com','2026-05-13 16:11:13'),(12,'Akash','9876543221','akash12@gmail.com','2026-05-15 12:04:41'),(13,'Vidhun','9677986223','Vidhun28@gmail.com','2026-05-15 12:22:06'),(17,'Pavithra','9841066262','Pavi142gmail.com','2026-05-15 16:47:38'),(18,'Leo','9876543210','thadaladiboyz@gmail.com','2026-05-16 13:04:48'),(19,'Sneha Pillai','9845001122','sneha.pillai@gmail.com','2026-05-19 13:38:14'),(20,'Arjun Das','9756112233','arjun.das@gmail.com','2026-05-19 13:38:14'),(21,'Meera Iyer','9967223344','meera.iyer@gmail.com','2026-05-19 13:38:14'),(22,'Rahul Verma','9878334455','rahul.verma@gmail.com','2026-05-19 13:38:14'),(23,'Ananya Krishnan','9989445566','ananya.k@gmail.com','2026-05-19 13:38:14'),(24,'Ravi Kumar','9841022262',NULL,'2026-05-25 12:40:13'),(25,'Harini','9677986223',NULL,'2026-05-25 14:52:20'),(26,'Vimal','9444195982',NULL,'2026-05-25 15:32:38'),(27,'Sara','7986399647',NULL,'2026-05-25 15:43:08'),(28,'Neha','8976543211',NULL,'2026-05-25 15:48:39'),(29,'sha','9807623456',NULL,'2026-05-25 15:50:30'),(30,'Ravi','7862102705',NULL,'2026-05-25 15:53:26'),(31,'Isha','8763262354',NULL,'2026-05-26 10:50:24'),(32,'harini','9677986223',NULL,'2026-05-26 12:12:54'),(33,'sha','983765421',NULL,'2026-05-26 12:13:50'),(34,'Ravi','9876543210',NULL,'2026-05-26 12:38:54'),(35,'ravi',NULL,NULL,'2026-05-26 13:08:17'),(36,'Harini','9677986223',NULL,'2026-05-27 11:10:16'),(37,'Ravi','9876543210',NULL,'2026-05-27 11:11:01'),(38,'sha',NULL,NULL,'2026-05-27 11:29:04'),(39,'shri',NULL,NULL,'2026-05-27 12:46:34'),(40,'walter',NULL,NULL,'2026-05-27 12:46:36'),(41,'Rajan','9876543122',NULL,'2026-05-28 15:23:52');
/*!40000 ALTER TABLE `customers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `finance_settings`
--

DROP TABLE IF EXISTS `finance_settings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `finance_settings` (
  `id` int NOT NULL AUTO_INCREMENT,
  `setting_key` varchar(100) NOT NULL,
  `setting_value` decimal(15,2) NOT NULL DEFAULT '0.00',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `setting_key` (`setting_key`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `finance_settings`
--

LOCK TABLES `finance_settings` WRITE;
/*!40000 ALTER TABLE `finance_settings` DISABLE KEYS */;
INSERT INTO `finance_settings` VALUES (1,'initial_capital',100000.00,'2026-05-29 11:20:51');
/*!40000 ALTER TABLE `finance_settings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products` (
  `sku` varchar(20) NOT NULL,
  `name` varchar(200) NOT NULL,
  `category` varchar(100) NOT NULL DEFAULT 'General',
  `price` decimal(10,2) NOT NULL DEFAULT '0.00',
  `stock` int NOT NULL DEFAULT '10',
  `low_stock_alert` int NOT NULL DEFAULT '10',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `supplier_id` int DEFAULT NULL,
  `supplier_cost` decimal(10,2) DEFAULT '0.00',
  PRIMARY KEY (`sku`),
  KEY `fk_supplier` (`supplier_id`),
  CONSTRAINT `fk_supplier` FOREIGN KEY (`supplier_id`) REFERENCES `suppliers` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES ('PRD001','Wireless Mouse','Electronics',599.00,29,10,'2026-05-12 15:38:25','2026-05-26 12:28:33',2,0.00),('PRD002','Mechanical Keyboard','Electronics',2000.00,17,10,'2026-05-12 15:38:25','2026-05-19 13:14:30',2,0.00),('PRD004','USB Pendrive 64GB','Electronics',699.00,30,10,'2026-05-12 15:38:25','2026-05-12 15:38:25',2,0.00),('PRD005','Basmati Rice 5KG','Grocery',650.00,13,10,'2026-05-12 15:38:25','2026-05-26 12:25:09',3,0.00),('PRD006','Sunflower Oil 1L','Grocery',180.00,22,10,'2026-05-12 15:38:25','2026-05-27 11:25:46',3,0.00),('PRD007','Sugar 1KG','Grocery',48.00,30,10,'2026-05-12 15:38:25','2026-05-26 11:06:44',7,0.00),('PRD008','Toor Dal 1KG','Grocery',145.00,24,10,'2026-05-12 15:38:25','2026-05-26 12:25:09',3,0.00),('PRD009','Floor Cleaner 1L','Home Essentials',120.00,20,10,'2026-05-12 15:38:25','2026-05-27 11:26:35',4,0.00),('PRD010','Detergent Powder 2KG','Home Essentials',210.00,13,10,'2026-05-12 15:38:25','2026-05-27 11:26:35',4,0.00),('PRD011','Bathroom Brush','Home Essentials',75.00,26,10,'2026-05-12 15:38:25','2026-05-25 15:48:39',4,0.00),('PRD012','Men T-Shirt','Fashion',499.00,8,10,'2026-05-12 15:38:25','2026-05-28 15:23:52',5,0.00),('PRD013','Women Handbag','Fashion',1000.00,20,10,'2026-05-12 15:38:25','2026-05-28 14:57:34',5,0.00),('PRD014','Sports Shoes','Fashion',1499.00,12,10,'2026-05-12 15:38:25','2026-05-27 11:26:35',5,0.00),('PRD015','Notebook A4','Stationery',60.00,52,10,'2026-05-12 15:38:25','2026-05-25 12:40:13',6,0.00),('PRD016','Blue Pen Pack','Stationery',120.00,45,10,'2026-05-12 15:38:25','2026-05-25 15:43:08',6,0.00),('PRD017','Office File Folder','Stationery',90.00,20,10,'2026-05-12 15:38:25','2026-05-12 16:56:32',6,0.00),('PRD018','Steel Water Bottle','Kitchen',350.00,25,10,'2026-05-12 15:38:25','2026-05-28 14:58:43',8,0.00),('PRD019','Non-stick Frying Pan','Kitchen',899.00,9,10,'2026-05-12 15:38:25','2026-05-27 12:46:36',8,0.00),('PRD020','Knife Set','Kitchen',650.00,20,10,'2026-05-12 15:38:25','2026-05-29 10:30:40',8,0.00),('PRD021','Micro Fiber Towel','Home Essentials',499.00,21,10,'2026-05-12 17:30:27','2026-05-27 12:46:34',10,0.00),('PRD022','Salt 1kg','Grocery',50.00,48,10,'2026-05-12 17:44:26','2026-05-25 12:46:16',7,0.00),('PRD023','Cargo Jean','Fashion',699.00,23,10,'2026-05-13 10:42:22','2026-05-27 11:11:01',11,0.00),('PRD024','Keybroad','Electronics',500.00,22,10,'2026-05-13 17:30:17','2026-05-28 15:00:55',12,0.00),('PRD025','Wireless Speaker','Electronics',800.00,14,10,'2026-05-19 11:19:15','2026-05-26 13:08:17',2,0.00),('PRD034','Full Cream Milk 500ml','Dairy',28.00,81,15,'2026-05-19 13:38:13','2026-05-26 12:38:54',17,0.00),('PRD035','Curd 400g','Dairy',40.00,64,15,'2026-05-19 13:38:13','2026-05-28 15:23:52',17,0.00),('PRD036','Paneer 200g','Dairy',90.00,31,10,'2026-05-19 13:38:13','2026-05-28 15:23:52',17,0.00),('PRD037','Butter 100g','Dairy',55.00,40,10,'2026-05-19 13:38:13','2026-05-26 12:25:09',17,0.00),('PRD038','Baby Diapers Pack of 20','Baby Care',350.00,30,5,'2026-05-19 13:38:13','2026-05-19 13:38:13',16,0.00),('PRD039','Baby Shampoo 200ml','Baby Care',180.00,21,5,'2026-05-19 13:38:13','2026-05-29 10:30:18',16,0.00),('PRD040','Baby Powder 300g','Baby Care',140.00,18,5,'2026-05-19 13:38:13','2026-05-25 11:32:32',16,0.00),('PRD041','Baby Wipes 80 Sheets','Baby Care',120.00,34,5,'2026-05-19 13:38:13','2026-05-26 12:12:54',16,0.00),('PRD042','Shampoo 400ml','Personal Care',220.00,39,10,'2026-05-19 13:38:13','2026-05-25 15:48:39',17,0.00),('PRD043','Conditioner 200ml','Personal Care',185.00,33,10,'2026-05-19 13:38:13','2026-05-27 11:29:04',17,0.00),('PRD044','Face Wash 100ml','Personal Care',150.00,41,10,'2026-05-19 13:38:13','2026-05-25 14:52:20',17,0.00),('PRD045','Toothpaste 150g','Personal Care',75.00,56,10,'2026-05-19 13:38:13','2026-05-27 11:29:04',17,0.00),('PRD046','Paracetamol 500mg Strip','Pharmacy',25.00,56,15,'2026-05-19 13:38:13','2026-05-28 15:21:18',17,0.00),('PRD047','Antacid Syrup 170ml','Pharmacy',85.00,39,10,'2026-05-19 13:38:13','2026-05-27 12:46:36',17,0.00),('PRD048','Vitamin C Tablets 10s','Pharmacy',50.00,57,10,'2026-05-19 13:38:13','2026-05-21 10:20:55',17,0.00),('PRD049','Bandage Roll 5m','Pharmacy',35.00,45,10,'2026-05-19 13:38:13','2026-05-27 11:25:46',17,0.00),('PRD050','Frozen Peas 500g','Frozen Foods',80.00,27,8,'2026-05-19 13:38:13','2026-05-28 15:24:18',18,0.00),('PRD051','Frozen Corn 500g','Frozen Foods',85.00,38,8,'2026-05-19 13:38:13','2026-05-28 14:29:49',18,0.00),('PRD052','Frozen French Fries 1kg','Frozen Foods',150.00,19,8,'2026-05-19 13:38:13','2026-05-25 15:32:38',18,0.00),('PRD053','Ice Cream Vanilla 500ml','Frozen Foods',180.00,21,8,'2026-05-19 13:38:13','2026-05-28 15:24:18',18,0.00),('PRD054','White Bread Loaf','Bakery',45.00,41,10,'2026-05-19 13:38:13','2026-05-27 12:46:35',18,0.00),('PRD055','Brown Bread Loaf','Bakery',55.00,42,10,'2026-05-19 13:38:13','2026-05-28 14:29:49',18,0.00),('PRD056','Croissant Pack of 4','Bakery',90.00,19,5,'2026-05-19 13:38:13','2026-05-26 12:28:33',3,0.00),('PRD057','Pav Bun Pack of 6','Bakery',40.00,30,10,'2026-05-19 13:38:13','2026-05-29 10:30:56',18,0.00),('PRD058','Organic Chia Seeds 500g','Grocery',249.00,23,10,'2026-05-19 14:30:00','2026-05-26 13:03:49',21,0.00),('PRD059','Wireless Keyboard','Electronics',3499.00,9,5,'2026-05-19 14:32:00','2026-05-27 11:11:01',22,0.00);
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sale_items`
--

DROP TABLE IF EXISTS `sale_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sale_items` (
  `id` int NOT NULL AUTO_INCREMENT,
  `sale_id` int NOT NULL,
  `sku` varchar(50) NOT NULL,
  `name` varchar(120) NOT NULL,
  `qty` int NOT NULL,
  `unit_price` decimal(10,2) NOT NULL,
  `line_total` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `sale_id` (`sale_id`),
  CONSTRAINT `sale_items_ibfk_1` FOREIGN KEY (`sale_id`) REFERENCES `sales` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=188 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sale_items`
--

LOCK TABLES `sale_items` WRITE;
/*!40000 ALTER TABLE `sale_items` DISABLE KEYS */;
INSERT INTO `sale_items` VALUES (1,1,'PRD006','Sunflower Oil 1L',2,180.00,360.00),(2,1,'PRD008','Toor Dal 1KG',1,146.00,146.00),(3,1,'PRD007','Sugar 1KG',2,48.00,96.00),(4,1,'PRD022','Salt 1kg',2,50.00,100.00),(5,1,'PRD011','Bathroom Brush',1,75.00,75.00),(6,2,'PRD002','Mechanical Keyboard',1,2499.00,2499.00),(7,3,'PRD006','Sunflower Oil 1L',2,180.00,360.00),(8,4,'PRD003','LED Monitor 24 Inch',1,8999.00,8999.00),(9,4,'PRD001','Wireless Mouse',1,599.00,599.00),(10,4,'PRD022','Salt 1kg',1,50.00,50.00),(11,5,'PRD005','Basmati Rice 5KG',1,650.00,650.00),(12,6,'PRD015','Notebook A4',3,60.00,180.00),(13,6,'PRD016','Blue Pen Pack',2,120.00,240.00),(14,7,'PRD001','Wireless Mouse',1,599.00,599.00),(15,8,'PRD001','Wireless Mouse',2,599.00,1198.00),(16,9,'PRD018','Steel Water Bottle',2,350.00,700.00),(17,10,'PRD015','Notebook A4',3,60.00,180.00),(18,10,'PRD016','Blue Pen Pack',1,120.00,120.00),(19,10,'PRD010','Detergent Powder 2KG',1,210.00,210.00),(20,10,'PRD022','Salt 1kg',2,50.00,100.00),(21,10,'PRD011','Bathroom Brush',1,75.00,75.00),(22,11,'PRD005','Basmati Rice 5KG',1,650.00,650.00),(23,11,'PRD022','Salt 1kg',1,50.00,50.00),(24,11,'PRD006','Sunflower Oil 1L',2,180.00,360.00),(25,12,'PRD010','Detergent Powder 2KG',2,210.00,420.00),(26,12,'PRD020','Knife Set',1,650.00,650.00),(27,12,'PRD021','Micro Fiber Towel',1,499.00,499.00),(28,13,'PRD005','Basmati Rice 5KG',1,650.00,650.00),(29,13,'PRD016','Blue Pen Pack',1,120.00,120.00),(30,13,'PRD012','Men T-Shirt',1,499.00,499.00),(31,14,'PRD016','Blue Pen Pack',1,120.00,120.00),(32,14,'PRD024','Keybroad',1,500.00,500.00),(33,15,'PRD008','Toor Dal 1KG',1,145.00,145.00),(34,15,'PRD007','Sugar 1KG',1,48.00,48.00),(35,16,'PRD006','Sunflower Oil 1L',1,180.00,180.00),(36,16,'PRD022','Salt 1kg',1,50.00,50.00),(37,16,'PRD009','Floor Cleaner 1L',1,120.00,120.00),(38,16,'PRD010','Detergent Powder 2KG',1,210.00,210.00),(39,17,'PRD005','Basmati Rice 5KG',1,650.00,650.00),(40,17,'PRD006','Sunflower Oil 1L',2,180.00,360.00),(41,17,'PRD020','Knife Set',1,650.00,650.00),(51,21,'PRD001','Wireless Mouse',1,599.00,599.00),(52,21,'PRD019','Non-stick Frying Pan',1,899.00,899.00),(53,21,'PRD021','Micro Fiber Towel',2,499.00,998.00),(54,22,'PRD015','Notebook A4',1,60.00,60.00),(55,22,'PRD018','Steel Water Bottle',1,350.00,350.00),(56,22,'PRD020','Knife Set',1,650.00,650.00),(57,23,'PRD003','LED Monitor 24 Inch',1,8999.00,8999.00),(58,23,'PRD002','Mechanical Keyboard',1,2499.00,2499.00),(59,24,'PRD026','Mango Juice 1L',3,85.00,255.00),(60,24,'PRD030','Potato Chips 150g',2,40.00,80.00),(61,24,'PRD035','Curd 400g',1,40.00,40.00),(62,24,'PRD037','Butter 100g',2,55.00,110.00),(63,24,'PRD028','Mineral Water 1L Pack',2,20.00,40.00),(64,24,'PRD031','Biscuit Pack Assorted',1,55.00,55.00),(65,25,'PRD054','White Bread Loaf',2,45.00,90.00),(66,25,'PRD034','Full Cream Milk 500ml',3,28.00,84.00),(67,25,'PRD035','Curd 400g',2,40.00,80.00),(68,25,'PRD030','Potato Chips 150g',2,40.00,80.00),(69,25,'PRD028','Mineral Water 1L Pack',3,20.00,60.00),(70,25,'PRD057','Pav Bun Pack of 6',1,40.00,40.00),(71,26,'PRD038','Baby Diapers Pack of 20',1,350.00,350.00),(72,26,'PRD041','Baby Wipes 80 Sheets',1,120.00,120.00),(73,26,'PRD040','Baby Powder 300g',1,140.00,140.00),(74,26,'PRD045','Toothpaste 150g',2,75.00,150.00),(75,26,'PRD028','Mineral Water 1L Pack',3,20.00,60.00),(76,27,'PRD046','Paracetamol 500mg Strip',2,25.00,50.00),(77,27,'PRD047','Antacid Syrup 170ml',1,85.00,85.00),(78,27,'PRD048','Vitamin C Tablets 10s',2,50.00,100.00),(79,27,'PRD049','Bandage Roll 5m',2,35.00,70.00),(80,27,'PRD028','Mineral Water 1L Pack',2,20.00,40.00),(81,28,'PRD050','Frozen Peas 500g',1,80.00,80.00),(82,28,'PRD051','Frozen Corn 500g',1,85.00,85.00),(83,28,'PRD053','Ice Cream Vanilla 500ml',2,180.00,360.00),(84,28,'PRD054','White Bread Loaf',1,45.00,45.00),(85,28,'PRD057','Pav Bun Pack of 6',1,40.00,40.00),(86,28,'PRD030','Potato Chips 150g',2,40.00,80.00),(87,29,'PRD029','Green Tea Box 25 Bags',1,130.00,130.00),(88,29,'PRD033','Namkeen Mix 200g',1,45.00,45.00),(89,29,'PRD028','Mineral Water 1L Pack',2,20.00,40.00),(90,29,'PRD057','Pav Bun Pack of 6',1,40.00,40.00),(91,30,'PRD044','Face Wash 100ml',1,150.00,150.00),(92,30,'PRD045','Toothpaste 150g',2,75.00,150.00),(93,30,'PRD028','Mineral Water 1L Pack',1,20.00,20.00),(94,31,'PRD013','Women Handbag',2,1000.00,2000.00),(95,31,'PRD039','Baby Shampoo 200ml',1,180.00,180.00),(96,31,'PRD055','Brown Bread Loaf',1,55.00,55.00),(97,32,'PRD035','Curd 400g',1,40.00,40.00),(98,32,'PRD040','Baby Powder 300g',10,140.00,1400.00),(99,32,'PRD020','Knife Set',2,650.00,1300.00),(100,33,'PRD015','Notebook A4',1,60.00,60.00),(101,33,'PRD011','Bathroom Brush',1,75.00,75.00),(102,33,'PRD022','Salt 1kg',1,50.00,50.00),(103,33,'PRD001','Wireless Mouse',1,599.00,599.00),(104,33,'PRD014','Sports Shoes',1,1499.00,1499.00),(105,34,'PRD058','Organic Chia Seeds 500g',1,249.00,249.00),(106,34,'PRD006','Sunflower Oil 1L',1,180.00,180.00),(107,34,'PRD035','Curd 400g',1,40.00,40.00),(108,34,'PRD036','Paneer 200g',1,90.00,90.00),(109,34,'PRD055','Brown Bread Loaf',1,55.00,55.00),(110,34,'PRD044','Face Wash 100ml',1,150.00,150.00),(111,35,'PRD052','Frozen French Fries 1kg',1,150.00,150.00),(112,35,'PRD053','Ice Cream Vanilla 500ml',1,180.00,180.00),(113,35,'PRD009','Floor Cleaner 1L',1,120.00,120.00),(114,35,'PRD019','Non-stick Frying Pan',1,899.00,899.00),(115,36,'PRD037','Butter 100g',1,55.00,55.00),(116,36,'PRD050','Frozen Peas 500g',1,80.00,80.00),(117,36,'PRD043','Conditioner 200ml',1,185.00,185.00),(118,36,'PRD047','Antacid Syrup 170ml',1,85.00,85.00),(119,36,'PRD016','Blue Pen Pack',1,120.00,120.00),(120,37,'PRD045','Toothpaste 150g',1,75.00,75.00),(121,37,'PRD042','Shampoo 400ml',1,220.00,220.00),(122,37,'PRD011','Bathroom Brush',1,75.00,75.00),(123,37,'PRD013','Women Handbag',1,1000.00,1000.00),(124,37,'PRD012','Men T-Shirt',1,499.00,499.00),(125,38,'PRD037','Butter 100g',2,55.00,110.00),(126,39,'PRD035','Curd 400g',2,40.00,80.00),(127,39,'PRD034','Full Cream Milk 500ml',1,28.00,28.00),(128,40,'PRD021','Micro Fiber Towel',1,499.00,499.00),(129,40,'PRD023','Cargo Jean',1,699.00,699.00),(130,40,'PRD024','Keybroad',1,500.00,500.00),(131,41,'PRD056','Croissant Pack of 4',1,90.00,90.00),(132,41,'PRD036','Paneer 200g',1,90.00,90.00),(133,41,'PRD053','Ice Cream Vanilla 500ml',1,180.00,180.00),(134,41,'PRD058','Organic Chia Seeds 500g',1,249.00,249.00),(135,41,'PRD006','Sunflower Oil 1L',1,180.00,180.00),(136,42,'PRD007','Sugar 1KG',1,48.00,48.00),(137,42,'PRD008','Toor Dal 1KG',1,145.00,145.00),(138,42,'PRD045','Toothpaste 150g',1,75.00,75.00),(139,43,'PRD057','Pav Bun Pack of 6',2,40.00,80.00),(140,43,'PRD037','Butter 100g',1,55.00,55.00),(141,44,'PRD059','Ergonomic Wireless Keyboard',2,3499.00,6998.00),(142,44,'PRD018','Steel Water Bottle',1,350.00,350.00),(143,45,'PRD041','Baby Wipes 80 Sheets',1,120.00,120.00),(144,45,'PRD039','Baby Shampoo 200ml',1,180.00,180.00),(145,45,'PRD010','Detergent Powder 2KG',1,210.00,210.00),(146,46,'PRD056','Croissant Pack of 4',1,90.00,90.00),(147,46,'PRD001','Wireless Mouse',1,599.00,599.00),(148,47,'PRD039','Baby Shampoo 200ml',1,180.00,180.00),(149,47,'PRD037','Butter 100g',1,55.00,55.00),(150,47,'PRD005','Basmati Rice 5KG',1,650.00,650.00),(151,47,'PRD013','Women Handbag',1,1000.00,1000.00),(152,47,'PRD008','Toor Dal 1KG',1,145.00,145.00),(153,48,'PRD034','Full Cream Milk 500ml',1,28.00,28.00),(154,48,'PRD059','Ergonomic Wireless Keyboard',1,3499.00,3499.00),(155,49,'PRD035','Curd 400g',1,40.00,40.00),(156,49,'PRD024','Keybroad',1,500.00,500.00),(157,49,'PRD025','Wireless Speaker',1,800.00,800.00),(158,50,'PRD055','Brown Bread Loaf',1,55.00,55.00),(159,50,'PRD054','White Bread Loaf',1,45.00,45.00),(160,51,'PRD059','Wireless Keyboard',1,3499.00,3499.00),(161,51,'PRD023','Cargo Jean',1,699.00,699.00),(162,51,'PRD012','Men T-Shirt',1,499.00,499.00),(163,52,'PRD006','Sunflower Oil 1L',1,180.00,180.00),(164,52,'PRD018','Steel Water Bottle',5,350.00,1750.00),(165,52,'PRD046','Paracetamol 500mg Strip',1,25.00,25.00),(166,52,'PRD049','Bandage Roll 5m',2,35.00,70.00),(167,52,'PRD051','Frozen Corn 500g',1,85.00,85.00),(168,53,'PRD010','Detergent Powder 2KG',1,210.00,210.00),(169,53,'PRD021','Micro Fiber Towel',1,499.00,499.00),(170,53,'PRD009','Floor Cleaner 1L',1,120.00,120.00),(171,53,'PRD024','Keybroad',1,500.00,500.00),(172,53,'PRD014','Sports Shoes',1,1499.00,1499.00),(173,54,'PRD035','Curd 400g',2,40.00,80.00),(174,54,'PRD036','Paneer 200g',1,90.00,90.00),(175,54,'PRD043','Conditioner 200ml',1,185.00,185.00),(176,54,'PRD045','Toothpaste 150g',2,75.00,150.00),(177,55,'PRD021','Micro Fiber Towel',1,499.00,499.00),(178,55,'PRD054','White Bread Loaf',1,45.00,45.00),(179,56,'PRD019','Non-stick Frying Pan',1,899.00,899.00),(180,56,'PRD047','Antacid Syrup 170ml',1,85.00,85.00),(181,57,'PRD035','Curd 400g',1,40.00,40.00),(182,57,'PRD036','Paneer 200g',1,90.00,90.00),(183,57,'PRD012','Men T-Shirt',1,499.00,499.00),(184,57,'PRD050','Frozen Peas 500g',1,80.00,80.00),(185,58,'PRD050','Frozen Peas 500g',2,80.00,160.00),(186,58,'PRD053','Ice Cream Vanilla 500ml',1,180.00,180.00),(187,58,'PRD039','Baby Shampoo 200ml',1,180.00,180.00);
/*!40000 ALTER TABLE `sale_items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sales`
--

DROP TABLE IF EXISTS `sales`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sales` (
  `id` int NOT NULL AUTO_INCREMENT,
  `invoice_no` varchar(20) NOT NULL,
  `customer` varchar(120) DEFAULT NULL,
  `customer_id` int DEFAULT NULL,
  `total` decimal(10,2) NOT NULL,
  `sale_date` datetime DEFAULT CURRENT_TIMESTAMP,
  `note` text,
  `status` enum('completed','refunded') DEFAULT 'completed',
  `cashier` varchar(64) DEFAULT NULL,
  `cashier_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `invoice_no` (`invoice_no`),
  KEY `idx_sales_cashier` (`cashier`),
  KEY `idx_sales_cashier_id` (`cashier_id`),
  CONSTRAINT `fk_sales_cashier` FOREIGN KEY (`cashier_id`) REFERENCES `users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=59 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sales`
--

LOCK TABLES `sales` WRITE;
/*!40000 ALTER TABLE `sales` DISABLE KEYS */;
INSERT INTO `sales` VALUES (1,'INV001','Ravi Kumar',1,778.00,'2026-05-01 10:15:00','Walk-in customer','completed',NULL,2),(2,'INV002','Priya Sharma',2,2499.00,'2026-05-02 11:30:00','Regular customer','completed',NULL,2),(3,'INV003','Arun Vel',3,360.00,'2026-05-03 09:45:00',NULL,'refunded',NULL,2),(4,'INV004','Meena Devi',4,9649.00,'2026-05-04 14:00:00','Bulk purchase','completed',NULL,2),(5,'INV005','Karthik R',5,650.00,'2026-05-05 16:20:00',NULL,'completed',NULL,2),(6,'INV006','Lakshmi S',6,420.00,'2026-05-06 12:10:00','Online order','refunded',NULL,2),(7,'INV007','Suresh P',7,599.00,'2026-05-07 10:00:00',NULL,'refunded',NULL,2),(8,'INV008','Divya N',8,1198.00,'2026-05-08 13:45:00','Festival discount','completed',NULL,2),(9,'INV009','Vijay M',9,700.00,'2026-05-09 15:30:00',NULL,'completed',NULL,2),(10,'INV010','Anitha B',10,630.00,'2026-05-10 11:00:00','Walk-in customer','completed',NULL,2),(11,'INV011','Harini',11,1060.00,'2026-05-13 15:51:39','Walk-in customer','completed',NULL,2),(12,'INV012','Lakshmi S',6,1569.00,'2026-05-13 16:26:18','Online order','completed',NULL,2),(13,'INV013','Meena Devi',4,1269.00,'2026-05-13 16:27:52','Bulk purchase','completed',NULL,2),(14,'INV014','Harini',11,620.00,'2026-05-15 10:56:01','Walk-in customer','refunded',NULL,2),(15,'INV015','Divya N',8,193.00,'2026-05-15 11:42:34','Online order','refunded',NULL,2),(16,'INV016','Akash',12,560.00,'2026-05-15 12:04:41','Online order','refunded',NULL,2),(17,'INV017','Vidhun',13,1660.00,'2026-05-15 12:22:06','Wholesale','completed',NULL,2),(21,'INV018','Suresh P',7,2496.00,'2026-05-15 12:32:09','Phone order','refunded',NULL,2),(22,'INV019','Pavithra',17,1060.00,'2026-05-15 16:47:38','Walk-in customer','refunded',NULL,2),(23,'INV020','Leo',18,11498.00,'2026-05-16 13:04:48',NULL,'refunded',NULL,2),(24,'INV021','Sneha Pillai',19,575.00,'2026-05-17 10:10:00','Walk-in customer','completed',NULL,2),(25,'INV022','Arjun Das',20,430.00,'2026-05-17 11:25:00','Online order','refunded',NULL,2),(26,'INV023','Meera Iyer',21,810.00,'2026-05-18 09:30:00','Bulk purchase','completed',NULL,2),(27,'INV024','Rahul Verma',22,345.00,'2026-05-18 14:50:00','Walk-in customer','refunded',NULL,2),(28,'INV025','Ananya Krishnan',23,690.00,'2026-05-19 09:05:00','Loyalty customer','refunded',NULL,2),(29,'INV026','Meera Iyer',21,250.00,'2026-05-19 10:00:00','Walk-in customer','completed',NULL,2),(30,'INV027','Sneha Pillai',19,320.00,'2026-05-19 11:30:00','Repeat customer','refunded',NULL,2),(31,'INV028','Harini',11,2235.00,'2026-05-21 10:36:46','Walk-in customer','completed',NULL,2),(32,'INV029','Meera Iyer',21,2740.00,'2026-05-25 11:32:32',NULL,'completed',NULL,2),(33,'INV030','Ravi Kumar',24,2283.00,'2026-05-25 12:40:13',NULL,'completed',NULL,2),(34,'INV031','Harini',25,764.00,'2026-05-25 14:52:20',NULL,'completed',NULL,2),(35,'INV032','Vimal',26,1349.00,'2026-05-25 15:32:38',NULL,'completed',NULL,2),(36,'INV033','Sara',27,525.00,'2026-05-25 15:43:08',NULL,'completed',NULL,2),(37,'INV034','Neha',28,1869.00,'2026-05-25 15:48:39',NULL,'completed',NULL,2),(38,'INV035','sha',29,110.00,'2026-05-25 15:50:30',NULL,'completed',NULL,2),(39,'INV036','Ravi',30,108.00,'2026-05-25 15:53:26',NULL,'completed',NULL,2),(40,'INV037','Isha',31,1698.00,'2026-05-26 10:50:24',NULL,'completed',NULL,2),(41,'INV038','Akash',12,789.00,'2026-05-26 11:06:15',NULL,'completed',NULL,2),(42,'INV039','Divya N',8,268.00,'2026-05-26 11:06:44',NULL,'completed',NULL,2),(43,'INV040','Karthik R',5,135.00,'2026-05-26 11:08:18','Cash','completed',NULL,2),(44,'INV041','Anitha B',10,7348.00,'2026-05-26 12:06:36','UPI','completed',NULL,2),(45,'INV042','harini',32,510.00,'2026-05-26 12:12:54','Cash','completed',NULL,2),(46,'INV043','sha',33,689.00,'2026-05-26 12:13:50','UPI','refunded',NULL,2),(47,'INV044','Pavithra',17,2030.00,'2026-05-26 12:25:09','Cash','completed',NULL,2),(48,'INV045','Ravi',34,3527.00,'2026-05-26 12:38:54','UPI','completed',NULL,2),(49,'INV046','ravi',35,1340.00,'2026-05-26 13:08:17','Cash','completed',NULL,2),(50,'INV047','Harini',36,100.00,'2026-05-27 11:10:16','Cash','completed',NULL,3),(51,'INV048','Ravi',37,4697.00,'2026-05-27 11:11:01','UPI','completed',NULL,2),(52,'INV049',NULL,NULL,2110.00,'2026-05-27 11:25:46','Cash','completed',NULL,2),(53,'INV050','Arjun Das',20,2828.00,'2026-05-27 11:26:35','Cash','completed',NULL,2),(54,'INV051','sha',38,505.00,'2026-05-27 11:29:04','UPI','completed',NULL,3),(55,'INV052','shri',39,544.00,'2026-05-27 12:46:34','UPI','completed',NULL,2),(56,'INV053','walter',40,984.00,'2026-05-27 12:46:36','Cash','completed',NULL,3),(57,'INV054','Rajan',41,709.00,'2026-05-28 15:23:52','Cash','completed',NULL,3),(58,'INV055','Harini',25,520.00,'2026-05-28 15:24:18','UPI','completed',NULL,3);
/*!40000 ALTER TABLE `sales` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `supplier_payments`
--

DROP TABLE IF EXISTS `supplier_payments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `supplier_payments` (
  `id` int NOT NULL AUTO_INCREMENT,
  `purchase_id` int NOT NULL,
  `supplier_id` int NOT NULL,
  `amount` decimal(12,2) NOT NULL,
  `payment_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `note` text,
  PRIMARY KEY (`id`),
  KEY `idx_purchase` (`purchase_id`),
  KEY `fk_spay_supplier` (`supplier_id`),
  CONSTRAINT `fk_spay_purchase` FOREIGN KEY (`purchase_id`) REFERENCES `supplier_purchases` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_spay_supplier` FOREIGN KEY (`supplier_id`) REFERENCES `suppliers` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `supplier_payments`
--

LOCK TABLES `supplier_payments` WRITE;
/*!40000 ALTER TABLE `supplier_payments` DISABLE KEYS */;
INSERT INTO `supplier_payments` VALUES (1,1,2,8058.90,'2026-05-20 18:00:00','Full electronics payment'),(2,2,3,5000.00,'2026-05-21 18:30:00','Advance grocery payment'),(3,4,5,11337.30,'2026-05-22 20:00:00','Fashion products fully paid'),(4,5,6,1500.00,'2026-05-23 17:15:00','Partial stationery payment'),(5,6,8,4401.00,'2026-05-24 21:10:00','Kitchen stock payment completed'),(6,7,17,1000.00,'2026-05-25 19:00:00','Dairy stock advance payment'),(7,8,18,2970.00,'2026-05-25 22:15:00','Baby products payment completed'),(8,10,22,4000.00,'2026-05-27 19:40:00','Advance payment for keyboards'),(9,9,21,1241.00,'2026-05-28 14:16:33',NULL),(10,11,18,400.00,'2026-05-28 14:29:49',''),(11,11,18,1000.00,'2026-05-29 10:28:31','Cheque');
/*!40000 ALTER TABLE `supplier_payments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `supplier_purchases`
--

DROP TABLE IF EXISTS `supplier_purchases`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `supplier_purchases` (
  `id` int NOT NULL AUTO_INCREMENT,
  `supplier_id` int NOT NULL,
  `invoice_ref` varchar(100) NOT NULL DEFAULT '',
  `total_amount` decimal(12,2) NOT NULL DEFAULT '0.00',
  `amount_paid` decimal(12,2) NOT NULL DEFAULT '0.00',
  `purchase_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `due_date` date DEFAULT NULL,
  `note` text,
  `status` enum('unpaid','partial','paid') NOT NULL DEFAULT 'unpaid',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_supplier` (`supplier_id`),
  CONSTRAINT `fk_sp_supplier` FOREIGN KEY (`supplier_id`) REFERENCES `suppliers` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `supplier_purchases`
--

LOCK TABLES `supplier_purchases` WRITE;
/*!40000 ALTER TABLE `supplier_purchases` DISABLE KEYS */;
INSERT INTO `supplier_purchases` VALUES (1,2,'INV-TECH-101',8058.90,8058.90,'2026-05-20 10:00:00','2026-06-05','10 Wireless Mouse + 1 Mechanical Keyboard + 2 USB Pendrive','paid','2026-05-28 12:51:37'),(2,3,'INV-GROC-102',8424.00,5000.00,'2026-05-21 11:30:00','2026-06-10','Rice, Sunflower Oil, Sugar, Toor Dal grocery stock','partial','2026-05-28 12:51:37'),(3,4,'INV-HOME-103',6327.00,0.00,'2026-05-22 09:20:00','2026-06-15','Floor Cleaner, Detergent Powder, Bathroom Brush','unpaid','2026-05-28 12:51:37'),(4,5,'INV-FASH-104',11337.30,11337.30,'2026-05-22 14:10:00','2026-06-03','T-Shirts, Women Handbags, Sports Shoes','paid','2026-05-28 12:51:37'),(5,6,'INV-STAT-105',3195.00,1500.00,'2026-05-23 12:45:00','2026-06-12','Notebook packs, Blue Pens, File Folders','partial','2026-05-28 12:51:37'),(6,8,'INV-KITCH-106',4401.00,4401.00,'2026-05-24 16:15:00','2026-06-08','Steel Bottles, Frying Pans, Knife Sets','paid','2026-05-28 12:51:37'),(7,17,'INV-DAIRY-107',1638.00,1000.00,'2026-05-25 10:30:00','2026-06-14','Milk, Curd, Butter and Paneer supply','partial','2026-05-28 12:51:37'),(8,18,'INV-BABY-108',2970.00,2970.00,'2026-05-25 17:40:00','2026-06-09','Baby diapers, shampoo, wipes and powder','paid','2026-05-28 12:51:37'),(9,21,'INV-ORG-109',2241.00,1241.00,'2026-05-26 13:10:00','2026-06-18','Organic chia seeds bulk order','partial','2026-05-28 12:51:37'),(10,22,'INV-APEX-110',9447.30,4000.00,'2026-05-27 15:00:00','2026-06-25','Premium wireless keyboards stock','partial','2026-05-28 12:51:37'),(11,18,'',1400.00,1400.00,'2026-05-28 00:00:00','2026-05-28','','paid','2026-05-28 14:29:49'),(12,5,'RESTOCK-PRD013-20260528145734',13500.00,0.00,'2026-05-28 00:00:00',NULL,'Auto-entry: 15 units of Women Handbag restocked by admin','unpaid','2026-05-28 14:57:34'),(13,8,'RESTOCK-PRD018-20260528145843',3780.00,0.00,'2026-05-28 00:00:00',NULL,'Auto-entry: 12 units of Steel Water Bottle restocked by admin','unpaid','2026-05-28 14:58:43'),(14,12,'RESTOCK-PRD024-20260528150055',4500.00,0.00,'2026-05-28 00:00:00',NULL,'Auto-entry: 10 units of Keybroad restocked by admin','unpaid','2026-05-28 15:00:55'),(15,16,'RESTOCK-PRD039-20260529103018',2430.00,0.00,'2026-05-29 00:00:00',NULL,'Auto-entry: 15 units of Baby Shampoo 200ml restocked by admin','unpaid','2026-05-29 10:30:18'),(16,8,'RESTOCK-PRD020-20260529103040',8775.00,0.00,'2026-05-29 00:00:00',NULL,'Auto-entry: 15 units of Knife Set restocked by admin','unpaid','2026-05-29 10:30:40');
/*!40000 ALTER TABLE `supplier_purchases` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `suppliers`
--

DROP TABLE IF EXISTS `suppliers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `suppliers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `supplier_name` varchar(100) NOT NULL,
  `contact` varchar(20) NOT NULL,
  `email` varchar(100) NOT NULL,
  `supplied_products` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `suppliers`
--

LOCK TABLES `suppliers` WRITE;
/*!40000 ALTER TABLE `suppliers` DISABLE KEYS */;
INSERT INTO `suppliers` VALUES (2,'Tech Supply Hub','9123456780','techsupply@gmail.com','4','2026-05-12 10:08:24'),(3,'Fresh Mart Distributors','9345678901','freshmart@gmail.com','4','2026-05-12 10:08:24'),(4,'Home Needs Wholesale','9789012345','homeneeds@gmail.com','3','2026-05-12 10:08:24'),(5,'Fashion World Suppliers','9012345678','fashionworld@gmail.com','3','2026-05-12 10:08:24'),(6,'Stationery Point','9567890123','stationery@gmail.com','3','2026-05-12 10:08:24'),(7,'Daily Essentials Pvt Ltd','9443216789','dailyessentials@gmail.com','2','2026-05-12 10:08:24'),(8,'Kitchen Plus Supply','9898989898','kitchenplus@gmail.com','3','2026-05-12 10:08:24'),(10,'Qp Suppliers','9444095242','QpSupply@gmail.com','1','2026-05-12 12:00:27'),(11,'HB Fashion store','9678377352','HBfashion@gmail.com','1','2026-05-13 05:11:02'),(12,'qr suppliers','9841066262','qr@gmail.com','1','2026-05-13 11:59:04'),(16,'BabyCare Distributors','9944001122','babycare@gmail.com','4','2026-05-19 08:08:13'),(17,'pharmacist Store','9933445566','pharmacy@gmail.com','12','2026-05-19 08:08:13'),(18,'Instant Food Distributors','9922334455','frozenfood@gmail.com','8','2026-05-19 08:08:13'),(21,'GreenField Organics','9876543210','info@greenfield.com','1','2026-05-19 09:00:00'),(22,'Apex Tech Distribution','9123456789','sales@apextech.com','1','2026-05-19 09:02:00');
/*!40000 ALTER TABLE `suppliers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` varchar(20) DEFAULT 'admin',
  `full_name` varchar(128) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'admin','240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9','admin','Admin','2026-05-19 10:12:58'),(2,'cashier1','b4c94003c562bb0d89535eca77f07284fe560fd48a7cc1ed99f0a56263d616ba','cashier','Billing Counter Representative','2026-05-19 10:20:22'),(3,'cashier2','cc8c368fde9cc291c8ea587790342f929d70fa06f612cd51b6141ea5bca46bdb','cashier',NULL,'2026-05-27 05:37:41');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-05-29 11:52:30
