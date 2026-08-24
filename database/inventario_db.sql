--
-- PostgreSQL database dump
--

-- Dumped from database version 15.6
-- Dumped by pg_dump version 15.6

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: inventario_db; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE inventario_db WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Spanish_Venezuela.1252';

ALTER DATABASE inventario_db OWNER TO postgres;

\connect inventario_db

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: public; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA public;

ALTER SCHEMA public OWNER TO postgres;

--
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA public IS 'standard public schema';

--
-- Name: actualizar_stock_automatico(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.actualizar_stock_automatico() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    IF (NEW.tipo = 'Entrada') THEN
        UPDATE cantidades 
        SET stock_actual = stock_actual + NEW.cantidad,
            ultima_actualizacion = CURRENT_TIMESTAMP
        WHERE product_id = NEW.product_id;
    ELSIF (NEW.tipo = 'Salida') THEN
        UPDATE cantidades 
        SET stock_actual = stock_actual - NEW.cantidad,
            ultima_actualizacion = CURRENT_TIMESTAMP
        WHERE product_id = NEW.product_id;
    END IF;
    RETURN NEW;
END;
$$;

ALTER FUNCTION public.actualizar_stock_automatico() OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: cantidades; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cantidades (
    id integer NOT NULL,
    product_id integer NOT NULL,
    stock_actual integer DEFAULT 0,
    ultima_actualizacion timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    stock_minimo integer DEFAULT 5
);

ALTER TABLE public.cantidades OWNER TO postgres;

--
-- Name: cantidades_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.cantidades_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE public.cantidades_id_seq OWNER TO postgres;

--
-- Name: cantidades_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.cantidades_id_seq OWNED BY public.cantidades.id;

--
-- Name: category; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.category (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);

ALTER TABLE public.category OWNER TO postgres;

--
-- Name: category_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.category_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE public.category_id_seq OWNER TO postgres;

--
-- Name: category_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.category_id_seq OWNED BY public.category.id;

--
-- Name: department; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.department (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    location character varying(150)
);

ALTER TABLE public.department OWNER TO postgres;

--
-- Name: department_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.department_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE public.department_id_seq OWNER TO postgres;

--
-- Name: department_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.department_id_seq OWNED BY public.department.id;

--
-- Name: foto; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.foto (
    id integer NOT NULL,
    url_imagen text NOT NULL,
    nombre character varying(100),
    product_id integer NOT NULL
);

ALTER TABLE public.foto OWNER TO postgres;

--
-- Name: COLUMN foto.url_imagen; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.foto.url_imagen IS 'Almacena la dirección web o ruta local de la imagen';

--
-- Name: COLUMN foto.product_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN public.foto.product_id IS 'Relación con la tabla product mediante su ID';

--
-- Name: foto_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.foto_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE public.foto_id_seq OWNER TO postgres;

--
-- Name: foto_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.foto_id_seq OWNED BY public.foto.id;

--
-- Name: movement; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.movement (
    id integer NOT NULL,
    tipo character varying(50) NOT NULL,
    cantidad integer NOT NULL,
    fecha timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    motivo text,
    product_id integer NOT NULL,
    user_id integer NOT NULL,
    origin_dept_id integer,
    dest_dept_id integer,
    detail_reason text
);

ALTER TABLE public.movement OWNER TO postgres;

--
-- Name: movement_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.movement_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE public.movement_id_seq OWNER TO postgres;

--
-- Name: movement_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.movement_id_seq OWNED BY public.movement.id;

--
-- Name: product; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.product (
    id integer NOT NULL,
    status character varying(100) NOT NULL,
    name character varying(150) NOT NULL,
    description text,
    precio real NOT NULL,
    category_id integer NOT NULL,
    model character varying(100),
    serial character varying(100),
    supplier_id integer
);

ALTER TABLE public.product OWNER TO postgres;

--
-- Name: product_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.product_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE public.product_id_seq OWNER TO postgres;

--
-- Name: product_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.product_id_seq OWNED BY public.product.id;

--
-- Name: supplier; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.supplier (
    id integer NOT NULL,
    name character varying(150) NOT NULL,
    phone character varying(20),
    email character varying(100)
);

ALTER TABLE public.supplier OWNER TO postgres;

--
-- Name: supplier_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.supplier_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE public.supplier_id_seq OWNER TO postgres;

--
-- Name: supplier_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.supplier_id_seq OWNED BY public.supplier.id;

--
-- Name: user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."user" (
    id integer NOT NULL,
    username character varying(150) NOT NULL,
    password character varying(150) NOT NULL,
    role character varying(50) DEFAULT 'consulta'::character varying NOT NULL
);

ALTER TABLE public."user" OWNER TO postgres;

--
-- Name: user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE public.user_id_seq OWNER TO postgres;

--
-- Name: user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_id_seq OWNED BY public."user".id;

--
-- Name: cantidades id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cantidades ALTER COLUMN id SET DEFAULT nextval('public.cantidades_id_seq'::regclass);

--
-- Name: category id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.category ALTER COLUMN id SET DEFAULT nextval('public.category_id_seq'::regclass);

--
-- Name: department id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.department ALTER COLUMN id SET DEFAULT nextval('public.department_id_seq'::regclass);

--
-- Name: foto id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.foto ALTER COLUMN id SET DEFAULT nextval('public.foto_id_seq'::regclass);

--
-- Name: movement id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.movement ALTER COLUMN id SET DEFAULT nextval('public.movement_id_seq'::regclass);

--
-- Name: product id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.product ALTER COLUMN id SET DEFAULT nextval('public.product_id_seq'::regclass);

--
-- Name: supplier id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.supplier ALTER COLUMN id SET DEFAULT nextval('public.supplier_id_seq'::regclass);

--
-- Name: user id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user" ALTER COLUMN id SET DEFAULT nextval('public.user_id_seq'::regclass);

--
-- Data for Name: cantidades; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.cantidades (id, product_id, stock_actual, ultima_actualizacion, stock_minimo) FROM stdin;
1	1	10	2026-01-15 10:00:00	5
2	2	5	2026-01-15 10:00:00	3
3	3	0	2026-01-15 10:00:00	2
\.


--
-- Data for Name: category; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.category (id, name) FROM stdin;
1	Electrónica
2	Muebles
3	Herramientas
4	Accesorios
5	Material de Oficina
6	Seguridad
7	Limpieza
8	Jardinería
9	Deportes
\.


--
-- Data for Name: department; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.department (id, name, location) FROM stdin;
1	Logística	Almacén Norte
2	Ventas	Oficina Central
3	Producción	Planta Sur
\.


--
-- Data for Name: foto; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.foto (id, url_imagen, nombre, product_id) FROM stdin;
1	https://ejemplo.com/foto1.jpg	Producto1	1
2	https://ejemplo.com/foto2.jpg	Producto2	2
3	https://ejemplo.com/foto3.jpg	Producto3	3
\.


--
-- Data for Name: movement; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.movement (id, tipo, cantidad, fecha, motivo, product_id, user_id, origin_dept_id, dest_dept_id, detail_reason) FROM stdin;
1	Entrada	10	2026-01-15 09:00:00	Compra inicial	1	1	\N	1	\N
2	Salida	2	2026-01-15 10:30:00	Venta	1	1	1	\N	\N
3	Entrada	5	2026-01-16 08:00:00	Reabastecimiento	2	1	\N	2	\N
4	Salida	1	2026-01-16 09:15:00	Uso interno	2	1	2	\N	\N
5	Entrada	3	2026-01-17 11:00:00	Devolución	3	1	3	3	\N
6	Salida	3	2026-01-17 14:30:00	Daño	3	1	3	\N	\N
7	Salida	1	2026-01-18 16:00:00	Préstamo	1	1	1	2	\N
\.


--
-- Data for Name: product; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.product (id, status, name, description, precio, category_id, model, serial, supplier_id) FROM stdin;
1	Activo	Laptop HP	Laptop HP Pavilion	850.5	1	HP-15	SN12345	1
2	Activo	Silla	Oficina	120	2	Ergo	SN54321	2
3	Activo	Martillo	Herramienta manual	15.5	3	M-100	SN67890	3
4	Activo	Monitor	LG 24 pulgadas	250	1	LG-24	SN11111	1
5	Activo	Teclado	Inalámbrico	45	4	K-100	SN22222	3
6	Activo	Mouse	Óptico	25	4	M-200	SN33333	3
7	Inactivo	Impresora	Láser	300	5	P-500	SN44444	2
8	Activo	Cámara	Seguridad	200	6	SC-100	SN55555	1
9	Activo	Escritorio	Madera	350	2	E-200	SN66666	2
10	Activo	Taladro	Eléctrico	150	3	T-300	SN77777	3
\.


--
-- Data for Name: supplier; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.supplier (id, name, phone, email) FROM stdin;
\.


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."user" (id, username, password, role) FROM stdin;
1	admin	pbkdf2:sha256:1000000$r6kOItqubuKe3Nc9$4563d4d94e844e7373c776d3ff69264b3ed2c3e75ebd5edb28a1126b32aee20f	admin
\.


--
-- Name: cantidades_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.cantidades_id_seq', 3, true);


--
-- Name: category_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.category_id_seq', 9, true);


--
-- Name: department_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.department_id_seq', 3, true);


--
-- Name: foto_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.foto_id_seq', 3, true);


--
-- Name: movement_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.movement_id_seq', 7, true);


--
-- Name: product_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.product_id_seq', 63, true);


--
-- Name: supplier_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.supplier_id_seq', 1, false);


--
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_id_seq', 1, true);


--
-- Name: cantidades cantidades_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cantidades
    ADD CONSTRAINT cantidades_pkey PRIMARY KEY (id);


--
-- Name: cantidades cantidades_product_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cantidades
    ADD CONSTRAINT cantidades_product_id_key UNIQUE (product_id);


--
-- Name: category category_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.category
    ADD CONSTRAINT category_pkey PRIMARY KEY (id);


--
-- Name: department department_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.department
    ADD CONSTRAINT department_pkey PRIMARY KEY (id);


--
-- Name: foto foto_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.foto
    ADD CONSTRAINT foto_pkey PRIMARY KEY (id);


--
-- Name: movement movement_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.movement
    ADD CONSTRAINT movement_pkey PRIMARY KEY (id);


--
-- Name: product product_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.product
    ADD CONSTRAINT product_pkey PRIMARY KEY (id);


--
-- Name: supplier supplier_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.supplier
    ADD CONSTRAINT supplier_pkey PRIMARY KEY (id);


--
-- Name: category unique_category_name; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.category
    ADD CONSTRAINT unique_category_name UNIQUE (name);


--
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- Name: user user_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_username_key UNIQUE (username);


--
-- Name: idx_movement_fecha; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_movement_fecha ON public.movement USING btree (fecha);


--
-- Name: idx_movement_tipo; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_movement_tipo ON public.movement USING btree (tipo);


--
-- Name: idx_product_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_product_name ON public.product USING btree (name);


--
-- Name: idx_product_sku; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_product_sku ON public.product USING btree (status);


--
-- Name: movement tr_actualizar_stock; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER tr_actualizar_stock AFTER INSERT ON public.movement FOR EACH ROW EXECUTE FUNCTION public.actualizar_stock_automatico();


--
-- Name: cantidades fk_producto; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cantidades
    ADD CONSTRAINT fk_producto FOREIGN KEY (product_id) REFERENCES public.product(id) ON DELETE CASCADE;


--
-- Name: foto fk_producto; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.foto
    ADD CONSTRAINT fk_producto FOREIGN KEY (product_id) REFERENCES public.product(id) ON DELETE CASCADE;


--
-- Name: movement movement_dest_dept_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.movement
    ADD CONSTRAINT movement_dest_dept_id_fkey FOREIGN KEY (dest_dept_id) REFERENCES public.department(id);


--
-- Name: movement movement_origin_dept_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.movement
    ADD CONSTRAINT movement_origin_dept_id_fkey FOREIGN KEY (origin_dept_id) REFERENCES public.department(id);


--
-- Name: movement movement_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.movement
    ADD CONSTRAINT movement_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.product(id);


--
-- Name: product product_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.product
    ADD CONSTRAINT product_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.category(id);


--
-- Name: product product_supplier_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.product
    ADD CONSTRAINT product_supplier_id_fkey FOREIGN KEY (supplier_id) REFERENCES public.supplier(id);


--
-- PostgreSQL database dump complete
--
