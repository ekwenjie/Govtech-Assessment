CREATE DATABASE IF NOT EXISTS `govgrantapi`;
USE `govgrantapi`;
DROP TABLE IF EXISTS `familymember`;
DROP TABLE IF EXISTS `household`;

CREATE TABLE IF NOT EXISTS `household`(
    `id` INT NOT NULL AUTO_INCREMENT,
    `housingType` VARCHAR(12) NOT NULL,
    PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
    
CREATE TABLE IF NOT EXISTS `familymember`(
    `id` INT NOT NULL AUTO_INCREMENT,
    `householdId` INT NOT NULL,
    `name` VARCHAR(30) NOT NULL,
    `gender` VARCHAR(1) NOT NULL,
    `maritalStatus` VARCHAR(10) NOT NULL,
    `spouse` INT,
    `occupationType` VARCHAR(10) NOT NULL,
    `annualIncome` INT NOT NULL,
    `dateOfBirth` DATE NOT NULL,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`householdId`) REFERENCES `household`(`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=UTF8;
    
INSERT INTO `household` (`id`, `housingType`) VALUES
(1, "Condominium"),
(2, "Bungalow"),
(3, "HDB"),
(4, "Mansion"),
(5, "Condominium"),
(6, "Executive");

INSERT INTO `familymember` (`id`, `householdId`, `name`, `gender`, `maritalStatus`, `spouse`, `occupationType`, `annualIncome`, `dateOfBirth`) VALUES
(1, 1, "Yolo Alex", "M", "Single", NULL, "Student", 0, "1990-01-01"),
(2, 2, "Bob", "M", "Married", 3, "Employed", 1000, "1991-01-01"),
(3, 2, "Cynthia", "F", "Married", 2, "Employed", 2000, "1992-01-01"),
(4, 4, "StudentBonus", "M", "Single", NULL, "Student", 0, "2010-01-01"),
(5, 3, "Multigeneration", "F", "Single", NULL, "Unemployed", 0, "2007-01-01"),
(6, 2, "Rich Elder", "M", "Single", NULL, "Employed", 200000, "1950-01-01"),
(7, 5, "Boss Baby", "F", "Single", NULL, "Unemployed", 0, "2022-09-09"),
(8, 6, "Old Baby", "M", "Single", NULL, "Unemployed", 0, "2022-01-01");


