ALTER TABLE transaction ADD COLUMN list_price float4;

UPDATE transaction
SET list_price = CAST(REPLACE(list_price_char, ',', '.') AS float4);

ALTER TABLE transaction DROP COLUMN list_price_char;