-- SQL script to create the `contacts` table for the emergency contacts application.
-- Adjust the database name and user credentials in `settings.py` when connecting via Django.

CREATE TABLE IF NOT EXISTS `contacts` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `first_name` VARCHAR(50) NOT NULL,
    `last_name` VARCHAR(50) NOT NULL,
    `email` VARCHAR(100) NOT NULL UNIQUE,
    `country_code` VARCHAR(5) NOT NULL DEFAULT '',
    `mobile_number` VARCHAR(20) DEFAULT NULL,
    `event_notification_type` ENUM('ALL_USERS', 'GROUPS') NOT NULL DEFAULT 'ALL_USERS',
    `event_notification_groups` TEXT DEFAULT NULL,
    `event_types` JSON NOT NULL,
    `status` ENUM('ACTIVE', 'INACTIVE') NOT NULL DEFAULT 'ACTIVE',
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
