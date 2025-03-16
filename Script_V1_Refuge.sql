DROP DATABASE IF EXISTS Refuge;
CREATE DATABASE IF NOT EXISTS Refuge;

CREATE TABLE Funcionario(
idFuncionario INT PRIMARY KEY AUTO_INCREMENT,
nome VARCHAR (45),
cpf CHAR(11),
telefone CHAR(11),
email VARCHAR (45)
);

CREATE TABLE Beneficiario (
idBeneficiario INT PRIMARY KEY AUTO_INCREMENT,
nome VARCHAR (45),
dtNasc DATE,
cpf CHAR(14),
genero ENUM('masculino', 'feminino', 'outro', 'prefiro-nao-dizer'),
sexualidade VARCHAR (45),
raça ENUM('Branco', 'Negro', 'Pardo', 'Amarelo', 'Indígena', 'Outro'),
nomeMae VARCHAR(100),
sisa CHAR(7),
stts ENUM('banido', 'suspenso', 'ativo', 'inativo') NOT NULL DEFAULT 'ativo',
descricao TEXT DEFAULT NULL,
dataAtivacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
CONSTRAINT status_desc CHECK(
(stts IN ('banido','suspenso') AND descricao IS NOT NULL AND descricao != '')
OR (stts IN ('ativo', 'inativo') )),
fkFuncionario INT, 
FOREIGN KEY (fkFuncionario) REFERENCES Funcionario(idFuncionario) ON DELETE SET NULL
);

CREATE TABLE Banho (
idBanho INT PRIMARY KEY AUTO_INCREMENT,
horario TIME,
dia DATE,
fkBeneficiario INT,
FOREIGN KEY (fkBeneficiario) REFERENCES Beneficiario(idBeneficiario) ON DELETE CASCADE
);

CREATE TABLE Refeicao(
idRefeicao INT PRIMARY KEY AUTO_INCREMENT,
nomeRefeicao VARCHAR (45),
horario TIME,
fkBeneficiarioR INT,
FOREIGN KEY (fkBeneficiarioR) REFERENCES Beneficiario (idBeneficiario) ON DELETE CASCADE
);

-- ON DELETE SET NULL - SIGNIFICA QUE SE UM FUNCIONARIO FOR EXCLUIDO, O CAMPO FUNCIONARIO AINDA EXISTIRA POREM FICARÁ NULL
-- ON DELETE CASCADE- SE UM BENEFICIARIO FOR DELETADO, AUTOMATICAMENTE OS REGISTROS DE BANHO E REFEICAO RELACIONADO A ESSE 
-- USUARIO TAMBEM SERÃO.

INSERT INTO Beneficiario (nome, dtNasc, cpf, genero, sexualidade, raça, nomeMae) VALUES 
('João Silva', '1990-05-15', '123.456.789-00', 'masculino', 'heterossexual', 'pardo', 'Maria Silva'),
('Maria Santos', '1985-08-22', '987.654.321-00', 'feminino', 'lésbica', 'branca', 'Ana Santos'),
('Carlos Souza', '1992-11-10', '111.222.333-44', 'masculino', 'bissexual', 'negro', 'Teresa Souza');

SELECT  * FROM Beneficiario;

INSERT INTO Beneficiario (nome, dtNasc, cpf, genero, sexualidade, raça, nomeMae, stts) VALUES 
('Alex Rocha', '1998-07-30', '999.888.777-66', 'outro', 'prefiro não dizer', 'branca', 'Joana Rocha', 'banido');

INSERT INTO Beneficiario (nome, dtNasc, cpf, genero, sexualidade, raça, nomeMae, stts, descricao) VALUES 
('Alex Rocha', '1998-07-30', '999.888.777-66', 'outro', 'prefiro não dizer', 'branca', 'Joana Rocha', 'banido', 'Mal Comportamento');

