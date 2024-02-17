ALTER TABLE transaction
    ADD COLUMN standard_cost float4;

UPDATE transaction
SET standard_cost = CASE
                        WHEN standard_cost_char IS NOT NULL THEN CAST(REPLACE(standard_cost_char, ',', '.') AS float4)
                        ELSE NULL
    END;

ALTER TABLE transaction
    DROP COLUMN standard_cost_char;

