DROP DATABASE refuge;
CREATE DATABASE refuge;
USE refuge;

CREATE TABLE Funcionario (
    id_funcionario INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(14) NOT NULL UNIQUE,
    telefone VARCHAR(20),
    email VARCHAR(100) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL
);

INSERT INTO Funcionario (nome, cpf, telefone, email, senha) VALUES
('João Silva', '123.456.789-00', '(11) 91234-5678', 'joao.silva@email.com', '1234'),
('Maria Oliveira', '987.654.321-00', '(11) 99876-5432', 'maria.oliveira@email.com', 'senha123'),
('Carlos Souza', '111.222.333-44', '(11) 97777-8888', 'carlos.souza@email.com', 'admin');

SELECT * FROM Funcionario;

CREATE TABLE Endereco (
    id_endereco INT AUTO_INCREMENT PRIMARY KEY,
    tipo_logradouro VARCHAR(50),
    nome_logradouro VARCHAR(100) NOT NULL,
    numero INT,
    complemento VARCHAR(100),
    bairro VARCHAR(80),
    cep VARCHAR(9) NOT NULL,
    nome_localidade VARCHAR(100),
    sigla_cidade VARCHAR(2)
);


INSERT INTO Endereco (
	tipo_logradouro,
    nome_logradouro,
    numero,
    complemento,
    bairro,
    cep,
    nome_localidade,
    sigla_cidade
) VALUES
('Rua', 'Praça da Árvore', 314, 'Apto 1', 'Jardim Silveira', '04241064', 'São Paulo', 'SP'),
('Avenida', 'Paulista', 1000, 'Bloco B', 'Bela Vista', '01311000', 'São Paulo', 'SP'),
('Travessa', 'Monte Alegre', 57, 'Casa 3', 'Perdizes', '05014000', 'São Paulo', 'SP');

SELECT * FROM Endereco;

CREATE TABLE TipoGenero (
    id_genero INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT
);


INSERT INTO tipoGenero (nome, descricao) VALUES
('Masculino', 'Pessoa que se identifica com o gênero masculino'),
('Feminino', 'Pessoa que se identifica com o gênero feminino'),
('Não-binário', 'Pessoa que não se identifica nem como homem nem como mulher'),
('Agênero', 'Pessoa que não se identifica com nenhum gênero'),
('Gênero fluido', 'Pessoa cuja identidade de gênero varia ao longo do tempo'),
('Bigênero', 'Pessoa que se identifica com dois gêneros, simultaneamente ou alternadamente'),
('Transgênero', 'Pessoa cuja identidade de gênero é diferente do sexo atribuído no nascimento'),
('Intergênero', 'Pessoa cuja identidade de gênero está entre masculino e feminino');

SELECT * FROM TipoGenero;

CREATE TABLE Beneficiario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome_registro VARCHAR(100) NOT NULL,
    nome_social VARCHAR(100),
    dt_nasc DATE NOT NULL,
    cpf VARCHAR(14) NOT NULL UNIQUE,
    raca VARCHAR(50), 
    nome_mae VARCHAR(100),
    foto_perfil VARCHAR(255),
    sisa VARCHAR(50),
    status VARCHAR(50), 
    data_ativacao DATETIME,
    fk_funcionario INT,
    fk_endereco INT,
    fk_genero INT,
    FOREIGN KEY (fk_funcionario) REFERENCES Funcionario(id_funcionario),
    FOREIGN KEY (fk_endereco) REFERENCES Endereco(id_endereco),
    FOREIGN KEY (fk_genero) REFERENCES TipoGenero(id_genero)
);


INSERT INTO beneficiario (
    nome_registro, nome_social, dt_nasc, cpf, raca, nome_mae,
    foto_perfil, sisa, status, data_ativacao,
    fk_funcionario, fk_endereco, fk_genero
) VALUES
('Lucas Oliveira', 'Lu Oliveira', '1997-09-12', '32576924590', 'PARDO', 'Maria de Lurdes',
 'lucas.jpg', '92817', 'ATIVO', '2025-05-01 10:00:00',
 1, 2, 3),
('Ana Souza', 'Anita Souza', '1995-04-20', '14567812300', 'BRANCO', 'Joana Souza',
 'ana.png', '73920', 'INATIVO', '2025-04-15 09:30:00',
 3, 2, 4),
('Carlos Nunes', 'C. Nunes', '1992-02-10', '98765432100', 'PRETO', 'Helena Nunes',
 'carlos.jpeg', '12678', 'ATIVO', '2025-04-29 14:10:00',
 1, 2, 2);
 
 
 SELECT * FROM Beneficiario;

