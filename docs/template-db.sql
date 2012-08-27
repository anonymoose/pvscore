--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

SET search_path = public, pg_catalog;

ALTER TABLE ONLY public.core_status DROP CONSTRAINT status_username_fkey;
ALTER TABLE ONLY public.core_status_event_reason DROP CONSTRAINT status_event_reason_event_id_fkey;
ALTER TABLE ONLY public.core_status DROP CONSTRAINT status_event_id_fkey;
ALTER TABLE ONLY public.crm_product_pricing DROP CONSTRAINT product_pricing_product_id_fkey;
ALTER TABLE ONLY public.crm_product_pricing DROP CONSTRAINT product_pricing_campaign_id_fkey;
ALTER TABLE ONLY public.crm_product DROP CONSTRAINT product_company_id_fkey;
ALTER TABLE ONLY public.crm_order_item DROP CONSTRAINT order_item_user_created_fkey;
ALTER TABLE ONLY public.crm_order_item DROP CONSTRAINT order_item_product_id_fkey;
ALTER TABLE ONLY public.crm_order_item DROP CONSTRAINT order_item_order_id_fkey;
ALTER TABLE ONLY public.crm_customer DROP CONSTRAINT customer_user_created_fkey;
ALTER TABLE ONLY public.crm_customer DROP CONSTRAINT customer_user_assigned_fkey;
ALTER TABLE ONLY public.crm_customer_order DROP CONSTRAINT customer_order_user_created_fkey;
ALTER TABLE ONLY public.crm_customer_order DROP CONSTRAINT customer_order_customer_id_fkey;
ALTER TABLE ONLY public.crm_customer DROP CONSTRAINT customer_campaign_id_fkey;
ALTER TABLE ONLY public.crm_customer_order DROP CONSTRAINT crm_customer_order_campaign_id_fkey;
ALTER TABLE ONLY public.crm_company DROP CONSTRAINT crm_company_status_id_fkey;
ALTER TABLE ONLY public.crm_company DROP CONSTRAINT crm_company_enterprise_id_fkey;
ALTER TABLE ONLY public.crm_communication DROP CONSTRAINT crm_communication_user_created_fkey;
ALTER TABLE ONLY public.crm_communication DROP CONSTRAINT crm_communication_company_id_fkey;
ALTER TABLE ONLY public.crm_billing DROP CONSTRAINT crm_billing_user_created_fkey;
ALTER TABLE ONLY public.crm_billing DROP CONSTRAINT crm_billing_status_id_fkey;
ALTER TABLE ONLY public.crm_billing_history DROP CONSTRAINT crm_billing_history_order_id_fkey;
ALTER TABLE ONLY public.crm_billing_history DROP CONSTRAINT crm_billing_history_customer_id_fkey;
ALTER TABLE ONLY public.crm_billing_history DROP CONSTRAINT crm_billing_history_billing_id_fkey;
ALTER TABLE ONLY public.crm_billing DROP CONSTRAINT crm_billing_customer_id_fkey;
ALTER TABLE ONLY public.core_user DROP CONSTRAINT core_user_enterprise_id_fkey;
ALTER TABLE ONLY public.core_status_event DROP CONSTRAINT core_status_event_enterprise_id_fkey;
ALTER TABLE ONLY public.cms_template DROP CONSTRAINT cms_template_enterprise_id_fkey;
ALTER TABLE ONLY public.cms_site DROP CONSTRAINT cms_site_user_created_fkey;
ALTER TABLE ONLY public.cms_site DROP CONSTRAINT cms_site_company_id_fkey;
ALTER TABLE ONLY public.cms_page DROP CONSTRAINT cms_page_user_created_fkey;
ALTER TABLE ONLY public.cms_page DROP CONSTRAINT cms_page_template_id_fkey;
ALTER TABLE ONLY public.cms_page DROP CONSTRAINT cms_page_site_id_fkey;
ALTER TABLE ONLY public.cms_page_content DROP CONSTRAINT cms_page_content_page_id_fkey;
ALTER TABLE ONLY public.cms_page_content DROP CONSTRAINT cms_page_content_content_id_fkey;
ALTER TABLE ONLY public.cms_content DROP CONSTRAINT cms_content_user_created_fkey;
ALTER TABLE ONLY public.cms_content DROP CONSTRAINT cms_content_site_id_fkey;
ALTER TABLE ONLY public.crm_campaign DROP CONSTRAINT campaign_company_id_fkey;
ALTER TABLE ONLY public.crm_appointment DROP CONSTRAINT appointment_user_created_fkey;
ALTER TABLE ONLY public.crm_appointment DROP CONSTRAINT appointment_user_completed_fkey;
ALTER TABLE ONLY public.crm_appointment DROP CONSTRAINT appointment_status_id_fkey;
ALTER TABLE ONLY public.crm_appointment DROP CONSTRAINT appointment_customer_id_fkey;
ALTER TABLE ONLY public.core_user DROP CONSTRAINT users_pkey;
ALTER TABLE ONLY public.core_status DROP CONSTRAINT status_pkey;
ALTER TABLE ONLY public.core_status_event_reason DROP CONSTRAINT status_event_reason_pkey;
ALTER TABLE ONLY public.core_status_event DROP CONSTRAINT status_event_pkey;
ALTER TABLE ONLY public.crm_product_pricing DROP CONSTRAINT product_pricing_pkey;
ALTER TABLE ONLY public.crm_product DROP CONSTRAINT product_pkey;
ALTER TABLE ONLY public.crm_order_item DROP CONSTRAINT order_item_pkey;
ALTER TABLE ONLY public.crm_customer DROP CONSTRAINT customer_pkey;
ALTER TABLE ONLY public.crm_customer_order DROP CONSTRAINT customer_order_pkey;
ALTER TABLE ONLY public.crm_enterprise DROP CONSTRAINT crm_enterprise_pkey;
ALTER TABLE ONLY public.crm_communication DROP CONSTRAINT crm_communication_pkey;
ALTER TABLE ONLY public.crm_billing DROP CONSTRAINT crm_billing_pkey;
ALTER TABLE ONLY public.crm_billing_history DROP CONSTRAINT crm_billing_history_pkey;
ALTER TABLE ONLY public.crm_company DROP CONSTRAINT company_pkey;
ALTER TABLE ONLY public.cms_template DROP CONSTRAINT cms_template_pkey;
ALTER TABLE ONLY public.cms_site DROP CONSTRAINT cms_site_pkey;
ALTER TABLE ONLY public.cms_page DROP CONSTRAINT cms_page_pkey;
ALTER TABLE ONLY public.cms_page_content DROP CONSTRAINT cms_page_content_pkey;
ALTER TABLE ONLY public.cms_content DROP CONSTRAINT cms_content_pkey;
ALTER TABLE ONLY public.crm_campaign DROP CONSTRAINT campaign_pkey;
ALTER TABLE ONLY public.core_attribute_value DROP CONSTRAINT attribute_value_pkey;
ALTER TABLE ONLY public.core_attribute DROP CONSTRAINT attribute_pkey;
ALTER TABLE ONLY public.core_association DROP CONSTRAINT association_pkey;
ALTER TABLE ONLY public.crm_appointment DROP CONSTRAINT appointment_pkey;
ALTER TABLE public.crm_product_pricing ALTER COLUMN product_pricing_id DROP DEFAULT;
ALTER TABLE public.crm_product ALTER COLUMN product_id DROP DEFAULT;
ALTER TABLE public.crm_order_item ALTER COLUMN order_item_id DROP DEFAULT;
ALTER TABLE public.crm_enterprise ALTER COLUMN enterprise_id DROP DEFAULT;
ALTER TABLE public.crm_customer_order ALTER COLUMN order_id DROP DEFAULT;
ALTER TABLE public.crm_customer ALTER COLUMN customer_id DROP DEFAULT;
ALTER TABLE public.crm_company ALTER COLUMN company_id DROP DEFAULT;
ALTER TABLE public.crm_communication ALTER COLUMN comm_id DROP DEFAULT;
ALTER TABLE public.crm_campaign ALTER COLUMN campaign_id DROP DEFAULT;
ALTER TABLE public.crm_billing_history ALTER COLUMN billing_history_id DROP DEFAULT;
ALTER TABLE public.crm_billing ALTER COLUMN billing_id DROP DEFAULT;
ALTER TABLE public.crm_appointment ALTER COLUMN appointment_id DROP DEFAULT;
ALTER TABLE public.core_status_event_reason ALTER COLUMN reason_id DROP DEFAULT;
ALTER TABLE public.core_status_event ALTER COLUMN event_id DROP DEFAULT;
ALTER TABLE public.core_status ALTER COLUMN status_id DROP DEFAULT;
ALTER TABLE public.core_attribute_value ALTER COLUMN attr_value_id DROP DEFAULT;
ALTER TABLE public.core_attribute ALTER COLUMN attr_id DROP DEFAULT;
ALTER TABLE public.core_association ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.cms_template ALTER COLUMN template_id DROP DEFAULT;
ALTER TABLE public.cms_site ALTER COLUMN site_id DROP DEFAULT;
ALTER TABLE public.cms_page_content ALTER COLUMN page_content_id DROP DEFAULT;
ALTER TABLE public.cms_page ALTER COLUMN page_id DROP DEFAULT;
ALTER TABLE public.cms_content ALTER COLUMN content_id DROP DEFAULT;
DROP SEQUENCE public.stock_symbol_symbol_id_seq;
DROP SEQUENCE public.status_status_id_seq;
DROP SEQUENCE public.status_event_reason_reason_id_seq;
DROP SEQUENCE public.status_event_event_id_seq;
DROP SEQUENCE public.short_volume_quote_id_seq;
DROP SEQUENCE public.sec_filing_report_id_seq;
DROP SEQUENCE public.product_product_id_seq;
DROP SEQUENCE public.product_pricing_product_pricing_id_seq;
DROP SEQUENCE public.order_item_order_item_id_seq;
DROP SEQUENCE public.eod_quote_quote_id_seq;
DROP SEQUENCE public.customer_order_order_id_seq;
DROP SEQUENCE public.customer_customer_id_seq;
DROP TABLE public.crm_product_pricing;
DROP TABLE public.crm_product;
DROP TABLE public.crm_order_item;
DROP SEQUENCE public.crm_enterprise_enterprise_id_seq;
DROP TABLE public.crm_enterprise;
DROP TABLE public.crm_customer_order;
DROP TABLE public.crm_customer;
DROP SEQUENCE public.crm_communication_comm_id_seq;
DROP TABLE public.crm_communication;
DROP SEQUENCE public.crm_billing_history_billing_history_id_seq;
DROP TABLE public.crm_billing_history;
DROP SEQUENCE public.crm_billing_billing_id_seq;
DROP TABLE public.crm_billing;
DROP TABLE public.core_user;
DROP TABLE public.core_status_event_reason;
DROP TABLE public.core_status_event;
DROP TABLE public.core_status;
DROP SEQUENCE public.company_company_id_seq;
DROP TABLE public.crm_company;
DROP SEQUENCE public.cms_template_template_id_seq;
DROP TABLE public.cms_template;
DROP SEQUENCE public.cms_site_site_id_seq;
DROP TABLE public.cms_site;
DROP SEQUENCE public.cms_page_page_id_seq;
DROP SEQUENCE public.cms_page_content_page_content_id_seq;
DROP TABLE public.cms_page_content;
DROP TABLE public.cms_page;
DROP SEQUENCE public.cms_content_content_id_seq;
DROP TABLE public.cms_content;
DROP SEQUENCE public.campaign_campaign_id_seq;
DROP TABLE public.crm_campaign;
DROP SEQUENCE public.attribute_value_attr_value_id_seq;
DROP TABLE public.core_attribute_value;
DROP SEQUENCE public.attribute_attr_id_seq;
DROP TABLE public.core_attribute;
DROP SEQUENCE public.association_id_seq;
DROP TABLE public.core_association;
DROP SEQUENCE public.appointment_appointment_id_seq;
DROP TABLE public.crm_appointment;
DROP SCHEMA public;
--
-- Name: public; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA public;


--
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON SCHEMA public IS 'standard public schema';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: crm_appointment; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE crm_appointment (
    appointment_id integer NOT NULL,
    customer_id integer,
    title character varying(255),
    description text,
    calendar_type character varying(50),
    remind boolean,
    user_created character varying(50),
    create_dt date DEFAULT now(),
    delete_dt date,
    user_completed character varying(50),
    completed_dt date,
    start_dt date,
    start_time character varying(20),
    end_time character varying(20),
    end_dt date,
    private boolean,
    phone character varying(20),
    data_1 character varying(250),
    data_2 character varying(250),
    status_id integer
);


--
-- Name: appointment_appointment_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE appointment_appointment_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: appointment_appointment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE appointment_appointment_id_seq OWNED BY crm_appointment.appointment_id;


--
-- Name: appointment_appointment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('appointment_appointment_id_seq', 12, true);


--
-- Name: core_association; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE core_association (
    id integer NOT NULL,
    one_id integer,
    one_type character varying(50),
    many_id integer,
    many_type character varying(50),
    create_dt date DEFAULT now()
);


--
-- Name: association_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE association_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: association_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE association_id_seq OWNED BY core_association.id;


--
-- Name: association_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('association_id_seq', 1, false);


--
-- Name: core_attribute; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE core_attribute (
    attr_id integer NOT NULL,
    fk_type character varying(50),
    attr_name character varying(100),
    attr_type character varying(32)
);


--
-- Name: attribute_attr_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE attribute_attr_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: attribute_attr_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE attribute_attr_id_seq OWNED BY core_attribute.attr_id;


--
-- Name: attribute_attr_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('attribute_attr_id_seq', 1, false);


--
-- Name: core_attribute_value; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE core_attribute_value (
    attr_value_id integer NOT NULL,
    attr_id integer,
    attr_value character varying(2000),
    fk_type character varying(50),
    fk_id integer
);


--
-- Name: attribute_value_attr_value_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE attribute_value_attr_value_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: attribute_value_attr_value_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE attribute_value_attr_value_id_seq OWNED BY core_attribute_value.attr_value_id;


--
-- Name: attribute_value_attr_value_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('attribute_value_attr_value_id_seq', 1, false);


--
-- Name: crm_campaign; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE crm_campaign (
    campaign_id integer NOT NULL,
    company_id integer,
    name character varying(100),
    create_dt date DEFAULT now(),
    delete_dt date,
    type character varying(50)
);


--
-- Name: campaign_campaign_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE campaign_campaign_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: campaign_campaign_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE campaign_campaign_id_seq OWNED BY crm_campaign.campaign_id;


--
-- Name: campaign_campaign_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('campaign_campaign_id_seq', 2, true);


--
-- Name: cms_content; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE cms_content (
    content_id integer NOT NULL,
    site_id integer,
    name character varying(50),
    data text,
    create_dt date DEFAULT now(),
    delete_dt date,
    user_created character varying(50),
    type character varying(50) DEFAULT 'html'::character varying
);


--
-- Name: cms_content_content_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE cms_content_content_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: cms_content_content_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE cms_content_content_id_seq OWNED BY cms_content.content_id;


--
-- Name: cms_content_content_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('cms_content_content_id_seq', 15, true);


--
-- Name: cms_page; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE cms_page (
    page_id integer NOT NULL,
    site_id integer,
    name character varying(50),
    create_dt date DEFAULT now(),
    delete_dt date,
    user_created character varying(50),
    seo_title character varying(512),
    seo_keywords character varying(1000),
    seo_description character varying(1000),
    url_path character varying(1000),
    template_id integer,
    top_level_menu boolean,
    published boolean,
    menu_sort_order integer,
    site_root boolean DEFAULT false
);


--
-- Name: cms_page_content; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE cms_page_content (
    page_content_id integer NOT NULL,
    page_id integer,
    content_id integer,
    name character varying(50)
);


--
-- Name: cms_page_content_page_content_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE cms_page_content_page_content_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: cms_page_content_page_content_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE cms_page_content_page_content_id_seq OWNED BY cms_page_content.page_content_id;


--
-- Name: cms_page_content_page_content_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('cms_page_content_page_content_id_seq', 14, true);


--
-- Name: cms_page_page_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE cms_page_page_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: cms_page_page_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE cms_page_page_id_seq OWNED BY cms_page.page_id;


--
-- Name: cms_page_page_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('cms_page_page_id_seq', 9, true);


--
-- Name: cms_site; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE cms_site (
    site_id integer NOT NULL,
    domain character varying(50),
    company_id integer,
    description character varying(100),
    root_page_id integer,
    create_dt date DEFAULT now(),
    delete_dt date,
    user_created character varying(50)
);


--
-- Name: cms_site_site_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE cms_site_site_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: cms_site_site_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE cms_site_site_id_seq OWNED BY cms_site.site_id;


--
-- Name: cms_site_site_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('cms_site_site_id_seq', 3, true);


--
-- Name: cms_template; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE cms_template (
    template_id integer NOT NULL,
    package character varying(50),
    name character varying(50),
    description character varying(500),
    path character varying(1000),
    create_dt date DEFAULT now(),
    delete_dt date,
    enterprise_id integer
);


--
-- Name: cms_template_template_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE cms_template_template_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: cms_template_template_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE cms_template_template_id_seq OWNED BY cms_template.template_id;


--
-- Name: cms_template_template_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('cms_template_template_id_seq', 8, true);


--
-- Name: crm_company; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE crm_company (
    company_id integer NOT NULL,
    name character varying(50),
    create_dt date DEFAULT now(),
    delete_dt date,
    enterprise_id integer,
    status_id integer
);


--
-- Name: company_company_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE company_company_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: company_company_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE company_company_id_seq OWNED BY crm_company.company_id;


--
-- Name: company_company_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('company_company_id_seq', 3, true);


--
-- Name: core_status; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE core_status (
    status_id integer NOT NULL,
    event_id integer,
    customer_id integer,
    fk_type character varying(50),
    fk_id integer,
    username character varying(75),
    note text,
    create_dt date DEFAULT now()
);


--
-- Name: core_status_event; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE core_status_event (
    event_id integer NOT NULL,
    event_type character varying(50),
    short_name character varying(50),
    display_name character varying(50),
    phase character varying(50),
    create_dt date DEFAULT now(),
    end_dt date,
    claim boolean,
    finalize boolean,
    is_system boolean,
    milestone_complete boolean,
    note_req boolean,
    dashboard boolean,
    reason_req boolean,
    change_status boolean,
    touch boolean,
    "position" integer,
    enterprise_id integer
);


--
-- Name: core_status_event_reason; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE core_status_event_reason (
    reason_id integer NOT NULL,
    event_id integer,
    name character varying(50),
    create_dt date DEFAULT now(),
    delete_dt date
);


--
-- Name: core_user; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE core_user (
    username character varying(50) NOT NULL,
    password character varying(75),
    fname character varying(50),
    lname character varying(50),
    create_dt date DEFAULT now(),
    delete_dt date,
    email character varying(50),
    api_key character varying(50),
    type character varying(50),
    allow_cms boolean DEFAULT false,
    enterprise_id integer
);


--
-- Name: crm_billing; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE crm_billing (
    billing_id integer NOT NULL,
    customer_id integer,
    note character varying(50),
    status_id integer,
    type character varying(50) DEFAULT 'Credit Card'::character varying,
    account_holder character varying(50),
    account_addr character varying(50),
    account_city character varying(50),
    account_state character varying(50),
    account_country character varying(50),
    account_zip character varying(50),
    cc_token character varying(50),
    cc_last_4 integer,
    cc_exp character varying(7),
    create_dt date DEFAULT now(),
    delete_dt date,
    user_created character varying(50),
    is_primary boolean DEFAULT false
);


--
-- Name: crm_billing_billing_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE crm_billing_billing_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: crm_billing_billing_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE crm_billing_billing_id_seq OWNED BY crm_billing.billing_id;


--
-- Name: crm_billing_billing_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('crm_billing_billing_id_seq', 19, true);


--
-- Name: crm_billing_history; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE crm_billing_history (
    billing_history_id integer NOT NULL,
    billing_id integer,
    order_id integer,
    customer_id integer,
    status_msg character varying(50),
    parent character varying(50),
    reference character varying(50),
    notes character varying(100),
    amount character varying(50),
    authorized character varying(50),
    date character varying(50),
    transaction character varying(20),
    uid character varying(40),
    create_dt date DEFAULT now(),
    delete_dt date
);


--
-- Name: crm_billing_history_billing_history_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE crm_billing_history_billing_history_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: crm_billing_history_billing_history_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE crm_billing_history_billing_history_id_seq OWNED BY crm_billing_history.billing_history_id;


--
-- Name: crm_billing_history_billing_history_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('crm_billing_history_billing_history_id_seq', 16, true);


--
-- Name: crm_communication; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE crm_communication (
    comm_id integer NOT NULL,
    company_id integer,
    name character varying(50),
    data text,
    create_dt date DEFAULT now(),
    delete_dt date,
    user_created character varying(50),
    type character varying(50) DEFAULT 'html'::character varying,
    url character varying(256),
    from_addr character varying(50),
    subject character varying(256)
);


--
-- Name: crm_communication_comm_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE crm_communication_comm_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: crm_communication_comm_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE crm_communication_comm_id_seq OWNED BY crm_communication.comm_id;


--
-- Name: crm_communication_comm_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('crm_communication_comm_id_seq', 1, true);


--
-- Name: crm_customer; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE crm_customer (
    customer_id integer NOT NULL,
    fname character varying(50),
    lname character varying(50),
    title character varying(50),
    company_name character varying(50),
    password character varying(50),
    campaign_id integer,
    orig_campaign_id integer,
    status_id integer,
    email character varying(50),
    create_dt date DEFAULT now(),
    delete_dt date,
    user_created character varying(50),
    user_assigned character varying(50),
    addr1 character varying(50),
    addr2 character varying(50),
    city character varying(50),
    state character varying(50),
    zip character varying(50),
    phone character varying(20),
    alt_phone character varying(20),
    fax character varying(20),
    notes text,
    cid_0 character varying(50),
    cid_1 character varying(50),
    cid_2 character varying(50),
    cid_3 character varying(50),
    cid_4 character varying(50),
    cid_5 character varying(50),
    cid_6 character varying(50),
    cid_7 character varying(50),
    cid_8 character varying(50),
    cid_9 character varying(50),
    ref_0 character varying(50),
    ref_1 character varying(50),
    ref_2 character varying(50),
    country character varying(50) DEFAULT 'US'::character varying
);


--
-- Name: crm_customer_order; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE crm_customer_order (
    order_id integer NOT NULL,
    customer_id integer,
    campaign_id integer,
    create_dt date DEFAULT now(),
    delete_dt date,
    status_id integer,
    user_created character varying(50),
    cancel_dt date
);


--
-- Name: crm_enterprise; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE crm_enterprise (
    enterprise_id integer NOT NULL,
    name character varying(50),
    create_dt date DEFAULT now(),
    delete_dt date
);


--
-- Name: crm_enterprise_enterprise_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE crm_enterprise_enterprise_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: crm_enterprise_enterprise_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE crm_enterprise_enterprise_id_seq OWNED BY crm_enterprise.enterprise_id;


--
-- Name: crm_enterprise_enterprise_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('crm_enterprise_enterprise_id_seq', 1, true);


--
-- Name: crm_order_item; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE crm_order_item (
    order_item_id integer NOT NULL,
    order_id integer,
    name character varying(100),
    unit_cost double precision,
    unit_price double precision,
    create_dt date DEFAULT now(),
    delete_dt date,
    quantity double precision,
    status_id integer,
    user_created character varying(50),
    product_id integer
);


--
-- Name: crm_product; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE crm_product (
    product_id integer NOT NULL,
    name character varying(100),
    description character varying(200),
    company_id integer,
    create_dt date DEFAULT now(),
    delete_dt date
);


--
-- Name: crm_product_pricing; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE crm_product_pricing (
    product_pricing_id integer NOT NULL,
    campaign_id integer,
    product_id integer,
    wholesale_price double precision,
    retail_price double precision,
    bill_method_type character varying(3),
    bill_freq_type character varying(3),
    create_dt date DEFAULT now(),
    delete_dt date
);


--
-- Name: customer_customer_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE customer_customer_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: customer_customer_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE customer_customer_id_seq OWNED BY crm_customer.customer_id;


--
-- Name: customer_customer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('customer_customer_id_seq', 19, true);


--
-- Name: customer_order_order_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE customer_order_order_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: customer_order_order_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE customer_order_order_id_seq OWNED BY crm_customer_order.order_id;


--
-- Name: customer_order_order_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('customer_order_order_id_seq', 43, true);


--
-- Name: eod_quote_quote_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE eod_quote_quote_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: eod_quote_quote_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('eod_quote_quote_id_seq', 18900798, true);


--
-- Name: order_item_order_item_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE order_item_order_item_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: order_item_order_item_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE order_item_order_item_id_seq OWNED BY crm_order_item.order_item_id;


--
-- Name: order_item_order_item_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('order_item_order_item_id_seq', 54, true);


--
-- Name: product_pricing_product_pricing_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE product_pricing_product_pricing_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: product_pricing_product_pricing_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE product_pricing_product_pricing_id_seq OWNED BY crm_product_pricing.product_pricing_id;


--
-- Name: product_pricing_product_pricing_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('product_pricing_product_pricing_id_seq', 10, true);


--
-- Name: product_product_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE product_product_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: product_product_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE product_product_id_seq OWNED BY crm_product.product_id;


--
-- Name: product_product_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('product_product_id_seq', 6, true);


--
-- Name: sec_filing_report_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE sec_filing_report_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: sec_filing_report_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('sec_filing_report_id_seq', 90784, true);


--
-- Name: short_volume_quote_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE short_volume_quote_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: short_volume_quote_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('short_volume_quote_id_seq', 54541, true);


--
-- Name: status_event_event_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE status_event_event_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: status_event_event_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE status_event_event_id_seq OWNED BY core_status_event.event_id;


--
-- Name: status_event_event_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('status_event_event_id_seq', 11, true);


--
-- Name: status_event_reason_reason_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE status_event_reason_reason_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: status_event_reason_reason_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE status_event_reason_reason_id_seq OWNED BY core_status_event_reason.reason_id;


--
-- Name: status_event_reason_reason_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('status_event_reason_reason_id_seq', 1, false);


--
-- Name: status_status_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE status_status_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: status_status_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE status_status_id_seq OWNED BY core_status.status_id;


--
-- Name: status_status_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('status_status_id_seq', 108, true);


--
-- Name: stock_symbol_symbol_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE stock_symbol_symbol_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: stock_symbol_symbol_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('stock_symbol_symbol_id_seq', 6903, true);


--
-- Name: content_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE cms_content ALTER COLUMN content_id SET DEFAULT nextval('cms_content_content_id_seq'::regclass);


--
-- Name: page_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE cms_page ALTER COLUMN page_id SET DEFAULT nextval('cms_page_page_id_seq'::regclass);


--
-- Name: page_content_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE cms_page_content ALTER COLUMN page_content_id SET DEFAULT nextval('cms_page_content_page_content_id_seq'::regclass);


--
-- Name: site_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE cms_site ALTER COLUMN site_id SET DEFAULT nextval('cms_site_site_id_seq'::regclass);


--
-- Name: template_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE cms_template ALTER COLUMN template_id SET DEFAULT nextval('cms_template_template_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE core_association ALTER COLUMN id SET DEFAULT nextval('association_id_seq'::regclass);


--
-- Name: attr_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE core_attribute ALTER COLUMN attr_id SET DEFAULT nextval('attribute_attr_id_seq'::regclass);


--
-- Name: attr_value_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE core_attribute_value ALTER COLUMN attr_value_id SET DEFAULT nextval('attribute_value_attr_value_id_seq'::regclass);


--
-- Name: status_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE core_status ALTER COLUMN status_id SET DEFAULT nextval('status_status_id_seq'::regclass);


--
-- Name: event_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE core_status_event ALTER COLUMN event_id SET DEFAULT nextval('status_event_event_id_seq'::regclass);


--
-- Name: reason_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE core_status_event_reason ALTER COLUMN reason_id SET DEFAULT nextval('status_event_reason_reason_id_seq'::regclass);


--
-- Name: appointment_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE crm_appointment ALTER COLUMN appointment_id SET DEFAULT nextval('appointment_appointment_id_seq'::regclass);


--
-- Name: billing_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE crm_billing ALTER COLUMN billing_id SET DEFAULT nextval('crm_billing_billing_id_seq'::regclass);


--
-- Name: billing_history_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE crm_billing_history ALTER COLUMN billing_history_id SET DEFAULT nextval('crm_billing_history_billing_history_id_seq'::regclass);


--
-- Name: campaign_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE crm_campaign ALTER COLUMN campaign_id SET DEFAULT nextval('campaign_campaign_id_seq'::regclass);


--
-- Name: comm_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE crm_communication ALTER COLUMN comm_id SET DEFAULT nextval('crm_communication_comm_id_seq'::regclass);


--
-- Name: company_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE crm_company ALTER COLUMN company_id SET DEFAULT nextval('company_company_id_seq'::regclass);


--
-- Name: customer_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE crm_customer ALTER COLUMN customer_id SET DEFAULT nextval('customer_customer_id_seq'::regclass);


--
-- Name: order_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE crm_customer_order ALTER COLUMN order_id SET DEFAULT nextval('customer_order_order_id_seq'::regclass);


--
-- Name: enterprise_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE crm_enterprise ALTER COLUMN enterprise_id SET DEFAULT nextval('crm_enterprise_enterprise_id_seq'::regclass);


--
-- Name: order_item_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE crm_order_item ALTER COLUMN order_item_id SET DEFAULT nextval('order_item_order_item_id_seq'::regclass);


--
-- Name: product_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE crm_product ALTER COLUMN product_id SET DEFAULT nextval('product_product_id_seq'::regclass);


--
-- Name: product_pricing_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE crm_product_pricing ALTER COLUMN product_pricing_id SET DEFAULT nextval('product_pricing_product_pricing_id_seq'::regclass);


--
-- Data for Name: cms_content; Type: TABLE DATA; Schema: public; Owner: -
--

COPY cms_content (content_id, site_id, name, data, create_dt, delete_dt, user_created, type) FROM stdin;
3	3	Products :: body-left	<br />\n<p style="text-align: justify; font-size: 11px; line-height: 14px; margin: 0px 0px 14px; padding: 0px;">\n\t<span class="Apple-style-span" style="border-collapse: separate; color: rgb(0, 0, 0); font-family: Times; font-style: normal; font-variant: normal; font-weight: normal; letter-spacing: normal; line-height: normal; orphans: 2; text-indent: 0px; text-transform: none; white-space: normal; widows: 2; word-spacing: 0px; font-size: medium;"><span class="Apple-style-span" style="font-family: Arial,Helvetica,sans; font-size: 11px; text-align: justify;">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris sit amet semper urna. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed sit amet purus arcu, in pharetra sem. Maecenas fringilla placerat ante eu fringilla. Aenean nec dolor malesuada lorem rutrum ornare. Proin aliquam fringilla purus sed vulputate. Donec vitae mi at lacus condimentum rhoncus. Sed quis ipsum tristique libero consectetur dictum. Nunc tempor tempus justo at facilisis. Curabitur mollis odio sodales lorem consequat id auctor ante sagittis. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Ut et ipsum at leo placerat luctus. Vivamus convallis rutrum facilisis. Nam interdum vulputate placerat. Ut pellentesque commodo cursus. Nam auctor vestibulum erat et luctus.</span></span></p>\n<br class="Apple-interchange-newline" />\n	2010-10-07	\N	kenneth.bedwell@gmail.com	html
4	3	Products :: body-right	<br />\n<p style="text-align: justify; font-size: 11px; line-height: 14px; margin: 0px 0px 14px; padding: 0px;">\n\t<span class="Apple-style-span" style="border-collapse: separate; color: rgb(0, 0, 0); font-family: Times; font-style: normal; font-variant: normal; font-weight: normal; letter-spacing: normal; line-height: normal; orphans: 2; text-indent: 0px; text-transform: none; white-space: normal; widows: 2; word-spacing: 0px; font-size: medium;"><span class="Apple-style-span" style="font-family: Arial,Helvetica,sans; font-size: 11px; text-align: justify;">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris sit amet semper urna. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed sit amet purus arcu, in pharetra sem. Maecenas fringilla placerat ante eu fringilla. Aenean nec dolor malesuada lorem rutrum ornare. Proin aliquam fringilla purus sed vulputate. Donec vitae mi at lacus condimentum rhoncus. Sed quis ipsum tristique libero consectetur dictum. Nunc tempor tempus justo at facilisis. Curabitur mollis odio sodales lorem consequat id auctor ante sagittis. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Ut et ipsum at leo placerat luctus. Vivamus convallis rutrum facilisis. Nam interdum vulputate placerat. Ut pellentesque commodo cursus. Nam auctor vestibulum erat et luctus.</span></span></p>\n<br class="Apple-interchange-newline" />\n	2010-10-07	\N	kenneth.bedwell@gmail.com	html
5	3	Testimonials :: content	<br />\nThis is where a bunch of testimonials would go.<br />\n<ol>\n\t<li>\n\t\tFirst Guy</li>\n\t<li>\n\t\tSecond Guy</li>\n\t<li>\n\t\tThird Guy</li>\n</ol>\n	2010-10-07	\N	kenneth.bedwell@gmail.com	html
6	3	About Us :: body-top	<span class="Apple-style-span" style="border-collapse: separate; color: rgb(0, 0, 0); font-family: Times; font-style: normal; font-variant: normal; font-weight: normal; letter-spacing: normal; line-height: normal; orphans: 2; text-indent: 0px; text-transform: none; white-space: normal; widows: 2; word-spacing: 0px; font-size: medium;"><span class="Apple-style-span" style="font-family: Arial,Helvetica,sans; font-size: 11px; text-align: justify;">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris sit amet semper urna. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed sit amet purus arcu, in pharetra sem. Maecenas fringilla placerat ante eu fringilla. Aenean nec dolor malesuada lorem rutrum ornare. Proin aliquam fringilla purus sed vulputate. Donec vitae mi at lacus condimentum rhoncus. Sed quis ipsum tristique libero consectetur dictum. Nunc tempor tempus justo at facilisis. Curabitur mollis odio sodales lorem consequat id auctor ante sagittis. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Ut et ipsum at leo placerat luctus. Vivamus convallis rutrum facilisis. Nam interdum vulputate placerat. Ut pellentesque commodo cursus. Nam auctor vestibulum erat et luctus.</span></span>	2010-10-07	\N	kenneth.bedwell@gmail.com	html
7	3	About Us :: body-left	<span class="Apple-style-span" style="border-collapse: separate; color: rgb(0, 0, 0); font-family: Times; font-style: normal; font-variant: normal; font-weight: normal; letter-spacing: normal; line-height: normal; orphans: 2; text-indent: 0px; text-transform: none; white-space: normal; widows: 2; word-spacing: 0px; font-size: medium;"><span class="Apple-style-span" style="font-family: Arial,Helvetica,sans; font-size: 11px; text-align: justify;">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris sit amet semper urna. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed sit amet purus arcu, in pharetra sem. Maecenas fringilla placerat ante eu fringilla. Aenean nec dolor malesuada lorem rutrum ornare. Proin aliquam fringilla purus sed vulputate. Donec vitae mi at lacus condimentum rhoncus. Sed quis ipsum tristique libero consectetur dictum. Nunc tempor tempus justo at facilisis. Curabitur mollis odio sodales lorem consequat id auctor ante sagittis. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Ut et ipsum at leo placerat luctus. Vivamus convallis rutrum facilisis. Nam interdum vulputate placerat. Ut pellentesque commodo cursus. Nam auctor vestibulum erat et luctus.</span></span>	2010-10-07	\N	kenneth.bedwell@gmail.com	html
10	3	FAQ :: content	<br />\n<strong>Frequently Asked Questions</strong>\n<ol>\n\t<li>\n\t\t<strong>What is Wealth Makers?<br />\n\t\t</strong></li>\n\t<li>\n\t\t<strong>How do you make predictions?<br />\n\t\t</strong></li>\n\t<li>\n\t\t<strong>etc.<br />\n\t\t</strong></li>\n</ol>\n<br />\n	2010-10-07	\N	kenneth.bedwell@gmail.com	html
11	3	Sign Up :: content	Signup!&nbsp; Our stuff is awesome<br />\n<br />\n<br />\n<div id="frm_customer">\n\t<form action="/crm/customer/save" method="POST">\n\t\t<div style="display: none;">\n\t\t\t&nbsp;</div>\n\t\t<input name="customer_id" type="hidden" value="1" />&nbsp;\n\t\t<table>\n\t\t\t<tbody>\n\t\t\t\t<tr valign="top">\n\t\t\t\t\t<td>\n\t\t\t\t\t\t<table>\n\t\t\t\t\t\t\t<tbody>\n\t\t\t\t\t\t\t\t<tr>\n\t\t\t\t\t\t\t\t\t<td>\n\t\t\t\t\t\t\t\t\t\t<label for="fname">First Name</label></td>\n\t\t\t\t\t\t\t\t\t<td>\n\t\t\t\t\t\t\t\t\t\t<input id="fname" name="fname" size="50" type="text" /></td>\n\t\t\t\t\t\t\t\t</tr>\n\t\t\t\t\t\t\t\t<tr>\n\t\t\t\t\t\t\t\t\t<td>\n\t\t\t\t\t\t\t\t\t\t<label for="lname">Last Name</label></td>\n\t\t\t\t\t\t\t\t\t<td>\n\t\t\t\t\t\t\t\t\t\t<input id="lname" name="lname" size="50" type="text" /></td>\n\t\t\t\t\t\t\t\t</tr>\n\t\t\t\t\t\t\t\t<tr>\n\t\t\t\t\t\t\t\t\t<td>\n\t\t\t\t\t\t\t\t\t\t<label for="password">Password</label></td>\n\t\t\t\t\t\t\t\t\t<td>\n\t\t\t\t\t\t\t\t\t\t<input id="password" name="password" size="50" type="text" /></td>\n\t\t\t\t\t\t\t\t</tr>\n\t\t\t\t\t\t\t\t<tr>\n\t\t\t\t\t\t\t\t\t<td>\n\t\t\t\t\t\t\t\t\t\t<label for="email">Email</label></td>\n\t\t\t\t\t\t\t\t\t<td>\n\t\t\t\t\t\t\t\t\t\t<input id="email" name="email" size="50" type="text" /></td>\n\t\t\t\t\t\t\t\t</tr>\n\t\t\t\t\t\t\t\t<tr valign="top">\n\t\t\t\t\t\t\t\t\t<td>\n\t\t\t\t\t\t\t\t\t\t&nbsp;</td>\n\t\t\t\t\t\t\t\t\t<td>\n\t\t\t\t\t\t\t\t\t\t&nbsp;</td>\n\t\t\t\t\t\t\t\t</tr>\n\t\t\t\t\t\t\t\t<tr>\n\t\t\t\t\t\t\t\t\t<td>\n\t\t\t\t\t\t\t\t\t\t<label for="title">Title</label></td>\n\t\t\t\t\t\t\t\t\t<td>\n\t\t\t\t\t\t\t\t\t\t<input id="title" name="title" size="50" type="text" /></td>\n\t\t\t\t\t\t\t\t</tr>\n\t\t\t\t\t\t\t\t<tr>\n\t\t\t\t\t\t\t\t\t<td>\n\t\t\t\t\t\t\t\t\t\t<label for="company_name">Company Name</label></td>\n\t\t\t\t\t\t\t\t\t<td>\n\t\t\t\t\t\t\t\t\t\t<input id="addr2" name="addr2" size="50" type="text" /></td>\n\t\t\t\t\t\t\t\t</tr>\n\t\t\t\t\t\t\t\t<tr>\n\t\t\t\t\t\t\t\t\t<td>\n\t\t\t\t\t\t\t\t\t\t<label for="addr1">Address</label></td>\n\t\t\t\t\t\t\t\t\t<td>\n\t\t\t\t\t\t\t\t\t\t<input id="addr1" name="addr1" size="50" type="text" /></td>\n\t\t\t\t\t\t\t\t</tr>\n\t\t\t\t\t\t\t\t<tr>\n\t\t\t\t\t\t\t\t\t<td>\n\t\t\t\t\t\t\t\t\t\t<label for="addr2">&nbsp;</label></td>\n\t\t\t\t\t\t\t\t\t<td>\n\t\t\t\t\t\t\t\t\t\t<input id="addr2" name="addr2" size="50" type="text" /></td>\n\t\t\t\t\t\t\t\t</tr>\n\t\t\t\t\t\t\t\t<tr>\n\t\t\t\t\t\t\t\t\t<td>\n\t\t\t\t\t\t\t\t\t\t<label for="city">City</label></td>\n\t\t\t\t\t\t\t\t\t<td>\n\t\t\t\t\t\t\t\t\t\t<input id="city" name="city" size="50" type="text" /></td>\n\t\t\t\t\t\t\t\t</tr>\n\t\t\t\t\t\t\t\t<tr>\n\t\t\t\t\t\t\t\t\t<td>\n\t\t\t\t\t\t\t\t\t\t<label for="state">State</label></td>\n\t\t\t\t\t\t\t\t\t<td>\n\t\t\t\t\t\t\t\t\t\t<input id="state" name="state" size="50" type="text" /></td>\n\t\t\t\t\t\t\t\t</tr>\n\t\t\t\t\t\t\t\t<tr>\n\t\t\t\t\t\t\t\t\t<td>\n\t\t\t\t\t\t\t\t\t\t<label for="zip">Zip</label></td>\n\t\t\t\t\t\t\t\t\t<td>\n\t\t\t\t\t\t\t\t\t\t<input id="zip" name="zip" size="50" type="text" /></td>\n\t\t\t\t\t\t\t\t</tr>\n\t\t\t\t\t\t\t\t<tr>\n\t\t\t\t\t\t\t\t\t<td>\n\t\t\t\t\t\t\t\t\t\t<label for="phone">Phone</label></td>\n\t\t\t\t\t\t\t\t\t<td>\n\t\t\t\t\t\t\t\t\t\t<input id="phone" name="phone" size="20" type="text" /></td>\n\t\t\t\t\t\t\t\t</tr>\n\t\t\t\t\t\t\t\t<tr>\n\t\t\t\t\t\t\t\t\t<td>\n\t\t\t\t\t\t\t\t\t\t<label for="alt_phone">Alternate Phone</label></td>\n\t\t\t\t\t\t\t\t\t<td>\n\t\t\t\t\t\t\t\t\t\t<input id="alt_phone" name="alt_phone" size="20" type="text" /></td>\n\t\t\t\t\t\t\t\t</tr>\n\t\t\t\t\t\t\t\t<tr>\n\t\t\t\t\t\t\t\t\t<td>\n\t\t\t\t\t\t\t\t\t\t<label for="fax">Fax</label></td>\n\t\t\t\t\t\t\t\t\t<td>\n\t\t\t\t\t\t\t\t\t\t<input id="fax" name="fax" size="20" type="text" /></td>\n\t\t\t\t\t\t\t\t</tr>\n\t\t\t\t\t\t\t\t<tr>\n\t\t\t\t\t\t\t\t\t<td nowrap="nowrap">\n\t\t\t\t\t\t\t\t\t\t<label for="bill_cc_num">Credit Card #</label></td>\n\t\t\t\t\t\t\t\t\t<td>\n\t\t\t\t\t\t\t\t\t\t<input id="bill_cc_num" name="bill_cc_num" size="16" type="text" /></td>\n\t\t\t\t\t\t\t\t</tr>\n\t\t\t\t\t\t\t\t<tr>\n\t\t\t\t\t\t\t\t\t<td nowrap="nowrap">\n\t\t\t\t\t\t\t\t\t\t<label for="cc_cvv">CVV</label></td>\n\t\t\t\t\t\t\t\t\t<td>\n\t\t\t\t\t\t\t\t\t\t<input id="bill_cc_cvv" name="bill_cc_cvv" size="4" type="text" /></td>\n\t\t\t\t\t\t\t\t</tr>\n\t\t\t\t\t\t\t\t<tr>\n\t\t\t\t\t\t\t\t\t<td>\n\t\t\t\t\t\t\t\t\t\t<label for="cc_exp">Expiration</label></td>\n\t\t\t\t\t\t\t\t\t<td>\n\t\t\t\t\t\t\t\t\t\t<input id="bill_cc_exp" name="bill_cc_exp" size="7" type="text" /></td>\n\t\t\t\t\t\t\t\t</tr>\n\t\t\t\t\t\t\t</tbody>\n\t\t\t\t\t\t</table>\n\t\t\t\t\t</td>\n\t\t\t\t</tr>\n\t\t\t\t<tr>\n\t\t\t\t\t<td colspan="2">\n\t\t\t\t\t\t&nbsp;</td>\n\t\t\t\t</tr>\n\t\t\t\t<tr>\n\t\t\t\t\t<td align="right">\n\t\t\t\t\t\t<input id="submit" name="submit" type="submit" value="Submit" /></td>\n\t\t\t\t\t<td>\n\t\t\t\t\t\t&nbsp;</td>\n\t\t\t\t\t<td>\n\t\t\t\t\t\t&nbsp;</td>\n\t\t\t\t</tr>\n\t\t\t</tbody>\n\t\t</table>\n\t</form>\n</div>	2010-10-07	\N	kenneth.bedwell@gmail.com	html
1	3	Home :: body-left	<p style="text-align: justify; font-size: 11px; line-height: 14px; margin: 0px 0px 14px; padding: 0px;">\n\t<span class="Apple-style-span" style="border-collapse: separate; color: rgb(0, 0, 0); font-family: Times; font-style: normal; font-variant: normal; font-weight: normal; letter-spacing: normal; line-height: normal; orphans: 2; text-indent: 0px; text-transform: none; white-space: normal; widows: 2; word-spacing: 0px; font-size: medium;"><span class="Apple-style-span" style="font-family: Arial,Helvetica,sans; font-size: 11px; text-align: justify;">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris sit amet semper urna. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed sit amet purus arcu, in pharetra sem. Maecenas fringilla placerat ante eu fringilla. Aenean nec dolor malesuada lorem rutrum ornare. Proin aliquam fringilla purus sed vulputate. Donec vitae mi at lacus condimentum rhoncus. Sed quis ipsum tristique libero consectetur dictum. Nunc tempor tempus justo at facilisis. Curabitur mollis odio sodales lorem consequat id auctor ante sagittis. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Ut et ipsum at leo placerat luctus. Vivamus convallis rutrum facilisis. Nam interdum vulputate placerat. Ut pellentesque commodo cursus. Nam auctor vestibulum erat et luctus.</span></span></p>\n<br class="Apple-interchange-newline" />	2010-10-07	\N	kenneth.bedwell@gmail.com	html
2	3	Home :: body-right	<p style="text-align: justify; font-size: 11px; line-height: 14px; margin: 0px 0px 14px; padding: 0px;">\n\t<span class="Apple-style-span" style="border-collapse: separate; color: rgb(0, 0, 0); font-family: Times; font-style: normal; font-variant: normal; font-weight: normal; letter-spacing: normal; line-height: normal; orphans: 2; text-indent: 0px; text-transform: none; white-space: normal; widows: 2; word-spacing: 0px; font-size: medium;"><span class="Apple-style-span" style="font-family: Arial,Helvetica,sans; font-size: 11px; text-align: justify;">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris sit amet semper urna. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed sit amet purus arcu, in pharetra sem. Maecenas fringilla placerat ante eu fringilla. Aenean nec dolor malesuada lorem rutrum ornare. Proin aliquam fringilla purus sed vulputate. Donec vitae mi at lacus condimentum rhoncus. Sed quis ipsum tristique libero consectetur dictum. Nunc tempor tempus justo at facilisis. Curabitur mollis odio sodales lorem consequat id auctor ante sagittis. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Ut et ipsum at leo placerat luctus. Vivamus convallis rutrum facilisis. Nam interdum vulputate placerat. Ut pellentesque commodo cursus. Nam auctor vestibulum erat et luctus.</span></span></p>\n<br class="Apple-interchange-newline" />	2010-10-07	\N	kenneth.bedwell@gmail.com	html
15	3	b1	{"banner1": "%3Cstrong%3Etest1x%3C%2Fstrong%3E", "banner0": "%3Cstrong%3Etest0x%3C%2Fstrong%3E", "banner3": "%3Cstrong%3Etest3x%3C%2Fstrong%3E", "banner2": "%3Cstrong%3Etest2x%3C%2Fstrong%3E", "banner4": "%3Cstrong%3Etest4%3C%2Fstrong%3E"}	2010-10-21	\N	kenneth.bedwell@gmail.com	banner
12	3	Login :: content	Login to your account<br />\n<br />\n<br />\n<form action="/portal/login/login" method="POST">\n\t<div id="dialog">\n\t\t<div style="text-align: center; padding-bottom: 10px;">\n\t\t\t&nbsp;</div>\n\t\t<table cellspacing="10" id="standard">\n\t\t\t<tbody>\n\t\t\t\t<tr>\n\t\t\t\t\t<td align="right" width="100">\n\t\t\t\t\t\tUsername</td>\n\t\t\t\t\t<td>\n\t\t\t\t\t\t<input id="username" name="username" type="text" /></td>\n\t\t\t\t</tr>\n\t\t\t\t<tr>\n\t\t\t\t\t<td align="right">\n\t\t\t\t\t\tPassword</td>\n\t\t\t\t\t<td>\n\t\t\t\t\t\t<input id="password" name="password" type="password" /></td>\n\t\t\t\t</tr>\n\t\t\t</tbody>\n\t\t</table>\n\t\t<div style="text-align: center; padding-bottom: 10px;">\n\t\t\t<input name="submit" type="submit" value="Login" /></div>\n\t</div>\n</form>	2010-10-07	\N	kenneth.bedwell@gmail.com	html
8	3	About Us :: body-right	<span class="Apple-style-span" style="border-collapse: separate; color: rgb(0, 0, 0); font-family: Times; font-style: normal; font-variant: normal; font-weight: normal; letter-spacing: normal; line-height: normal; orphans: 2; text-indent: 0px; text-transform: none; white-space: normal; widows: 2; word-spacing: 0px; font-size: medium;"><span class="Apple-style-span" style="font-family: Arial,Helvetica,sans; font-size: 11px; text-align: justify;">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris sit amet semper urna. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed sit amet purus arcu, in pharetra sem. Maecenas fringilla placerat ante eu fringilla. Aenean nec dolor malesuada lorem rutrum ornare. Proin aliquam fringilla purus sed vulputate. Donec vitae mi at lacus condimentum rhoncus. Sed quis ipsum tristique libero consectetur dictum. Nunc tempor tempus justo at facilisis. Curabitur mollis odio sodales lorem consequat id auctor ante sagittis. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Ut et ipsum at leo placerat luctus. Vivamus convallis rutrum facilisis. Nam interdum vulputate placerat. Ut pellentesque commodo cursus. Nam auctor vestibulum erat et luctus.</span></span>	2010-10-07	\N	kenneth.bedwell@gmail.com	html
9	3	Contact Us :: content	<span class="Apple-style-span" style="border-collapse: separate; color: rgb(0, 0, 0); font-family: Times; font-style: normal; font-variant: normal; font-weight: normal; letter-spacing: normal; line-height: normal; orphans: 2; text-indent: 0px; text-transform: none; white-space: normal; widows: 2; word-spacing: 0px; font-size: medium;"><span class="Apple-style-span" style="font-family: Arial,Helvetica,sans; font-size: 11px; text-align: justify;">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris sit amet semper urna. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed sit amet purus arcu, in pharetra sem. Maecenas fringilla placerat ante eu fringilla. Aenean nec dolor malesuada lorem rutrum ornare. Proin aliquam fringilla purus sed vulputate. Donec vitae mi at lacus condimentum rhoncus. Sed quis ipsum tristique libero consectetur dictum. Nunc tempor tempus justo at facilisis. Curabitur mollis odio sodales lorem consequat id auctor ante sagittis. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Ut et ipsum at leo placerat luctus. Vivamus convallis rutrum facilisis. Nam interdum vulputate placerat. Ut pellentesque commodo cursus. Nam auctor vestibulum erat et luctus.<br />\n<br />\n</span></span><span class="Apple-style-span" style="border-collapse: separate; color: rgb(0, 0, 0); font-family: Times; font-style: normal; font-variant: normal; font-weight: normal; letter-spacing: normal; line-height: normal; orphans: 2; text-indent: 0px; text-transform: none; white-space: normal; widows: 2; word-spacing: 0px; font-size: medium;"><span class="Apple-style-span" style="font-family: Arial,Helvetica,sans; font-size: 11px; text-align: justify;">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris sit amet semper urna. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed sit amet purus arcu, in pharetra sem. Maecenas fringilla placerat ante eu fringilla. Aenean nec dolor malesuada lorem rutrum ornare. Proin aliquam fringilla purus sed vulputate. Donec vitae mi at lacus condimentum rhoncus. Sed quis ipsum tristique libero consectetur dictum. Nunc tempor tempus justo at facilisis. Curabitur mollis odio sodales lorem consequat id auctor ante sagittis. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Ut et ipsum at leo placerat luctus. Vivamus convallis rutrum facilisis. Nam interdum vulputate placerat. Ut pellentesque commodo cursus. Nam auctor vestibulum erat et luctus.<br />\n<br />\n</span></span><span class="Apple-style-span" style="border-collapse: separate; color: rgb(0, 0, 0); font-family: Times; font-style: normal; font-variant: normal; font-weight: normal; letter-spacing: normal; line-height: normal; orphans: 2; text-indent: 0px; text-transform: none; white-space: normal; widows: 2; word-spacing: 0px; font-size: medium;"><span class="Apple-style-span" style="font-family: Arial,Helvetica,sans; font-size: 11px; text-align: justify;">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris sit amet semper urna. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed sit amet purus arcu, in pharetra sem. Maecenas fringilla placerat ante eu fringilla. Aenean nec dolor malesuada lorem rutrum ornare. Proin aliquam fringilla purus sed vulputate. Donec vitae mi at lacus condimentum rhoncus. Sed quis ipsum tristique libero consectetur dictum. Nunc tempor tempus justo at facilisis. Curabitur mollis odio sodales lorem consequat id auctor ante sagittis. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Ut et ipsum at leo placerat luctus. Vivamus convallis rutrum facilisis. Nam interdum vulputate placerat. Ut pellentesque commodo cursus. Nam auctor vestibulum erat et luctus.</span></span>	2010-10-07	\N	kenneth.bedwell@gmail.com	html
13	3	Thanks! :: content	Thanks for signing up.&nbsp; You will get an email shortly with your login information.<br />	2010-10-20	\N	kenneth.bedwell@gmail.com	html
14	3	Sign Up :: content	Our stuff is great.&nbsp; Buy some.<br />	2010-10-20	\N	kenneth.bedwell@gmail.com	html
\.


--
-- Data for Name: cms_page; Type: TABLE DATA; Schema: public; Owner: -
--

COPY cms_page (page_id, site_id, name, create_dt, delete_dt, user_created, seo_title, seo_keywords, seo_description, url_path, template_id, top_level_menu, published, menu_sort_order, site_root) FROM stdin;
9	3	Thanks!	2010-10-20	\N	kenneth.bedwell@gmail.com	Thanks for signing up!	\N	\N	Thanks	7	f	t	\N	f
7	3	Sign Up	2010-10-07	\N	kenneth.bedwell@gmail.com	WealthMakers - Sign Up	\N	\N	SignUp	8	t	t	1000	f
2	3	Products	2010-10-07	\N	kenneth.bedwell@gmail.com	WealthMakers - Products	Products	Stocks products and such	Products	6	t	t	20	f
6	3	FAQ	2010-10-07	\N	kenneth.bedwell@gmail.com	Frequently Asked Questions	\N	\N	FAQ	7	t	t	50	f
3	3	Testimonials	2010-10-07	\N	kenneth.bedwell@gmail.com	\N	\N	\N	Testimonials	7	t	t	30	f
4	3	About Us	2010-10-07	\N	kenneth.bedwell@gmail.com	WealthMakers - About Us	\N	\N	AboutUs	5	t	t	40	f
5	3	Contact Us	2010-10-07	\N	kenneth.bedwell@gmail.com	WealthMakers - Contact Us	\N	\N	Contact	7	t	t	500	f
8	3	Login	2010-10-07	\N	kenneth.bedwell@gmail.com	WealthMakers - Login	\N	\N	Login	7	f	t	\N	f
1	3	Home	2010-10-07	\N	kenneth.bedwell@gmail.com	WealthMakers - Home	\N	\N	Home	4	t	t	10	t
\.


--
-- Data for Name: cms_page_content; Type: TABLE DATA; Schema: public; Owner: -
--

COPY cms_page_content (page_content_id, page_id, content_id, name) FROM stdin;
3	2	3	body-left
4	2	4	body-right
10	6	10	content
5	3	5	content
6	4	6	body-top
7	4	7	body-left
8	4	8	body-right
9	5	9	content
12	8	12	content
1	1	1	body-left
2	1	2	body-right
13	9	13	content
14	7	14	content
\.


--
-- Data for Name: cms_site; Type: TABLE DATA; Schema: public; Owner: -
--

COPY cms_site (site_id, domain, company_id, description, root_page_id, create_dt, delete_dt, user_created) FROM stdin;
3	pv.com	1	\N	\N	2010-10-05	\N	kenneth.bedwell@gmail.com
\.


--
-- Data for Name: cms_template; Type: TABLE DATA; Schema: public; Owner: -
--

COPY cms_template (template_id, package, name, description, path, create_dt, delete_dt, enterprise_id) FROM stdin;
3	Test 01	index	Index page	tpl_a	2010-10-05	\N	1
4	Test 03	index	Free Website Template	tpl_c	2010-10-05	\N	1
5	Test 03	left_right_top	Left Right Columns w/ top	tpl_c	2010-10-07	\N	1
6	Test 03	left_right	Left Right Columns	tpl_c	2010-10-07	\N	1
7	Test 03	single_element	One big space in the middle	tpl_c	2010-10-07	\N	1
8	Test 03	signup	Signup form	tpl_c	2010-10-20	\N	1
\.


--
-- Data for Name: core_association; Type: TABLE DATA; Schema: public; Owner: -
--

COPY core_association (id, one_id, one_type, many_id, many_type, create_dt) FROM stdin;
\.


--
-- Data for Name: core_attribute; Type: TABLE DATA; Schema: public; Owner: -
--

COPY core_attribute (attr_id, fk_type, attr_name, attr_type) FROM stdin;
\.


--
-- Data for Name: core_attribute_value; Type: TABLE DATA; Schema: public; Owner: -
--

COPY core_attribute_value (attr_value_id, attr_id, attr_value, fk_type, fk_id) FROM stdin;
\.


--
-- Data for Name: core_status; Type: TABLE DATA; Schema: public; Owner: -
--

COPY core_status (status_id, event_id, customer_id, fk_type, fk_id, username, note, create_dt) FROM stdin;
\.


--
-- Data for Name: core_status_event; Type: TABLE DATA; Schema: public; Owner: -
--

COPY core_status_event (event_id, event_type, short_name, display_name, phase, create_dt, end_dt, claim, finalize, is_system, milestone_complete, note_req, dashboard, reason_req, change_status, touch, "position", enterprise_id) FROM stdin;
1	Customer	Test1	Test1	test	2010-09-13	\N	t	f	f	f	f	f	t	f	f	1	1
3	OrderItem	DELETED	Deleted		2010-09-16	\N	f	f	t	f	f	f	f	t	f	1	1
2	OrderItem	MODIFIED	Modified		2010-09-16	\N	f	f	t	f	f	f	f	t	f	1	1
4	CustomerOrder	MODIFIED	Modified		2010-09-16	\N	f	f	t	f	f	f	f	t	f	1	1
5	CustomerOrder	DELETED	Deleted		2010-09-16	\N	f	f	t	f	f	f	f	t	f	1	1
6	CustomerOrder	CREATED	Created		2010-09-16	\N	f	f	t	f	f	f	f	t	f	1	1
7	OrderItem	CREATED	Created		2010-09-16	\N	f	f	t	f	f	f	f	t	f	1	1
8	CustomerOrder	BILLING_DECLINED	Billing Declined	\N	2010-10-20	\N	f	f	t	f	f	f	f	f	f	1	1
9	CustomerOrder	BILLING_SUCCESS	Billing Success	\N	2010-10-20	\N	f	f	t	f	f	f	f	f	f	1	1
10	Communication	SENT	Sent Communication	\N	2010-10-22	\N	f	f	t	f	f	f	f	f	t	1	1
11	Customer	Test4	Test4	\N	2010-11-08	\N	t	f	f	t	f	f	f	t	f	1	1
\.


--
-- Data for Name: core_status_event_reason; Type: TABLE DATA; Schema: public; Owner: -
--

COPY core_status_event_reason (reason_id, event_id, name, create_dt, delete_dt) FROM stdin;
\.


--
-- Data for Name: core_user; Type: TABLE DATA; Schema: public; Owner: -
--

COPY core_user (username, password, fname, lname, create_dt, delete_dt, email, api_key, type, allow_cms, enterprise_id) FROM stdin;
kenneth.bedwell@gmail.com	4476212f8f185ba416fc0708bebcc91b	Ken	Bedwell	2010-08-21	\N	kenneth.bedwell@gmail.com	\N	Admin	t	1
aric@bludigitalmedia.com	1a1dc91c907325c69271ddf0c944bc72	Aric	Berquist	2010-11-09	\N	aric@bludigitalmedia.com	\N	Internal	t	\N
\.


--
-- Data for Name: crm_appointment; Type: TABLE DATA; Schema: public; Owner: -
--

COPY crm_appointment (appointment_id, customer_id, title, description, calendar_type, remind, user_created, create_dt, delete_dt, user_completed, completed_dt, start_dt, start_time, end_time, end_dt, private, phone, data_1, data_2, status_id) FROM stdin;
\.


--
-- Data for Name: crm_billing; Type: TABLE DATA; Schema: public; Owner: -
--

COPY crm_billing (billing_id, customer_id, note, status_id, type, account_holder, account_addr, account_city, account_state, account_country, account_zip, cc_token, cc_last_4, cc_exp, create_dt, delete_dt, user_created, is_primary) FROM stdin;
\.


--
-- Data for Name: crm_billing_history; Type: TABLE DATA; Schema: public; Owner: -
--

COPY crm_billing_history (billing_history_id, billing_id, order_id, customer_id, status_msg, parent, reference, notes, amount, authorized, date, transaction, uid, create_dt, delete_dt) FROM stdin;
\.


--
-- Data for Name: crm_campaign; Type: TABLE DATA; Schema: public; Owner: -
--

COPY crm_campaign (campaign_id, company_id, name, create_dt, delete_dt, type) FROM stdin;
1	1	UKVid01	2010-09-09	\N	\N
\.


--
-- Data for Name: crm_communication; Type: TABLE DATA; Schema: public; Owner: -
--

COPY crm_communication (comm_id, company_id, name, data, create_dt, delete_dt, user_created, type, url, from_addr, subject) FROM stdin;
\.


--
-- Data for Name: crm_company; Type: TABLE DATA; Schema: public; Owner: -
--

COPY crm_company (company_id, name, create_dt, delete_dt, enterprise_id, status_id) FROM stdin;
1	UKVid	2010-08-21	\N	1	\N
\.


--
-- Data for Name: crm_customer; Type: TABLE DATA; Schema: public; Owner: -
--

COPY crm_customer (customer_id, fname, lname, title, company_name, password, campaign_id, orig_campaign_id, status_id, email, create_dt, delete_dt, user_created, user_assigned, addr1, addr2, city, state, zip, phone, alt_phone, fax, notes, cid_0, cid_1, cid_2, cid_3, cid_4, cid_5, cid_6, cid_7, cid_8, cid_9, ref_0, ref_1, ref_2, country) FROM stdin;
\.


--
-- Data for Name: crm_customer_order; Type: TABLE DATA; Schema: public; Owner: -
--

COPY crm_customer_order (order_id, customer_id, campaign_id, create_dt, delete_dt, status_id, user_created, cancel_dt) FROM stdin;
\.


--
-- Data for Name: crm_enterprise; Type: TABLE DATA; Schema: public; Owner: -
--

COPY crm_enterprise (enterprise_id, name, create_dt, delete_dt) FROM stdin;
1	UKVid	2010-11-05	\N
\.


--
-- Data for Name: crm_order_item; Type: TABLE DATA; Schema: public; Owner: -
--

COPY crm_order_item (order_item_id, order_id, name, unit_cost, unit_price, create_dt, delete_dt, quantity, status_id, user_created, product_id) FROM stdin;
\.


--
-- Data for Name: crm_product; Type: TABLE DATA; Schema: public; Owner: -
--

COPY crm_product (product_id, name, description, company_id, create_dt, delete_dt) FROM stdin;
\.


--
-- Data for Name: crm_product_pricing; Type: TABLE DATA; Schema: public; Owner: -
--

COPY crm_product_pricing (product_pricing_id, campaign_id, product_id, wholesale_price, retail_price, bill_method_type, bill_freq_type, create_dt, delete_dt) FROM stdin;
\.


--
-- Name: appointment_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY crm_appointment
    ADD CONSTRAINT appointment_pkey PRIMARY KEY (appointment_id);


--
-- Name: association_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY core_association
    ADD CONSTRAINT association_pkey PRIMARY KEY (id);


--
-- Name: attribute_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY core_attribute
    ADD CONSTRAINT attribute_pkey PRIMARY KEY (attr_id);


--
-- Name: attribute_value_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY core_attribute_value
    ADD CONSTRAINT attribute_value_pkey PRIMARY KEY (attr_value_id);


--
-- Name: campaign_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY crm_campaign
    ADD CONSTRAINT campaign_pkey PRIMARY KEY (campaign_id);


--
-- Name: cms_content_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY cms_content
    ADD CONSTRAINT cms_content_pkey PRIMARY KEY (content_id);


--
-- Name: cms_page_content_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY cms_page_content
    ADD CONSTRAINT cms_page_content_pkey PRIMARY KEY (page_content_id);


--
-- Name: cms_page_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY cms_page
    ADD CONSTRAINT cms_page_pkey PRIMARY KEY (page_id);


--
-- Name: cms_site_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY cms_site
    ADD CONSTRAINT cms_site_pkey PRIMARY KEY (site_id);


--
-- Name: cms_template_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY cms_template
    ADD CONSTRAINT cms_template_pkey PRIMARY KEY (template_id);


--
-- Name: company_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY crm_company
    ADD CONSTRAINT company_pkey PRIMARY KEY (company_id);


--
-- Name: crm_billing_history_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY crm_billing_history
    ADD CONSTRAINT crm_billing_history_pkey PRIMARY KEY (billing_history_id);


--
-- Name: crm_billing_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY crm_billing
    ADD CONSTRAINT crm_billing_pkey PRIMARY KEY (billing_id);


--
-- Name: crm_communication_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY crm_communication
    ADD CONSTRAINT crm_communication_pkey PRIMARY KEY (comm_id);


--
-- Name: crm_enterprise_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY crm_enterprise
    ADD CONSTRAINT crm_enterprise_pkey PRIMARY KEY (enterprise_id);


--
-- Name: customer_order_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY crm_customer_order
    ADD CONSTRAINT customer_order_pkey PRIMARY KEY (order_id);


--
-- Name: customer_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY crm_customer
    ADD CONSTRAINT customer_pkey PRIMARY KEY (customer_id);


--
-- Name: order_item_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY crm_order_item
    ADD CONSTRAINT order_item_pkey PRIMARY KEY (order_item_id);


--
-- Name: product_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY crm_product
    ADD CONSTRAINT product_pkey PRIMARY KEY (product_id);


--
-- Name: product_pricing_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY crm_product_pricing
    ADD CONSTRAINT product_pricing_pkey PRIMARY KEY (product_pricing_id);


--
-- Name: status_event_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY core_status_event
    ADD CONSTRAINT status_event_pkey PRIMARY KEY (event_id);


--
-- Name: status_event_reason_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY core_status_event_reason
    ADD CONSTRAINT status_event_reason_pkey PRIMARY KEY (reason_id);


--
-- Name: status_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY core_status
    ADD CONSTRAINT status_pkey PRIMARY KEY (status_id);


--
-- Name: users_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY core_user
    ADD CONSTRAINT users_pkey PRIMARY KEY (username);


--
-- Name: appointment_customer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY crm_appointment
    ADD CONSTRAINT appointment_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES crm_customer(customer_id);


--
-- Name: appointment_status_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY crm_appointment
    ADD CONSTRAINT appointment_status_id_fkey FOREIGN KEY (status_id) REFERENCES core_status(status_id);


--
-- Name: appointment_user_completed_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY crm_appointment
    ADD CONSTRAINT appointment_user_completed_fkey FOREIGN KEY (user_completed) REFERENCES core_user(username);


--
-- Name: appointment_user_created_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY crm_appointment
    ADD CONSTRAINT appointment_user_created_fkey FOREIGN KEY (user_created) REFERENCES core_user(username);


--
-- Name: campaign_company_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY crm_campaign
    ADD CONSTRAINT campaign_company_id_fkey FOREIGN KEY (company_id) REFERENCES crm_company(company_id);


--
-- Name: cms_content_site_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY cms_content
    ADD CONSTRAINT cms_content_site_id_fkey FOREIGN KEY (site_id) REFERENCES cms_site(site_id);


--
-- Name: cms_content_user_created_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY cms_content
    ADD CONSTRAINT cms_content_user_created_fkey FOREIGN KEY (user_created) REFERENCES core_user(username);


--
-- Name: cms_page_content_content_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY cms_page_content
    ADD CONSTRAINT cms_page_content_content_id_fkey FOREIGN KEY (content_id) REFERENCES cms_content(content_id);


--
-- Name: cms_page_content_page_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY cms_page_content
    ADD CONSTRAINT cms_page_content_page_id_fkey FOREIGN KEY (page_id) REFERENCES cms_page(page_id);


--
-- Name: cms_page_site_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY cms_page
    ADD CONSTRAINT cms_page_site_id_fkey FOREIGN KEY (site_id) REFERENCES cms_site(site_id);


--
-- Name: cms_page_template_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY cms_page
    ADD CONSTRAINT cms_page_template_id_fkey FOREIGN KEY (template_id) REFERENCES cms_template(template_id);


--
-- Name: cms_page_user_created_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY cms_page
    ADD CONSTRAINT cms_page_user_created_fkey FOREIGN KEY (user_created) REFERENCES core_user(username);


--
-- Name: cms_site_company_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY cms_site
    ADD CONSTRAINT cms_site_company_id_fkey FOREIGN KEY (company_id) REFERENCES crm_company(company_id);


--
-- Name: cms_site_user_created_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY cms_site
    ADD CONSTRAINT cms_site_user_created_fkey FOREIGN KEY (user_created) REFERENCES core_user(username);


--
-- Name: cms_template_enterprise_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY cms_template
    ADD CONSTRAINT cms_template_enterprise_id_fkey FOREIGN KEY (enterprise_id) REFERENCES crm_enterprise(enterprise_id);


--
-- Name: core_status_event_enterprise_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY core_status_event
    ADD CONSTRAINT core_status_event_enterprise_id_fkey FOREIGN KEY (enterprise_id) REFERENCES crm_enterprise(enterprise_id);


--
-- Name: core_user_enterprise_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY core_user
    ADD CONSTRAINT core_user_enterprise_id_fkey FOREIGN KEY (enterprise_id) REFERENCES crm_enterprise(enterprise_id);


--
-- Name: crm_billing_customer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY crm_billing
    ADD CONSTRAINT crm_billing_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES crm_customer(customer_id);


--
-- Name: crm_billing_history_billing_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY crm_billing_history
    ADD CONSTRAINT crm_billing_history_billing_id_fkey FOREIGN KEY (billing_id) REFERENCES crm_billing(billing_id);


--
-- Name: crm_billing_history_customer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY crm_billing_history
    ADD CONSTRAINT crm_billing_history_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES crm_customer(customer_id);


--
-- Name: crm_billing_history_order_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY crm_billing_history
    ADD CONSTRAINT crm_billing_history_order_id_fkey FOREIGN KEY (order_id) REFERENCES crm_customer_order(order_id);


--
-- Name: crm_billing_status_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY crm_billing
    ADD CONSTRAINT crm_billing_status_id_fkey FOREIGN KEY (status_id) REFERENCES core_status(status_id);


--
-- Name: crm_billing_user_created_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY crm_billing
    ADD CONSTRAINT crm_billing_user_created_fkey FOREIGN KEY (user_created) REFERENCES core_user(username);


--
-- Name: crm_communication_company_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY crm_communication
    ADD CONSTRAINT crm_communication_company_id_fkey FOREIGN KEY (company_id) REFERENCES crm_company(company_id);


--
-- Name: crm_communication_user_created_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY crm_communication
    ADD CONSTRAINT crm_communication_user_created_fkey FOREIGN KEY (user_created) REFERENCES core_user(username);


--
-- Name: crm_company_enterprise_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY crm_company
    ADD CONSTRAINT crm_company_enterprise_id_fkey FOREIGN KEY (enterprise_id) REFERENCES crm_enterprise(enterprise_id);


--
-- Name: crm_company_status_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY crm_company
    ADD CONSTRAINT crm_company_status_id_fkey FOREIGN KEY (status_id) REFERENCES core_status(status_id);


--
-- Name: crm_customer_order_campaign_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY crm_customer_order
    ADD CONSTRAINT crm_customer_order_campaign_id_fkey FOREIGN KEY (campaign_id) REFERENCES crm_campaign(campaign_id);


--
-- Name: customer_campaign_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY crm_customer
    ADD CONSTRAINT customer_campaign_id_fkey FOREIGN KEY (campaign_id) REFERENCES crm_campaign(campaign_id);


--
-- Name: customer_order_customer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY crm_customer_order
    ADD CONSTRAINT customer_order_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES crm_customer(customer_id);


--
-- Name: customer_order_user_created_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY crm_customer_order
    ADD CONSTRAINT customer_order_user_created_fkey FOREIGN KEY (user_created) REFERENCES core_user(username);


--
-- Name: customer_user_assigned_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY crm_customer
    ADD CONSTRAINT customer_user_assigned_fkey FOREIGN KEY (user_assigned) REFERENCES core_user(username);


--
-- Name: customer_user_created_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY crm_customer
    ADD CONSTRAINT customer_user_created_fkey FOREIGN KEY (user_created) REFERENCES core_user(username);


--
-- Name: order_item_order_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY crm_order_item
    ADD CONSTRAINT order_item_order_id_fkey FOREIGN KEY (order_id) REFERENCES crm_customer_order(order_id);


--
-- Name: order_item_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY crm_order_item
    ADD CONSTRAINT order_item_product_id_fkey FOREIGN KEY (product_id) REFERENCES crm_product(product_id);


--
-- Name: order_item_user_created_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY crm_order_item
    ADD CONSTRAINT order_item_user_created_fkey FOREIGN KEY (user_created) REFERENCES core_user(username);


--
-- Name: product_company_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY crm_product
    ADD CONSTRAINT product_company_id_fkey FOREIGN KEY (company_id) REFERENCES crm_company(company_id);


--
-- Name: product_pricing_campaign_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY crm_product_pricing
    ADD CONSTRAINT product_pricing_campaign_id_fkey FOREIGN KEY (campaign_id) REFERENCES crm_campaign(campaign_id);


--
-- Name: product_pricing_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY crm_product_pricing
    ADD CONSTRAINT product_pricing_product_id_fkey FOREIGN KEY (product_id) REFERENCES crm_product(product_id);


--
-- Name: status_event_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY core_status
    ADD CONSTRAINT status_event_id_fkey FOREIGN KEY (event_id) REFERENCES core_status_event(event_id);


--
-- Name: status_event_reason_event_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY core_status_event_reason
    ADD CONSTRAINT status_event_reason_event_id_fkey FOREIGN KEY (event_id) REFERENCES core_status_event(event_id);


--
-- Name: status_username_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY core_status
    ADD CONSTRAINT status_username_fkey FOREIGN KEY (username) REFERENCES core_user(username);


--
-- Name: public; Type: ACL; Schema: -; Owner: -
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

