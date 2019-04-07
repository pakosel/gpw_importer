CREATE SEQUENCE public.quotes_1_id_seq
  INCREMENT 1
  MINVALUE 0
  NO MAXVALUE
  START 0
  CACHE 1;
ALTER TABLE public.quotes_1_id_seq
  OWNER TO postgres;

  
CREATE TABLE public.quotes
(
  id integer NOT NULL DEFAULT nextval('quotes_1_id_seq'::regclass),
  name character varying(100),
  ticker character varying(100),
  date date NOT NULL,
  price numeric(10,4) NOT NULL,
  CONSTRAINT quotes_1_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.quotes
  OWNER TO postgres;
