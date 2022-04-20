-- PROCEDURE FOR TRANSFERING A PRODUCT FROM A WAREHOUSET TO ANOTHER WAREHOUSE AS TRANSACTION
CREATE
OR REPLACE PROCEDURE public.varastosiirto(
	varastosta character varying,
	varastoon character varying,
	tuote_id character varying,
	tuote_maara real,
	asiakas character varying,
	v_henkilo character varying,
	tap_paiva date DEFAULT CURRENT_DATE,
	pal_paiva date DEFAULT CURRENT_DATE,
	a_tunnus uuid DEFAULT uuid_generate_v4()
) 

LANGUAGE 'plpgsql' -- Functionality of the procedure in BODY section

AS $ BODY $ -- Transaction 2 entries to accounting table: crediting and debiting warehouse accounts
BEGIN
INSERT INTO
	varastotapahtuma (
		arkistotunnus,
		varasto_id,
		viivakoodi,
		maara,
		aikaleima,
		palautuspaiva,
		asiakas_id,
		varastonhoitaja_id
	)
VALUES
	(
		a_tunnus,
		varastosta,
		tuote_id,
		tuote_maara * -1,
		tap_paiva,
		pal_paiva,
		asiakas,
		v_henkilo
	);

INSERT INTO
	varastotapahtuma (
		arkistotunnus,
		varasto_id,
		viivakoodi,
		maara,
		aikaleima,
		palautuspaiva,
		asiakas_id,
		varastonhoitaja_id
	)
VALUES
	(
		a_tunnus,
		varastoon,
		tuote_id,
		tuote_maara,
		tap_paiva,
		pal_paiva,
		asiakas,
		v_henkilo
	);

END;

$ BODY $;