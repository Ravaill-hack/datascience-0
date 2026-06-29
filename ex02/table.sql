CREATE TABLE data_2022_oct (
    event_time DATETIME PRIMARY KEY,
    event_type VARCHAR(4),
    product_id INT,
    price NUMERIC(10, 2),
    user_id INT,
    user_session UUID
)

