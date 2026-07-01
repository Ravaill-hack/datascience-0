DROP TABLE IF EXISTS data_2022_oct;

CREATE TABLE data_2022_oct (
    event_time TIMESTAMP,
    event_type VARCHAR,
    product_id INT,
    price NUMERIC(10, 2),
    user_id INT,
    user_session UUID,
    id BIGSERIAL PRIMARY KEY
);

COPY data_2022_oct (event_time, event_type, product_id, price, user_id, user_session)
FROM '/data/data_2022_oct.csv'
DELIMITER ','
CSV HEADER;

