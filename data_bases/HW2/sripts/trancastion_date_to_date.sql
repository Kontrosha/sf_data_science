ALTER TABLE transaction ADD COLUMN transaction_date_new DATE;

UPDATE transaction
SET transaction_date_new = TO_DATE(transaction_date, 'DD.MM.YYYY');

ALTER TABLE transaction DROP COLUMN transaction_date;

ALTER TABLE transaction RENAME COLUMN transaction_date_new TO transaction_date;
