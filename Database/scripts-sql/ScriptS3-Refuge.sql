DROP DATABASE refuge;
CREATE DATABASE refuge;
USE refuge;

-- TABELA DOCUMENTADA
-- TABELA DE FUNCIONÁRIO
CREATE TABLE funcionario (
    id_funcionario INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(15) NOT NULL UNIQUE,
    telefone VARCHAR(20),
    email VARCHAR(100) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL
);

-- TABELA DOCUMENTADA
-- TABELA DE ENDEREÇO
CREATE TABLE endereco (
    id_endereco INT AUTO_INCREMENT PRIMARY KEY,
    tipo_logradouro VARCHAR(50),
    nome_logradouro VARCHAR(100) NOT NULL,
    numero INT,
    complemento VARCHAR(100),
    bairro VARCHAR(80),
    cep VARCHAR(9) NOT NULL,
    nome_localidade VARCHAR(100)
);

-- TABELA DOCUMENTADA
-- TABELA DE TIPO DE GÊNERO
CREATE TABLE tipo_genero (
    id_genero INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT
);

-- TABELA DOCUMENTADA
-- TABELA DE TIPO DE SEXUALIDADE
CREATE TABLE tipo_sexualidade (
    id_sexualidade INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(50) UNIQUE NOT NULL,
    descricao TEXT
);

-- TABELA DOCUMENTADA
-- TABELA DE BENEFICIÁRIO
CREATE TABLE beneficiario (
    id_beneficiario INT AUTO_INCREMENT PRIMARY KEY,
    nome_registro VARCHAR(100) NOT NULL,
    nome_social VARCHAR(100),
    dt_nasc DATE,
    cpf VARCHAR(14) UNIQUE,
    estrangeiro BOOLEAN,
    raca ENUM('BRANCO', 'PRETO', 'PARDO', 'AMARELA', 'INDIGENA', 'NAO_DECLARADO'), 
    sexo ENUM('FEMININO', 'MASCULINO', 'NAO_DECLARADO'),
    nome_mae VARCHAR(100),
    egresso_prisional BOOLEAN,
    local_dorme ENUM('CASA', 'RUA', 'CENTRO_ACOLHIDA', 'PENSAO', 'PASSAGEM_PELA_CIDADE'),
    foto_perfil VARCHAR(255),
    sisa VARCHAR(50),
    `status` ENUM('ATIVO', 'INATIVO', 'BANIDO', 'SUSPENSO'),
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
)auto_increment = 1;

-- OK
-- TABELA DE TIPO DE ATENDIMENTO
CREATE TABLE tipo_atendimento (
		id_tipo_atendimento INT AUTO_INCREMENT PRIMARY KEY,
		nome VARCHAR(100) NOT NULL,
		descricao VARCHAR(250),
		data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
		fk_funcionario INT,
		FOREIGN KEY (fk_funcionario) REFERENCES funcionario(id_funcionario)
);

-- TABELA DOCUMENTADA
-- TABELA DE REGISTRO DO ATENDIMENTO
CREATE TABLE registro_atendimento (
    id_registro_atendimento INT AUTO_INCREMENT PRIMARY KEY,
    fk_beneficiario INT NOT NULL,
    fk_tipo INT NOT NULL,
    data_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (fk_beneficiario) REFERENCES beneficiario(id_beneficiario),
    FOREIGN KEY (fk_tipo) REFERENCES tipo_atendimento(id_tipo_atendimento)
);

-- TABELA DOCUMENTADA
-- TABELA DE CATEGORIA DE CONDIÇÃO DE SAÚDE
CREATE TABLE categoria (
    id_categoria INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL
);

-- TABELA DOCUMENTADA
-- TABELA DE CONDIÇÃO DE SAÚDE 
CREATE TABLE condicao_saude (
	id_condicao_saude INT AUTO_INCREMENT PRIMARY KEY,
    descricao VARCHAR(250),
    data_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    tratamento VARCHAR(250),
    observacoes VARCHAR(250),
    fk_beneficiario INT NOT NULL,
    fk_categoria INT NOT NULL,
    FOREIGN KEY (fk_beneficiario) REFERENCES beneficiario(id_beneficiario),
    FOREIGN KEY (fk_categoria) REFERENCES categoria(id_categoria)
);

SELECT * FROM funcionario;
SELECT * FROM endereco;
SELECT * FROM condicao_saude;
SELECT * FROM categoria;
SELECT * FROM registro_atendimento;
SELECT * FROM tipo_atendimento;
SELECT * FROM beneficiario;
SELECT * FROM tipo_genero;

      