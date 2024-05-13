
-- FACULDADES = (
--     ('ESEC', 'Escola Superior de Educação e Comunicação'),
--     ('ESGHT', 'Escola Superior de Gestão Hotelaria e Turismo'),
--     ('ESS', 'Escola Superior de Saúde'),
--     ('ISE', 'Instituto Superior de Engenharia'),
--     ('FCHS', 'Faculdade de Ciências Humanas e Sociais'),
--     ('FCT', 'Faculdade de Ciências e Tecnologias'),
--     ('FE', 'Faculdade de Economia'),
--     ('DCBM', 'Departamento de Ciências Biomédicas e Medicina'),
-- )


-- DEPARTAMENTOS_DCBM = (
--     ('1', 'DCBM'),
-- )

-- CURSOS_DCBM = (
--     ('1', 'Ciências Biomédicas'),
--     ('2', 'Medicina'),
--     ('3', 'Oncologia'),
-- )


-- DEPARTAMENTOS_FE = (
--     ('1', 'FE'),
-- )

-- CURSOS_FE = (
--     ('1', 'Economia'),
--     ('2', 'Gestão de Empresas'),
--     ('3', 'Sociologia'),
-- )


-- DEPARTAMENTOS_FCT = (
--     ('1', 'Ciências Biológicas e Bioengenharia'),
--     ('2', 'Ciências da terra, do mar e do ambiente'),
--     ('3', 'Engenharia Eletrónica e Informática'),
--     ('4', 'Física'),
--     ('5', 'Matemática'),
--     ('6', 'Química e Farmácia'),
-- )

-- CURSOS_FCT = (
--     ('1', 'Agronomia'),
--     ('2', 'Arquitetura Paisagista'),
--     ('3', 'Bioengenharia'),
--     ('4', 'Biologia'),
--     ('5', 'Biologia Marinha'),
--     ('6', 'Bioquímica'),
--     ('7', 'Biotecnologia'),
--     ('8', 'Engenharia Informática'),
--     ('9', 'Gestão Marinha e Costeira'),
--     ('10', 'Matemática Aplicada à Economia e à Gestão'),
--     ('1', 'Ciências Farmacêuticas'),
-- )


-- DEPARTAMENTOS_FCHS = (
--     ('1', 'Psicologia e Ciências da Educação'),
--     ('2', 'Artes e Humanidades'),
-- )

-- CURSOS_FCHS = (
--     ('1', 'Artes Visuais'),
--     ('2', 'Ciências da Educação e da Formação'),
--     ('3', 'Línguas e Comunicação'),
--     ('4', 'Línguas, Literaturas e Culturas'),
--     ('5', 'Património Cultural e Arqueologia'),
--     ('6', 'Psicologia'),
-- )



-- DEPARTAMENTOS_ISE = (
--     ('1', 'Engenharia Alimentar'),
--     ('2', 'Engenharia Civil'),
--     ('3', 'Engenharia Eletrotécnica'),
--     ('4', 'Engenharia Mecânica'),
-- )


-- CURSOS_ISE = (
--     ('1', 'Engenharia Alimentar'),
--     ('2', 'Engenharia Civil'),
--     ('3', 'Engenharia Elétrica e Eletrónica'),
--     ('4', 'Engenharia Mecânica'),
--     ('5', 'Tecnologia e Segurança Alimentar'),
--     ('6', 'Tecnologias de Informação e Comunicação'),
-- )




-- DEPARTAMENTOS_ESS = (
--     ('1', 'ESS'),
-- )

-- CURSOS_ESS = (
--     ('1', 'Bioengenharia'),
--     ('2', 'Ciências Biomédicas Laboratoriais'),
--     ('3', 'Dietética e Nutrição'),
--     ('4', 'Enfermagem'),
--     ('5', 'Farmácia'),
--     ('6', 'Imagem Médica e Radioterapia'),
--     ('7', 'Ortoprotesia'),
--     ('8', 'Terapia da Fala'),
-- )



-- DEPARTAMENTOS_ESGHT = (
--     ('1', 'ESGHT'),
-- )

-- CURSOS_ESGHT = (
--     ('1', 'Gestão'),
--     ('2', 'Gestão Hoteleira'),
--     ('3', 'Marketing'),
--     ('4', 'Turismo'),
-- )


-- DEPARTAMENTOS_ESEC = (
--     ('1', 'Ciências Sociais e da Educação'),
--     ('2', 'Comunicação, Artes e Design'),
--     ('3', 'Línguas, Literaturas e Culturas'),
--     ('4', 'Ciências Exatas, Naturais e Desporto '),
-- )


-- CURSOS_ESEC = (
--     ('1', 'Ciências da Comunicação'),
--     ('2', 'Design de Comunicação'),
--     ('3', 'Desporto'),
--     ('4', 'Educação Básica'),
--     ('5', 'Educação Social'),
--     ('6', 'Imagem Animada'),
-- )

INSERT INTO Horario (inicio,fim) VALUES ('12:00','14:00');

INSERT INTO Campus VALUES ('1','Penha');
INSERT INTO Campus VALUES ('2','Gambelas');
INSERT INTO Campus VALUES ('3','Portimao');


INSERT INTO UnidadeOrganica (ID,Sigla,Nome,CampusID) VALUES ('1','ESEC', 'Escola Superior de Educação e Comunicação','1'),
('2','ESGHT', 'Escola Superior de Gestão Hotelaria e Turismo','3'),
('3','ESS', 'Escola Superior de Saúde','2'),
('4','ISE', 'Instituto Superior de Engenharia','1'),
('5','FCHS', 'Faculdade de Ciências Humanas e Sociais','2'),
('6','FCT', 'Faculdade de Ciências e Tecnologias','2'),
('7','FE', 'Faculdade de Economia','2'),
('8','DCBM', 'Departamento de Ciências Biomédicas e Medicina','2');

INSERT INTO Departamento (ID,Sigla,Nome,UnidadeOrganicaID) VALUES ('1','CSE','Ciências Sociais e da Educação','1'),
('2','CAD','Comunicação, Artes e Design','1'),
('3','LLC','Línguas, Literaturas e Culturas','1'),
('4','CNND','Ciências Exatas, Naturais e Desporto','1');

INSERT INTO Curso (ID, Sigla, Nome, Unidadeorganica) VALUES ('1','CC' ,'Ciências da Comunicação','1'),
('2','DC' ,'Design de Comunicação','1'),
('3','Desporto' ,'Desporto','1'),
('4','EB' ,'Educação Básica','1'),
('5','ES' ,'Educação Social','1'),
('6','IA' ,'Imagem Animada','1');

INSERT INTO Departamento (ID,Sigla,Nome,UnidadeOrganicaID) VALUES ('5','ESGHT','Escola Superior de Gestão Hotelaria e Turismo','2');

INSERT INTO Curso (ID, Sigla, Nome, Unidadeorganica) VALUES ('7', 'Gestão', 'Gestão','2'),
('8','GH', 'Gestão Hoteleira','2'),
('9', 'Marketing', 'Marketing','2'),
('10', 'Turismo', 'Turismo','2');

INSERT INTO Departamento (ID,Sigla,Nome,UnidadeOrganicaID) VALUES ('6','ESS','Escola Superior de Saúde','3');

INSERT INTO Curso (ID, Sigla, Nome, Unidadeorganica) VALUES ('11', 'Bioengenharia', 'Bioengenharia','3'),
('12', 'CBL', 'Ciências Biomédicas Laboratoriais','3'),
('13', 'DN', 'Dietética e Nutrição','3'),
('14', 'Enfermagem', 'Enfermagem','3'),
('15', 'Farmácia', 'Farmácia','3'),
('16', 'IMR', 'Imagem Médica e Radioterapia','3'),
('17', 'Ortoprotesia', 'Ortoprotesia','3'),
('18', 'TF', 'Terapia da Fala','3');

INSERT INTO Departamento (ID,Sigla,Nome,UnidadeOrganicaID) VALUES ('7', 'EA', 'Engenharia Alimentar','4'),
('8','EC' , 'Engenharia Civil','4'),
('9','EE' , 'Engenharia Eletrotécnica','4'),
('10','EM' , 'Engenharia Mecânica','4');

INSERT INTO Curso (ID, Sigla, Nome, Unidadeorganica) VALUES ('19','EA', 'Engenharia Alimentar','4'),
('20','EC', 'Engenharia Civil','4'),
('21','EEE', 'Engenharia Elétrica e Eletrónica','4'),
('22','EM', 'Engenharia Mecânica','4'),
('23','TSA', 'Tecnologia e Segurança Alimentar','4'),
('24','TIC', 'Tecnologias de Informação e Comunicação','4');

INSERT INTO Departamento (ID,Sigla,Nome,UnidadeOrganicaID) VALUES ('20','PCE', 'Psicologia e Ciências da Educação','5'),
('11','AH', 'Artes e Humanidades','5');

INSERT INTO Curso (ID, Sigla, Nome, Unidadeorganica) VALUES ('25', 'AV', 'Artes Visuais','5'),
('26', 'CEF', 'Ciências da Educação e da Formação','5'),
('27', 'LC', 'Línguas e Comunicação','5'),
('28', 'LLC', 'Línguas, Literaturas e Culturas','5'),
('29','PCA', 'Património Cultural e Arqueologia','5'),
('30','Psicologia', 'Psicologia','5');

INSERT INTO Departamento (ID,Sigla,Nome,UnidadeOrganicaID) VALUES ('12','CBB', 'Ciências Biológicas e Bioengenharia','6'),
('13','CTMA', 'Ciências da terra, do mar e do ambiente','6'),
('14','EEI', 'Engenharia Eletrónica e Informática','6'),
('15','Física', 'Física','6'),
('16','Matemática', 'Matemática','6'),
('17','QF', 'Química e Farmácia','6');

INSERT INTO Curso (ID, Sigla, Nome, Unidadeorganica) VALUES ('31', 'Agronomia', 'Agronomia','6'),
('32', 'AP', 'Arquitetura Paisagista','6'),
('33', 'Bioengenharia', 'Bioengenharia','6'),
('34', 'Biologia', 'Biologia','6'),
('35', 'BM', 'Biologia Marinha','6'),
('36', 'Bioquímica', 'Bioquímica','6'),
('37', 'Biotecnologia', 'Biotecnologia','6'),
('38', 'EI', 'Engenharia Informática','6'),
('39', 'GMC', 'Gestão Marinha e Costeira','6'),
('40', 'MAEG', 'Matemática Aplicada à Economia e à Gestão','6'),
('41', 'CF', 'Ciências Farmacêuticas','6');

INSERT INTO Departamento (ID,Sigla,Nome,UnidadeOrganicaID) VALUES ('18', 'FE', 'Faculdade de Economia','7');

INSERT INTO Curso (ID, Sigla, Nome, Unidadeorganica) VALUES ('42', 'Economia', 'Economia','7'),
('43', 'GE', 'Gestão de Empresas','7'),
('44', 'Sociologia', 'Sociologia','7');

INSERT INTO Departamento (ID,Sigla,Nome,UnidadeOrganicaID) VALUES ('19', 'DCBM', 'Departamento de Ciências Biomédicas e Medicina','8');

INSERT INTO Curso (ID, Sigla, Nome, Unidadeorganica) VALUES ('45', 'CB', 'Ciências Biomédicas','8'),
('46', 'Medicina', 'Medicina','8'),
('47', 'Oncologia', 'Oncologia','8');
