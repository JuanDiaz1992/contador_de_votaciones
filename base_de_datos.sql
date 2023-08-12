

create database voting;

use voting;

create table coordinator(
  idCoordinator INT NOT NULL auto_increment primary key,
  name VARCHAR(50) not null,
  document TINYINT not null,
  email VARCHAR(50) not null,
  password VARCHAR(100) not null
  );
  
create table county(
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    code_county VARCHAR(255) NOT NULL UNIQUE,
    county VARCHAR(255) NOT NULL,
    population INT NOT NULL,
    area FLOAT NOT NULL
);

create table election(
	idElection INT NOT NULL AUTO_INCREMENT,
    year INT NOT NULL,
    voteCount INT NOT NULL,
    politicalParty VARCHAR(50) NOT NULL,
	idCounty INT,
    idCoordinator INT,
    PRIMARY KEY (idElection),
    FOREIGN KEY (idCounty) REFERENCES County(id),
    FOREIGN KEY (idCoordinator) REFERENCES Coordinator(idCoordinator)
);
    
USE voting;
SELECT * FROM election where year= 2022;
SELECT * FROM election;
SELECT * FROM coordinator;

INSERT INTO county (code_county, county, population, area) VALUES ("01015", "Calhoun", 118572, 605.868);


DELETE FROM election WHERE idElection = 2;

DROP TABLE county;

DELETE FROM county;
create table county(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    code_county VARCHAR(255) NOT NULL UNIQUE,
    county VARCHAR(255) NOT NULL,
    population INT NOT NULL,
    area FLOAT NOT NULL
);

create table election(
    idElection INT NOT NULL AUTO_INCREMENT,
    year INT NOT NULL,
    voteCount INT NOT NULL,
    politicalParty VARCHAR(50) NOT NULL,
    idCounty INT,
    idCoordinator INT,
    PRIMARY KEY (idElection),
    FOREIGN KEY (idCounty) REFERENCES County(id),
    FOREIGN KEY (idCoordinator) REFERENCES Coordinator(idCoordinator)
);