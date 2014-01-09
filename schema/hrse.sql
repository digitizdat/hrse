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
  `uuid` VARCHAR(45) NULL ,
  PRIMARY KEY (`idparticipant`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hrse`.`sequences`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `hrse`.`sequences` ;

CREATE  TABLE IF NOT EXISTS `hrse`.`sequences` (
  `idsequences` INT NOT NULL AUTO_INCREMENT ,
  `uuid` VARCHAR(45) NULL ,
  `sequence` VARCHAR(256) NULL ,
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
