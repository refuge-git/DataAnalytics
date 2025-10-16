DROP DATABASE refuge;
CREATE DATABASE refuge;
USE refuge;

-- TABELA DE FUNCIONÁRIO
CREATE TABLE funcionario (
    id_funcionario INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(14) NOT NULL UNIQUE,
    telefone VARCHAR(20),
    email VARCHAR(100) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL
);

INSERT INTO funcionario (nome, cpf, telefone, email, senha) VALUES
('João Silva', '123.456.789-00', '(11) 91234-5678', 'joao.silva@email.com', '1234'),
('Maria Oliveira', '987.654.321-00', '(11) 99876-5432', 'maria.oliveira@email.com', 'senha123'),
('Carlos Souza', '111.222.333-44', '(11) 97777-8888', 'carlos.souza@email.com', 'admin');

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

INSERT INTO endereco (tipo_logradouro, nome_logradouro, numero, complemento, bairro, cep, nome_localidade) VALUES
('Rua', 'Praça da Árvore', 314, 'Apto 1', 'Jardim Silveira', '04241064', 'São Paulo'),
('Avenida', 'Paulista', 1000, 'Bloco B', 'Bela Vista', '01311000', 'São Paulo'),
('Travessa', 'Monte Alegre', 57, 'Casa 3', 'Perdizes', '05014000', 'São Paulo');


-- TABELA DE TIPO DE GÊNERO
CREATE TABLE tipo_genero (
    id_genero INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT
);

INSERT INTO tipo_genero (nome, descricao) VALUES
('Cisgênero', 'Pessoa cuja identidade de gênero corresponde ao sexo atribuído no nascimento'),
('Transgênero', 'Pessoa cuja identidade de gênero é diferente do sexo atribuído no nascimento'),
('Agênero', 'Pessoa que não se identifica com nenhum gênero'),
('Não declarado', 'Pessoa que optou por não declarar sua identidade de gênero');



-- TABELA DE TIPO DE SEXUALIDADE
CREATE TABLE tipo_sexualidade (
    id_sexualidade INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(50) UNIQUE NOT NULL,
    descricao VARCHAR(255)
);

INSERT INTO tipo_sexualidade (nome, descricao) VALUES
('Heterossexual', 'Pessoa que sente atração por pessoas do gênero oposto'),
('Homossexual', 'Pessoa que sente atração por pessoas do mesmo gênero'),
('Bissexual', 'Pessoa que sente atração por mais de um gênero'),
('Assexual', 'Pessoa que não sente atração sexual'),
('Pansexual', 'Pessoa que sente atração independente de gênero'),
('Queer', 'Pessoa cuja identidade de gênero e/ou sexualidade não se encaixa em normas tradicionais'),
('Não declarado', 'Pessoa que preferiu não declarar sua sexualidade');

SELECT * FROM tipo_sexualidade;

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
);

INSERT INTO beneficiario (
    nome_registro, nome_social, dt_nasc, cpf, estrangeiro, raca, sexo,
    nome_mae, egresso_prisional, local_dorme, foto_perfil, sisa, `status`,
    data_ativacao, fk_funcionario, fk_endereco, fk_genero, fk_sexualidade, observacao
) VALUES (
    'Lucas Andrade', 'Luk', '1992-01-15', '234.567.890-12', false, 'PARDO', 'MASCULINO',
    'Sandra Andrade', false, 'CASA', 'lucas.jpg', 'SISA101', 'ATIVO',
    NOW(), 1, 1, 2, 3, 'Perfil completo e ativo'),
    ('Marta Silva', NULL, '1987-07-20', '234.567.890-11', false, 'BRANCO', 'FEMININO',
    'Claudia Silva', true, 'CENTRO_ACOLHIDA', NULL, 'SISA102', 'SUSPENSO',
    NOW(), 2, 2, 1, 6, 'Em reabilitação social'),
    ('Diego Santos', NULL, '2001-11-03', '345.678.901-22', false, 'PRETO', 'MASCULINO',
    'Juliana Santos', false, 'RUA', 'diego.png', 'SISA103', 'ATIVO',
    NOW(), 3, 3, 3, 1, 'Necessita acompanhamento psicológico'),
	('Ana Beatriz Lima', 'Bia', '1999-04-09', '456.789.012-33', true, 'AMARELA', 'FEMININO',
    'Márcia Lima', false, 'PENSAO', NULL, 'SISA104', 'INATIVO',
    NOW(), 2, 1, 4, 2, 'Documentação pendente'),
	('José Carlos Ferreira', NULL, '1975-09-29', '567.890.123-44', false, 'INDIGENA', 'NAO_DECLARADO',
    'Marinalva Ferreira', true, 'PASSAGEM_PELA_CIDADE', NULL, 'SISA105', 'BANIDO',
    NOW(), 1, 3, 1, 5, 'Histórico de comportamento inadequado'),
	('José Santos', NULL, '1985-05-12', '123.456.789-00', false, 'PARDO', 'MASCULINO',
    'Maria Souza Santos', true, 'CENTRO_ACOLHIDA', NULL, '123456', 'ATIVO',
    NOW(), 2, 2, 1, 6, 'Em reabilitação social');
 

-- TABELA DE TIPO DE ATENDIMENTO
CREATE TABLE tipo_atendimento (
    id_tipo_atendimento INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    descricao VARCHAR(250),
    data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    fk_funcionario INT,
    FOREIGN KEY (fk_funcionario) REFERENCES funcionario(id_funcionario)
);

INSERT INTO tipo_atendimento (nome, descricao, fk_funcionario)
VALUES 
('Refeição', 'Distribuição de refeições aos assistidos.', 1),
('Banho', 'Oferecimento de banho e cuidados de higiene pessoal.', 2),
('Lavagem de Roupa', 'Serviço de lavanderia para roupas pessoais.', 3);

-- TABELA DE REGISTRO DO ATENDIMENTO
CREATE TABLE registro_atendimento (
    id_registro_atendimento INT AUTO_INCREMENT PRIMARY KEY,
    fk_beneficiario INT NOT NULL,
    fk_tipo INT NOT NULL,
    data_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (fk_beneficiario) REFERENCES beneficiario(id_beneficiario),
    FOREIGN KEY (fk_tipo) REFERENCES tipo_atendimento(id_tipo_atendimento)
);

INSERT INTO registro_atendimento (fk_beneficiario, fk_tipo)
VALUES 
(1, 1),
(2, 2),
(1, 3);

-- TABELA DE CATEGORIA DE CONDIÇÃO DE SAÚDE
CREATE TABLE categoria (
    id_categoria INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL
);

INSERT INTO categoria (nome) VALUES 
('Deficiência'),
('Doença'),
('Transtorno');

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

INSERT INTO condicao_saude (descricao, tratamento, observacoes, fk_beneficiario, fk_categoria)
VALUES 
('Deficiência visual parcial', 'Uso de óculos e acompanhamento oftalmológico', 'Paciente adaptado ao uso de lentes corretivas', 1, 1),
('Diabetes tipo 2', 'Uso diário de metformina e dieta controlada', 'Necessita acompanhamento mensal', 2, 2),
('Transtorno de ansiedade generalizada', 'Psicoterapia e uso de ansiolíticos', 'Crises controladas com terapia', 3, 3),
('Hipertensão arterial', 'Uso contínuo de losartana', 'Monitoramento de pressão diário', 4, 2), 
('Transtorno depressivo maior', 'Uso de antidepressivos e apoio psicológico', 'Melhora nos últimos dois meses', 5, 3);

USE refuge;

SELECT * FROM funcionario;
SELECT * FROM endereco;
SELECT * FROM condicao_saude;
SELECT * FROM categoria;
SELECT * FROM registro_atendimento;
SELECT * FROM tipo_atendimento;
SELECT * FROM beneficiario;
SELECT * FROM tipo_genero;


-- DADOS PARA A DASH
INSERT INTO registro_atendimento (fk_beneficiario, fk_tipo, data_hora)
VALUES
-- 🔹 Abril
(1, 1, '2025-04-05 10:15:00'),
(1, 1, '2025-04-06 11:30:00'),
(1, 1, '2025-04-12 14:20:00'),
(2, 1, '2025-04-09 09:10:00'),
(2, 1, '2025-04-10 15:00:00'),
(3, 1, '2025-04-18 13:00:00'),

-- 🔹 Maio
(1, 1, '2025-05-01 10:00:00'),
(1, 1, '2025-05-03 10:00:00'),
(1, 1, '2025-05-07 15:00:00'),
(2, 1, '2025-05-10 16:30:00'),
(2, 1, '2025-05-18 13:00:00'),
(2, 1, '2025-05-20 09:30:00'),
(3, 1, '2025-05-15 08:45:00'),

-- 🔹 Junho
(1, 1, '2025-06-02 10:00:00'),
(1, 1, '2025-06-03 09:30:00'),
(1, 1, '2025-06-15 11:00:00'),
(2, 1, '2025-06-05 14:00:00'),
(2, 1, '2025-06-07 15:20:00'),
(2, 1, '2025-06-20 17:00:00'),
(3, 1, '2025-06-25 09:00:00'),
(3, 1, '2025-06-27 09:30:00'),

-- 🔹 Julho
(1, 1, '2025-07-01 09:00:00'),
(1, 1, '2025-07-04 14:30:00'),
(2, 1, '2025-07-02 16:00:00'),
(2, 1, '2025-07-08 15:10:00'),
(2, 1, '2025-07-09 10:40:00'),
(3, 1, '2025-07-15 11:30:00'),

-- 🔹 Agosto
(1, 1, '2025-08-02 09:10:00'),
(1, 1, '2025-08-04 14:20:00'),
(1, 1, '2025-08-05 15:50:00'),
(2, 1, '2025-08-06 11:10:00'),
(2, 1, '2025-08-09 17:30:00'),
(3, 1, '2025-08-10 08:20:00'),
(3, 1, '2025-08-20 12:00:00'),

-- 🔹 Outubro (mês atual)
(1, 1, '2025-10-02 09:15:00'),
(1, 1, '2025-10-04 10:45:00'),
(1, 1, '2025-10-06 13:20:00'),
(2, 1, '2025-10-08 15:00:00'),
(2, 1, '2025-10-10 09:00:00'),
(3, 1, '2025-10-11 08:40:00');

truncate table registro_atendimento;
INSERT INTO registro_atendimento (fk_beneficiario, fk_tipo, data_hora) VALUES
(1, 1, '2025-10-13 06:15:00'),
(2, 2, '2025-10-13 08:45:00'),
(3, 1, '2025-10-13 10:05:00'),
(4, 1, '2025-10-13 12:20:00'),
(5, 2, '2025-10-13 14:00:00'),
(1, 2, '2025-10-13 06:25:00'),
(2, 1, '2025-10-13 08:25:00'),
(3, 3, '2025-10-13 11:05:00'),
(4, 3, '2025-10-13 12:10:00'),
(5, 1, '2025-10-13 14:20:00'),
(1, 1, '2025-10-14 06:15:00'),
(2, 2, '2025-10-14 08:45:00'),
(3, 1, '2025-10-14 10:05:00'),
(4, 3, '2025-10-14 12:20:00'),
(5, 2, '2025-10-14 14:00:00'),
(1, 1, '2025-10-15 06:25:00'),
(2, 1, '2025-10-15 08:25:00'),
(3, 1, '2025-10-14 11:05:00'),
(4, 2, '2025-10-14 12:10:00'),
(5, 1, '2025-10-14 14:20:00');

    