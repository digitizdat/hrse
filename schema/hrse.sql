SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

DROP SCHEMA IF EXISTS `hrse` ;
CREATE SCHEMA IF NOT EXISTS `hrse` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ;
USE `hrse` ;

-- -----------------------------------------------------
-- Table `hrse`.`participant`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hrse`.`participant` ;

CREATE  TABLE IF NOT EXISTS `hrse`.`participant` (
 `idparticipant` INT NOT NULL AUTO_INCREMENT ,
 `admitted` TIMESTAMP NOT NULL DEFAULT NOW() ,
 `fingerprint` VARCHAR(45) NOT NULL,
 `useragent` VARCHAR(256) NOT NULL,
 `maritalstatus` VARCHAR(64) NOT NULL,
 `curzip` VARCHAR(10) NOT NULL,
 `origzip` VARCHAR(10) NOT NULL,
 `family` VARCHAR(4) NOT NULL,
 `residence` VARCHAR(4) NOT NULL,
 `age` VARCHAR(4) NOT NULL,
 `education` VARCHAR(64) NOT NULL,
 `handed` VARCHAR(5) NOT NULL,
 `income` VARCHAR(6) NOT NULL,
 `military` VARCHAR(3) NOT NULL,
 `sex` VARCHAR(6) NOT NULL,
 `employment` VARCHAR(64) NOT NULL,
 PRIMARY KEY (`idparticipant`) ,
 UNIQUE INDEX `fingerprint_UNIQUE` (`fingerprint` ASC) )
ENGINE = InnoDB;
-- CREATE  TABLE IF NOT EXISTS `hrse`.`participant` (
--   `idparticipant` INT NOT NULL AUTO_INCREMENT ,
--   `admitted` TIMESTAMP NOT NULL DEFAULT NOW() ,
--  `fingerprint` VARCHAR(45) NOT NULL,
--  `useragent` VARCHAR(256) NOT NULL,
--  `maritalstatus` VARCHAR(64) NOT NULL DEFAULT "na",
--  `curzip` VARCHAR(10) NOT NULL DEFAULT "na",
--  `origzip` VARCHAR(10) NOT NULL DEFAULT "na",
--  `family` VARCHAR(4) NOT NULL DEFAULT "na",
--  `residence` VARCHAR(4) NOT NULL DEFAULT "na",
--  `age` VARCHAR(4) NOT NULL DEFAULT "na",
--  `education` VARCHAR(64) NOT NULL DEFAULT "na",
--  `handed` VARCHAR(5) NOT NULL DEFAULT "na",
--  `income` VARCHAR(6) NOT NULL DEFAULT "na",
--  `military` VARCHAR(3) NOT NULL DEFAULT "na",
--  `sex` VARCHAR(6) NOT NULL DEFAULT "na",
--  `employment` VARCHAR(64) NOT NULL DEFAULT "na",
--  PRIMARY KEY (`idparticipant`) ,
--  UNIQUE INDEX `fingerprint_UNIQUE` (`fingerprint` ASC) )
-- ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `hrse`.`sequences`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hrse`.`sequences` ;

CREATE  TABLE IF NOT EXISTS `hrse`.`sequences` (
  `idsequences` INT NOT NULL AUTO_INCREMENT ,
  `fingerprint` VARCHAR(45) NOT NULL ,
  `sequence` VARCHAR(256) NOT NULL ,
  `submitted` TIMESTAMP NOT NULL DEFAULT NOW() ,
  `useragent` VARCHAR(256) NOT NULL,
  PRIMARY KEY (`idsequences`) )
ENGINE = InnoDB;

USE `hrse` ;

SET SQL_MODE = '';
GRANT USAGE ON *.* TO hrseweb;
 DROP USER hrseweb;
SET SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';
CREATE USER 'hrseweb';

GRANT SELECT, INSERT, UPDATE, TRIGGER ON TABLE `hrse`.* TO 'hrseweb';

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
