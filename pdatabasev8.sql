-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Aug 12, 2024 at 01:48 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `pdatabasev8`
--

-- --------------------------------------------------------

--
-- Table structure for table `department`
--

CREATE TABLE `department` (
  `ID` int(11) NOT NULL,
  `Name` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `department`
--

INSERT INTO `department` (`ID`, `Name`) VALUES
(1, 'General'),
(3, 'CS'),
(4, 'IS'),
(5, 'SE'),
(6, 'AI');

-- --------------------------------------------------------

--
-- Table structure for table `instructor`
--

CREATE TABLE `instructor` (
  `ID` int(11) NOT NULL,
  `Name` varchar(100) DEFAULT NULL,
  `Role` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `instructor`
--

INSERT INTO `instructor` (`ID`, `Name`, `Role`) VALUES
(2, 'Ahmed', 'Dr'),
(3, 'mohammed ', 'TA'),
(4, 'Ali', 'Dr'),
(5, 'Heba', 'TA'),
(6, 'Hassan', 'Dr');

-- --------------------------------------------------------

--
-- Table structure for table `instructorload`
--

CREATE TABLE `instructorload` (
  `instructor_ID` int(11) NOT NULL,
  `subject_ID` int(11) NOT NULL,
  `No_sections` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `instructorload`
--

INSERT INTO `instructorload` (`instructor_ID`, `subject_ID`, `No_sections`) VALUES
(2, 3, 6),
(4, 3, 5),
(5, 3, 4);

-- --------------------------------------------------------

--
-- Table structure for table `level`
--

CREATE TABLE `level` (
  `ID` int(11) NOT NULL,
  `Dept_ID` int(11) DEFAULT NULL,
  `levelNo` int(11) DEFAULT NULL,
  `No_sections` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `level`
--

INSERT INTO `level` (`ID`, `Dept_ID`, `levelNo`, `No_sections`) VALUES
(1, 1, 1, 11),
(2, 6, 1, 2),
(3, 4, 4, 4),
(4, 4, 3, 5),
(5, 1, 2, 10),
(6, 5, 1, 2);

-- --------------------------------------------------------

--
-- Table structure for table `location`
--

CREATE TABLE `location` (
  `ID` int(11) NOT NULL,
  `Name` varchar(100) DEFAULT NULL,
  `capacity` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `location`
--

INSERT INTO `location` (`ID`, `Name`, `capacity`) VALUES
(1, 'Hall1', 250),
(2, 'Hall2', 200),
(3, 'Lab', 60);

-- --------------------------------------------------------

--
-- Table structure for table `login`
--

CREATE TABLE `login` (
  `ID` int(11) NOT NULL,
  `UName` varchar(50) NOT NULL,
  `Pass` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `schedule`
--

CREATE TABLE `schedule` (
  `ID` int(11) NOT NULL,
  `level_ID` int(11) DEFAULT NULL,
  `subject_ID` int(11) DEFAULT NULL,
  `instructor_ID` int(11) DEFAULT NULL,
  `Location_ID` int(11) DEFAULT NULL,
  `Day` varchar(10) DEFAULT NULL,
  `sections` varchar(20) DEFAULT NULL,
  `time_start` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `subject`
--

CREATE TABLE `subject` (
  `ID` int(11) NOT NULL,
  `level_ID` int(11) DEFAULT NULL,
  `Name` varchar(100) DEFAULT NULL,
  `Times_Per_Week` int(11) DEFAULT NULL,
  `sectionHour` int(11) DEFAULT NULL,
  `LectureHour` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `subject`
--

INSERT INTO `subject` (`ID`, `level_ID`, `Name`, `Times_Per_Week`, `sectionHour`, `LectureHour`) VALUES
(3, 1, 'fundamental of programming', 1, 2, 2),
(4, 5, 'analysis of algorithms', 1, 2, 2),
(5, 3, 'Dayabase', 1, 2, 2);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `department`
--
ALTER TABLE `department`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `instructor`
--
ALTER TABLE `instructor`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `instructorload`
--
ALTER TABLE `instructorload`
  ADD PRIMARY KEY (`instructor_ID`,`subject_ID`),
  ADD KEY `subject_ID` (`subject_ID`);

--
-- Indexes for table `level`
--
ALTER TABLE `level`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `Dept_ID` (`Dept_ID`);

--
-- Indexes for table `location`
--
ALTER TABLE `location`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `login`
--
ALTER TABLE `login`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `schedule`
--
ALTER TABLE `schedule`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `level_ID` (`level_ID`),
  ADD KEY `subject_ID` (`subject_ID`),
  ADD KEY `instructor_ID` (`instructor_ID`),
  ADD KEY `Location_ID` (`Location_ID`),
  ADD KEY `level_ID_2` (`level_ID`,`subject_ID`,`instructor_ID`,`Location_ID`);

--
-- Indexes for table `subject`
--
ALTER TABLE `subject`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `level_ID` (`level_ID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `department`
--
ALTER TABLE `department`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `instructor`
--
ALTER TABLE `instructor`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `level`
--
ALTER TABLE `level`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `location`
--
ALTER TABLE `location`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `login`
--
ALTER TABLE `login`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `schedule`
--
ALTER TABLE `schedule`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=48;

--
-- AUTO_INCREMENT for table `subject`
--
ALTER TABLE `subject`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `instructorload`
--
ALTER TABLE `instructorload`
  ADD CONSTRAINT `InstructorLoad_ibfk_1` FOREIGN KEY (`instructor_ID`) REFERENCES `instructor` (`ID`),
  ADD CONSTRAINT `InstructorLoad_ibfk_2` FOREIGN KEY (`subject_ID`) REFERENCES `subject` (`ID`);

--
-- Constraints for table `level`
--
ALTER TABLE `level`
  ADD CONSTRAINT `Level_ibfk_1` FOREIGN KEY (`Dept_ID`) REFERENCES `department` (`ID`);

--
-- Constraints for table `schedule`
--
ALTER TABLE `schedule`
  ADD CONSTRAINT `Schedule_ibfk_1` FOREIGN KEY (`level_ID`) REFERENCES `level` (`ID`),
  ADD CONSTRAINT `Schedule_ibfk_2` FOREIGN KEY (`subject_ID`) REFERENCES `subject` (`ID`),
  ADD CONSTRAINT `Schedule_ibfk_3` FOREIGN KEY (`instructor_ID`) REFERENCES `instructor` (`ID`),
  ADD CONSTRAINT `Schedule_ibfk_4` FOREIGN KEY (`Location_ID`) REFERENCES `location` (`ID`);

--
-- Constraints for table `subject`
--
ALTER TABLE `subject`
  ADD CONSTRAINT `Subject_ibfk_1` FOREIGN KEY (`level_ID`) REFERENCES `level` (`ID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
