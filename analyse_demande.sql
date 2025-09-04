-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Aug 19, 2025 at 09:57 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `analyse_demande`
--

-- --------------------------------------------------------

--
-- Table structure for table `demande`
--

CREATE TABLE `demande` (
  `code` varchar(12) NOT NULL,
  `objet` text DEFAULT NULL,
  `ppr` varchar(10) DEFAULT NULL,
  `nom` varchar(30) DEFAULT NULL,
  `prenom` varchar(30) DEFAULT NULL,
  `description` text DEFAULT NULL,
  `date_demande` datetime DEFAULT NULL,
  `etat` int(11) DEFAULT NULL,
  `bureau` varchar(10) DEFAULT NULL,
  `direction` varchar(30) DEFAULT NULL,
  `mail` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `demande`
--

INSERT INTO `demande` (`code`, `objet`, `ppr`, `nom`, `prenom`, `description`, `date_demande`, `etat`, `bureau`, `direction`, `mail`) VALUES
('2xhe29sBchTr', 'ayvciuaôzi iauzbdiubza', 'he127482', 'a', 'a', 'aubifuab ziub iauzbdouabzaz diuazbudabofua ziudauizi', '2025-08-18 10:22:24', 4, 'B1974', 'direction1', 'ezzahirmoaad@gmail.com'),
('3M7LG4lnJ4tm', 'probléme d\'application', 'as383838', 'e', 'f', 'j\'ai un probléme avec l\'application de comptabilite.', '2025-08-15 19:34:02', 4, 'B1030', 'direction1', 'ezzahirmoaad@gmail.com'),
('3xqpIVU9nvAT', 'problème d\'ordinateur', 'as333333', 'e', 'a', 'j\'ai un probléme avec mon ordinateur.', '2025-08-15 19:45:46', 1, 'B1030', 'direction1', 'ezzahirmoaad@gmail.com'),
('4MncA4MGszj7', 'probléme d\'application', 'as383838', 'e', 'f', 'j\'ai un probléme avec l\'application de comptabilite.', '2025-08-15 19:36:20', 4, 'B1030', 'direction1', 'ezzahirmoaad@gmail.com'),
('8ih9I77HqC12', 'aozuibfaoin oaizfboiabsoi azodiaizbfoaiz oizbaoizzbfa', 'ae21483802', 'a', 'a', 'oainaoik iscanbizfboaizd oaizniaboibafoz odianzif', '2025-08-18 10:27:38', 4, 'B103', 'direction1', 'ezzahirmoaad@gmail.com'),
('9HSz137Ig6cD', 'probléme de site', 'ud128422', 'a', 'a', 'je ne peux pas acceder a un site.', '2025-08-18 10:23:46', 3, 'B1030', 'direction1', 'ezzahirmoaad@gmail.com'),
('A5hXm4Hpv15X', 'aiknvoineap oinscoinazd', 'ae21483802', 'a', 'z', 'akjdnoizn,oaisfoianzpoza azoif,naopz,oxaz azoinaoiz,x', '2025-08-15 19:44:32', 4, 'B3333', 'direction1', 'ezzahirmoaad@gmail.com'),
('h2IU6lG52Ur4', 'iudb vouabzodiboaiz foainzoibasx', 'ic1837273', 'a', 'a', 'zoabzfoianos cbazndoiazboia zdooianzifnaoisn aoz ddoaizndoiano', '2025-08-18 10:25:26', 1, 'b1930', 'direction1', 'ezzahirmoaad@gmail.com'),
('I9vY1b6Ig6uM', 'problème d\'ordinateur', 'rr777777', 'a', 'a', 'j\'ai un probléme avec la battrie de mon ordinateur, elle se decharge rappidement.', '2025-08-18 10:26:58', 3, 'B103', 'direction1', 'ezzahirmoaad@gmail.com'),
('r3iFa6txO9VN', 'probléme d\'application', 'as383838', 'e', 'f', 'j\'ai un problem avec l\'application de comptabilite', '2025-08-15 19:35:36', 3, 'B1030', 'direction1', 'ezzahirmoaad@gmail.com'),
('TMJJ194554aJ', 'probléme d\'application', 'as383838', 'e', 'f', 'j\'ai un probléme avec l\'application de comptabilite.', '2025-08-15 19:36:58', 3, 'B1030', 'direction1', 'ezzahirmoaad@gmail.com'),
('tO3r3BlDr6N7', 'problème d\'ordinateur', 'as123456', 'a', 'z', 'j\'ai un probléme avec mon ordinateur.', '2025-08-15 12:09:39', 3, 'B1030', 'direction1', 'ezzahirmoaad@gmail.com'),
('TzxRmruLG2vy', 'problème d\'ordinateur', 'ux183727', 'a', 'a', 'mon pc ne marche pas.', '2025-08-18 10:24:40', 1, 'b1938', 'direction1', 'ezzahirmoaad@gmail.com'),
('w9HSz137Ig6c', 'problème d\'ordinateur', 'as123456', 'a', 'a', 'j\'ai un probléme', '2025-08-18 11:04:50', 1, 'B1030', 'direction1', 'ezzahirmoaad@gmail.com');

-- --------------------------------------------------------

--
-- Table structure for table `table_etat`
--

CREATE TABLE `table_etat` (
  `id` int(11) NOT NULL,
  `code` varchar(12) DEFAULT NULL,
  `etat` int(11) DEFAULT NULL,
  `date_etat` datetime DEFAULT NULL,
  `description` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `table_etat`
--

INSERT INTO `table_etat` (`id`, `code`, `etat`, `date_etat`, `description`) VALUES
(1, 'tO3r3BlDr6N7', 1, '2025-08-17 12:09:39', ''),
(2, 'tO3r3BlDr6N7', 3, '2025-08-17 16:24:12', 'probléme d\'ordinateur qui n\'est pas commun ou facile a regler.'),
(3, '3M7LG4lnJ4tm', 1, '2025-08-17 19:34:02', ''),
(4, 'r3iFa6txO9VN', 1, '2025-08-17 19:35:36', ''),
(5, '4MncA4MGszj7', 1, '2025-08-17 19:36:20', ''),
(6, 'TMJJ194554aJ', 1, '2025-08-17 19:36:58', ''),
(7, 'TMJJ194554aJ', 3, '2025-08-17 19:42:50', 'probléme Résolue.'),
(8, 'r3iFa6txO9VN', 3, '2025-08-17 19:43:11', 'probléme résolue.'),
(9, '4MncA4MGszj7', 4, '2025-08-17 19:43:23', 'spam'),
(10, '3M7LG4lnJ4tm', 4, '2025-08-17 19:43:31', 'spam.'),
(11, 'A5hXm4Hpv15X', 1, '2025-08-17 19:44:32', ''),
(12, 'A5hXm4Hpv15X', 4, '2025-08-17 19:44:56', 'erreur.'),
(13, '3xqpIVU9nvAT', 1, '2025-08-17 19:45:46', ''),
(14, '2xhe29sBchTr', 1, '2025-08-18 10:22:24', ''),
(15, '9HSz137Ig6cD', 1, '2025-08-18 10:23:46', ''),
(16, 'TzxRmruLG2vy', 1, '2025-08-18 10:24:40', ''),
(17, 'h2IU6lG52Ur4', 1, '2025-08-18 10:25:26', ''),
(18, 'I9vY1b6Ig6uM', 1, '2025-08-18 10:26:58', ''),
(19, '8ih9I77HqC12', 1, '2025-08-18 10:27:38', ''),
(20, 'I9vY1b6Ig6uM', 3, '2025-08-18 10:29:58', 'probléme sérieux de la battrie.'),
(21, '9HSz137Ig6cD', 3, '2025-08-18 10:30:32', 'erreur dans le site.'),
(22, '2xhe29sBchTr', 4, '2025-08-18 10:30:53', 'l\'utilisateur spam.'),
(23, '8ih9I77HqC12', 4, '2025-08-18 10:31:11', ''),
(24, 'w9HSz137Ig6c', 1, '2025-08-18 11:04:50', '');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `demande`
--
ALTER TABLE `demande`
  ADD PRIMARY KEY (`code`);

--
-- Indexes for table `table_etat`
--
ALTER TABLE `table_etat`
  ADD PRIMARY KEY (`id`),
  ADD KEY `code` (`code`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `table_etat`
--
ALTER TABLE `table_etat`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `table_etat`
--
ALTER TABLE `table_etat`
  ADD CONSTRAINT `table_etat_ibfk_1` FOREIGN KEY (`code`) REFERENCES `demande` (`code`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
