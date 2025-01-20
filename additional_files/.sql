CREATE TABLE `users` (
   `user_id` int NOT NULL AUTO_INCREMENT,
   `username` varchar(50) NOT NULL,
   `firstname` varchar(50) DEFAULT NULL,
   `lastname` varchar(50) DEFAULT NULL,
   `dob` date DEFAULT NULL,
   `email` varchar(100) NOT NULL,
   `password` varchar(255) NOT NULL,
   `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
   `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
   `user_type` varchar(45) NOT NULL DEFAULT 'resident',
   PRIMARY KEY (`user_id`),
   UNIQUE KEY `username` (`username`),
   UNIQUE KEY `email` (`email`)
 ) 

 CREATE TABLE `notification` (
   `notification_id` int NOT NULL AUTO_INCREMENT,
   `user_id` int NOT NULL,
   `calendar_event_id` int DEFAULT NULL,
   `bill_id` int DEFAULT NULL,
   `notification_type` enum('calendar_event','bill_info') NOT NULL,
   `read_status` enum('unread','read') DEFAULT 'unread',
   `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
   `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
   PRIMARY KEY (`notification_id`),
   KEY `fk_notification_user` (`user_id`),
   KEY `fk_notification_event` (`calendar_event_id`),
   KEY `fk_notification_bill` (`bill_id`),
   CONSTRAINT `fk_notification_bill` FOREIGN KEY (`bill_id`) REFERENCES `bill_info` (`bill_id`) ON DELETE CASCADE,
   CONSTRAINT `fk_notification_event` FOREIGN KEY (`calendar_event_id`) REFERENCES `calendar_event` (`calendar_event_id`) ON DELETE CASCADE,
   CONSTRAINT `fk_notification_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE
 )