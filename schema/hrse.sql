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
 `referrer` VARCHAR(1024) NOT NULL DEFAULT "na",
 `original_id` INT NOT NULL DEFAULT 0,
 `age` VARCHAR(4) NOT NULL DEFAULT "na",
 `sex` VARCHAR(6) NOT NULL DEFAULT "na",
 `handedness` VARCHAR(5) NOT NULL DEFAULT "na",
 `favcolor` VARCHAR(16) NOT NULL DEFAULT "na",
 `enoughhours` VARCHAR(4) NOT NULL DEFAULT "na",
 `superpower` VARCHAR(16) NOT NULL DEFAULT "na",
 `residence` VARCHAR(4) NOT NULL DEFAULT "na",
 `family` VARCHAR(4) NOT NULL DEFAULT "na",
 `pets` VARCHAR(4) NOT NULL DEFAULT "na",
 `maritalstatus` VARCHAR(64) NOT NULL DEFAULT "na",
 `military` VARCHAR(3) NOT NULL DEFAULT "na",
 `education` VARCHAR(64) NOT NULL DEFAULT "na",
 PRIMARY KEY (`idparticipant`) ,
 UNIQUE INDEX `fingerprint_UNIQUE` (`fingerprint` ASC) )
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `hrse`.`sequences`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hrse`.`sequences` ;

CREATE  TABLE IF NOT EXISTS `hrse`.`sequences` (
  `idsequences` INT NOT NULL AUTO_INCREMENT ,
  `fingerprint` VARCHAR(45) NOT NULL,
  `sequence` VARCHAR(256) NOT NULL,
  `submitted` TIMESTAMP NOT NULL DEFAULT NOW() ,
  `useragent` VARCHAR(256) NOT NULL DEFAULT "na",
  `keyboard` BOOLEAN NOT NULL DEFAULT False,
  `mouse` BOOLEAN NOT NULL DEFAULT False,
  `touch` BOOLEAN NOT NULL DEFAULT False,
  `starttime` BIGINT UNSIGNED NOT NULL DEFAULT 0,
  `firstchartime` BIGINT UNSIGNED NOT NULL DEFAULT 0,
  `lastchartime` BIGINT UNSIGNED NOT NULL DEFAULT 0,
  `endtime` BIGINT UNSIGNED NOT NULL DEFAULT 0,
  `tbcmax` INT UNSIGNED NOT NULL DEFAULT 0,
  `tbcmin` INT UNSIGNED NOT NULL DEFAULT 0,
  `tbcmean` DOUBLE PRECISION(16,8) UNSIGNED NOT NULL DEFAULT 0.0,
  `tbcmedian` INT UNSIGNED NOT NULL DEFAULT 0,
  `tbcrange` INT UNSIGNED NOT NULL DEFAULT 0,
  `tbcstdev` DOUBLE PRECISION(16,8) UNSIGNED NOT NULL DEFAULT 0.0,
  `tbcsumsqrd` INT UNSIGNED NOT NULL DEFAULT 0,
  `tbcsumsqerr` DOUBLE PRECISION(16,8) UNSIGNED NOT NULL DEFAULT 0.0,
  `tbcmeansqerr` DOUBLE PRECISION(16,8) UNSIGNED NOT NULL DEFAULT 0.0,
  `tbcgeomean` DOUBLE PRECISION(16,8) UNSIGNED NOT NULL DEFAULT 0.0,
  `tbcvariance` DOUBLE PRECISION(16,8) UNSIGNED NOT NULL DEFAULT 0.0,
  `tbccoeffvar` DOUBLE PRECISION(16,8) UNSIGNED NOT NULL DEFAULT 0.0,
  `screenwidth` VARCHAR(8) NOT NULL DEFAULT "0",
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
