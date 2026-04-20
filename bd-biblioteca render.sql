CREATE TABLE usuarios (
id SERIAL PRIMARY KEY,
usuario VARCHAR(50),
password VARCHAR(50)
);

INSERT INTO usuarios (usuario,password)
VALUES ('marcos','2319');

CREATE TABLE libros (
id SERIAL PRIMARY KEY,
titulo VARCHAR(100),
autor VARCHAR(100),
anio INT,
precio DECIMAL
);

SELECT * FROM usuarios;
SELECT * FROM libros;