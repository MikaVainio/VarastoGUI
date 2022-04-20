CREATE
OR REPLACE VIEW public.lainassa AS
SELECT
    varastotapahtuma.varasto_id,
    varastotapahtuma.asiakas_id,
    varastotapahtuma.viivakoodi
FROM
    varastotapahtuma
    JOIN varasto ON varastotapahtuma.varasto_id = varasto.varasto_id
    JOIN varastotyyppi ON varastotyyppi.varastotyyppi_id = varasto.varastotyyppi_id

-- When varastotyyppi id is 4 the product is in "lended to a student" type of warehouse
WHERE
    varastotyyppi.varastotyyppi_id = 4

-- By grouping records of the resultset are coupled to single lender and product    
GROUP BY
    varastotapahtuma.varasto_id,
    varastotapahtuma.asiakas_id,
    varastotapahtuma.viivakoodi
    
-- if total is more than 0 lending is active    
HAVING
    sum(varastotapahtuma.maara) > 0

ORDER BY
    varastotapahtuma.varasto_id,
    varastotapahtuma.asiakas_id;

ALTER TABLE
    public.lainassa OWNER TO postgres;