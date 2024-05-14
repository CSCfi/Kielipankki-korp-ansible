CREATE TABLE IF NOT EXISTS `auth_allow` (
  `person` varchar(80) NOT NULL,
  `corpus` varchar(80) NOT NULL,
  PRIMARY KEY (`person`,`corpus`),
  KEY `corpus` (`corpus`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
CREATE TABLE IF NOT EXISTS `auth_academic` (
  `person` varchar(80) NOT NULL,
  PRIMARY KEY (`person`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
CREATE TABLE IF NOT EXISTS `auth_lbr_map` (
  `lbr_id` varchar(255) NOT NULL DEFAULT '',
  `corpus` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`lbr_id`,`corpus`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
CREATE TABLE IF NOT EXISTS `auth_license` (
  `corpus` varchar(80) NOT NULL,
  `license` varchar(6) NOT NULL,
  PRIMARY KEY (`corpus`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
CREATE TABLE IF NOT EXISTS `auth_secret` (
  `person` varchar(80) NOT NULL,
  `secret` varchar(240) NOT NULL,
  PRIMARY KEY (`person`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
