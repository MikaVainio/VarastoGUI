-- A VIEW FOR CALCULATING TOTALS BY WAREHOUSE AND PRODUCT -HUMAN READABLE

CREATE OR REPLACE VIEW public.saldolista
 AS
 SELECT varasto.varaston_nimi,
    tuote.nimike,
    sum(varastotapahtuma.maara) AS saldo
   FROM tuote
     JOIN varastotapahtuma ON tuote.viivakoodi = varastotapahtuma.viivakoodi
     JOIN varasto ON varasto.varasto_id = varastotapahtuma.varasto_id
  GROUP BY varasto.varaston_nimi, tuote.nimike
  ORDER BY varasto.varaston_nimi;

ALTER TABLE public.saldolista
    OWNER TO postgres;
