CREATE TABLE IF NOT EXISTS `timedata_date` (
  `corpus` varchar(48) NOT NULL DEFAULT '',
  `datefrom` date NOT NULL DEFAULT '0000-00-00',
  `dateto` date NOT NULL DEFAULT '0000-00-00',
  `tokens` int(11) NOT NULL DEFAULT 0,
  PRIMARY KEY (`corpus`,`datefrom`,`dateto`,`tokens`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=COMPRESSED;
CREATE TABLE IF NOT EXISTS `lemgram_index` (
  `lemgram` varchar(64) NOT NULL,
  `freq` int(11) NOT NULL DEFAULT 0,
  `freq_prefix` int(11) NOT NULL DEFAULT 0,
  `freq_suffix` int(11) NOT NULL DEFAULT 0,
  `corpus` varchar(48) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`lemgram`,`corpus`,`freq`,`freq_prefix`,`freq_suffix`),
  KEY `corpus` (`corpus`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=COMPRESSED;
