create database FinalProject;
-- -----------------------------------------------------
-- Table `FinalProject`.`Symbol`
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS `FinalProject`.`Symbol` (
  `SymbolID` INT NOT NULL,
  `Type` VARCHAR(45) NULL,
  PRIMARY KEY (`SymbolID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `FinalProject`.`Trade`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `FinalProject`.`Trade` (
  `TradeID` INT NOT NULL AUTO_INCREMENT,
  `SymbolID` INT NOT NULL,
  `Date` DATETIME NULL,
  `Quantity` VARCHAR(25) NULL,
  `Price` VARCHAR(45) NULL,
  PRIMARY KEY (`TradeID`, `SymbolID`),
  CONSTRAINT `fk_Trade_Symbol`
    FOREIGN KEY (`SymbolID`)
    REFERENCES `FinalProject`.`Symbol` (`SymbolID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `FinalProject`.`PL`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `FinalProject`.`PL` (
  `PLID` INT NOT NULL AUTO_INCREMENT,
  `SymbolID` INT NOT NULL,
  `Quantity` VARCHAR(45) NULL,
  `VWAP` VARCHAR(45) NULL,
  `UPL` VARCHAR(45) NULL,
  `RPL` VARCHAR(45) NULL,
  PRIMARY KEY (`PLID`, `SymbolID`),
  CONSTRAINT `fk_PL_Symbol1`
    FOREIGN KEY (`SymbolID`)
    REFERENCES `FinalProject`.`Symbol` (`SymbolID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

use FinalProject;

insert into Symbol
value
(0,'CASH'),
(1,'BTC'),
(2,'ETH'),
(4,'LTC');

insert into PL
value
(1,0,0,0,100000,0);


insert into PL
value
(2,1,0,0,0,0);


insert into PL
value
(3,2,0,0,0,0);


insert into PL
value
(4,4,0,0,0,0);
