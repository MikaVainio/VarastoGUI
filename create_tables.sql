-- CREATE TABLES AND SEQUENCES FOR THE RASEKO LENDING DATABASE

BEGIN;


CREATE TABLE IF NOT EXISTS public.henkilo
(
    henkilo_id character varying NOT NULL,
    roolinimitys character varying(20) NOT NULL,
    etunimi character varying(20) NOT NULL,
    sukunimi character varying(20) NOT NULL,
    PRIMARY KEY (henkilo_id)
);

COMMENT ON COLUMN public.henkilo.henkilo_id
    IS 'User identity: SAMAccountName -> student number or teachers username';

CREATE TABLE IF NOT EXISTS public.rooli
(
    roolinimitys character varying(20) NOT NULL,
    PRIMARY KEY (roolinimitys)
);

);


CREATE TABLE IF NOT EXISTS public.tuote
(
    viivakoodi character varying(30) NOT NULL,
    tuote_id integer NOT NULL,
    tuoteryhma_id integer NOT NULL,
    nimike character varying(50) NOT NULL,
    hankintapaikka character varying(50) NOT NULL,
    kustannuspaikka character varying(10) NOT NULL,
    tuotekuva bytea,
    PRIMARY KEY (viivakoodi)
);

COMMENT ON COLUMN public.tuote.viivakoodi
    IS 'Identifier of the product -> Barcode';

COMMENT ON COLUMN public.tuote.tuote_id
    IS 'Autonumbered produckt id for products without EAN Code';

COMMENT ON COLUMN public.tuote.hankintapaikka
    IS 'Supplier of the product';

COMMENT ON COLUMN public.tuote.kustannuspaikka
    IS 'Accounting code for expenses';

COMMENT ON COLUMN public.tuote.tuotekuva
    IS 'Picture of the product';

CREATE TABLE IF NOT EXISTS public.tuoteryhma
(
    tuoteryhma_id integer NOT NULL,
    ryhman_nimi character varying(50) NOT NULL,
    PRIMARY KEY (tuoteryhma_id)
);

CREATE TABLE IF NOT EXISTS public.varasto
(
    varasto_id character varying(20) NOT NULL,
    varastotyyppi_id integer NOT NULL,
    varaston_nimi character varying(30) NOT NULL,
    PRIMARY KEY (varasto_id)
);

CREATE TABLE IF NOT EXISTS public.varastotapahtuma
(
    tapahtuma_id integer NOT NULL,
    arkistotunnus uuid NOT NULL,
    varasto_id character varying(20) NOT NULL,
    viivakoodi character varying(30) NOT NULL,
    maara real NOT NULL,
    aikaleima date NOT NULL,
    palautuspaiva date NOT NULL,
    asiakas_id character varying NOT NULL,
    varastonhoitaja_id character varying NOT NULL,
    PRIMARY KEY (tapahtuma_id)
);

COMMENT ON COLUMN public.varastotapahtuma.tapahtuma_id
    IS 'varastotapahtuma_id allows relations to tables created in the future. At the moment a dummy id';

COMMENT ON COLUMN public.varastotapahtuma.arkistotunnus
    IS 'Field type UUID identifies 2 phase transaction';

COMMENT ON COLUMN public.varastotapahtuma.viivakoodi
    IS 'Identifier of the product -> Barcode';

COMMENT ON COLUMN public.varastotapahtuma.maara
    IS 'Amount of products in the transaction';

COMMENT ON COLUMN public.varastotapahtuma.aikaleima
    IS 'Transaction date, default value today';

COMMENT ON COLUMN public.varastotapahtuma.palautuspaiva
    IS 'Default value today';

COMMENT ON COLUMN public.varastotapahtuma.asiakas_id
    IS 'User identity: SAMAccountName -> student number or teachers username';

COMMENT ON COLUMN public.varastotapahtuma.varastonhoitaja_id
    IS 'User identity: SAMAccountName -> student number or teachers username';

CREATE TABLE IF NOT EXISTS public.varastotyyppi
(
    varastotyyppi_id integer NOT NULL,
    varastotyyppi_nimi character varying(30) NOT NULL,
    PRIMARY KEY (varastotyyppi_id)
);

ALTER TABLE public.henkilo
    ADD FOREIGN KEY (roolinimitys)
    REFERENCES public.rooli (roolinimitys)
    NOT VALID;


ALTER TABLE public.tuote
    ADD FOREIGN KEY (tuoteryhma_id)
    REFERENCES public.tuoteryhma (tuoteryhma_id)
    NOT VALID;


ALTER TABLE public.varasto
    ADD FOREIGN KEY (varastotyyppi_id)
    REFERENCES public.varastotyyppi (varastotyyppi_id)
    NOT VALID;


ALTER TABLE public.varastotapahtuma
    ADD FOREIGN KEY (asiakas_id)
    REFERENCES public.henkilo (henkilo_id)
    NOT VALID;


ALTER TABLE public.varastotapahtuma
    ADD FOREIGN KEY (varastonhoitaja_id)
    REFERENCES public.henkilo (henkilo_id)
    NOT VALID;


ALTER TABLE public.varastotapahtuma
    ADD FOREIGN KEY (viivakoodi)
    REFERENCES public.tuote (viivakoodi)
    NOT VALID;


ALTER TABLE public.varastotapahtuma
    ADD FOREIGN KEY (varasto_id)
    REFERENCES public.varasto (varasto_id)
    NOT VALID;

END;