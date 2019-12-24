-- phpMyAdmin SQL Dump
-- version 4.9.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 24, 2019 at 09:54 AM
-- Server version: 8.0.13
-- PHP Version: 7.3.8

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `flask-test`
--

-- --------------------------------------------------------

--
-- Table structure for table `Location`
--

CREATE TABLE `Location` (
  `location_id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `Location`
--

INSERT INTO `Location` (`location_id`, `name`) VALUES
(1, 'Vashi'),
(2, 'Seawoods'),
(3, 'Khar'),
(4, 'Bandra');

-- --------------------------------------------------------

--
-- Table structure for table `Product`
--

CREATE TABLE `Product` (
  `product_id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `Product`
--

INSERT INTO `Product` (`product_id`, `name`) VALUES
(1, 'MacBook Air'),
(2, 'MacBook Pro 13\"'),
(3, 'MacBook Pro 16”'),
(4, 'iMac'),
(5, 'iMac Pro'),
(6, 'Mac Pro'),
(7, 'Mac Mini'),
(8, 'Pro Display XDR');

-- --------------------------------------------------------

--
-- Table structure for table `ProductMovement`
--

CREATE TABLE `ProductMovement` (
  `movement_id` int(10) UNSIGNED NOT NULL,
  `timestamp` timestamp NOT NULL,
  `from_location` int(11) NOT NULL,
  `to_location` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `qty` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `ProductMovement`
--

INSERT INTO `ProductMovement` (`movement_id`, `timestamp`, `from_location`, `to_location`, `product_id`, `qty`) VALUES
(1, '2019-12-23 10:35:10', 0, 1, 1, 10),
(2, '2019-12-23 14:51:13', 0, 3, 1, 5),
(3, '2019-12-23 14:52:15', 0, 4, 4, 25),
(4, '2019-12-23 16:01:35', 0, 2, 3, 10),
(5, '2019-12-23 16:02:29', 2, 0, 3, 2),
(6, '2019-12-23 16:04:44', 4, 2, 4, 5),
(7, '2019-12-23 16:25:54', 0, 3, 3, 50),
(8, '2019-12-23 17:12:47', 0, 4, 3, 15);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Location`
--
ALTER TABLE `Location`
  ADD PRIMARY KEY (`location_id`);

--
-- Indexes for table `Product`
--
ALTER TABLE `Product`
  ADD PRIMARY KEY (`product_id`);

--
-- Indexes for table `ProductMovement`
--
ALTER TABLE `ProductMovement`
  ADD PRIMARY KEY (`movement_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `Location`
--
ALTER TABLE `Location`
  MODIFY `location_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `Product`
--
ALTER TABLE `Product`
  MODIFY `product_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT for table `ProductMovement`
--
ALTER TABLE `ProductMovement`
  MODIFY `movement_id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
