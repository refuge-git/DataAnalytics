
SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;

CREATE DATABASE refuge
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE refuge;

-- TABELA FUNCIONÁRIO
CREATE TABLE funcionario (
    id_funcionario INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(14) NOT NULL UNIQUE,
    telefone VARCHAR(20),
    email VARCHAR(100) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL
) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_unicode_ci;


-- TABELA ENDEREÇO
CREATE TABLE endereco (
    id_endereco INT AUTO_INCREMENT PRIMARY KEY,
    tipo_logradouro VARCHAR(50),
    nome_logradouro VARCHAR(100) NOT NULL,
    numero INT,
    complemento VARCHAR(100),
    bairro VARCHAR(80),
    cep VARCHAR(9) NOT NULL,
    nome_localidade VARCHAR(100),
    sigla_cidade VARCHAR(2)
) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_unicode_ci;


-- TIPO GÊNERO
CREATE TABLE tipo_genero (
    id_genero INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT
) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_unicode_ci;


-- TIPO SEXUALIDADE
CREATE TABLE tipo_sexualidade (
    id_sexualidade INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(50) UNIQUE NOT NULL,
    descricao VARCHAR(255)
) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_unicode_ci;


-- BENEFICIÁRIO
CREATE TABLE beneficiario (
    id_beneficiario INT AUTO_INCREMENT PRIMARY KEY,
    nome_registro VARCHAR(100) NOT NULL,
    nome_social VARCHAR(100),
    dt_nasc DATE,
    cpf VARCHAR(14) UNIQUE,
    estrangeiro BOOLEAN,
    raca ENUM('BRANCO','PRETO','PARDO','AMARELA','INDIGENA','NAO_DECLARADO'), 
    sexo ENUM('FEMININO','MASCULINO','NAO_DECLARADO'),
    nome_mae VARCHAR(100),
    egresso_prisional BOOLEAN,
    local_dorme ENUM('CASA','RUA','CENTRO_ACOLHIDA','PENSAO','PASSAGEM_PELA_CIDADE'),
    foto_perfil VARCHAR(255),
    sisa VARCHAR(50) UNIQUE,
    status ENUM('ATIVO','INATIVO','BANIDO','SUSPENSO'),
    data_ativacao DATETIME,
    fk_funcionario INT,
    fk_endereco INT,
    fk_genero INT,
    fk_sexualidade INT,
    observacao VARCHAR(250),
    FOREIGN KEY (fk_funcionario) REFERENCES funcionario(id_funcionario),
    FOREIGN KEY (fk_endereco) REFERENCES endereco(id_endereco),
    FOREIGN KEY (fk_genero) REFERENCES tipo_genero(id_genero),
    FOREIGN KEY (fk_sexualidade) REFERENCES tipo_sexualidade(id_sexualidade)
) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_unicode_ci;


-- TIPO ATENDIMENTO
CREATE TABLE tipo_atendimento (
    id_tipo_atendimento INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao VARCHAR(250),
    data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    fk_funcionario INT,
    FOREIGN KEY (fk_funcionario) REFERENCES funcionario(id_funcionario)
) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_unicode_ci;


-- REGISTRO ATENDIMENTO
CREATE TABLE registro_atendimento (
    id_registro_atendimento INT AUTO_INCREMENT PRIMARY KEY,
    fk_beneficiario INT NOT NULL,
    fk_tipo INT NOT NULL,
    data_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (fk_beneficiario) REFERENCES beneficiario(id_beneficiario),
    FOREIGN KEY (fk_tipo) REFERENCES tipo_atendimento(id_tipo_atendimento)
) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_unicode_ci;


-- CATEGORIA
CREATE TABLE categoria (
    id_categoria INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL
) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_unicode_ci;


-- CONDIÇÃO SAÚDE
CREATE TABLE condicao_saude (
    id_condicao_saude INT AUTO_INCREMENT PRIMARY KEY,
    diagnostico VARCHAR(100),
    descricao VARCHAR(250),
    data_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    tratamento VARCHAR(250),
    observacoes VARCHAR(250),
    fk_beneficiario INT NOT NULL,
    fk_categoria INT NOT NULL,
    FOREIGN KEY (fk_beneficiario) REFERENCES beneficiario(id_beneficiario),
    FOREIGN KEY (fk_categoria) REFERENCES categoria(id_categoria)
) ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_unicode_ci;


INSERT INTO tipo_genero (nome, descricao) VALUES
('Cisgênero', 'Pessoa cuja identidade de gênero corresponde ao sexo atribuído no nascimento'),
('Transgênero', 'Pessoa cuja identidade de gênero é diferente do sexo atribuído no nascimento'),
('Agênero', 'Pessoa que não se identifica com nenhum gênero'),
('Não declarado', 'Pessoa que optou por não declarar sua identidade de gênero');

INSERT INTO tipo_sexualidade (nome, descricao) VALUES
('Heterossexual', 'Pessoa que sente atração por pessoas do gênero oposto'),
('Homossexual', 'Pessoa que sente atração por pessoas do mesmo gênero'),
('Bissexual', 'Pessoa que sente atração por mais de um gênero'),
('Assexual', 'Pessoa que não sente atração sexual'),
('Pansexual', 'Pessoa que sente atração independente de gênero'),
('Queer', 'Pessoa cuja identidade de gênero e/ou sexualidade não se encaixa em normas tradicionais'),
('Não declarado', 'Pessoa que preferiu não declarar sua sexualidade');

INSERT INTO categoria (nome) VALUES 
('Deficiência'),
('Doença'),
('Transtorno');
