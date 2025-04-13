DROP DATABASE IF EXISTS Refuge;
CREATE DATABASE IF NOT EXISTS Refuge;
USE Refuge;

CREATE TABLE Funcionario(
id_funcionario INT PRIMARY KEY AUTO_INCREMENT,
nome VARCHAR (45),
cpf CHAR(11),
telefone CHAR(11),
email VARCHAR (45)
);

CREATE TABLE Beneficiario (
id_beneficiario INT PRIMARY KEY AUTO_INCREMENT,
nome VARCHAR (45),
dt_nasc DATE,
cpf CHAR(14),
genero ENUM('masculino', 'feminino', 'outro', 'prefiro-nao-dizer'),
sexualidade VARCHAR (45),
raca ENUM('Branco', 'Negro', 'Pardo', 'Amarelo', 'Indígena', 'Outro'),
nome_mae VARCHAR(100),
sisa CHAR(7),
status_atividade ENUM('banido', 'suspenso', 'ativo', 'inativo') NOT NULL DEFAULT 'ativo',
descricao TEXT DEFAULT NULL,
data_ativacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
CONSTRAINT status_desc CHECK(
(status_atividade IN ('banido','suspenso') AND descricao IS NOT NULL AND descricao != '')
OR (status_atividade IN ('ativo', 'inativo') )),
fk_funcionario INT, 
FOREIGN KEY (fk_funcionario) REFERENCES Funcionario(id_funcionario) ON DELETE SET NULL
);

CREATE TABLE Atividade (
id_atividade INT PRIMARY KEY AUTO_INCREMENT,
nome VARCHAR(45),
descricao VARCHAR(100),
data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
fk_beneficiario INT,
FOREIGN KEY (fk_beneficiario) REFERENCES Beneficiario(id_beneficiario) ON DELETE CASCADE
);

CREATE TABLE Endereco (
id_endereco INT PRIMARY KEY AUTO_INCREMENT,
cep VARCHAR(9),
rua VARCHAR(45),
bairro VARCHAR(45),
logradouro VARCHAR(45),
numero INT,
complemento VARCHAR(20),
fk_beneficiario INT,
FOREIGN KEY (fk_beneficiario) REFERENCES Beneficiario(id_beneficiario)
);

CREATE TABLE CondicaoSaude (
id_condicao_saude INT PRIMARY KEY AUTO_INCREMENT,
descricao VARCHAR(200),
data_diagnostico DATETIME,
tratamento VARCHAR(100),
observacoes VARCHAR(200),
fk_beneficiario INT,
FOREIGN KEY (fk_beneficiario) REFERENCES Beneficiario(id_beneficiario)
);


-- ON DELETE SET NULL - SIGNIFICA QUE SE UM FUNCIONARIO FOR EXCLUIDO, O CAMPO FUNCIONARIO AINDA EXISTIRA POREM FICARÁ NULL
-- ON DELETE CASCADE- SE UM BENEFICIARIO FOR DELETADO, AUTOMATICAMENTE OS REGISTROS DE ATIVIDADE RELACIONADO A ESSE 
-- USUARIO TAMBEM SERÃO.

-- Inserindo funcionários
INSERT INTO Funcionario (nome, cpf, telefone, email) VALUES
('João Silva', '12345678901', '11987654321', 'joao.silva@email.com'),
('Maria Souza', '23456789012', '11976543210', 'maria.souza@email.com');

-- Inserindo beneficiários
INSERT INTO Beneficiario (nome, dt_nasc, cpf, genero, sexualidade, raca, nome_mae, sisa, status_atividade, descricao, fk_funcionario) VALUES
('Carlos Santos', '1990-05-20', '34567890123', 'masculino', 'heterossexual', 'Pardo', 'Ana Santos', '1234567', 'ativo', NULL, 1),
('Fernanda Lima', '1985-10-15', '45678901234', 'feminino', 'bissexual', 'Branco', 'Rita Lima', '7654321', 'suspenso', 'Documentação pendente', 2),
('José Oliveira', '2000-08-05', '56789012345', 'masculino', 'homossexual', 'Negro', 'Maria Oliveira', '9876543', 'banido', 'Fraude detectada', 1);

-- Inserindo atividades
INSERT INTO Atividade (nome, descricao, fk_beneficiario) VALUES
('Consulta médica', 'Consulta com clínico geral', 1),
('Atendimento psicológico', 'Sessão de terapia individual', 2);

-- Inserindo endereços
INSERT INTO Endereco (cep, rua, bairro, logradouro, numero, complemento, fk_beneficiario) VALUES
('01001-000', 'Rua das Flores', 'Centro', 'Avenida', 100, 'Apto 202', 1),
('02002-000', 'Rua das Palmeiras', 'Jardins', 'Rua', 250, NULL, 2);

-- Inserindo condições de saúde
INSERT INTO CondicaoSaude (descricao, data_diagnostico, tratamento, observacoes, fk_beneficiario) VALUES
('Hipertensão arterial', '2023-03-10 14:30:00', 'Uso de medicamentos diários', 'Monitorar pressão semanalmente', 1),
('Ansiedade generalizada', '2022-07-25 09:00:00', 'Psicoterapia e medicação', 'Evitar gatilhos emocionais', 2);


select * from Funcionario;
select * from Beneficiario;
select * from Atividade;
select * from Endereco;
select * from CondicaoSaude;