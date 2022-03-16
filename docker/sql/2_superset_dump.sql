--
-- PostgreSQL database dump
--

-- Dumped from database version 10.3
-- Dumped by pg_dump version 11.2

-- Started on 2022-03-11 14:51:15

ALTER DATABASE superset OWNER TO postgres;

\connect superset

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 842 (class 1247 OID 3963196)
-- Name: emaildeliverytype; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.emaildeliverytype AS ENUM (
    'attachment',
    'inline'
);


ALTER TYPE public.emaildeliverytype OWNER TO postgres;

--
-- TOC entry 873 (class 1247 OID 3963340)
-- Name: objecttypes; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.objecttypes AS ENUM (
    'query',
    'chart',
    'dashboard'
);


ALTER TYPE public.objecttypes OWNER TO postgres;

--
-- TOC entry 850 (class 1247 OID 3963234)
-- Name: sliceemailreportformat; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.sliceemailreportformat AS ENUM (
    'visualization',
    'data'
);


ALTER TYPE public.sliceemailreportformat OWNER TO postgres;

--
-- TOC entry 866 (class 1247 OID 3963310)
-- Name: tagtypes; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.tagtypes AS ENUM (
    'custom',
    'type',
    'owner',
    'favorited_by'
);


ALTER TYPE public.tagtypes OWNER TO postgres;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 197 (class 1259 OID 3962444)
-- Name: ab_permission; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ab_permission (
    id integer NOT NULL,
    name character varying(100) NOT NULL
);


ALTER TABLE public.ab_permission OWNER TO postgres;

--
-- TOC entry 196 (class 1259 OID 3962442)
-- Name: ab_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ab_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ab_permission_id_seq OWNER TO postgres;

--
-- TOC entry 207 (class 1259 OID 3962507)
-- Name: ab_permission_view; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ab_permission_view (
    id integer NOT NULL,
    permission_id integer,
    view_menu_id integer
);


ALTER TABLE public.ab_permission_view OWNER TO postgres;

--
-- TOC entry 206 (class 1259 OID 3962505)
-- Name: ab_permission_view_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ab_permission_view_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ab_permission_view_id_seq OWNER TO postgres;

--
-- TOC entry 211 (class 1259 OID 3962545)
-- Name: ab_permission_view_role; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ab_permission_view_role (
    id integer NOT NULL,
    permission_view_id integer,
    role_id integer
);


ALTER TABLE public.ab_permission_view_role OWNER TO postgres;

--
-- TOC entry 210 (class 1259 OID 3962543)
-- Name: ab_permission_view_role_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ab_permission_view_role_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ab_permission_view_role_id_seq OWNER TO postgres;

--
-- TOC entry 205 (class 1259 OID 3962495)
-- Name: ab_register_user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ab_register_user (
    id integer NOT NULL,
    first_name character varying(64) NOT NULL,
    last_name character varying(64) NOT NULL,
    username character varying(64) NOT NULL,
    password character varying(256),
    email character varying(64) NOT NULL,
    registration_date timestamp without time zone,
    registration_hash character varying(256)
);


ALTER TABLE public.ab_register_user OWNER TO postgres;

--
-- TOC entry 204 (class 1259 OID 3962493)
-- Name: ab_register_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ab_register_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ab_register_user_id_seq OWNER TO postgres;

--
-- TOC entry 201 (class 1259 OID 3962462)
-- Name: ab_role; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ab_role (
    id integer NOT NULL,
    name character varying(64) NOT NULL
);


ALTER TABLE public.ab_role OWNER TO postgres;

--
-- TOC entry 200 (class 1259 OID 3962460)
-- Name: ab_role_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ab_role_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ab_role_id_seq OWNER TO postgres;

--
-- TOC entry 203 (class 1259 OID 3962471)
-- Name: ab_user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ab_user (
    id integer NOT NULL,
    first_name character varying(64) NOT NULL,
    last_name character varying(64) NOT NULL,
    username character varying(64) NOT NULL,
    password character varying(256),
    active boolean,
    email character varying(64) NOT NULL,
    last_login timestamp without time zone,
    login_count integer,
    fail_login_count integer,
    created_on timestamp without time zone,
    changed_on timestamp without time zone,
    created_by_fk integer,
    changed_by_fk integer
);


ALTER TABLE public.ab_user OWNER TO postgres;

--
-- TOC entry 202 (class 1259 OID 3962469)
-- Name: ab_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ab_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ab_user_id_seq OWNER TO postgres;

--
-- TOC entry 209 (class 1259 OID 3962526)
-- Name: ab_user_role; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ab_user_role (
    id integer NOT NULL,
    user_id integer,
    role_id integer
);


ALTER TABLE public.ab_user_role OWNER TO postgres;

--
-- TOC entry 208 (class 1259 OID 3962524)
-- Name: ab_user_role_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ab_user_role_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ab_user_role_id_seq OWNER TO postgres;

--
-- TOC entry 199 (class 1259 OID 3962453)
-- Name: ab_view_menu; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ab_view_menu (
    id integer NOT NULL,
    name character varying(255) NOT NULL
);


ALTER TABLE public.ab_view_menu OWNER TO postgres;

--
-- TOC entry 198 (class 1259 OID 3962451)
-- Name: ab_view_menu_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ab_view_menu_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ab_view_menu_id_seq OWNER TO postgres;

--
-- TOC entry 250 (class 1259 OID 3963007)
-- Name: access_request; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.access_request (
    created_on timestamp without time zone,
    changed_on timestamp without time zone,
    id integer NOT NULL,
    datasource_type character varying(200),
    datasource_id integer,
    changed_by_fk integer,
    created_by_fk integer
);


ALTER TABLE public.access_request OWNER TO postgres;

--
-- TOC entry 249 (class 1259 OID 3963005)
-- Name: access_request_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.access_request_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.access_request_id_seq OWNER TO postgres;

--
-- TOC entry 3660 (class 0 OID 0)
-- Dependencies: 249
-- Name: access_request_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.access_request_id_seq OWNED BY public.access_request.id;


--
-- TOC entry 212 (class 1259 OID 3962562)
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- TOC entry 286 (class 1259 OID 3963560)
-- Name: alert_logs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alert_logs (
    id integer NOT NULL,
    scheduled_dttm timestamp without time zone,
    dttm_start timestamp without time zone,
    dttm_end timestamp without time zone,
    alert_id integer,
    state character varying(10)
);


ALTER TABLE public.alert_logs OWNER TO postgres;

--
-- TOC entry 285 (class 1259 OID 3963558)
-- Name: alert_logs_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.alert_logs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.alert_logs_id_seq OWNER TO postgres;

--
-- TOC entry 3661 (class 0 OID 0)
-- Dependencies: 285
-- Name: alert_logs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.alert_logs_id_seq OWNED BY public.alert_logs.id;


--
-- TOC entry 288 (class 1259 OID 3963573)
-- Name: alert_owner; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alert_owner (
    id integer NOT NULL,
    user_id integer,
    alert_id integer
);


ALTER TABLE public.alert_owner OWNER TO postgres;

--
-- TOC entry 287 (class 1259 OID 3963571)
-- Name: alert_owner_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.alert_owner_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.alert_owner_id_seq OWNER TO postgres;

--
-- TOC entry 3662 (class 0 OID 0)
-- Dependencies: 287
-- Name: alert_owner_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.alert_owner_id_seq OWNED BY public.alert_owner.id;


--
-- TOC entry 284 (class 1259 OID 3963538)
-- Name: alerts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alerts (
    id integer NOT NULL,
    label character varying(150) NOT NULL,
    active boolean,
    crontab character varying(50) NOT NULL,
    alert_type character varying(50),
    log_retention integer NOT NULL,
    grace_period integer NOT NULL,
    recipients text,
    slice_id integer,
    dashboard_id integer,
    last_eval_dttm timestamp without time zone,
    last_state character varying(10),
    slack_channel text,
    changed_by_fk integer,
    changed_on timestamp without time zone,
    created_by_fk integer,
    created_on timestamp without time zone,
    validator_config text,
    database_id integer NOT NULL,
    sql text NOT NULL,
    validator_type character varying(100) NOT NULL
);


ALTER TABLE public.alerts OWNER TO postgres;

--
-- TOC entry 283 (class 1259 OID 3963536)
-- Name: alerts_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.alerts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.alerts_id_seq OWNER TO postgres;

--
-- TOC entry 3663 (class 0 OID 0)
-- Dependencies: 283
-- Name: alerts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.alerts_id_seq OWNED BY public.alerts.id;


--
-- TOC entry 258 (class 1259 OID 3963100)
-- Name: annotation; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.annotation (
    created_on timestamp without time zone,
    changed_on timestamp without time zone,
    id integer NOT NULL,
    start_dttm timestamp without time zone,
    end_dttm timestamp without time zone,
    layer_id integer,
    short_descr character varying(500),
    long_descr text,
    changed_by_fk integer,
    created_by_fk integer,
    json_metadata text
);


ALTER TABLE public.annotation OWNER TO postgres;

--
-- TOC entry 257 (class 1259 OID 3963098)
-- Name: annotation_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.annotation_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.annotation_id_seq OWNER TO postgres;

--
-- TOC entry 3664 (class 0 OID 0)
-- Dependencies: 257
-- Name: annotation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.annotation_id_seq OWNED BY public.annotation.id;


--
-- TOC entry 256 (class 1259 OID 3963079)
-- Name: annotation_layer; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.annotation_layer (
    created_on timestamp without time zone,
    changed_on timestamp without time zone,
    id integer NOT NULL,
    name character varying(250),
    descr text,
    changed_by_fk integer,
    created_by_fk integer
);


ALTER TABLE public.annotation_layer OWNER TO postgres;

--
-- TOC entry 255 (class 1259 OID 3963077)
-- Name: annotation_layer_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.annotation_layer_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.annotation_layer_id_seq OWNER TO postgres;

--
-- TOC entry 3665 (class 0 OID 0)
-- Dependencies: 255
-- Name: annotation_layer_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.annotation_layer_id_seq OWNED BY public.annotation_layer.id;


--
-- TOC entry 292 (class 1259 OID 3963680)
-- Name: cache_keys; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cache_keys (
    id integer NOT NULL,
    cache_key character varying(256) NOT NULL,
    cache_timeout integer,
    datasource_uid character varying(64) NOT NULL,
    created_on timestamp without time zone
);


ALTER TABLE public.cache_keys OWNER TO postgres;

--
-- TOC entry 291 (class 1259 OID 3963678)
-- Name: cache_keys_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.cache_keys_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.cache_keys_id_seq OWNER TO postgres;

--
-- TOC entry 3666 (class 0 OID 0)
-- Dependencies: 291
-- Name: cache_keys_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.cache_keys_id_seq OWNED BY public.cache_keys.id;


--
-- TOC entry 214 (class 1259 OID 3962569)
-- Name: clusters; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.clusters (
    created_on timestamp without time zone,
    changed_on timestamp without time zone,
    id integer NOT NULL,
    cluster_name character varying(250) NOT NULL,
    broker_host character varying(255),
    broker_port integer,
    broker_endpoint character varying(255),
    metadata_last_refreshed timestamp without time zone,
    created_by_fk integer,
    changed_by_fk integer,
    cache_timeout integer,
    verbose_name character varying(250),
    broker_pass bytea,
    broker_user character varying(255),
    uuid uuid
);


ALTER TABLE public.clusters OWNER TO postgres;

--
-- TOC entry 213 (class 1259 OID 3962567)
-- Name: clusters_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.clusters_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.clusters_id_seq OWNER TO postgres;

--
-- TOC entry 3667 (class 0 OID 0)
-- Dependencies: 213
-- Name: clusters_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.clusters_id_seq OWNED BY public.clusters.id;


--
-- TOC entry 224 (class 1259 OID 3962697)
-- Name: columns; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.columns (
    created_on timestamp without time zone,
    changed_on timestamp without time zone,
    id integer NOT NULL,
    column_name character varying(255) NOT NULL,
    is_active boolean,
    type character varying(32),
    groupby boolean,
    filterable boolean,
    description text,
    created_by_fk integer,
    changed_by_fk integer,
    dimension_spec_json text,
    verbose_name character varying(1024),
    datasource_id integer,
    uuid uuid
);


ALTER TABLE public.columns OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 3962695)
-- Name: columns_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.columns_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.columns_id_seq OWNER TO postgres;

--
-- TOC entry 3668 (class 0 OID 0)
-- Dependencies: 223
-- Name: columns_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.columns_id_seq OWNED BY public.columns.id;


--
-- TOC entry 240 (class 1259 OID 3962884)
-- Name: css_templates; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.css_templates (
    created_on timestamp without time zone,
    changed_on timestamp without time zone,
    id integer NOT NULL,
    template_name character varying(250),
    css text,
    changed_by_fk integer,
    created_by_fk integer
);


ALTER TABLE public.css_templates OWNER TO postgres;

--
-- TOC entry 239 (class 1259 OID 3962882)
-- Name: css_templates_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.css_templates_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.css_templates_id_seq OWNER TO postgres;

--
-- TOC entry 3669 (class 0 OID 0)
-- Dependencies: 239
-- Name: css_templates_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.css_templates_id_seq OWNED BY public.css_templates.id;


--
-- TOC entry 262 (class 1259 OID 3963203)
-- Name: dashboard_email_schedules; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.dashboard_email_schedules (
    created_on timestamp without time zone,
    changed_on timestamp without time zone,
    id integer NOT NULL,
    active boolean,
    crontab character varying(50),
    recipients text,
    deliver_as_group boolean,
    delivery_type public.emaildeliverytype,
    dashboard_id integer,
    created_by_fk integer,
    changed_by_fk integer,
    user_id integer,
    slack_channel text,
    uuid uuid
);


ALTER TABLE public.dashboard_email_schedules OWNER TO postgres;

--
-- TOC entry 261 (class 1259 OID 3963201)
-- Name: dashboard_email_schedules_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.dashboard_email_schedules_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.dashboard_email_schedules_id_seq OWNER TO postgres;

--
-- TOC entry 3670 (class 0 OID 0)
-- Dependencies: 261
-- Name: dashboard_email_schedules_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.dashboard_email_schedules_id_seq OWNED BY public.dashboard_email_schedules.id;


--
-- TOC entry 304 (class 1259 OID 3963849)
-- Name: dashboard_roles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.dashboard_roles (
    id integer NOT NULL,
    role_id integer NOT NULL,
    dashboard_id integer
);


ALTER TABLE public.dashboard_roles OWNER TO postgres;

--
-- TOC entry 303 (class 1259 OID 3963847)
-- Name: dashboard_roles_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.dashboard_roles_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.dashboard_roles_id_seq OWNER TO postgres;

--
-- TOC entry 3671 (class 0 OID 0)
-- Dependencies: 303
-- Name: dashboard_roles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.dashboard_roles_id_seq OWNED BY public.dashboard_roles.id;


--
-- TOC entry 234 (class 1259 OID 3962822)
-- Name: dashboard_slices; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.dashboard_slices (
    id integer NOT NULL,
    dashboard_id integer,
    slice_id integer
);


ALTER TABLE public.dashboard_slices OWNER TO postgres;

--
-- TOC entry 233 (class 1259 OID 3962820)
-- Name: dashboard_slices_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.dashboard_slices_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.dashboard_slices_id_seq OWNER TO postgres;

--
-- TOC entry 3672 (class 0 OID 0)
-- Dependencies: 233
-- Name: dashboard_slices_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.dashboard_slices_id_seq OWNED BY public.dashboard_slices.id;


--
-- TOC entry 244 (class 1259 OID 3962930)
-- Name: dashboard_user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.dashboard_user (
    id integer NOT NULL,
    user_id integer,
    dashboard_id integer
);


ALTER TABLE public.dashboard_user OWNER TO postgres;

--
-- TOC entry 243 (class 1259 OID 3962928)
-- Name: dashboard_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.dashboard_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.dashboard_user_id_seq OWNER TO postgres;

--
-- TOC entry 3673 (class 0 OID 0)
-- Dependencies: 243
-- Name: dashboard_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.dashboard_user_id_seq OWNED BY public.dashboard_user.id;


--
-- TOC entry 216 (class 1259 OID 3962592)
-- Name: dashboards; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.dashboards (
    created_on timestamp without time zone,
    changed_on timestamp without time zone,
    id integer NOT NULL,
    dashboard_title character varying(500),
    position_json text,
    created_by_fk integer,
    changed_by_fk integer,
    css text,
    description text,
    slug character varying(255),
    json_metadata text,
    published boolean,
    uuid uuid,
    certified_by text,
    certification_details text
);


ALTER TABLE public.dashboards OWNER TO postgres;

--
-- TOC entry 215 (class 1259 OID 3962590)
-- Name: dashboards_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.dashboards_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.dashboards_id_seq OWNER TO postgres;

--
-- TOC entry 3674 (class 0 OID 0)
-- Dependencies: 215
-- Name: dashboards_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.dashboards_id_seq OWNED BY public.dashboards.id;


--
-- TOC entry 220 (class 1259 OID 3962636)
-- Name: datasources; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.datasources (
    created_on timestamp without time zone,
    changed_on timestamp without time zone,
    id integer NOT NULL,
    datasource_name character varying(255) NOT NULL,
    is_featured boolean,
    is_hidden boolean,
    description text,
    default_endpoint text,
    created_by_fk integer,
    changed_by_fk integer,
    "offset" integer,
    cache_timeout integer,
    perm character varying(1000),
    filter_select_enabled boolean,
    params character varying(1000),
    fetch_values_from character varying(100),
    schema_perm character varying(1000),
    cluster_id integer NOT NULL,
    uuid uuid
);


ALTER TABLE public.datasources OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 3962634)
-- Name: datasources_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.datasources_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.datasources_id_seq OWNER TO postgres;

--
-- TOC entry 3675 (class 0 OID 0)
-- Dependencies: 219
-- Name: datasources_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.datasources_id_seq OWNED BY public.datasources.id;


--
-- TOC entry 218 (class 1259 OID 3962613)
-- Name: dbs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.dbs (
    created_on timestamp without time zone,
    changed_on timestamp without time zone,
    id integer NOT NULL,
    database_name character varying(250) NOT NULL,
    sqlalchemy_uri character varying(1024) NOT NULL,
    created_by_fk integer,
    changed_by_fk integer,
    password bytea,
    cache_timeout integer,
    extra text,
    select_as_create_table_as boolean,
    allow_ctas boolean,
    expose_in_sqllab boolean,
    force_ctas_schema character varying(250),
    allow_run_async boolean,
    allow_dml boolean,
    verbose_name character varying(250),
    impersonate_user boolean,
    allow_multi_schema_metadata_fetch boolean,
    allow_csv_upload boolean DEFAULT true NOT NULL,
    encrypted_extra bytea,
    server_cert bytea,
    allow_cvas boolean,
    uuid uuid,
    configuration_method character varying(255) DEFAULT 'sqlalchemy_form'::character varying
);


ALTER TABLE public.dbs OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 3962611)
-- Name: dbs_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.dbs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.dbs_id_seq OWNER TO postgres;

--
-- TOC entry 3676 (class 0 OID 0)
-- Dependencies: 217
-- Name: dbs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.dbs_id_seq OWNED BY public.dbs.id;


--
-- TOC entry 268 (class 1259 OID 3963291)
-- Name: druiddatasource_user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.druiddatasource_user (
    id integer NOT NULL,
    user_id integer,
    datasource_id integer
);


ALTER TABLE public.druiddatasource_user OWNER TO postgres;

--
-- TOC entry 267 (class 1259 OID 3963289)
-- Name: druiddatasource_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.druiddatasource_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.druiddatasource_user_id_seq OWNER TO postgres;

--
-- TOC entry 3677 (class 0 OID 0)
-- Dependencies: 267
-- Name: druiddatasource_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.druiddatasource_user_id_seq OWNED BY public.druiddatasource_user.id;


--
-- TOC entry 302 (class 1259 OID 3963822)
-- Name: dynamic_plugin; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.dynamic_plugin (
    created_on timestamp without time zone,
    changed_on timestamp without time zone,
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    key character varying(50) NOT NULL,
    bundle_url character varying(1000) NOT NULL,
    created_by_fk integer,
    changed_by_fk integer
);


ALTER TABLE public.dynamic_plugin OWNER TO postgres;

--
-- TOC entry 301 (class 1259 OID 3963820)
-- Name: dynamic_plugin_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.dynamic_plugin_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.dynamic_plugin_id_seq OWNER TO postgres;

--
-- TOC entry 3678 (class 0 OID 0)
-- Dependencies: 301
-- Name: dynamic_plugin_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.dynamic_plugin_id_seq OWNED BY public.dynamic_plugin.id;


--
-- TOC entry 242 (class 1259 OID 3962905)
-- Name: favstar; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.favstar (
    id integer NOT NULL,
    user_id integer,
    class_name character varying(50),
    obj_id integer,
    dttm timestamp without time zone
);


ALTER TABLE public.favstar OWNER TO postgres;

--
-- TOC entry 241 (class 1259 OID 3962903)
-- Name: favstar_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.favstar_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.favstar_id_seq OWNER TO postgres;

--
-- TOC entry 3679 (class 0 OID 0)
-- Dependencies: 241
-- Name: favstar_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.favstar_id_seq OWNED BY public.favstar.id;


--
-- TOC entry 306 (class 1259 OID 3963935)
-- Name: filter_sets; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.filter_sets (
    created_on timestamp without time zone,
    changed_on timestamp without time zone,
    id integer NOT NULL,
    name character varying(500) NOT NULL,
    description text,
    json_metadata text NOT NULL,
    owner_id integer NOT NULL,
    owner_type character varying(255) NOT NULL,
    dashboard_id integer NOT NULL,
    created_by_fk integer,
    changed_by_fk integer
);


ALTER TABLE public.filter_sets OWNER TO postgres;

--
-- TOC entry 305 (class 1259 OID 3963933)
-- Name: filter_sets_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.filter_sets_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.filter_sets_id_seq OWNER TO postgres;

--
-- TOC entry 3680 (class 0 OID 0)
-- Dependencies: 305
-- Name: filter_sets_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.filter_sets_id_seq OWNED BY public.filter_sets.id;


--
-- TOC entry 252 (class 1259 OID 3963033)
-- Name: keyvalue; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.keyvalue (
    id integer NOT NULL,
    value text NOT NULL
);


ALTER TABLE public.keyvalue OWNER TO postgres;

--
-- TOC entry 251 (class 1259 OID 3963031)
-- Name: keyvalue_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.keyvalue_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.keyvalue_id_seq OWNER TO postgres;

--
-- TOC entry 3681 (class 0 OID 0)
-- Dependencies: 251
-- Name: keyvalue_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.keyvalue_id_seq OWNED BY public.keyvalue.id;


--
-- TOC entry 236 (class 1259 OID 3962842)
-- Name: logs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.logs (
    id integer NOT NULL,
    action character varying(512),
    user_id integer,
    json text,
    dttm timestamp without time zone,
    dashboard_id integer,
    slice_id integer,
    duration_ms integer,
    referrer character varying(1024)
);


ALTER TABLE public.logs OWNER TO postgres;

--
-- TOC entry 235 (class 1259 OID 3962840)
-- Name: logs_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.logs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.logs_id_seq OWNER TO postgres;

--
-- TOC entry 3682 (class 0 OID 0)
-- Dependencies: 235
-- Name: logs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.logs_id_seq OWNED BY public.logs.id;


--
-- TOC entry 226 (class 1259 OID 3962718)
-- Name: metrics; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.metrics (
    id integer NOT NULL,
    metric_name character varying(255) NOT NULL,
    verbose_name character varying(1024),
    metric_type character varying(32),
    json text NOT NULL,
    description text,
    changed_by_fk integer,
    changed_on timestamp without time zone,
    created_by_fk integer,
    created_on timestamp without time zone,
    d3format character varying(128),
    warning_text text,
    datasource_id integer,
    uuid uuid
);


ALTER TABLE public.metrics OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 3962716)
-- Name: metrics_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.metrics_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.metrics_id_seq OWNER TO postgres;

--
-- TOC entry 3683 (class 0 OID 0)
-- Dependencies: 225
-- Name: metrics_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.metrics_id_seq OWNED BY public.metrics.id;


--
-- TOC entry 248 (class 1259 OID 3962985)
-- Name: query; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.query (
    id integer NOT NULL,
    client_id character varying(11) NOT NULL,
    database_id integer NOT NULL,
    tmp_table_name character varying(256),
    tab_name character varying(256),
    sql_editor_id character varying(256),
    user_id integer,
    status character varying(16),
    schema character varying(256),
    sql text,
    select_sql text,
    executed_sql text,
    "limit" integer,
    select_as_cta boolean,
    select_as_cta_used boolean,
    progress integer,
    rows integer,
    error_message text,
    start_time numeric(20,6),
    changed_on timestamp without time zone,
    end_time numeric(20,6),
    results_key character varying(64),
    start_running_time numeric(20,6),
    end_result_backend_time numeric(20,6),
    tracking_url text,
    extra_json text,
    tmp_schema_name character varying(256),
    ctas_method character varying(16),
    limiting_factor character varying(255) DEFAULT 'UNKNOWN'::character varying
);


ALTER TABLE public.query OWNER TO postgres;

--
-- TOC entry 247 (class 1259 OID 3962983)
-- Name: query_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.query_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.query_id_seq OWNER TO postgres;

--
-- TOC entry 3684 (class 0 OID 0)
-- Dependencies: 247
-- Name: query_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.query_id_seq OWNED BY public.query.id;


--
-- TOC entry 296 (class 1259 OID 3963762)
-- Name: report_execution_log; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.report_execution_log (
    id integer NOT NULL,
    scheduled_dttm timestamp without time zone NOT NULL,
    start_dttm timestamp without time zone,
    end_dttm timestamp without time zone,
    value double precision,
    value_row_json text,
    state character varying(50) NOT NULL,
    error_message text,
    report_schedule_id integer NOT NULL,
    uuid uuid
);


ALTER TABLE public.report_execution_log OWNER TO postgres;

--
-- TOC entry 295 (class 1259 OID 3963760)
-- Name: report_execution_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.report_execution_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.report_execution_log_id_seq OWNER TO postgres;

--
-- TOC entry 3685 (class 0 OID 0)
-- Dependencies: 295
-- Name: report_execution_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.report_execution_log_id_seq OWNED BY public.report_execution_log.id;


--
-- TOC entry 298 (class 1259 OID 3963778)
-- Name: report_recipient; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.report_recipient (
    id integer NOT NULL,
    type character varying(50) NOT NULL,
    recipient_config_json text,
    report_schedule_id integer NOT NULL,
    created_on timestamp without time zone,
    changed_on timestamp without time zone,
    created_by_fk integer,
    changed_by_fk integer
);


ALTER TABLE public.report_recipient OWNER TO postgres;

--
-- TOC entry 297 (class 1259 OID 3963776)
-- Name: report_recipient_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.report_recipient_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.report_recipient_id_seq OWNER TO postgres;

--
-- TOC entry 3686 (class 0 OID 0)
-- Dependencies: 297
-- Name: report_recipient_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.report_recipient_id_seq OWNED BY public.report_recipient.id;


--
-- TOC entry 294 (class 1259 OID 3963721)
-- Name: report_schedule; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.report_schedule (
    id integer NOT NULL,
    type character varying(50) NOT NULL,
    name character varying(150) NOT NULL,
    description text,
    context_markdown text,
    active boolean,
    crontab character varying(1000) NOT NULL,
    sql text,
    chart_id integer,
    dashboard_id integer,
    database_id integer,
    last_eval_dttm timestamp without time zone,
    last_state character varying(50),
    last_value double precision,
    last_value_row_json text,
    validator_type character varying(100),
    validator_config_json text,
    log_retention integer,
    grace_period integer,
    created_on timestamp without time zone,
    changed_on timestamp without time zone,
    created_by_fk integer,
    changed_by_fk integer,
    working_timeout integer,
    report_format character varying(50) DEFAULT 'PNG'::character varying,
    creation_method character varying(255) DEFAULT 'alerts_reports'::character varying,
    timezone character varying(100) DEFAULT 'UTC'::character varying NOT NULL
);


ALTER TABLE public.report_schedule OWNER TO postgres;

--
-- TOC entry 293 (class 1259 OID 3963719)
-- Name: report_schedule_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.report_schedule_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.report_schedule_id_seq OWNER TO postgres;

--
-- TOC entry 3687 (class 0 OID 0)
-- Dependencies: 293
-- Name: report_schedule_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.report_schedule_id_seq OWNED BY public.report_schedule.id;


--
-- TOC entry 300 (class 1259 OID 3963804)
-- Name: report_schedule_user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.report_schedule_user (
    id integer NOT NULL,
    user_id integer NOT NULL,
    report_schedule_id integer NOT NULL
);


ALTER TABLE public.report_schedule_user OWNER TO postgres;

--
-- TOC entry 299 (class 1259 OID 3963802)
-- Name: report_schedule_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.report_schedule_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.report_schedule_user_id_seq OWNER TO postgres;

--
-- TOC entry 3688 (class 0 OID 0)
-- Dependencies: 299
-- Name: report_schedule_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.report_schedule_user_id_seq OWNED BY public.report_schedule_user.id;


--
-- TOC entry 280 (class 1259 OID 3963502)
-- Name: rls_filter_roles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rls_filter_roles (
    id integer NOT NULL,
    role_id integer NOT NULL,
    rls_filter_id integer
);


ALTER TABLE public.rls_filter_roles OWNER TO postgres;

--
-- TOC entry 279 (class 1259 OID 3963500)
-- Name: rls_filter_roles_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.rls_filter_roles_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.rls_filter_roles_id_seq OWNER TO postgres;

--
-- TOC entry 3689 (class 0 OID 0)
-- Dependencies: 279
-- Name: rls_filter_roles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.rls_filter_roles_id_seq OWNED BY public.rls_filter_roles.id;


--
-- TOC entry 282 (class 1259 OID 3963520)
-- Name: rls_filter_tables; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rls_filter_tables (
    id integer NOT NULL,
    table_id integer,
    rls_filter_id integer
);


ALTER TABLE public.rls_filter_tables OWNER TO postgres;

--
-- TOC entry 281 (class 1259 OID 3963518)
-- Name: rls_filter_tables_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.rls_filter_tables_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.rls_filter_tables_id_seq OWNER TO postgres;

--
-- TOC entry 3690 (class 0 OID 0)
-- Dependencies: 281
-- Name: rls_filter_tables_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.rls_filter_tables_id_seq OWNED BY public.rls_filter_tables.id;


--
-- TOC entry 278 (class 1259 OID 3963476)
-- Name: row_level_security_filters; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.row_level_security_filters (
    created_on timestamp without time zone,
    changed_on timestamp without time zone,
    id integer NOT NULL,
    clause text NOT NULL,
    created_by_fk integer,
    changed_by_fk integer,
    filter_type character varying(255),
    group_key character varying(255)
);


ALTER TABLE public.row_level_security_filters OWNER TO postgres;

--
-- TOC entry 277 (class 1259 OID 3963474)
-- Name: row_level_security_filters_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.row_level_security_filters_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.row_level_security_filters_id_seq OWNER TO postgres;

--
-- TOC entry 3691 (class 0 OID 0)
-- Dependencies: 277
-- Name: row_level_security_filters_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.row_level_security_filters_id_seq OWNED BY public.row_level_security_filters.id;


--
-- TOC entry 254 (class 1259 OID 3963048)
-- Name: saved_query; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.saved_query (
    created_on timestamp without time zone,
    changed_on timestamp without time zone,
    id integer NOT NULL,
    user_id integer,
    db_id integer,
    label character varying(256),
    schema character varying(128),
    sql text,
    description text,
    changed_by_fk integer,
    created_by_fk integer,
    extra_json text,
    last_run timestamp without time zone,
    rows integer,
    uuid uuid
);


ALTER TABLE public.saved_query OWNER TO postgres;

--
-- TOC entry 253 (class 1259 OID 3963046)
-- Name: saved_query_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.saved_query_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.saved_query_id_seq OWNER TO postgres;

--
-- TOC entry 3692 (class 0 OID 0)
-- Dependencies: 253
-- Name: saved_query_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.saved_query_id_seq OWNED BY public.saved_query.id;


--
-- TOC entry 264 (class 1259 OID 3963241)
-- Name: slice_email_schedules; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.slice_email_schedules (
    created_on timestamp without time zone,
    changed_on timestamp without time zone,
    id integer NOT NULL,
    active boolean,
    crontab character varying(50),
    recipients text,
    deliver_as_group boolean,
    delivery_type public.emaildeliverytype,
    slice_id integer,
    email_format public.sliceemailreportformat,
    created_by_fk integer,
    changed_by_fk integer,
    user_id integer,
    slack_channel text,
    uuid uuid
);


ALTER TABLE public.slice_email_schedules OWNER TO postgres;

--
-- TOC entry 263 (class 1259 OID 3963239)
-- Name: slice_email_schedules_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.slice_email_schedules_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.slice_email_schedules_id_seq OWNER TO postgres;

--
-- TOC entry 3693 (class 0 OID 0)
-- Dependencies: 263
-- Name: slice_email_schedules_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.slice_email_schedules_id_seq OWNED BY public.slice_email_schedules.id;


--
-- TOC entry 246 (class 1259 OID 3962948)
-- Name: slice_user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.slice_user (
    id integer NOT NULL,
    user_id integer,
    slice_id integer
);


ALTER TABLE public.slice_user OWNER TO postgres;

--
-- TOC entry 245 (class 1259 OID 3962946)
-- Name: slice_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.slice_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.slice_user_id_seq OWNER TO postgres;

--
-- TOC entry 3694 (class 0 OID 0)
-- Dependencies: 245
-- Name: slice_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.slice_user_id_seq OWNED BY public.slice_user.id;


--
-- TOC entry 228 (class 1259 OID 3962739)
-- Name: slices; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.slices (
    created_on timestamp without time zone,
    changed_on timestamp without time zone,
    id integer NOT NULL,
    slice_name character varying(250),
    datasource_type character varying(200),
    datasource_name character varying(2000),
    viz_type character varying(250),
    params text,
    created_by_fk integer,
    changed_by_fk integer,
    description text,
    cache_timeout integer,
    perm character varying(2000),
    datasource_id integer,
    schema_perm character varying(1000),
    uuid uuid,
    query_context text,
    last_saved_at timestamp without time zone,
    last_saved_by_fk integer,
    certified_by text,
    certification_details text
);


ALTER TABLE public.slices OWNER TO postgres;

--
-- TOC entry 227 (class 1259 OID 3962737)
-- Name: slices_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.slices_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.slices_id_seq OWNER TO postgres;

--
-- TOC entry 3695 (class 0 OID 0)
-- Dependencies: 227
-- Name: slices_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.slices_id_seq OWNED BY public.slices.id;


--
-- TOC entry 230 (class 1259 OID 3962770)
-- Name: sql_metrics; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sql_metrics (
    created_on timestamp without time zone,
    changed_on timestamp without time zone,
    id integer NOT NULL,
    metric_name character varying(255) NOT NULL,
    verbose_name character varying(1024),
    metric_type character varying(32),
    table_id integer,
    expression text NOT NULL,
    description text,
    created_by_fk integer,
    changed_by_fk integer,
    d3format character varying(128),
    warning_text text,
    extra text,
    uuid uuid
);


ALTER TABLE public.sql_metrics OWNER TO postgres;

--
-- TOC entry 229 (class 1259 OID 3962768)
-- Name: sql_metrics_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.sql_metrics_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.sql_metrics_id_seq OWNER TO postgres;

--
-- TOC entry 3696 (class 0 OID 0)
-- Dependencies: 229
-- Name: sql_metrics_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.sql_metrics_id_seq OWNED BY public.sql_metrics.id;


--
-- TOC entry 290 (class 1259 OID 3963648)
-- Name: sql_observations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sql_observations (
    id integer NOT NULL,
    dttm timestamp without time zone,
    alert_id integer,
    value double precision,
    error_msg character varying(500)
);


ALTER TABLE public.sql_observations OWNER TO postgres;

--
-- TOC entry 289 (class 1259 OID 3963646)
-- Name: sql_observations_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.sql_observations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.sql_observations_id_seq OWNER TO postgres;

--
-- TOC entry 3697 (class 0 OID 0)
-- Dependencies: 289
-- Name: sql_observations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.sql_observations_id_seq OWNED BY public.sql_observations.id;


--
-- TOC entry 266 (class 1259 OID 3963273)
-- Name: sqlatable_user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sqlatable_user (
    id integer NOT NULL,
    user_id integer,
    table_id integer
);


ALTER TABLE public.sqlatable_user OWNER TO postgres;

--
-- TOC entry 265 (class 1259 OID 3963271)
-- Name: sqlatable_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.sqlatable_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.sqlatable_user_id_seq OWNER TO postgres;

--
-- TOC entry 3698 (class 0 OID 0)
-- Dependencies: 265
-- Name: sqlatable_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.sqlatable_user_id_seq OWNED BY public.sqlatable_user.id;


--
-- TOC entry 274 (class 1259 OID 3963400)
-- Name: tab_state; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tab_state (
    created_on timestamp without time zone,
    changed_on timestamp without time zone,
    extra_json text,
    id integer NOT NULL,
    user_id integer,
    label character varying(256),
    active boolean,
    database_id integer,
    schema character varying(256),
    sql text,
    query_limit integer,
    latest_query_id character varying(11),
    autorun boolean NOT NULL,
    template_params text,
    created_by_fk integer,
    changed_by_fk integer,
    hide_left_bar boolean DEFAULT false NOT NULL
);


ALTER TABLE public.tab_state OWNER TO postgres;

--
-- TOC entry 273 (class 1259 OID 3963398)
-- Name: tab_state_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tab_state_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tab_state_id_seq OWNER TO postgres;

--
-- TOC entry 3699 (class 0 OID 0)
-- Dependencies: 273
-- Name: tab_state_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tab_state_id_seq OWNED BY public.tab_state.id;


--
-- TOC entry 232 (class 1259 OID 3962796)
-- Name: table_columns; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.table_columns (
    created_on timestamp without time zone,
    changed_on timestamp without time zone,
    id integer NOT NULL,
    table_id integer,
    column_name character varying(255) NOT NULL,
    is_dttm boolean,
    is_active boolean,
    type character varying(32),
    groupby boolean,
    filterable boolean,
    description text,
    created_by_fk integer,
    changed_by_fk integer,
    expression text,
    verbose_name character varying(1024),
    python_date_format character varying(255),
    uuid uuid,
    extra text
);


ALTER TABLE public.table_columns OWNER TO postgres;

--
-- TOC entry 231 (class 1259 OID 3962794)
-- Name: table_columns_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.table_columns_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.table_columns_id_seq OWNER TO postgres;

--
-- TOC entry 3700 (class 0 OID 0)
-- Dependencies: 231
-- Name: table_columns_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.table_columns_id_seq OWNED BY public.table_columns.id;


--
-- TOC entry 276 (class 1259 OID 3963437)
-- Name: table_schema; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.table_schema (
    created_on timestamp without time zone,
    changed_on timestamp without time zone,
    extra_json text,
    id integer NOT NULL,
    tab_state_id integer,
    database_id integer NOT NULL,
    schema character varying(256),
    "table" character varying(256),
    description text,
    expanded boolean,
    created_by_fk integer,
    changed_by_fk integer
);


ALTER TABLE public.table_schema OWNER TO postgres;

--
-- TOC entry 275 (class 1259 OID 3963435)
-- Name: table_schema_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.table_schema_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.table_schema_id_seq OWNER TO postgres;

--
-- TOC entry 3701 (class 0 OID 0)
-- Dependencies: 275
-- Name: table_schema_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.table_schema_id_seq OWNED BY public.table_schema.id;


--
-- TOC entry 222 (class 1259 OID 3962669)
-- Name: tables; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tables (
    created_on timestamp without time zone,
    changed_on timestamp without time zone,
    id integer NOT NULL,
    table_name character varying(250) NOT NULL,
    main_dttm_col character varying(250),
    default_endpoint text,
    database_id integer NOT NULL,
    created_by_fk integer,
    changed_by_fk integer,
    "offset" integer,
    description text,
    is_featured boolean,
    cache_timeout integer,
    schema character varying(255),
    sql text,
    params text,
    perm character varying(1000),
    filter_select_enabled boolean,
    fetch_values_predicate text,
    is_sqllab_view boolean DEFAULT false,
    template_params text,
    schema_perm character varying(1000),
    extra text,
    uuid uuid
);


ALTER TABLE public.tables OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 3962667)
-- Name: tables_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tables_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tables_id_seq OWNER TO postgres;

--
-- TOC entry 3702 (class 0 OID 0)
-- Dependencies: 221
-- Name: tables_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tables_id_seq OWNED BY public.tables.id;


--
-- TOC entry 270 (class 1259 OID 3963321)
-- Name: tag; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tag (
    created_on timestamp without time zone,
    changed_on timestamp without time zone,
    id integer NOT NULL,
    name character varying(250),
    type public.tagtypes,
    created_by_fk integer,
    changed_by_fk integer
);


ALTER TABLE public.tag OWNER TO postgres;

--
-- TOC entry 269 (class 1259 OID 3963319)
-- Name: tag_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tag_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tag_id_seq OWNER TO postgres;

--
-- TOC entry 3703 (class 0 OID 0)
-- Dependencies: 269
-- Name: tag_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tag_id_seq OWNED BY public.tag.id;


--
-- TOC entry 272 (class 1259 OID 3963349)
-- Name: tagged_object; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tagged_object (
    created_on timestamp without time zone,
    changed_on timestamp without time zone,
    id integer NOT NULL,
    tag_id integer,
    object_id integer,
    object_type public.objecttypes,
    created_by_fk integer,
    changed_by_fk integer
);


ALTER TABLE public.tagged_object OWNER TO postgres;

--
-- TOC entry 271 (class 1259 OID 3963347)
-- Name: tagged_object_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tagged_object_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tagged_object_id_seq OWNER TO postgres;

--
-- TOC entry 3704 (class 0 OID 0)
-- Dependencies: 271
-- Name: tagged_object_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tagged_object_id_seq OWNED BY public.tagged_object.id;


--
-- TOC entry 238 (class 1259 OID 3962863)
-- Name: url; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.url (
    created_on timestamp without time zone,
    changed_on timestamp without time zone,
    id integer NOT NULL,
    url text,
    created_by_fk integer,
    changed_by_fk integer
);


ALTER TABLE public.url OWNER TO postgres;

--
-- TOC entry 237 (class 1259 OID 3962861)
-- Name: url_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.url_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.url_id_seq OWNER TO postgres;

--
-- TOC entry 3705 (class 0 OID 0)
-- Dependencies: 237
-- Name: url_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.url_id_seq OWNED BY public.url.id;


--
-- TOC entry 260 (class 1259 OID 3963169)
-- Name: user_attribute; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_attribute (
    created_on timestamp without time zone,
    changed_on timestamp without time zone,
    id integer NOT NULL,
    user_id integer,
    welcome_dashboard_id integer,
    created_by_fk integer,
    changed_by_fk integer
);


ALTER TABLE public.user_attribute OWNER TO postgres;

--
-- TOC entry 259 (class 1259 OID 3963167)
-- Name: user_attribute_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_attribute_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_attribute_id_seq OWNER TO postgres;

--
-- TOC entry 3706 (class 0 OID 0)
-- Dependencies: 259
-- Name: user_attribute_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_attribute_id_seq OWNED BY public.user_attribute.id;


--
-- TOC entry 3064 (class 2604 OID 3963010)
-- Name: access_request id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.access_request ALTER COLUMN id SET DEFAULT nextval('public.access_request_id_seq'::regclass);


--
-- TOC entry 3083 (class 2604 OID 3963563)
-- Name: alert_logs id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alert_logs ALTER COLUMN id SET DEFAULT nextval('public.alert_logs_id_seq'::regclass);


--
-- TOC entry 3084 (class 2604 OID 3963576)
-- Name: alert_owner id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alert_owner ALTER COLUMN id SET DEFAULT nextval('public.alert_owner_id_seq'::regclass);


--
-- TOC entry 3082 (class 2604 OID 3963541)
-- Name: alerts id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alerts ALTER COLUMN id SET DEFAULT nextval('public.alerts_id_seq'::regclass);


--
-- TOC entry 3068 (class 2604 OID 3963103)
-- Name: annotation id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.annotation ALTER COLUMN id SET DEFAULT nextval('public.annotation_id_seq'::regclass);


--
-- TOC entry 3067 (class 2604 OID 3963082)
-- Name: annotation_layer id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.annotation_layer ALTER COLUMN id SET DEFAULT nextval('public.annotation_layer_id_seq'::regclass);


--
-- TOC entry 3086 (class 2604 OID 3963683)
-- Name: cache_keys id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cache_keys ALTER COLUMN id SET DEFAULT nextval('public.cache_keys_id_seq'::regclass);


--
-- TOC entry 3042 (class 2604 OID 3962572)
-- Name: clusters id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clusters ALTER COLUMN id SET DEFAULT nextval('public.clusters_id_seq'::regclass);


--
-- TOC entry 3050 (class 2604 OID 3962700)
-- Name: columns id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.columns ALTER COLUMN id SET DEFAULT nextval('public.columns_id_seq'::regclass);


--
-- TOC entry 3058 (class 2604 OID 3962887)
-- Name: css_templates id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.css_templates ALTER COLUMN id SET DEFAULT nextval('public.css_templates_id_seq'::regclass);


--
-- TOC entry 3070 (class 2604 OID 3963206)
-- Name: dashboard_email_schedules id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dashboard_email_schedules ALTER COLUMN id SET DEFAULT nextval('public.dashboard_email_schedules_id_seq'::regclass);


--
-- TOC entry 3095 (class 2604 OID 3963852)
-- Name: dashboard_roles id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dashboard_roles ALTER COLUMN id SET DEFAULT nextval('public.dashboard_roles_id_seq'::regclass);


--
-- TOC entry 3055 (class 2604 OID 3962825)
-- Name: dashboard_slices id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dashboard_slices ALTER COLUMN id SET DEFAULT nextval('public.dashboard_slices_id_seq'::regclass);


--
-- TOC entry 3060 (class 2604 OID 3962933)
-- Name: dashboard_user id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dashboard_user ALTER COLUMN id SET DEFAULT nextval('public.dashboard_user_id_seq'::regclass);


--
-- TOC entry 3043 (class 2604 OID 3962595)
-- Name: dashboards id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dashboards ALTER COLUMN id SET DEFAULT nextval('public.dashboards_id_seq'::regclass);


--
-- TOC entry 3047 (class 2604 OID 3962639)
-- Name: datasources id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.datasources ALTER COLUMN id SET DEFAULT nextval('public.datasources_id_seq'::regclass);


--
-- TOC entry 3044 (class 2604 OID 3962616)
-- Name: dbs id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dbs ALTER COLUMN id SET DEFAULT nextval('public.dbs_id_seq'::regclass);


--
-- TOC entry 3073 (class 2604 OID 3963294)
-- Name: druiddatasource_user id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.druiddatasource_user ALTER COLUMN id SET DEFAULT nextval('public.druiddatasource_user_id_seq'::regclass);


--
-- TOC entry 3094 (class 2604 OID 3963825)
-- Name: dynamic_plugin id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dynamic_plugin ALTER COLUMN id SET DEFAULT nextval('public.dynamic_plugin_id_seq'::regclass);


--
-- TOC entry 3059 (class 2604 OID 3962908)
-- Name: favstar id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.favstar ALTER COLUMN id SET DEFAULT nextval('public.favstar_id_seq'::regclass);


--
-- TOC entry 3096 (class 2604 OID 3963938)
-- Name: filter_sets id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.filter_sets ALTER COLUMN id SET DEFAULT nextval('public.filter_sets_id_seq'::regclass);


--
-- TOC entry 3065 (class 2604 OID 3963036)
-- Name: keyvalue id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.keyvalue ALTER COLUMN id SET DEFAULT nextval('public.keyvalue_id_seq'::regclass);


--
-- TOC entry 3056 (class 2604 OID 3962845)
-- Name: logs id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.logs ALTER COLUMN id SET DEFAULT nextval('public.logs_id_seq'::regclass);


--
-- TOC entry 3051 (class 2604 OID 3962721)
-- Name: metrics id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.metrics ALTER COLUMN id SET DEFAULT nextval('public.metrics_id_seq'::regclass);


--
-- TOC entry 3062 (class 2604 OID 3962988)
-- Name: query id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.query ALTER COLUMN id SET DEFAULT nextval('public.query_id_seq'::regclass);


--
-- TOC entry 3091 (class 2604 OID 3963765)
-- Name: report_execution_log id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.report_execution_log ALTER COLUMN id SET DEFAULT nextval('public.report_execution_log_id_seq'::regclass);


--
-- TOC entry 3092 (class 2604 OID 3963781)
-- Name: report_recipient id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.report_recipient ALTER COLUMN id SET DEFAULT nextval('public.report_recipient_id_seq'::regclass);


--
-- TOC entry 3087 (class 2604 OID 3963724)
-- Name: report_schedule id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.report_schedule ALTER COLUMN id SET DEFAULT nextval('public.report_schedule_id_seq'::regclass);


--
-- TOC entry 3093 (class 2604 OID 3963807)
-- Name: report_schedule_user id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.report_schedule_user ALTER COLUMN id SET DEFAULT nextval('public.report_schedule_user_id_seq'::regclass);


--
-- TOC entry 3080 (class 2604 OID 3963505)
-- Name: rls_filter_roles id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rls_filter_roles ALTER COLUMN id SET DEFAULT nextval('public.rls_filter_roles_id_seq'::regclass);


--
-- TOC entry 3081 (class 2604 OID 3963523)
-- Name: rls_filter_tables id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rls_filter_tables ALTER COLUMN id SET DEFAULT nextval('public.rls_filter_tables_id_seq'::regclass);


--
-- TOC entry 3079 (class 2604 OID 3963479)
-- Name: row_level_security_filters id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.row_level_security_filters ALTER COLUMN id SET DEFAULT nextval('public.row_level_security_filters_id_seq'::regclass);


--
-- TOC entry 3066 (class 2604 OID 3963051)
-- Name: saved_query id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.saved_query ALTER COLUMN id SET DEFAULT nextval('public.saved_query_id_seq'::regclass);


--
-- TOC entry 3071 (class 2604 OID 3963244)
-- Name: slice_email_schedules id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.slice_email_schedules ALTER COLUMN id SET DEFAULT nextval('public.slice_email_schedules_id_seq'::regclass);


--
-- TOC entry 3061 (class 2604 OID 3962951)
-- Name: slice_user id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.slice_user ALTER COLUMN id SET DEFAULT nextval('public.slice_user_id_seq'::regclass);


--
-- TOC entry 3052 (class 2604 OID 3962742)
-- Name: slices id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.slices ALTER COLUMN id SET DEFAULT nextval('public.slices_id_seq'::regclass);


--
-- TOC entry 3053 (class 2604 OID 3962773)
-- Name: sql_metrics id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sql_metrics ALTER COLUMN id SET DEFAULT nextval('public.sql_metrics_id_seq'::regclass);


--
-- TOC entry 3085 (class 2604 OID 3963651)
-- Name: sql_observations id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sql_observations ALTER COLUMN id SET DEFAULT nextval('public.sql_observations_id_seq'::regclass);


--
-- TOC entry 3072 (class 2604 OID 3963276)
-- Name: sqlatable_user id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sqlatable_user ALTER COLUMN id SET DEFAULT nextval('public.sqlatable_user_id_seq'::regclass);


--
-- TOC entry 3076 (class 2604 OID 3963403)
-- Name: tab_state id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tab_state ALTER COLUMN id SET DEFAULT nextval('public.tab_state_id_seq'::regclass);


--
-- TOC entry 3054 (class 2604 OID 3962799)
-- Name: table_columns id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.table_columns ALTER COLUMN id SET DEFAULT nextval('public.table_columns_id_seq'::regclass);


--
-- TOC entry 3078 (class 2604 OID 3963440)
-- Name: table_schema id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.table_schema ALTER COLUMN id SET DEFAULT nextval('public.table_schema_id_seq'::regclass);


--
-- TOC entry 3048 (class 2604 OID 3962672)
-- Name: tables id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tables ALTER COLUMN id SET DEFAULT nextval('public.tables_id_seq'::regclass);


--
-- TOC entry 3074 (class 2604 OID 3963324)
-- Name: tag id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tag ALTER COLUMN id SET DEFAULT nextval('public.tag_id_seq'::regclass);


--
-- TOC entry 3075 (class 2604 OID 3963352)
-- Name: tagged_object id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tagged_object ALTER COLUMN id SET DEFAULT nextval('public.tagged_object_id_seq'::regclass);


--
-- TOC entry 3057 (class 2604 OID 3962866)
-- Name: url id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.url ALTER COLUMN id SET DEFAULT nextval('public.url_id_seq'::regclass);


--
-- TOC entry 3069 (class 2604 OID 3963172)
-- Name: user_attribute id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_attribute ALTER COLUMN id SET DEFAULT nextval('public.user_attribute_id_seq'::regclass);


--
-- TOC entry 3545 (class 0 OID 3962444)
-- Dependencies: 197
-- Data for Name: ab_permission; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.ab_permission (id, name) VALUES (1, 'can_read');
INSERT INTO public.ab_permission (id, name) VALUES (2, 'can_write');
INSERT INTO public.ab_permission (id, name) VALUES (3, 'can_this_form_post');
INSERT INTO public.ab_permission (id, name) VALUES (4, 'can_this_form_get');
INSERT INTO public.ab_permission (id, name) VALUES (5, 'can_delete');
INSERT INTO public.ab_permission (id, name) VALUES (6, 'can_edit');
INSERT INTO public.ab_permission (id, name) VALUES (7, 'can_userinfo');
INSERT INTO public.ab_permission (id, name) VALUES (8, 'can_add');
INSERT INTO public.ab_permission (id, name) VALUES (9, 'can_show');
INSERT INTO public.ab_permission (id, name) VALUES (10, 'can_list');
INSERT INTO public.ab_permission (id, name) VALUES (11, 'resetmypassword');
INSERT INTO public.ab_permission (id, name) VALUES (12, 'resetpasswords');
INSERT INTO public.ab_permission (id, name) VALUES (13, 'userinfoedit');
INSERT INTO public.ab_permission (id, name) VALUES (14, 'copyrole');
INSERT INTO public.ab_permission (id, name) VALUES (15, 'can_get');
INSERT INTO public.ab_permission (id, name) VALUES (16, 'can_invalidate');
INSERT INTO public.ab_permission (id, name) VALUES (17, 'can_download');
INSERT INTO public.ab_permission (id, name) VALUES (18, 'muldelete');
INSERT INTO public.ab_permission (id, name) VALUES (19, 'can_query');
INSERT INTO public.ab_permission (id, name) VALUES (20, 'can_time_range');
INSERT INTO public.ab_permission (id, name) VALUES (21, 'can_query_form_data');
INSERT INTO public.ab_permission (id, name) VALUES (22, 'can_external_metadata_by_name');
INSERT INTO public.ab_permission (id, name) VALUES (23, 'can_save');
INSERT INTO public.ab_permission (id, name) VALUES (24, 'can_external_metadata');
INSERT INTO public.ab_permission (id, name) VALUES (25, 'can_get_value');
INSERT INTO public.ab_permission (id, name) VALUES (26, 'can_store');
INSERT INTO public.ab_permission (id, name) VALUES (27, 'can_shortner');
INSERT INTO public.ab_permission (id, name) VALUES (28, 'can_my_queries');
INSERT INTO public.ab_permission (id, name) VALUES (29, 'can_fetch_datasource_metadata');
INSERT INTO public.ab_permission (id, name) VALUES (30, 'can_datasources');
INSERT INTO public.ab_permission (id, name) VALUES (31, 'can_warm_up_cache');
INSERT INTO public.ab_permission (id, name) VALUES (32, 'can_validate_sql_json');
INSERT INTO public.ab_permission (id, name) VALUES (33, 'can_created_dashboards');
INSERT INTO public.ab_permission (id, name) VALUES (34, 'can_recent_activity');
INSERT INTO public.ab_permission (id, name) VALUES (35, 'can_save_dash');
INSERT INTO public.ab_permission (id, name) VALUES (36, 'can_slice_json');
INSERT INTO public.ab_permission (id, name) VALUES (37, 'can_tables');
INSERT INTO public.ab_permission (id, name) VALUES (38, 'can_available_domains');
INSERT INTO public.ab_permission (id, name) VALUES (39, 'can_log');
INSERT INTO public.ab_permission (id, name) VALUES (40, 'can_request_access');
INSERT INTO public.ab_permission (id, name) VALUES (41, 'can_filter');
INSERT INTO public.ab_permission (id, name) VALUES (42, 'can_slice');
INSERT INTO public.ab_permission (id, name) VALUES (43, 'can_sqllab_viz');
INSERT INTO public.ab_permission (id, name) VALUES (44, 'can_user_slices');
INSERT INTO public.ab_permission (id, name) VALUES (45, 'can_stop_query');
INSERT INTO public.ab_permission (id, name) VALUES (46, 'can_results');
INSERT INTO public.ab_permission (id, name) VALUES (47, 'can_queries');
INSERT INTO public.ab_permission (id, name) VALUES (48, 'can_csrf_token');
INSERT INTO public.ab_permission (id, name) VALUES (49, 'can_profile');
INSERT INTO public.ab_permission (id, name) VALUES (50, 'can_sql_json');
INSERT INTO public.ab_permission (id, name) VALUES (51, 'can_testconn');
INSERT INTO public.ab_permission (id, name) VALUES (52, 'can_annotation_json');
INSERT INTO public.ab_permission (id, name) VALUES (53, 'can_import_dashboards');
INSERT INTO public.ab_permission (id, name) VALUES (54, 'can_fave_dashboards');
INSERT INTO public.ab_permission (id, name) VALUES (55, 'can_sqllab');
INSERT INTO public.ab_permission (id, name) VALUES (56, 'can_estimate_query_cost');
INSERT INTO public.ab_permission (id, name) VALUES (57, 'can_favstar');
INSERT INTO public.ab_permission (id, name) VALUES (58, 'can_fave_slices');
INSERT INTO public.ab_permission (id, name) VALUES (59, 'can_override_role_permissions');
INSERT INTO public.ab_permission (id, name) VALUES (60, 'can_add_slices');
INSERT INTO public.ab_permission (id, name) VALUES (61, 'can_explore');
INSERT INTO public.ab_permission (id, name) VALUES (62, 'can_select_star');
INSERT INTO public.ab_permission (id, name) VALUES (63, 'can_approve');
INSERT INTO public.ab_permission (id, name) VALUES (64, 'can_schemas_access_for_file_upload');
INSERT INTO public.ab_permission (id, name) VALUES (65, 'can_schemas');
INSERT INTO public.ab_permission (id, name) VALUES (66, 'can_search_queries');
INSERT INTO public.ab_permission (id, name) VALUES (67, 'can_csv');
INSERT INTO public.ab_permission (id, name) VALUES (68, 'can_extra_table_metadata');
INSERT INTO public.ab_permission (id, name) VALUES (69, 'can_created_slices');
INSERT INTO public.ab_permission (id, name) VALUES (70, 'can_sqllab_history');
INSERT INTO public.ab_permission (id, name) VALUES (71, 'can_sync_druid_source');
INSERT INTO public.ab_permission (id, name) VALUES (72, 'can_fave_dashboards_by_username');
INSERT INTO public.ab_permission (id, name) VALUES (73, 'can_sqllab_table_viz');
INSERT INTO public.ab_permission (id, name) VALUES (74, 'can_publish');
INSERT INTO public.ab_permission (id, name) VALUES (75, 'can_copy_dash');
INSERT INTO public.ab_permission (id, name) VALUES (76, 'can_explore_json');
INSERT INTO public.ab_permission (id, name) VALUES (77, 'can_dashboard');
INSERT INTO public.ab_permission (id, name) VALUES (78, 'can_post');
INSERT INTO public.ab_permission (id, name) VALUES (79, 'can_expanded');
INSERT INTO public.ab_permission (id, name) VALUES (80, 'can_put');
INSERT INTO public.ab_permission (id, name) VALUES (81, 'can_activate');
INSERT INTO public.ab_permission (id, name) VALUES (82, 'can_delete_query');
INSERT INTO public.ab_permission (id, name) VALUES (83, 'can_migrate_query');
INSERT INTO public.ab_permission (id, name) VALUES (84, 'can_suggestions');
INSERT INTO public.ab_permission (id, name) VALUES (85, 'can_tagged_objects');
INSERT INTO public.ab_permission (id, name) VALUES (86, 'yaml_export');
INSERT INTO public.ab_permission (id, name) VALUES (87, 'can_scan_new_datasources');
INSERT INTO public.ab_permission (id, name) VALUES (88, 'can_refresh_datasources');
INSERT INTO public.ab_permission (id, name) VALUES (89, 'menu_access');
INSERT INTO public.ab_permission (id, name) VALUES (90, 'all_datasource_access');
INSERT INTO public.ab_permission (id, name) VALUES (91, 'all_database_access');
INSERT INTO public.ab_permission (id, name) VALUES (92, 'all_query_access');
INSERT INTO public.ab_permission (id, name) VALUES (93, 'can_share_dashboard');
INSERT INTO public.ab_permission (id, name) VALUES (94, 'can_share_chart');
INSERT INTO public.ab_permission (id, name) VALUES (95, 'database_access');
INSERT INTO public.ab_permission (id, name) VALUES (96, 'schema_access');


--
-- TOC entry 3555 (class 0 OID 3962507)
-- Dependencies: 207
-- Data for Name: ab_permission_view; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (1, 1, 1);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (2, 2, 1);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (3, 1, 2);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (4, 2, 2);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (5, 1, 3);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (6, 2, 3);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (7, 1, 4);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (8, 2, 4);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (9, 1, 5);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (10, 2, 5);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (11, 1, 6);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (12, 2, 6);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (13, 1, 7);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (14, 2, 7);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (15, 1, 8);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (16, 2, 8);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (17, 1, 9);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (18, 2, 9);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (19, 1, 10);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (20, 3, 15);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (21, 4, 15);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (22, 3, 16);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (23, 4, 16);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (24, 3, 17);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (25, 4, 17);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (26, 5, 19);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (27, 6, 19);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (28, 7, 19);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (29, 8, 19);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (30, 9, 19);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (31, 10, 19);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (32, 11, 19);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (33, 12, 19);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (34, 13, 19);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (35, 5, 20);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (36, 6, 20);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (37, 8, 20);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (38, 9, 20);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (39, 10, 20);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (40, 14, 20);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (41, 15, 21);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (42, 9, 22);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (43, 15, 23);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (44, 10, 24);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (45, 16, 25);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (46, 8, 26);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (47, 5, 26);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (48, 6, 26);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (49, 10, 26);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (50, 5, 27);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (51, 17, 27);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (52, 6, 27);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (53, 8, 27);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (54, 2, 27);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (55, 9, 27);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (56, 10, 27);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (57, 5, 28);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (58, 17, 28);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (59, 6, 28);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (60, 8, 28);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (61, 9, 28);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (62, 10, 28);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (63, 18, 28);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (64, 19, 29);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (65, 20, 29);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (66, 21, 29);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (67, 3, 30);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (68, 4, 30);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (69, 3, 31);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (70, 4, 31);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (71, 3, 32);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (72, 4, 32);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (73, 22, 33);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (74, 23, 33);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (75, 15, 33);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (76, 24, 33);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (77, 25, 34);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (78, 26, 34);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (79, 27, 35);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (80, 28, 36);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (81, 29, 37);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (82, 30, 37);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (83, 31, 37);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (84, 32, 37);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (85, 33, 37);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (86, 34, 37);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (87, 35, 37);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (88, 36, 37);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (89, 37, 37);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (90, 38, 37);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (91, 39, 37);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (92, 40, 37);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (93, 41, 37);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (94, 42, 37);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (95, 43, 37);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (96, 44, 37);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (97, 45, 37);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (98, 46, 37);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (99, 47, 37);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (100, 48, 37);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (101, 49, 37);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (102, 50, 37);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (103, 51, 37);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (104, 52, 37);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (105, 53, 37);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (106, 54, 37);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (107, 55, 37);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (108, 56, 37);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (109, 57, 37);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (110, 58, 37);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (111, 59, 37);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (112, 60, 37);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (113, 61, 37);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (114, 62, 37);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (115, 63, 37);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (116, 64, 37);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (117, 65, 37);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (118, 66, 37);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (119, 67, 37);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (120, 68, 37);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (121, 69, 37);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (122, 70, 37);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (123, 71, 37);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (124, 72, 37);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (125, 73, 37);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (126, 74, 37);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (127, 75, 37);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (128, 76, 37);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (129, 77, 37);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (130, 78, 38);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (131, 79, 38);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (132, 5, 38);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (133, 80, 39);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (134, 81, 39);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (135, 5, 39);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (136, 15, 39);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (137, 82, 39);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (138, 83, 39);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (139, 78, 39);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (140, 5, 40);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (141, 84, 40);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (142, 15, 40);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (143, 78, 40);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (144, 85, 40);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (145, 1, 41);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (146, 5, 42);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (147, 6, 42);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (148, 8, 42);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (149, 9, 42);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (150, 10, 42);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (151, 18, 42);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (152, 5, 43);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (153, 6, 43);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (154, 8, 43);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (155, 9, 43);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (156, 10, 43);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (157, 18, 43);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (158, 5, 44);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (159, 6, 44);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (160, 8, 44);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (161, 9, 44);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (162, 10, 44);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (163, 9, 45);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (164, 10, 45);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (165, 9, 46);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (166, 10, 46);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (167, 5, 47);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (168, 6, 47);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (169, 8, 47);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (170, 9, 47);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (171, 10, 47);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (172, 18, 47);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (173, 5, 48);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (174, 6, 48);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (175, 8, 48);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (176, 9, 48);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (177, 10, 48);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (178, 18, 48);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (179, 86, 48);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (180, 5, 49);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (181, 6, 49);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (182, 8, 49);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (183, 9, 49);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (184, 10, 49);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (185, 18, 49);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (186, 86, 49);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (187, 5, 50);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (188, 6, 50);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (189, 8, 50);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (190, 10, 50);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (191, 5, 51);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (192, 6, 51);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (193, 8, 51);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (194, 10, 51);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (195, 87, 52);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (196, 88, 52);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (197, 89, 53);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (198, 89, 54);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (199, 89, 55);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (200, 89, 56);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (201, 89, 57);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (202, 89, 58);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (203, 89, 59);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (204, 89, 60);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (205, 89, 61);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (206, 89, 62);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (207, 89, 63);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (208, 89, 64);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (209, 89, 65);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (210, 89, 66);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (211, 89, 67);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (212, 89, 68);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (213, 89, 69);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (214, 89, 70);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (215, 89, 71);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (216, 89, 72);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (217, 89, 73);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (218, 89, 74);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (219, 89, 75);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (220, 89, 76);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (221, 89, 77);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (222, 89, 78);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (223, 89, 79);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (224, 89, 80);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (225, 89, 81);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (226, 89, 82);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (227, 89, 83);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (228, 89, 84);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (229, 90, 85);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (230, 91, 86);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (231, 92, 87);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (232, 93, 37);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (233, 94, 37);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (234, 95, 88);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (235, 96, 89);
INSERT INTO public.ab_permission_view (id, permission_id, view_menu_id) VALUES (236, 96, 90);


--
-- TOC entry 3559 (class 0 OID 3962545)
-- Dependencies: 211
-- Data for Name: ab_permission_view_role; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (1, 20, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (2, 21, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (3, 22, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (4, 23, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (5, 24, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (6, 25, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (7, 26, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (8, 27, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (9, 28, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (10, 29, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (11, 30, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (12, 31, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (13, 32, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (14, 33, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (15, 34, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (16, 35, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (17, 36, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (18, 37, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (19, 38, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (20, 39, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (21, 40, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (22, 41, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (23, 42, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (24, 43, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (25, 9, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (26, 10, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (27, 44, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (28, 45, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (29, 7, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (30, 8, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (31, 3, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (32, 4, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (33, 15, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (34, 16, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (35, 17, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (36, 18, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (37, 11, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (38, 12, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (39, 19, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (40, 1, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (41, 2, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (42, 5, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (43, 6, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (44, 46, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (45, 47, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (46, 48, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (47, 49, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (48, 50, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (49, 51, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (50, 52, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (51, 53, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (52, 54, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (53, 55, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (54, 56, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (55, 57, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (56, 58, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (57, 59, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (58, 60, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (59, 61, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (60, 62, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (61, 63, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (62, 64, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (63, 65, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (64, 66, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (65, 67, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (66, 68, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (67, 69, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (68, 70, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (69, 71, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (70, 72, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (71, 73, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (72, 74, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (73, 75, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (74, 76, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (75, 77, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (76, 78, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (77, 79, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (78, 80, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (79, 81, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (80, 82, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (81, 83, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (82, 84, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (83, 85, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (84, 86, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (85, 87, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (86, 88, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (87, 89, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (88, 90, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (89, 91, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (90, 92, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (91, 93, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (92, 94, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (93, 95, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (94, 96, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (95, 97, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (96, 98, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (97, 99, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (98, 100, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (99, 101, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (100, 102, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (101, 103, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (102, 104, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (103, 105, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (104, 106, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (105, 107, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (106, 108, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (107, 109, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (108, 110, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (109, 111, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (110, 112, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (111, 113, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (112, 114, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (113, 115, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (114, 116, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (115, 117, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (116, 118, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (117, 119, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (118, 120, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (119, 121, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (120, 122, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (121, 123, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (122, 124, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (123, 125, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (124, 126, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (125, 127, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (126, 128, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (127, 129, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (128, 130, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (129, 131, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (130, 132, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (131, 133, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (132, 134, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (133, 135, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (134, 136, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (135, 137, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (136, 138, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (137, 139, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (138, 140, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (139, 141, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (140, 142, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (141, 143, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (142, 144, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (143, 13, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (144, 14, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (145, 145, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (146, 146, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (147, 147, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (148, 148, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (149, 149, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (150, 150, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (151, 151, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (152, 152, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (153, 153, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (154, 154, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (155, 155, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (156, 156, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (157, 157, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (158, 158, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (159, 159, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (160, 160, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (161, 161, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (162, 162, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (163, 163, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (164, 164, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (165, 165, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (166, 166, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (167, 167, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (168, 168, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (169, 169, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (170, 170, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (171, 171, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (172, 172, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (173, 173, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (174, 174, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (175, 175, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (176, 176, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (177, 177, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (178, 178, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (179, 179, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (180, 180, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (181, 181, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (182, 182, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (183, 183, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (184, 184, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (185, 185, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (186, 186, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (187, 187, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (188, 188, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (189, 189, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (190, 190, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (191, 191, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (192, 192, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (193, 193, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (194, 194, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (195, 195, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (196, 196, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (197, 197, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (198, 198, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (199, 199, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (200, 200, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (201, 201, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (202, 202, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (203, 203, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (204, 204, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (205, 205, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (206, 206, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (207, 207, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (208, 208, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (209, 209, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (210, 210, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (211, 211, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (212, 212, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (213, 213, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (214, 214, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (215, 215, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (216, 216, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (217, 217, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (218, 218, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (219, 219, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (220, 220, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (221, 221, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (222, 222, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (223, 223, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (224, 224, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (225, 225, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (226, 226, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (227, 227, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (228, 228, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (229, 229, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (230, 230, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (231, 231, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (232, 232, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (233, 233, 1);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (234, 1, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (235, 2, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (236, 3, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (237, 4, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (238, 5, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (239, 6, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (240, 7, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (241, 8, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (242, 9, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (243, 10, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (244, 11, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (245, 12, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (246, 15, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (247, 16, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (248, 17, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (249, 19, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (250, 22, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (251, 23, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (252, 24, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (253, 25, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (254, 28, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (255, 32, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (256, 41, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (257, 42, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (258, 43, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (259, 44, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (260, 45, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (261, 46, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (262, 47, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (263, 48, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (264, 49, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (265, 55, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (266, 56, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (267, 64, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (268, 65, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (269, 66, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (270, 67, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (271, 68, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (272, 69, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (273, 70, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (274, 71, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (275, 72, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (276, 73, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (277, 74, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (278, 75, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (279, 76, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (280, 77, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (281, 78, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (282, 79, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (283, 80, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (284, 81, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (285, 82, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (286, 83, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (287, 84, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (288, 85, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (289, 86, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (290, 87, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (291, 88, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (292, 89, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (293, 90, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (294, 91, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (295, 92, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (296, 93, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (297, 94, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (298, 95, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (299, 96, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (300, 97, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (301, 98, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (302, 99, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (303, 100, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (304, 101, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (305, 103, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (306, 104, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (307, 105, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (308, 106, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (309, 107, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (310, 108, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (311, 109, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (312, 110, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (313, 112, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (314, 113, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (315, 114, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (316, 116, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (317, 117, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (318, 118, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (319, 119, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (320, 120, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (321, 121, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (322, 122, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (323, 124, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (324, 125, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (325, 126, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (326, 127, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (327, 128, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (328, 129, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (329, 130, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (330, 131, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (331, 132, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (332, 133, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (333, 134, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (334, 135, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (335, 136, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (336, 137, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (337, 138, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (338, 139, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (339, 140, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (340, 141, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (341, 142, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (342, 143, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (343, 144, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (344, 145, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (345, 146, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (346, 147, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (347, 148, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (348, 149, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (349, 150, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (350, 151, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (351, 152, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (352, 153, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (353, 154, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (354, 155, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (355, 156, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (356, 157, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (357, 158, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (358, 159, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (359, 160, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (360, 161, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (361, 162, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (362, 163, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (363, 164, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (364, 165, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (365, 166, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (366, 173, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (367, 174, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (368, 175, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (369, 176, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (370, 177, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (371, 178, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (372, 179, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (373, 183, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (374, 184, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (375, 187, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (376, 188, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (377, 189, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (378, 190, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (379, 191, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (380, 192, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (381, 193, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (382, 194, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (383, 195, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (384, 196, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (385, 198, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (386, 199, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (387, 201, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (388, 202, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (389, 203, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (390, 204, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (391, 205, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (392, 206, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (393, 207, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (394, 208, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (395, 209, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (396, 210, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (397, 211, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (398, 212, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (399, 213, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (400, 214, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (401, 216, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (402, 217, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (403, 218, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (404, 219, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (405, 220, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (406, 221, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (407, 222, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (408, 223, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (409, 224, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (410, 225, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (411, 226, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (412, 227, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (413, 229, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (414, 230, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (415, 232, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (416, 233, 3);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (417, 1, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (418, 2, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (419, 3, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (420, 4, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (421, 5, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (422, 6, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (423, 7, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (424, 8, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (425, 9, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (426, 10, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (427, 11, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (428, 15, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (429, 16, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (430, 17, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (431, 19, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (432, 22, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (433, 23, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (434, 24, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (435, 25, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (436, 28, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (437, 32, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (438, 41, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (439, 42, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (440, 43, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (441, 44, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (442, 45, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (443, 46, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (444, 47, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (445, 48, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (446, 49, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (447, 55, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (448, 56, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (449, 64, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (450, 65, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (451, 66, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (452, 67, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (453, 68, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (454, 69, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (455, 70, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (456, 71, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (457, 72, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (458, 73, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (459, 75, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (460, 76, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (461, 77, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (462, 78, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (463, 79, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (464, 80, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (465, 81, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (466, 82, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (467, 83, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (468, 84, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (469, 85, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (470, 86, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (471, 87, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (472, 88, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (473, 89, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (474, 90, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (475, 91, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (476, 92, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (477, 93, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (478, 94, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (479, 95, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (480, 96, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (481, 97, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (482, 98, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (483, 99, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (484, 100, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (485, 101, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (486, 103, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (487, 104, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (488, 105, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (489, 106, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (490, 107, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (491, 108, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (492, 109, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (493, 110, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (494, 112, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (495, 113, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (496, 114, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (497, 116, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (498, 117, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (499, 118, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (500, 119, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (501, 120, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (502, 121, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (503, 122, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (504, 124, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (505, 125, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (506, 126, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (507, 127, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (508, 128, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (509, 129, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (510, 130, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (511, 131, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (512, 132, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (513, 133, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (514, 134, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (515, 135, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (516, 136, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (517, 137, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (518, 138, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (519, 139, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (520, 140, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (521, 141, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (522, 142, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (523, 143, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (524, 144, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (525, 145, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (526, 146, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (527, 147, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (528, 148, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (529, 149, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (530, 150, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (531, 152, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (532, 153, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (533, 154, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (534, 155, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (535, 156, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (536, 158, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (537, 159, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (538, 160, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (539, 161, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (540, 162, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (541, 163, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (542, 164, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (543, 165, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (544, 166, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (545, 176, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (546, 177, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (547, 183, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (548, 184, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (549, 190, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (550, 194, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (551, 195, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (552, 196, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (553, 198, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (554, 199, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (555, 201, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (556, 202, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (557, 203, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (558, 205, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (559, 206, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (560, 208, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (561, 209, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (562, 210, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (563, 211, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (564, 212, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (565, 213, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (566, 214, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (567, 216, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (568, 217, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (569, 218, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (570, 219, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (571, 220, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (572, 221, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (573, 223, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (574, 224, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (575, 225, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (576, 226, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (577, 227, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (578, 232, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (579, 233, 4);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (580, 111, 5);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (581, 115, 5);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (582, 1, 6);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (583, 17, 6);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (584, 95, 6);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (585, 102, 6);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (586, 107, 6);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (587, 119, 6);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (588, 125, 6);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (589, 215, 6);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (590, 216, 6);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (591, 217, 6);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (592, 218, 6);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (593, 1, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (594, 2, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (595, 3, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (596, 4, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (597, 5, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (598, 6, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (599, 7, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (600, 8, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (601, 9, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (602, 10, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (603, 11, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (604, 12, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (605, 15, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (606, 16, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (607, 17, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (608, 19, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (609, 22, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (610, 23, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (611, 24, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (612, 25, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (613, 28, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (614, 32, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (615, 41, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (616, 42, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (617, 43, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (618, 44, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (619, 45, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (620, 46, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (621, 47, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (622, 48, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (623, 49, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (624, 55, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (625, 56, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (626, 64, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (627, 65, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (628, 66, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (629, 67, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (630, 68, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (631, 69, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (632, 70, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (633, 71, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (634, 72, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (635, 73, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (636, 74, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (637, 75, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (638, 76, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (639, 77, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (640, 78, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (641, 79, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (642, 80, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (643, 81, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (644, 82, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (645, 83, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (646, 84, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (647, 85, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (648, 86, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (649, 87, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (650, 88, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (651, 89, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (652, 90, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (653, 91, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (654, 92, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (655, 93, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (656, 94, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (657, 95, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (658, 96, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (659, 97, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (660, 98, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (661, 99, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (662, 100, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (663, 101, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (664, 103, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (665, 104, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (666, 105, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (667, 106, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (668, 107, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (669, 108, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (670, 109, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (671, 110, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (672, 112, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (673, 113, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (674, 114, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (675, 116, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (676, 117, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (677, 118, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (678, 119, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (679, 120, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (680, 121, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (681, 122, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (682, 124, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (683, 125, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (684, 126, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (685, 127, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (686, 128, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (687, 129, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (688, 130, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (689, 131, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (690, 132, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (691, 133, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (692, 134, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (693, 135, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (694, 136, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (695, 137, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (696, 138, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (697, 139, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (698, 140, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (699, 141, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (700, 142, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (701, 143, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (702, 144, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (703, 145, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (704, 146, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (705, 147, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (706, 148, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (707, 149, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (708, 150, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (709, 151, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (710, 152, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (711, 153, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (712, 154, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (713, 155, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (714, 156, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (715, 157, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (716, 158, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (717, 159, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (718, 160, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (719, 161, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (720, 162, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (721, 163, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (722, 164, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (723, 165, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (724, 166, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (725, 173, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (726, 174, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (727, 175, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (728, 176, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (729, 177, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (730, 178, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (731, 179, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (732, 183, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (733, 184, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (734, 187, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (735, 188, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (736, 189, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (737, 190, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (738, 191, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (739, 192, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (740, 193, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (741, 194, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (742, 195, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (743, 196, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (744, 198, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (745, 199, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (746, 201, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (747, 202, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (748, 203, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (749, 204, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (750, 205, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (751, 206, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (752, 207, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (753, 208, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (754, 209, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (755, 210, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (756, 211, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (757, 212, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (758, 213, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (759, 214, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (760, 216, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (761, 217, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (762, 218, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (763, 219, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (764, 220, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (765, 221, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (766, 222, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (767, 223, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (768, 224, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (769, 225, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (770, 226, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (771, 227, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (772, 229, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (773, 230, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (774, 232, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (775, 233, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (776, 102, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (777, 215, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (778, 234, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (779, 235, 7);
INSERT INTO public.ab_permission_view_role (id, permission_view_id, role_id) VALUES (780, 236, 7);


--
-- TOC entry 3553 (class 0 OID 3962495)
-- Dependencies: 205
-- Data for Name: ab_register_user; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3549 (class 0 OID 3962462)
-- Dependencies: 201
-- Data for Name: ab_role; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.ab_role (id, name) VALUES (1, 'Admin');
INSERT INTO public.ab_role (id, name) VALUES (2, 'Public');
INSERT INTO public.ab_role (id, name) VALUES (3, 'Alpha');
INSERT INTO public.ab_role (id, name) VALUES (4, 'Gamma');
INSERT INTO public.ab_role (id, name) VALUES (5, 'granter');
INSERT INTO public.ab_role (id, name) VALUES (6, 'sql_lab');
INSERT INTO public.ab_role (id, name) VALUES (7, 'ath_role1');


--
-- TOC entry 3551 (class 0 OID 3962471)
-- Dependencies: 203
-- Data for Name: ab_user; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.ab_user (id, first_name, last_name, username, password, active, email, last_login, login_count, fail_login_count, created_on, changed_on, created_by_fk, changed_by_fk) VALUES (1, 'admin', 'user', 'admin', 'pbkdf2:sha256:150000$jApxlwC7$e62cf567efd0087166a104d47452ac4e6404fad9219c35233ea211848bfe5c32', true, 'admin@fab.org', '2022-03-11 14:38:49.938936', 1, 0, '2022-03-11 14:37:25.172328', '2022-03-11 14:37:25.172328', NULL, NULL);


--
-- TOC entry 3557 (class 0 OID 3962526)
-- Dependencies: 209
-- Data for Name: ab_user_role; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.ab_user_role (id, user_id, role_id) VALUES (1, 1, 1);


--
-- TOC entry 3547 (class 0 OID 3962453)
-- Dependencies: 199
-- Data for Name: ab_view_menu; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.ab_view_menu (id, name) VALUES (1, 'SavedQuery');
INSERT INTO public.ab_view_menu (id, name) VALUES (2, 'CssTemplate');
INSERT INTO public.ab_view_menu (id, name) VALUES (3, 'ReportSchedule');
INSERT INTO public.ab_view_menu (id, name) VALUES (4, 'Chart');
INSERT INTO public.ab_view_menu (id, name) VALUES (5, 'Annotation');
INSERT INTO public.ab_view_menu (id, name) VALUES (6, 'Dataset');
INSERT INTO public.ab_view_menu (id, name) VALUES (7, 'Log');
INSERT INTO public.ab_view_menu (id, name) VALUES (8, 'Dashboard');
INSERT INTO public.ab_view_menu (id, name) VALUES (9, 'Database');
INSERT INTO public.ab_view_menu (id, name) VALUES (10, 'Query');
INSERT INTO public.ab_view_menu (id, name) VALUES (11, 'SupersetIndexView');
INSERT INTO public.ab_view_menu (id, name) VALUES (12, 'UtilView');
INSERT INTO public.ab_view_menu (id, name) VALUES (13, 'LocaleView');
INSERT INTO public.ab_view_menu (id, name) VALUES (14, 'SecurityApi');
INSERT INTO public.ab_view_menu (id, name) VALUES (15, 'ResetPasswordView');
INSERT INTO public.ab_view_menu (id, name) VALUES (16, 'ResetMyPasswordView');
INSERT INTO public.ab_view_menu (id, name) VALUES (17, 'UserInfoEditView');
INSERT INTO public.ab_view_menu (id, name) VALUES (18, 'CustomAuthDBView');
INSERT INTO public.ab_view_menu (id, name) VALUES (19, 'UserDBModelView');
INSERT INTO public.ab_view_menu (id, name) VALUES (20, 'RoleModelView');
INSERT INTO public.ab_view_menu (id, name) VALUES (21, 'OpenApi');
INSERT INTO public.ab_view_menu (id, name) VALUES (22, 'SwaggerView');
INSERT INTO public.ab_view_menu (id, name) VALUES (23, 'MenuApi');
INSERT INTO public.ab_view_menu (id, name) VALUES (24, 'AsyncEventsRestApi');
INSERT INTO public.ab_view_menu (id, name) VALUES (25, 'CacheRestApi');
INSERT INTO public.ab_view_menu (id, name) VALUES (26, 'FilterSets');
INSERT INTO public.ab_view_menu (id, name) VALUES (27, 'DynamicPlugin');
INSERT INTO public.ab_view_menu (id, name) VALUES (28, 'RowLevelSecurityFiltersModelView');
INSERT INTO public.ab_view_menu (id, name) VALUES (29, 'Api');
INSERT INTO public.ab_view_menu (id, name) VALUES (30, 'CsvToDatabaseView');
INSERT INTO public.ab_view_menu (id, name) VALUES (31, 'ExcelToDatabaseView');
INSERT INTO public.ab_view_menu (id, name) VALUES (32, 'ColumnarToDatabaseView');
INSERT INTO public.ab_view_menu (id, name) VALUES (33, 'Datasource');
INSERT INTO public.ab_view_menu (id, name) VALUES (34, 'KV');
INSERT INTO public.ab_view_menu (id, name) VALUES (35, 'R');
INSERT INTO public.ab_view_menu (id, name) VALUES (36, 'SqlLab');
INSERT INTO public.ab_view_menu (id, name) VALUES (37, 'Superset');
INSERT INTO public.ab_view_menu (id, name) VALUES (38, 'TableSchemaView');
INSERT INTO public.ab_view_menu (id, name) VALUES (39, 'TabStateView');
INSERT INTO public.ab_view_menu (id, name) VALUES (40, 'TagView');
INSERT INTO public.ab_view_menu (id, name) VALUES (41, 'SecurityRestApi');
INSERT INTO public.ab_view_menu (id, name) VALUES (42, 'DashboardEmailScheduleView');
INSERT INTO public.ab_view_menu (id, name) VALUES (43, 'SliceEmailScheduleView');
INSERT INTO public.ab_view_menu (id, name) VALUES (44, 'AlertModelView');
INSERT INTO public.ab_view_menu (id, name) VALUES (45, 'AlertLogModelView');
INSERT INTO public.ab_view_menu (id, name) VALUES (46, 'AlertObservationModelView');
INSERT INTO public.ab_view_menu (id, name) VALUES (47, 'AccessRequestsModelView');
INSERT INTO public.ab_view_menu (id, name) VALUES (48, 'DruidDatasourceModelView');
INSERT INTO public.ab_view_menu (id, name) VALUES (49, 'DruidClusterModelView');
INSERT INTO public.ab_view_menu (id, name) VALUES (50, 'DruidMetricInlineView');
INSERT INTO public.ab_view_menu (id, name) VALUES (51, 'DruidColumnInlineView');
INSERT INTO public.ab_view_menu (id, name) VALUES (52, 'Druid');
INSERT INTO public.ab_view_menu (id, name) VALUES (53, 'Security');
INSERT INTO public.ab_view_menu (id, name) VALUES (54, 'List Users');
INSERT INTO public.ab_view_menu (id, name) VALUES (55, 'List Roles');
INSERT INTO public.ab_view_menu (id, name) VALUES (56, 'Row Level Security');
INSERT INTO public.ab_view_menu (id, name) VALUES (57, 'Action Log');
INSERT INTO public.ab_view_menu (id, name) VALUES (58, 'Access requests');
INSERT INTO public.ab_view_menu (id, name) VALUES (59, 'Home');
INSERT INTO public.ab_view_menu (id, name) VALUES (60, 'Manage');
INSERT INTO public.ab_view_menu (id, name) VALUES (61, 'Annotation Layers');
INSERT INTO public.ab_view_menu (id, name) VALUES (62, 'Plugins');
INSERT INTO public.ab_view_menu (id, name) VALUES (63, 'CSS Templates');
INSERT INTO public.ab_view_menu (id, name) VALUES (64, 'Import Dashboards');
INSERT INTO public.ab_view_menu (id, name) VALUES (65, 'Dashboard Email Schedules');
INSERT INTO public.ab_view_menu (id, name) VALUES (66, 'Chart Emails');
INSERT INTO public.ab_view_menu (id, name) VALUES (67, 'Alerts');
INSERT INTO public.ab_view_menu (id, name) VALUES (68, 'Alerts & Report');
INSERT INTO public.ab_view_menu (id, name) VALUES (69, 'Dashboards');
INSERT INTO public.ab_view_menu (id, name) VALUES (70, 'Charts');
INSERT INTO public.ab_view_menu (id, name) VALUES (71, 'SQL Lab');
INSERT INTO public.ab_view_menu (id, name) VALUES (72, 'SQL Editor');
INSERT INTO public.ab_view_menu (id, name) VALUES (73, 'Saved Queries');
INSERT INTO public.ab_view_menu (id, name) VALUES (74, 'Query Search');
INSERT INTO public.ab_view_menu (id, name) VALUES (75, 'Data');
INSERT INTO public.ab_view_menu (id, name) VALUES (76, 'Databases');
INSERT INTO public.ab_view_menu (id, name) VALUES (77, 'Datasets');
INSERT INTO public.ab_view_menu (id, name) VALUES (78, 'Upload a CSV');
INSERT INTO public.ab_view_menu (id, name) VALUES (79, 'Upload a Columnar file');
INSERT INTO public.ab_view_menu (id, name) VALUES (80, 'Upload Excel');
INSERT INTO public.ab_view_menu (id, name) VALUES (81, 'Druid Datasources');
INSERT INTO public.ab_view_menu (id, name) VALUES (82, 'Druid Clusters');
INSERT INTO public.ab_view_menu (id, name) VALUES (83, 'Scan New Datasources');
INSERT INTO public.ab_view_menu (id, name) VALUES (84, 'Refresh Druid Metadata');
INSERT INTO public.ab_view_menu (id, name) VALUES (85, 'all_datasource_access');
INSERT INTO public.ab_view_menu (id, name) VALUES (86, 'all_database_access');
INSERT INTO public.ab_view_menu (id, name) VALUES (87, 'all_query_access');
INSERT INTO public.ab_view_menu (id, name) VALUES (88, '[AthleteDataSQL].(id:1)');
INSERT INTO public.ab_view_menu (id, name) VALUES (89, '[AthleteDataSQL].[information_schema]');
INSERT INTO public.ab_view_menu (id, name) VALUES (90, '[AthleteDataSQL].[public]');


--
-- TOC entry 3598 (class 0 OID 3963007)
-- Dependencies: 250
-- Data for Name: access_request; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3560 (class 0 OID 3962562)
-- Dependencies: 212
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.alembic_version (version_num) VALUES ('aea15018d53b');


--
-- TOC entry 3634 (class 0 OID 3963560)
-- Dependencies: 286
-- Data for Name: alert_logs; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3636 (class 0 OID 3963573)
-- Dependencies: 288
-- Data for Name: alert_owner; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3632 (class 0 OID 3963538)
-- Dependencies: 284
-- Data for Name: alerts; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3606 (class 0 OID 3963100)
-- Dependencies: 258
-- Data for Name: annotation; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3604 (class 0 OID 3963079)
-- Dependencies: 256
-- Data for Name: annotation_layer; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3640 (class 0 OID 3963680)
-- Dependencies: 292
-- Data for Name: cache_keys; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3562 (class 0 OID 3962569)
-- Dependencies: 214
-- Data for Name: clusters; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3572 (class 0 OID 3962697)
-- Dependencies: 224
-- Data for Name: columns; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3588 (class 0 OID 3962884)
-- Dependencies: 240
-- Data for Name: css_templates; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3610 (class 0 OID 3963203)
-- Dependencies: 262
-- Data for Name: dashboard_email_schedules; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3652 (class 0 OID 3963849)
-- Dependencies: 304
-- Data for Name: dashboard_roles; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3582 (class 0 OID 3962822)
-- Dependencies: 234
-- Data for Name: dashboard_slices; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3592 (class 0 OID 3962930)
-- Dependencies: 244
-- Data for Name: dashboard_user; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3564 (class 0 OID 3962592)
-- Dependencies: 216
-- Data for Name: dashboards; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3568 (class 0 OID 3962636)
-- Dependencies: 220
-- Data for Name: datasources; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3566 (class 0 OID 3962613)
-- Dependencies: 218
-- Data for Name: dbs; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.dbs (created_on, changed_on, id, database_name, sqlalchemy_uri, created_by_fk, changed_by_fk, password, cache_timeout, extra, select_as_create_table_as, allow_ctas, expose_in_sqllab, force_ctas_schema, allow_run_async, allow_dml, verbose_name, impersonate_user, allow_multi_schema_metadata_fetch, allow_csv_upload, encrypted_extra, server_cert, allow_cvas, uuid, configuration_method) VALUES ('2022-03-11 14:40:11.086864', '2022-03-11 14:40:13.840234', 1, 'AthleteDataSQL', 'postgresql+psycopg2://postgres:XXXXXXXXXX@db:5432/postgres', 1, 1, '\x5033417a62332b68666b2f6b7a6a2b4c7578744d54513d3d', NULL, '{"metadata_params":{},"engine_params":{},"schemas_allowed_for_csv_upload":[]}', false, false, true, NULL, false, false, NULL, true, false, false, '\x61323573714c54774b517976716a4c70536d6c4463513d3d', NULL, false, 'c133ed5d-ea5c-4392-b88c-4e32749f2a2f', 'dynamic_form');


--
-- TOC entry 3616 (class 0 OID 3963291)
-- Dependencies: 268
-- Data for Name: druiddatasource_user; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3650 (class 0 OID 3963822)
-- Dependencies: 302
-- Data for Name: dynamic_plugin; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3590 (class 0 OID 3962905)
-- Dependencies: 242
-- Data for Name: favstar; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3654 (class 0 OID 3963935)
-- Dependencies: 306
-- Data for Name: filter_sets; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3600 (class 0 OID 3963033)
-- Dependencies: 252
-- Data for Name: keyvalue; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3584 (class 0 OID 3962842)
-- Dependencies: 236
-- Data for Name: logs; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.logs (id, action, user_id, json, dttm, dashboard_id, slice_id, duration_ms, referrer) VALUES (1, 'welcome', NULL, '{"path": "/superset/welcome/", "object_ref": "Superset.welcome"}', '2022-03-11 03:38:39.639721', NULL, 0, 7, NULL);
INSERT INTO public.logs (id, action, user_id, json, dttm, dashboard_id, slice_id, duration_ms, referrer) VALUES (2, 'welcome', 1, '{"path": "/superset/welcome/", "object_ref": "Superset.welcome"}', '2022-03-11 03:38:50.340993', NULL, 0, 382, 'http://127.0.0.1:8088/login/');
INSERT INTO public.logs (id, action, user_id, json, dttm, dashboard_id, slice_id, duration_ms, referrer) VALUES (3, 'recent_activity', 1, '{"path": "/superset/recent_activity/1/", "limit": "6", "url_rule": "/superset/recent_activity/<int:user_id>/", "object_ref": "Superset.recent_activity", "user_id": 1}', '2022-03-11 03:38:51.02423', NULL, 0, 18, 'http://127.0.0.1:8088/superset/welcome/');
INSERT INTO public.logs (id, action, user_id, json, dttm, dashboard_id, slice_id, duration_ms, referrer) VALUES (4, 'ChartRestApi.get_list', 1, '{"path": "/api/v1/chart/", "q": "(filters:!((col:created_by,opr:rel_o_m,value:0)),order_column:changed_on_delta_humanized,order_direction:desc,page:0,page_size:5)", "rison": {"filters": [{"col": "created_by", "opr": "rel_o_m", "value": 0}], "order_column": "changed_on_delta_humanized", "order_direction": "desc", "page": 0, "page_size": 5}}', '2022-03-11 03:38:51.456232', NULL, 0, 295, 'http://127.0.0.1:8088/superset/welcome/');
INSERT INTO public.logs (id, action, user_id, json, dttm, dashboard_id, slice_id, duration_ms, referrer) VALUES (5, 'SavedQueryRestApi.get_list', 1, '{"path": "/api/v1/saved_query/", "q": "(filters:!((col:created_by,opr:rel_o_m,value:''1'')),order_column:changed_on_delta_humanized,order_direction:desc,page:0,page_size:5)", "rison": {"filters": [{"col": "created_by", "opr": "rel_o_m", "value": "1"}], "order_column": "changed_on_delta_humanized", "order_direction": "desc", "page": 0, "page_size": 5}}', '2022-03-11 03:38:51.479231', NULL, 0, 173, 'http://127.0.0.1:8088/superset/welcome/');
INSERT INTO public.logs (id, action, user_id, json, dttm, dashboard_id, slice_id, duration_ms, referrer) VALUES (6, 'ChartRestApi.get_list', 1, '{"path": "/api/v1/chart/", "q": "(filters:!((col:created_by,opr:rel_o_m,value:''1'')),order_column:changed_on_delta_humanized,order_direction:desc,page:0,page_size:5)", "rison": {"filters": [{"col": "created_by", "opr": "rel_o_m", "value": "1"}], "order_column": "changed_on_delta_humanized", "order_direction": "desc", "page": 0, "page_size": 5}}', '2022-03-11 03:38:51.59623', NULL, 0, 322, 'http://127.0.0.1:8088/superset/welcome/');
INSERT INTO public.logs (id, action, user_id, json, dttm, dashboard_id, slice_id, duration_ms, referrer) VALUES (7, 'DashboardRestApi.get_list', 1, '{"path": "/api/v1/dashboard/", "q": "(filters:!((col:created_by,opr:rel_o_m,value:''1'')),order_column:changed_on_delta_humanized,order_direction:desc,page:0,page_size:5)", "rison": {"filters": [{"col": "created_by", "opr": "rel_o_m", "value": "1"}], "order_column": "changed_on_delta_humanized", "order_direction": "desc", "page": 0, "page_size": 5}}', '2022-03-11 03:38:51.606229', NULL, 0, 320, 'http://127.0.0.1:8088/superset/welcome/');
INSERT INTO public.logs (id, action, user_id, json, dttm, dashboard_id, slice_id, duration_ms, referrer) VALUES (8, 'DashboardRestApi.get_list', 1, '{"path": "/api/v1/dashboard/", "q": "(filters:!((col:created_by,opr:rel_o_m,value:0)),order_column:changed_on_delta_humanized,order_direction:desc,page:0,page_size:5)", "rison": {"filters": [{"col": "created_by", "opr": "rel_o_m", "value": 0}], "order_column": "changed_on_delta_humanized", "order_direction": "desc", "page": 0, "page_size": 5}}', '2022-03-11 03:38:51.689232', NULL, 0, 111, 'http://127.0.0.1:8088/superset/welcome/');
INSERT INTO public.logs (id, action, user_id, json, dttm, dashboard_id, slice_id, duration_ms, referrer) VALUES (9, 'ChartRestApi.info', 1, '{"path": "/api/v1/chart/_info", "q": "(keys:!(permissions))", "rison": {"keys": ["permissions"]}}', '2022-03-11 03:38:51.828227', NULL, 0, 11, 'http://127.0.0.1:8088/superset/welcome/');
INSERT INTO public.logs (id, action, user_id, json, dttm, dashboard_id, slice_id, duration_ms, referrer) VALUES (10, 'DashboardRestApi.info', 1, '{"path": "/api/v1/dashboard/_info", "q": "(keys:!(permissions))", "rison": {"keys": ["permissions"]}}', '2022-03-11 03:38:51.830228', NULL, 0, 11, 'http://127.0.0.1:8088/superset/welcome/');
INSERT INTO public.logs (id, action, user_id, json, dttm, dashboard_id, slice_id, duration_ms, referrer) VALUES (11, 'DatabaseRestApi.info', 1, '{"path": "/api/v1/database/_info", "q": "(keys:!(permissions))", "rison": {"keys": ["permissions"]}}', '2022-03-11 03:39:03.084445', NULL, 0, 21, 'http://127.0.0.1:8088/databaseview/list/?pageIndex=0&sortColumn=changed_on_delta_humanized&sortOrder=desc');
INSERT INTO public.logs (id, action, user_id, json, dttm, dashboard_id, slice_id, duration_ms, referrer) VALUES (12, 'DatabaseRestApi.get_list', 1, '{"path": "/api/v1/database/", "q": "(order_column:changed_on_delta_humanized,order_direction:desc,page:0,page_size:25)", "rison": {"order_column": "changed_on_delta_humanized", "order_direction": "desc", "page": 0, "page_size": 25}}', '2022-03-11 03:39:03.120446', NULL, 0, 61, 'http://127.0.0.1:8088/databaseview/list/?pageIndex=0&sortColumn=changed_on_delta_humanized&sortOrder=desc');
INSERT INTO public.logs (id, action, user_id, json, dttm, dashboard_id, slice_id, duration_ms, referrer) VALUES (13, 'DatabaseRestApi.available', 1, '{"path": "/api/v1/database/available/", "object_ref": "DatabaseRestApi.available"}', '2022-03-11 03:39:06.23505', NULL, 0, 361, 'http://127.0.0.1:8088/databaseview/list/?pageIndex=0&sortColumn=changed_on_delta_humanized&sortOrder=desc');
INSERT INTO public.logs (id, action, user_id, json, dttm, dashboard_id, slice_id, duration_ms, referrer) VALUES (14, 'validation_error', 1, '{"path": "/api/v1/database/validate_parameters", "engine": "postgresql"}', '2022-03-11 03:39:13.025587', NULL, 0, NULL, 'http://127.0.0.1:8088/databaseview/list/?pageIndex=0&sortColumn=changed_on_delta_humanized&sortOrder=desc');
INSERT INTO public.logs (id, action, user_id, json, dttm, dashboard_id, slice_id, duration_ms, referrer) VALUES (15, 'validation_error', 1, '{"path": "/api/v1/database/validate_parameters", "engine": "postgresql"}', '2022-03-11 03:39:16.238833', NULL, 0, NULL, 'http://127.0.0.1:8088/databaseview/list/?pageIndex=0&sortColumn=changed_on_delta_humanized&sortOrder=desc');
INSERT INTO public.logs (id, action, user_id, json, dttm, dashboard_id, slice_id, duration_ms, referrer) VALUES (16, 'validation_error', 1, '{"path": "/api/v1/database/validate_parameters", "engine": "postgresql"}', '2022-03-11 03:39:20.971846', NULL, 0, NULL, 'http://127.0.0.1:8088/databaseview/list/?pageIndex=0&sortColumn=changed_on_delta_humanized&sortOrder=desc');
INSERT INTO public.logs (id, action, user_id, json, dttm, dashboard_id, slice_id, duration_ms, referrer) VALUES (17, 'DatabaseRestApi.validate_parameters', 1, '{"path": "/api/v1/database/validate_parameters", "object_ref": "DatabaseRestApi.validate_parameters"}', '2022-03-11 03:39:28.045072', NULL, 0, 77, 'http://127.0.0.1:8088/databaseview/list/?pageIndex=0&sortColumn=changed_on_delta_humanized&sortOrder=desc');
INSERT INTO public.logs (id, action, user_id, json, dttm, dashboard_id, slice_id, duration_ms, referrer) VALUES (18, 'DatabaseRestApi.validate_parameters', 1, '{"path": "/api/v1/database/validate_parameters", "object_ref": "DatabaseRestApi.validate_parameters"}', '2022-03-11 03:40:06.297794', NULL, 0, 94, 'http://127.0.0.1:8088/databaseview/list/?pageIndex=0&sortColumn=changed_on_delta_humanized&sortOrder=desc');
INSERT INTO public.logs (id, action, user_id, json, dttm, dashboard_id, slice_id, duration_ms, referrer) VALUES (19, 'test_connection_attempt', 1, '{"path": "/api/v1/database/", "engine": "PostgresEngineSpec"}', '2022-03-11 03:40:10.791864', NULL, 0, NULL, 'http://127.0.0.1:8088/databaseview/list/?pageIndex=0&sortColumn=changed_on_delta_humanized&sortOrder=desc');
INSERT INTO public.logs (id, action, user_id, json, dttm, dashboard_id, slice_id, duration_ms, referrer) VALUES (20, 'DatabaseRestApi.validate_parameters', 1, '{"path": "/api/v1/database/validate_parameters", "object_ref": "DatabaseRestApi.validate_parameters"}', '2022-03-11 03:40:10.847867', NULL, 0, 81, 'http://127.0.0.1:8088/databaseview/list/?pageIndex=0&sortColumn=changed_on_delta_humanized&sortOrder=desc');
INSERT INTO public.logs (id, action, user_id, json, dttm, dashboard_id, slice_id, duration_ms, referrer) VALUES (21, 'test_connection_success', 1, '{"path": "/api/v1/database/", "engine": "PostgresEngineSpec"}', '2022-03-11 03:40:10.863873', NULL, 0, NULL, 'http://127.0.0.1:8088/databaseview/list/?pageIndex=0&sortColumn=changed_on_delta_humanized&sortOrder=desc');
INSERT INTO public.logs (id, action, user_id, json, dttm, dashboard_id, slice_id, duration_ms, referrer) VALUES (22, 'DatabaseRestApi.post', 1, '{"path": "/api/v1/database/", "object_ref": "DatabaseRestApi.post"}', '2022-03-11 03:40:11.162864', NULL, 0, 387, 'http://127.0.0.1:8088/databaseview/list/?pageIndex=0&sortColumn=changed_on_delta_humanized&sortOrder=desc');
INSERT INTO public.logs (id, action, user_id, json, dttm, dashboard_id, slice_id, duration_ms, referrer) VALUES (23, 'DatabaseRestApi.get_list', 1, '{"path": "/api/v1/database/", "q": "(order_column:changed_on_delta_humanized,order_direction:desc,page:0,page_size:25)", "rison": {"order_column": "changed_on_delta_humanized", "order_direction": "desc", "page": 0, "page_size": 25}}', '2022-03-11 03:40:11.280864', NULL, 0, 36, 'http://127.0.0.1:8088/databaseview/list/?pageIndex=0&sortColumn=changed_on_delta_humanized&sortOrder=desc');
INSERT INTO public.logs (id, action, user_id, json, dttm, dashboard_id, slice_id, duration_ms, referrer) VALUES (24, 'DatabaseRestApi.validate_parameters', 1, '{"path": "/api/v1/database/validate_parameters", "object_ref": "DatabaseRestApi.validate_parameters"}', '2022-03-11 03:40:13.892235', NULL, 0, 85, 'http://127.0.0.1:8088/databaseview/list/?pageIndex=0&sortColumn=changed_on_delta_humanized&sortOrder=desc');
INSERT INTO public.logs (id, action, user_id, json, dttm, dashboard_id, slice_id, duration_ms, referrer) VALUES (25, 'DatabaseRestApi.put', 1, '{"path": "/api/v1/database/1", "url_rule": "/api/v1/database/<int:pk>", "object_ref": "DatabaseRestApi.put", "pk": 1}', '2022-03-11 03:40:14.076234', NULL, 0, 268, 'http://127.0.0.1:8088/databaseview/list/?pageIndex=0&sortColumn=changed_on_delta_humanized&sortOrder=desc');
INSERT INTO public.logs (id, action, user_id, json, dttm, dashboard_id, slice_id, duration_ms, referrer) VALUES (26, 'DatabaseRestApi.get_list', 1, '{"path": "/api/v1/database/", "q": "(order_column:changed_on_delta_humanized,order_direction:desc,page:0,page_size:25)", "rison": {"order_column": "changed_on_delta_humanized", "order_direction": "desc", "page": 0, "page_size": 25}}', '2022-03-11 03:40:14.205234', NULL, 0, 36, 'http://127.0.0.1:8088/databaseview/list/?pageIndex=0&sortColumn=changed_on_delta_humanized&sortOrder=desc');
INSERT INTO public.logs (id, action, user_id, json, dttm, dashboard_id, slice_id, duration_ms, referrer) VALUES (31, 'ChartRestApi.get_list', 1, '{"path": "/api/v1/chart/", "q": "(filters:!((col:created_by,opr:rel_o_m,value:''1'')),order_column:changed_on_delta_humanized,order_direction:desc,page:0,page_size:5)", "rison": {"filters": [{"col": "created_by", "opr": "rel_o_m", "value": "1"}], "order_column": "changed_on_delta_humanized", "order_direction": "desc", "page": 0, "page_size": 5}}', '2022-03-11 03:41:45.229325', NULL, 0, 179, 'http://127.0.0.1:8088/superset/welcome/');
INSERT INTO public.logs (id, action, user_id, json, dttm, dashboard_id, slice_id, duration_ms, referrer) VALUES (27, 'welcome', 1, '{"path": "/superset/welcome/", "object_ref": "Superset.welcome"}', '2022-03-11 03:41:44.341345', NULL, 0, 149, NULL);
INSERT INTO public.logs (id, action, user_id, json, dttm, dashboard_id, slice_id, duration_ms, referrer) VALUES (32, 'DashboardRestApi.get_list', 1, '{"path": "/api/v1/dashboard/", "q": "(filters:!((col:created_by,opr:rel_o_m,value:0)),order_column:changed_on_delta_humanized,order_direction:desc,page:0,page_size:5)", "rison": {"filters": [{"col": "created_by", "opr": "rel_o_m", "value": 0}], "order_column": "changed_on_delta_humanized", "order_direction": "desc", "page": 0, "page_size": 5}}', '2022-03-11 03:41:45.318326', NULL, 0, 77, 'http://127.0.0.1:8088/superset/welcome/');
INSERT INTO public.logs (id, action, user_id, json, dttm, dashboard_id, slice_id, duration_ms, referrer) VALUES (28, 'recent_activity', 1, '{"path": "/superset/recent_activity/1/", "limit": "6", "url_rule": "/superset/recent_activity/<int:user_id>/", "object_ref": "Superset.recent_activity", "user_id": 1}', '2022-03-11 03:41:44.997325', NULL, 0, 18, 'http://127.0.0.1:8088/superset/welcome/');
INSERT INTO public.logs (id, action, user_id, json, dttm, dashboard_id, slice_id, duration_ms, referrer) VALUES (33, 'ChartRestApi.get_list', 1, '{"path": "/api/v1/chart/", "q": "(filters:!((col:created_by,opr:rel_o_m,value:0)),order_column:changed_on_delta_humanized,order_direction:desc,page:0,page_size:5)", "rison": {"filters": [{"col": "created_by", "opr": "rel_o_m", "value": 0}], "order_column": "changed_on_delta_humanized", "order_direction": "desc", "page": 0, "page_size": 5}}', '2022-03-11 03:41:45.377325', NULL, 0, 99, 'http://127.0.0.1:8088/superset/welcome/');
INSERT INTO public.logs (id, action, user_id, json, dttm, dashboard_id, slice_id, duration_ms, referrer) VALUES (29, 'SavedQueryRestApi.get_list', 1, '{"path": "/api/v1/saved_query/", "q": "(filters:!((col:created_by,opr:rel_o_m,value:''1'')),order_column:changed_on_delta_humanized,order_direction:desc,page:0,page_size:5)", "rison": {"filters": [{"col": "created_by", "opr": "rel_o_m", "value": "1"}], "order_column": "changed_on_delta_humanized", "order_direction": "desc", "page": 0, "page_size": 5}}', '2022-03-11 03:41:45.139333', NULL, 0, 132, 'http://127.0.0.1:8088/superset/welcome/');
INSERT INTO public.logs (id, action, user_id, json, dttm, dashboard_id, slice_id, duration_ms, referrer) VALUES (34, 'ChartRestApi.info', 1, '{"path": "/api/v1/chart/_info", "q": "(keys:!(permissions))", "rison": {"keys": ["permissions"]}}', '2022-03-11 03:41:45.491327', NULL, 0, 13, 'http://127.0.0.1:8088/superset/welcome/');
INSERT INTO public.logs (id, action, user_id, json, dttm, dashboard_id, slice_id, duration_ms, referrer) VALUES (30, 'DashboardRestApi.get_list', 1, '{"path": "/api/v1/dashboard/", "q": "(filters:!((col:created_by,opr:rel_o_m,value:''1'')),order_column:changed_on_delta_humanized,order_direction:desc,page:0,page_size:5)", "rison": {"filters": [{"col": "created_by", "opr": "rel_o_m", "value": "1"}], "order_column": "changed_on_delta_humanized", "order_direction": "desc", "page": 0, "page_size": 5}}', '2022-03-11 03:41:45.170326', NULL, 0, 173, 'http://127.0.0.1:8088/superset/welcome/');
INSERT INTO public.logs (id, action, user_id, json, dttm, dashboard_id, slice_id, duration_ms, referrer) VALUES (35, 'DashboardRestApi.info', 1, '{"path": "/api/v1/dashboard/_info", "q": "(keys:!(permissions))", "rison": {"keys": ["permissions"]}}', '2022-03-11 03:41:45.492326', NULL, 0, 9, 'http://127.0.0.1:8088/superset/welcome/');


--
-- TOC entry 3574 (class 0 OID 3962718)
-- Dependencies: 226
-- Data for Name: metrics; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3596 (class 0 OID 3962985)
-- Dependencies: 248
-- Data for Name: query; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3644 (class 0 OID 3963762)
-- Dependencies: 296
-- Data for Name: report_execution_log; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3646 (class 0 OID 3963778)
-- Dependencies: 298
-- Data for Name: report_recipient; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3642 (class 0 OID 3963721)
-- Dependencies: 294
-- Data for Name: report_schedule; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3648 (class 0 OID 3963804)
-- Dependencies: 300
-- Data for Name: report_schedule_user; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3628 (class 0 OID 3963502)
-- Dependencies: 280
-- Data for Name: rls_filter_roles; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3630 (class 0 OID 3963520)
-- Dependencies: 282
-- Data for Name: rls_filter_tables; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3626 (class 0 OID 3963476)
-- Dependencies: 278
-- Data for Name: row_level_security_filters; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3602 (class 0 OID 3963048)
-- Dependencies: 254
-- Data for Name: saved_query; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3612 (class 0 OID 3963241)
-- Dependencies: 264
-- Data for Name: slice_email_schedules; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3594 (class 0 OID 3962948)
-- Dependencies: 246
-- Data for Name: slice_user; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3576 (class 0 OID 3962739)
-- Dependencies: 228
-- Data for Name: slices; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3578 (class 0 OID 3962770)
-- Dependencies: 230
-- Data for Name: sql_metrics; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3638 (class 0 OID 3963648)
-- Dependencies: 290
-- Data for Name: sql_observations; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3614 (class 0 OID 3963273)
-- Dependencies: 266
-- Data for Name: sqlatable_user; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3622 (class 0 OID 3963400)
-- Dependencies: 274
-- Data for Name: tab_state; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3580 (class 0 OID 3962796)
-- Dependencies: 232
-- Data for Name: table_columns; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3624 (class 0 OID 3963437)
-- Dependencies: 276
-- Data for Name: table_schema; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3570 (class 0 OID 3962669)
-- Dependencies: 222
-- Data for Name: tables; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3618 (class 0 OID 3963321)
-- Dependencies: 270
-- Data for Name: tag; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3620 (class 0 OID 3963349)
-- Dependencies: 272
-- Data for Name: tagged_object; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3586 (class 0 OID 3962863)
-- Dependencies: 238
-- Data for Name: url; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3608 (class 0 OID 3963169)
-- Dependencies: 260
-- Data for Name: user_attribute; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 3707 (class 0 OID 0)
-- Dependencies: 196
-- Name: ab_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ab_permission_id_seq', 96, true);


--
-- TOC entry 3708 (class 0 OID 0)
-- Dependencies: 206
-- Name: ab_permission_view_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ab_permission_view_id_seq', 236, true);


--
-- TOC entry 3709 (class 0 OID 0)
-- Dependencies: 210
-- Name: ab_permission_view_role_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ab_permission_view_role_id_seq', 780, true);


--
-- TOC entry 3710 (class 0 OID 0)
-- Dependencies: 204
-- Name: ab_register_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ab_register_user_id_seq', 1, false);


--
-- TOC entry 3711 (class 0 OID 0)
-- Dependencies: 200
-- Name: ab_role_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ab_role_id_seq', 7, true);


--
-- TOC entry 3712 (class 0 OID 0)
-- Dependencies: 202
-- Name: ab_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ab_user_id_seq', 1, true);


--
-- TOC entry 3713 (class 0 OID 0)
-- Dependencies: 208
-- Name: ab_user_role_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ab_user_role_id_seq', 1, true);


--
-- TOC entry 3714 (class 0 OID 0)
-- Dependencies: 198
-- Name: ab_view_menu_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.ab_view_menu_id_seq', 90, true);


--
-- TOC entry 3715 (class 0 OID 0)
-- Dependencies: 249
-- Name: access_request_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.access_request_id_seq', 1, false);


--
-- TOC entry 3716 (class 0 OID 0)
-- Dependencies: 285
-- Name: alert_logs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.alert_logs_id_seq', 1, false);


--
-- TOC entry 3717 (class 0 OID 0)
-- Dependencies: 287
-- Name: alert_owner_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.alert_owner_id_seq', 1, false);


--
-- TOC entry 3718 (class 0 OID 0)
-- Dependencies: 283
-- Name: alerts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.alerts_id_seq', 1, false);


--
-- TOC entry 3719 (class 0 OID 0)
-- Dependencies: 257
-- Name: annotation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.annotation_id_seq', 1, false);


--
-- TOC entry 3720 (class 0 OID 0)
-- Dependencies: 255
-- Name: annotation_layer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.annotation_layer_id_seq', 1, false);


--
-- TOC entry 3721 (class 0 OID 0)
-- Dependencies: 291
-- Name: cache_keys_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.cache_keys_id_seq', 1, false);


--
-- TOC entry 3722 (class 0 OID 0)
-- Dependencies: 213
-- Name: clusters_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.clusters_id_seq', 1, false);


--
-- TOC entry 3723 (class 0 OID 0)
-- Dependencies: 223
-- Name: columns_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.columns_id_seq', 1, false);


--
-- TOC entry 3724 (class 0 OID 0)
-- Dependencies: 239
-- Name: css_templates_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.css_templates_id_seq', 1, false);


--
-- TOC entry 3725 (class 0 OID 0)
-- Dependencies: 261
-- Name: dashboard_email_schedules_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.dashboard_email_schedules_id_seq', 1, false);


--
-- TOC entry 3726 (class 0 OID 0)
-- Dependencies: 303
-- Name: dashboard_roles_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.dashboard_roles_id_seq', 1, false);


--
-- TOC entry 3727 (class 0 OID 0)
-- Dependencies: 233
-- Name: dashboard_slices_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.dashboard_slices_id_seq', 1, false);


--
-- TOC entry 3728 (class 0 OID 0)
-- Dependencies: 243
-- Name: dashboard_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.dashboard_user_id_seq', 1, false);


--
-- TOC entry 3729 (class 0 OID 0)
-- Dependencies: 215
-- Name: dashboards_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.dashboards_id_seq', 1, false);


--
-- TOC entry 3730 (class 0 OID 0)
-- Dependencies: 219
-- Name: datasources_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.datasources_id_seq', 1, false);


--
-- TOC entry 3731 (class 0 OID 0)
-- Dependencies: 217
-- Name: dbs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.dbs_id_seq', 1, true);


--
-- TOC entry 3732 (class 0 OID 0)
-- Dependencies: 267
-- Name: druiddatasource_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.druiddatasource_user_id_seq', 1, false);


--
-- TOC entry 3733 (class 0 OID 0)
-- Dependencies: 301
-- Name: dynamic_plugin_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.dynamic_plugin_id_seq', 1, false);


--
-- TOC entry 3734 (class 0 OID 0)
-- Dependencies: 241
-- Name: favstar_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.favstar_id_seq', 1, false);


--
-- TOC entry 3735 (class 0 OID 0)
-- Dependencies: 305
-- Name: filter_sets_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.filter_sets_id_seq', 1, false);


--
-- TOC entry 3736 (class 0 OID 0)
-- Dependencies: 251
-- Name: keyvalue_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.keyvalue_id_seq', 1, false);


--
-- TOC entry 3737 (class 0 OID 0)
-- Dependencies: 235
-- Name: logs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.logs_id_seq', 35, true);


--
-- TOC entry 3738 (class 0 OID 0)
-- Dependencies: 225
-- Name: metrics_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.metrics_id_seq', 1, false);


--
-- TOC entry 3739 (class 0 OID 0)
-- Dependencies: 247
-- Name: query_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.query_id_seq', 1, false);


--
-- TOC entry 3740 (class 0 OID 0)
-- Dependencies: 295
-- Name: report_execution_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.report_execution_log_id_seq', 1, false);


--
-- TOC entry 3741 (class 0 OID 0)
-- Dependencies: 297
-- Name: report_recipient_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.report_recipient_id_seq', 1, false);


--
-- TOC entry 3742 (class 0 OID 0)
-- Dependencies: 293
-- Name: report_schedule_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.report_schedule_id_seq', 1, false);


--
-- TOC entry 3743 (class 0 OID 0)
-- Dependencies: 299
-- Name: report_schedule_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.report_schedule_user_id_seq', 1, false);


--
-- TOC entry 3744 (class 0 OID 0)
-- Dependencies: 279
-- Name: rls_filter_roles_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.rls_filter_roles_id_seq', 1, false);


--
-- TOC entry 3745 (class 0 OID 0)
-- Dependencies: 281
-- Name: rls_filter_tables_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.rls_filter_tables_id_seq', 1, false);


--
-- TOC entry 3746 (class 0 OID 0)
-- Dependencies: 277
-- Name: row_level_security_filters_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.row_level_security_filters_id_seq', 1, false);


--
-- TOC entry 3747 (class 0 OID 0)
-- Dependencies: 253
-- Name: saved_query_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.saved_query_id_seq', 1, false);


--
-- TOC entry 3748 (class 0 OID 0)
-- Dependencies: 263
-- Name: slice_email_schedules_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.slice_email_schedules_id_seq', 1, false);


--
-- TOC entry 3749 (class 0 OID 0)
-- Dependencies: 245
-- Name: slice_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.slice_user_id_seq', 1, false);


--
-- TOC entry 3750 (class 0 OID 0)
-- Dependencies: 227
-- Name: slices_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.slices_id_seq', 1, false);


--
-- TOC entry 3751 (class 0 OID 0)
-- Dependencies: 229
-- Name: sql_metrics_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.sql_metrics_id_seq', 1, false);


--
-- TOC entry 3752 (class 0 OID 0)
-- Dependencies: 289
-- Name: sql_observations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.sql_observations_id_seq', 1, false);


--
-- TOC entry 3753 (class 0 OID 0)
-- Dependencies: 265
-- Name: sqlatable_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.sqlatable_user_id_seq', 1, false);


--
-- TOC entry 3754 (class 0 OID 0)
-- Dependencies: 273
-- Name: tab_state_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tab_state_id_seq', 1, false);


--
-- TOC entry 3755 (class 0 OID 0)
-- Dependencies: 231
-- Name: table_columns_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.table_columns_id_seq', 1, false);


--
-- TOC entry 3756 (class 0 OID 0)
-- Dependencies: 275
-- Name: table_schema_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.table_schema_id_seq', 1, false);


--
-- TOC entry 3757 (class 0 OID 0)
-- Dependencies: 221
-- Name: tables_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tables_id_seq', 1, false);


--
-- TOC entry 3758 (class 0 OID 0)
-- Dependencies: 269
-- Name: tag_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tag_id_seq', 1, false);


--
-- TOC entry 3759 (class 0 OID 0)
-- Dependencies: 271
-- Name: tagged_object_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tagged_object_id_seq', 1, false);


--
-- TOC entry 3760 (class 0 OID 0)
-- Dependencies: 237
-- Name: url_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.url_id_seq', 1, false);


--
-- TOC entry 3761 (class 0 OID 0)
-- Dependencies: 259
-- Name: user_attribute_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_attribute_id_seq', 1, false);


--
-- TOC entry 3162 (class 2606 OID 3962977)
-- Name: tables _customer_location_uc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tables
    ADD CONSTRAINT _customer_location_uc UNIQUE (database_id, schema, table_name);


--
-- TOC entry 3098 (class 2606 OID 3962450)
-- Name: ab_permission ab_permission_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ab_permission
    ADD CONSTRAINT ab_permission_name_key UNIQUE (name);


--
-- TOC entry 3100 (class 2606 OID 3962448)
-- Name: ab_permission ab_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ab_permission
    ADD CONSTRAINT ab_permission_pkey PRIMARY KEY (id);


--
-- TOC entry 3120 (class 2606 OID 3962513)
-- Name: ab_permission_view ab_permission_view_permission_id_view_menu_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ab_permission_view
    ADD CONSTRAINT ab_permission_view_permission_id_view_menu_id_key UNIQUE (permission_id, view_menu_id);


--
-- TOC entry 3122 (class 2606 OID 3962511)
-- Name: ab_permission_view ab_permission_view_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ab_permission_view
    ADD CONSTRAINT ab_permission_view_pkey PRIMARY KEY (id);


--
-- TOC entry 3128 (class 2606 OID 3962551)
-- Name: ab_permission_view_role ab_permission_view_role_permission_view_id_role_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ab_permission_view_role
    ADD CONSTRAINT ab_permission_view_role_permission_view_id_role_id_key UNIQUE (permission_view_id, role_id);


--
-- TOC entry 3130 (class 2606 OID 3962549)
-- Name: ab_permission_view_role ab_permission_view_role_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ab_permission_view_role
    ADD CONSTRAINT ab_permission_view_role_pkey PRIMARY KEY (id);


--
-- TOC entry 3116 (class 2606 OID 3962502)
-- Name: ab_register_user ab_register_user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ab_register_user
    ADD CONSTRAINT ab_register_user_pkey PRIMARY KEY (id);


--
-- TOC entry 3118 (class 2606 OID 3962504)
-- Name: ab_register_user ab_register_user_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ab_register_user
    ADD CONSTRAINT ab_register_user_username_key UNIQUE (username);


--
-- TOC entry 3106 (class 2606 OID 3962468)
-- Name: ab_role ab_role_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ab_role
    ADD CONSTRAINT ab_role_name_key UNIQUE (name);


--
-- TOC entry 3108 (class 2606 OID 3962466)
-- Name: ab_role ab_role_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ab_role
    ADD CONSTRAINT ab_role_pkey PRIMARY KEY (id);


--
-- TOC entry 3110 (class 2606 OID 3962482)
-- Name: ab_user ab_user_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ab_user
    ADD CONSTRAINT ab_user_email_key UNIQUE (email);


--
-- TOC entry 3112 (class 2606 OID 3962478)
-- Name: ab_user ab_user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ab_user
    ADD CONSTRAINT ab_user_pkey PRIMARY KEY (id);


--
-- TOC entry 3124 (class 2606 OID 3962530)
-- Name: ab_user_role ab_user_role_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ab_user_role
    ADD CONSTRAINT ab_user_role_pkey PRIMARY KEY (id);


--
-- TOC entry 3126 (class 2606 OID 3962532)
-- Name: ab_user_role ab_user_role_user_id_role_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ab_user_role
    ADD CONSTRAINT ab_user_role_user_id_role_id_key UNIQUE (user_id, role_id);


--
-- TOC entry 3114 (class 2606 OID 3962480)
-- Name: ab_user ab_user_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ab_user
    ADD CONSTRAINT ab_user_username_key UNIQUE (username);


--
-- TOC entry 3102 (class 2606 OID 3963308)
-- Name: ab_view_menu ab_view_menu_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ab_view_menu
    ADD CONSTRAINT ab_view_menu_name_key UNIQUE (name);


--
-- TOC entry 3104 (class 2606 OID 3962457)
-- Name: ab_view_menu ab_view_menu_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ab_view_menu
    ADD CONSTRAINT ab_view_menu_pkey PRIMARY KEY (id);


--
-- TOC entry 3218 (class 2606 OID 3963012)
-- Name: access_request access_request_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.access_request
    ADD CONSTRAINT access_request_pkey PRIMARY KEY (id);


--
-- TOC entry 3132 (class 2606 OID 3962566)
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- TOC entry 3270 (class 2606 OID 3963565)
-- Name: alert_logs alert_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alert_logs
    ADD CONSTRAINT alert_logs_pkey PRIMARY KEY (id);


--
-- TOC entry 3272 (class 2606 OID 3963578)
-- Name: alert_owner alert_owner_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alert_owner
    ADD CONSTRAINT alert_owner_pkey PRIMARY KEY (id);


--
-- TOC entry 3267 (class 2606 OID 3963546)
-- Name: alerts alerts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alerts
    ADD CONSTRAINT alerts_pkey PRIMARY KEY (id);


--
-- TOC entry 3226 (class 2606 OID 3963087)
-- Name: annotation_layer annotation_layer_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.annotation_layer
    ADD CONSTRAINT annotation_layer_pkey PRIMARY KEY (id);


--
-- TOC entry 3228 (class 2606 OID 3963108)
-- Name: annotation annotation_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.annotation
    ADD CONSTRAINT annotation_pkey PRIMARY KEY (id);


--
-- TOC entry 3277 (class 2606 OID 3963685)
-- Name: cache_keys cache_keys_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cache_keys
    ADD CONSTRAINT cache_keys_pkey PRIMARY KEY (id);


--
-- TOC entry 3212 (class 2606 OID 3963029)
-- Name: query client_id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.query
    ADD CONSTRAINT client_id UNIQUE (client_id);


--
-- TOC entry 3134 (class 2606 OID 3962579)
-- Name: clusters clusters_cluster_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clusters
    ADD CONSTRAINT clusters_cluster_name_key UNIQUE (cluster_name);


--
-- TOC entry 3136 (class 2606 OID 3962577)
-- Name: clusters clusters_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clusters
    ADD CONSTRAINT clusters_pkey PRIMARY KEY (id);


--
-- TOC entry 3138 (class 2606 OID 3963045)
-- Name: clusters clusters_verbose_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clusters
    ADD CONSTRAINT clusters_verbose_name_key UNIQUE (verbose_name);


--
-- TOC entry 3168 (class 2606 OID 3962705)
-- Name: columns columns_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.columns
    ADD CONSTRAINT columns_pkey PRIMARY KEY (id);


--
-- TOC entry 3204 (class 2606 OID 3962892)
-- Name: css_templates css_templates_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.css_templates
    ADD CONSTRAINT css_templates_pkey PRIMARY KEY (id);


--
-- TOC entry 3233 (class 2606 OID 3963211)
-- Name: dashboard_email_schedules dashboard_email_schedules_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dashboard_email_schedules
    ADD CONSTRAINT dashboard_email_schedules_pkey PRIMARY KEY (id);


--
-- TOC entry 3298 (class 2606 OID 3963854)
-- Name: dashboard_roles dashboard_roles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dashboard_roles
    ADD CONSTRAINT dashboard_roles_pkey PRIMARY KEY (id);


--
-- TOC entry 3196 (class 2606 OID 3962827)
-- Name: dashboard_slices dashboard_slices_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dashboard_slices
    ADD CONSTRAINT dashboard_slices_pkey PRIMARY KEY (id);


--
-- TOC entry 3208 (class 2606 OID 3962935)
-- Name: dashboard_user dashboard_user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dashboard_user
    ADD CONSTRAINT dashboard_user_pkey PRIMARY KEY (id);


--
-- TOC entry 3142 (class 2606 OID 3962600)
-- Name: dashboards dashboards_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dashboards
    ADD CONSTRAINT dashboards_pkey PRIMARY KEY (id);


--
-- TOC entry 3156 (class 2606 OID 3962644)
-- Name: datasources datasources_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.datasources
    ADD CONSTRAINT datasources_pkey PRIMARY KEY (id);


--
-- TOC entry 3148 (class 2606 OID 3962623)
-- Name: dbs dbs_database_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dbs
    ADD CONSTRAINT dbs_database_name_key UNIQUE (database_name);


--
-- TOC entry 3150 (class 2606 OID 3962621)
-- Name: dbs dbs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dbs
    ADD CONSTRAINT dbs_pkey PRIMARY KEY (id);


--
-- TOC entry 3152 (class 2606 OID 3963043)
-- Name: dbs dbs_verbose_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dbs
    ADD CONSTRAINT dbs_verbose_name_key UNIQUE (verbose_name);


--
-- TOC entry 3245 (class 2606 OID 3963296)
-- Name: druiddatasource_user druiddatasource_user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.druiddatasource_user
    ADD CONSTRAINT druiddatasource_user_pkey PRIMARY KEY (id);


--
-- TOC entry 3292 (class 2606 OID 3963832)
-- Name: dynamic_plugin dynamic_plugin_key_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dynamic_plugin
    ADD CONSTRAINT dynamic_plugin_key_key UNIQUE (key);


--
-- TOC entry 3294 (class 2606 OID 3963834)
-- Name: dynamic_plugin dynamic_plugin_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dynamic_plugin
    ADD CONSTRAINT dynamic_plugin_name_key UNIQUE (name);


--
-- TOC entry 3296 (class 2606 OID 3963830)
-- Name: dynamic_plugin dynamic_plugin_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dynamic_plugin
    ADD CONSTRAINT dynamic_plugin_pkey PRIMARY KEY (id);


--
-- TOC entry 3206 (class 2606 OID 3962910)
-- Name: favstar favstar_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.favstar
    ADD CONSTRAINT favstar_pkey PRIMARY KEY (id);


--
-- TOC entry 3300 (class 2606 OID 3963943)
-- Name: filter_sets filter_sets_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.filter_sets
    ADD CONSTRAINT filter_sets_pkey PRIMARY KEY (id);


--
-- TOC entry 3144 (class 2606 OID 3962839)
-- Name: dashboards idx_unique_slug; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dashboards
    ADD CONSTRAINT idx_unique_slug UNIQUE (slug);


--
-- TOC entry 3220 (class 2606 OID 3963041)
-- Name: keyvalue keyvalue_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.keyvalue
    ADD CONSTRAINT keyvalue_pkey PRIMARY KEY (id);


--
-- TOC entry 3200 (class 2606 OID 3962850)
-- Name: logs logs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.logs
    ADD CONSTRAINT logs_pkey PRIMARY KEY (id);


--
-- TOC entry 3174 (class 2606 OID 3962726)
-- Name: metrics metrics_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.metrics
    ADD CONSTRAINT metrics_pkey PRIMARY KEY (id);


--
-- TOC entry 3215 (class 2606 OID 3962993)
-- Name: query query_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.query
    ADD CONSTRAINT query_pkey PRIMARY KEY (id);


--
-- TOC entry 3286 (class 2606 OID 3963770)
-- Name: report_execution_log report_execution_log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.report_execution_log
    ADD CONSTRAINT report_execution_log_pkey PRIMARY KEY (id);


--
-- TOC entry 3288 (class 2606 OID 3963786)
-- Name: report_recipient report_recipient_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.report_recipient
    ADD CONSTRAINT report_recipient_pkey PRIMARY KEY (id);


--
-- TOC entry 3282 (class 2606 OID 3963729)
-- Name: report_schedule report_schedule_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.report_schedule
    ADD CONSTRAINT report_schedule_pkey PRIMARY KEY (id);


--
-- TOC entry 3290 (class 2606 OID 3963809)
-- Name: report_schedule_user report_schedule_user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.report_schedule_user
    ADD CONSTRAINT report_schedule_user_pkey PRIMARY KEY (id);


--
-- TOC entry 3263 (class 2606 OID 3963507)
-- Name: rls_filter_roles rls_filter_roles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rls_filter_roles
    ADD CONSTRAINT rls_filter_roles_pkey PRIMARY KEY (id);


--
-- TOC entry 3265 (class 2606 OID 3963525)
-- Name: rls_filter_tables rls_filter_tables_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rls_filter_tables
    ADD CONSTRAINT rls_filter_tables_pkey PRIMARY KEY (id);


--
-- TOC entry 3261 (class 2606 OID 3963484)
-- Name: row_level_security_filters row_level_security_filters_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.row_level_security_filters
    ADD CONSTRAINT row_level_security_filters_pkey PRIMARY KEY (id);


--
-- TOC entry 3222 (class 2606 OID 3963056)
-- Name: saved_query saved_query_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.saved_query
    ADD CONSTRAINT saved_query_pkey PRIMARY KEY (id);


--
-- TOC entry 3239 (class 2606 OID 3963249)
-- Name: slice_email_schedules slice_email_schedules_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.slice_email_schedules
    ADD CONSTRAINT slice_email_schedules_pkey PRIMARY KEY (id);


--
-- TOC entry 3210 (class 2606 OID 3962953)
-- Name: slice_user slice_user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.slice_user
    ADD CONSTRAINT slice_user_pkey PRIMARY KEY (id);


--
-- TOC entry 3180 (class 2606 OID 3962747)
-- Name: slices slices_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.slices
    ADD CONSTRAINT slices_pkey PRIMARY KEY (id);


--
-- TOC entry 3184 (class 2606 OID 3962778)
-- Name: sql_metrics sql_metrics_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sql_metrics
    ADD CONSTRAINT sql_metrics_pkey PRIMARY KEY (id);


--
-- TOC entry 3275 (class 2606 OID 3963656)
-- Name: sql_observations sql_observations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sql_observations
    ADD CONSTRAINT sql_observations_pkey PRIMARY KEY (id);


--
-- TOC entry 3243 (class 2606 OID 3963278)
-- Name: sqlatable_user sqlatable_user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sqlatable_user
    ADD CONSTRAINT sqlatable_user_pkey PRIMARY KEY (id);


--
-- TOC entry 3255 (class 2606 OID 3963408)
-- Name: tab_state tab_state_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tab_state
    ADD CONSTRAINT tab_state_pkey PRIMARY KEY (id);


--
-- TOC entry 3190 (class 2606 OID 3962804)
-- Name: table_columns table_columns_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.table_columns
    ADD CONSTRAINT table_columns_pkey PRIMARY KEY (id);


--
-- TOC entry 3258 (class 2606 OID 3963445)
-- Name: table_schema table_schema_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.table_schema
    ADD CONSTRAINT table_schema_pkey PRIMARY KEY (id);


--
-- TOC entry 3164 (class 2606 OID 3962677)
-- Name: tables tables_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tables
    ADD CONSTRAINT tables_pkey PRIMARY KEY (id);


--
-- TOC entry 3247 (class 2606 OID 3963328)
-- Name: tag tag_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tag
    ADD CONSTRAINT tag_name_key UNIQUE (name);


--
-- TOC entry 3249 (class 2606 OID 3963326)
-- Name: tag tag_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tag
    ADD CONSTRAINT tag_pkey PRIMARY KEY (id);


--
-- TOC entry 3252 (class 2606 OID 3963354)
-- Name: tagged_object tagged_object_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tagged_object
    ADD CONSTRAINT tagged_object_pkey PRIMARY KEY (id);


--
-- TOC entry 3140 (class 2606 OID 3963701)
-- Name: clusters uq_clusters_uuid; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clusters
    ADD CONSTRAINT uq_clusters_uuid UNIQUE (uuid);


--
-- TOC entry 3170 (class 2606 OID 3963145)
-- Name: columns uq_columns_column_name; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.columns
    ADD CONSTRAINT uq_columns_column_name UNIQUE (column_name, datasource_id);


--
-- TOC entry 3172 (class 2606 OID 3963705)
-- Name: columns uq_columns_uuid; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.columns
    ADD CONSTRAINT uq_columns_uuid UNIQUE (uuid);


--
-- TOC entry 3236 (class 2606 OID 3963709)
-- Name: dashboard_email_schedules uq_dashboard_email_schedules_uuid; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dashboard_email_schedules
    ADD CONSTRAINT uq_dashboard_email_schedules_uuid UNIQUE (uuid);


--
-- TOC entry 3198 (class 2606 OID 3963382)
-- Name: dashboard_slices uq_dashboard_slice; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dashboard_slices
    ADD CONSTRAINT uq_dashboard_slice UNIQUE (dashboard_id, slice_id);


--
-- TOC entry 3146 (class 2606 OID 3963691)
-- Name: dashboards uq_dashboards_uuid; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dashboards
    ADD CONSTRAINT uq_dashboards_uuid UNIQUE (uuid);


--
-- TOC entry 3158 (class 2606 OID 3963468)
-- Name: datasources uq_datasources_cluster_id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.datasources
    ADD CONSTRAINT uq_datasources_cluster_id UNIQUE (cluster_id, datasource_name);


--
-- TOC entry 3160 (class 2606 OID 3963703)
-- Name: datasources uq_datasources_uuid; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.datasources
    ADD CONSTRAINT uq_datasources_uuid UNIQUE (uuid);


--
-- TOC entry 3154 (class 2606 OID 3963689)
-- Name: dbs uq_dbs_uuid; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dbs
    ADD CONSTRAINT uq_dbs_uuid UNIQUE (uuid);


--
-- TOC entry 3176 (class 2606 OID 3963147)
-- Name: metrics uq_metrics_metric_name; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.metrics
    ADD CONSTRAINT uq_metrics_metric_name UNIQUE (metric_name, datasource_id);


--
-- TOC entry 3178 (class 2606 OID 3963707)
-- Name: metrics uq_metrics_uuid; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.metrics
    ADD CONSTRAINT uq_metrics_uuid UNIQUE (uuid);


--
-- TOC entry 3284 (class 2606 OID 3963846)
-- Name: report_schedule uq_report_schedule_name_type; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.report_schedule
    ADD CONSTRAINT uq_report_schedule_name_type UNIQUE (name, type);


--
-- TOC entry 3224 (class 2606 OID 3963718)
-- Name: saved_query uq_saved_query_uuid; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.saved_query
    ADD CONSTRAINT uq_saved_query_uuid UNIQUE (uuid);


--
-- TOC entry 3241 (class 2606 OID 3963711)
-- Name: slice_email_schedules uq_slice_email_schedules_uuid; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.slice_email_schedules
    ADD CONSTRAINT uq_slice_email_schedules_uuid UNIQUE (uuid);


--
-- TOC entry 3182 (class 2606 OID 3963693)
-- Name: slices uq_slices_uuid; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.slices
    ADD CONSTRAINT uq_slices_uuid UNIQUE (uuid);


--
-- TOC entry 3186 (class 2606 OID 3963380)
-- Name: sql_metrics uq_sql_metrics_metric_name; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sql_metrics
    ADD CONSTRAINT uq_sql_metrics_metric_name UNIQUE (metric_name, table_id);


--
-- TOC entry 3188 (class 2606 OID 3963699)
-- Name: sql_metrics uq_sql_metrics_uuid; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sql_metrics
    ADD CONSTRAINT uq_sql_metrics_uuid UNIQUE (uuid);


--
-- TOC entry 3192 (class 2606 OID 3963371)
-- Name: table_columns uq_table_columns_column_name; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.table_columns
    ADD CONSTRAINT uq_table_columns_column_name UNIQUE (column_name, table_id);


--
-- TOC entry 3194 (class 2606 OID 3963697)
-- Name: table_columns uq_table_columns_uuid; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.table_columns
    ADD CONSTRAINT uq_table_columns_uuid UNIQUE (uuid);


--
-- TOC entry 3166 (class 2606 OID 3963695)
-- Name: tables uq_tables_uuid; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tables
    ADD CONSTRAINT uq_tables_uuid UNIQUE (uuid);


--
-- TOC entry 3202 (class 2606 OID 3962871)
-- Name: url url_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.url
    ADD CONSTRAINT url_pkey PRIMARY KEY (id);


--
-- TOC entry 3231 (class 2606 OID 3963174)
-- Name: user_attribute user_attribute_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_attribute
    ADD CONSTRAINT user_attribute_pkey PRIMARY KEY (id);


--
-- TOC entry 3268 (class 1259 OID 3963557)
-- Name: ix_alerts_active; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_alerts_active ON public.alerts USING btree (active);


--
-- TOC entry 3278 (class 1259 OID 3963686)
-- Name: ix_cache_keys_datasource_uid; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_cache_keys_datasource_uid ON public.cache_keys USING btree (datasource_uid);


--
-- TOC entry 3279 (class 1259 OID 3963916)
-- Name: ix_creation_method; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_creation_method ON public.report_schedule USING btree (creation_method);


--
-- TOC entry 3234 (class 1259 OID 3963232)
-- Name: ix_dashboard_email_schedules_active; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_dashboard_email_schedules_active ON public.dashboard_email_schedules USING btree (active);


--
-- TOC entry 3213 (class 1259 OID 3963030)
-- Name: ix_query_results_key; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_query_results_key ON public.query USING btree (results_key);


--
-- TOC entry 3280 (class 1259 OID 3963759)
-- Name: ix_report_schedule_active; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_report_schedule_active ON public.report_schedule USING btree (active);


--
-- TOC entry 3259 (class 1259 OID 3963687)
-- Name: ix_row_level_security_filters_filter_type; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_row_level_security_filters_filter_type ON public.row_level_security_filters USING btree (filter_type);


--
-- TOC entry 3237 (class 1259 OID 3963270)
-- Name: ix_slice_email_schedules_active; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_slice_email_schedules_active ON public.slice_email_schedules USING btree (active);


--
-- TOC entry 3273 (class 1259 OID 3963667)
-- Name: ix_sql_observations_dttm; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_sql_observations_dttm ON public.sql_observations USING btree (dttm);


--
-- TOC entry 3253 (class 1259 OID 3963434)
-- Name: ix_tab_state_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_tab_state_id ON public.tab_state USING btree (id);


--
-- TOC entry 3256 (class 1259 OID 3963466)
-- Name: ix_table_schema_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_table_schema_id ON public.table_schema USING btree (id);


--
-- TOC entry 3250 (class 1259 OID 3963383)
-- Name: ix_tagged_object_object_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_tagged_object_object_id ON public.tagged_object USING btree (object_id);


--
-- TOC entry 3229 (class 1259 OID 3963124)
-- Name: ti_dag_state; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ti_dag_state ON public.annotation USING btree (layer_id, start_dttm, end_dttm);


--
-- TOC entry 3216 (class 1259 OID 3963004)
-- Name: ti_user_id_changed_on; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ti_user_id_changed_on ON public.query USING btree (user_id, changed_on);


--
-- TOC entry 3304 (class 2606 OID 3962514)
-- Name: ab_permission_view ab_permission_view_permission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ab_permission_view
    ADD CONSTRAINT ab_permission_view_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES public.ab_permission(id);


--
-- TOC entry 3308 (class 2606 OID 3962552)
-- Name: ab_permission_view_role ab_permission_view_role_permission_view_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ab_permission_view_role
    ADD CONSTRAINT ab_permission_view_role_permission_view_id_fkey FOREIGN KEY (permission_view_id) REFERENCES public.ab_permission_view(id);


--
-- TOC entry 3307 (class 2606 OID 3962557)
-- Name: ab_permission_view_role ab_permission_view_role_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ab_permission_view_role
    ADD CONSTRAINT ab_permission_view_role_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.ab_role(id);


--
-- TOC entry 3303 (class 2606 OID 3962519)
-- Name: ab_permission_view ab_permission_view_view_menu_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ab_permission_view
    ADD CONSTRAINT ab_permission_view_view_menu_id_fkey FOREIGN KEY (view_menu_id) REFERENCES public.ab_view_menu(id);


--
-- TOC entry 3301 (class 2606 OID 3962488)
-- Name: ab_user ab_user_changed_by_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ab_user
    ADD CONSTRAINT ab_user_changed_by_fk_fkey FOREIGN KEY (changed_by_fk) REFERENCES public.ab_user(id);


--
-- TOC entry 3302 (class 2606 OID 3962483)
-- Name: ab_user ab_user_created_by_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ab_user
    ADD CONSTRAINT ab_user_created_by_fk_fkey FOREIGN KEY (created_by_fk) REFERENCES public.ab_user(id);


--
-- TOC entry 3305 (class 2606 OID 3962538)
-- Name: ab_user_role ab_user_role_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ab_user_role
    ADD CONSTRAINT ab_user_role_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.ab_role(id);


--
-- TOC entry 3306 (class 2606 OID 3962533)
-- Name: ab_user_role ab_user_role_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ab_user_role
    ADD CONSTRAINT ab_user_role_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.ab_user(id);


--
-- TOC entry 3350 (class 2606 OID 3963013)
-- Name: access_request access_request_changed_by_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.access_request
    ADD CONSTRAINT access_request_changed_by_fk_fkey FOREIGN KEY (changed_by_fk) REFERENCES public.ab_user(id);


--
-- TOC entry 3349 (class 2606 OID 3963018)
-- Name: access_request access_request_created_by_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.access_request
    ADD CONSTRAINT access_request_created_by_fk_fkey FOREIGN KEY (created_by_fk) REFERENCES public.ab_user(id);


--
-- TOC entry 3401 (class 2606 OID 3963566)
-- Name: alert_logs alert_logs_alert_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alert_logs
    ADD CONSTRAINT alert_logs_alert_id_fkey FOREIGN KEY (alert_id) REFERENCES public.alerts(id);


--
-- TOC entry 3403 (class 2606 OID 3963579)
-- Name: alert_owner alert_owner_alert_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alert_owner
    ADD CONSTRAINT alert_owner_alert_id_fkey FOREIGN KEY (alert_id) REFERENCES public.alerts(id);


--
-- TOC entry 3402 (class 2606 OID 3963584)
-- Name: alert_owner alert_owner_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alert_owner
    ADD CONSTRAINT alert_owner_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.ab_user(id);


--
-- TOC entry 3400 (class 2606 OID 3963547)
-- Name: alerts alerts_dashboard_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alerts
    ADD CONSTRAINT alerts_dashboard_id_fkey FOREIGN KEY (dashboard_id) REFERENCES public.dashboards(id);


--
-- TOC entry 3396 (class 2606 OID 3963712)
-- Name: alerts alerts_database_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alerts
    ADD CONSTRAINT alerts_database_id_fkey FOREIGN KEY (database_id) REFERENCES public.dbs(id);


--
-- TOC entry 3398 (class 2606 OID 3963668)
-- Name: alerts alerts_ibfk_3; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alerts
    ADD CONSTRAINT alerts_ibfk_3 FOREIGN KEY (changed_by_fk) REFERENCES public.ab_user(id);


--
-- TOC entry 3397 (class 2606 OID 3963673)
-- Name: alerts alerts_ibfk_4; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alerts
    ADD CONSTRAINT alerts_ibfk_4 FOREIGN KEY (created_by_fk) REFERENCES public.ab_user(id);


--
-- TOC entry 3399 (class 2606 OID 3963552)
-- Name: alerts alerts_slice_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alerts
    ADD CONSTRAINT alerts_slice_id_fkey FOREIGN KEY (slice_id) REFERENCES public.slices(id);


--
-- TOC entry 3359 (class 2606 OID 3963109)
-- Name: annotation annotation_changed_by_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.annotation
    ADD CONSTRAINT annotation_changed_by_fk_fkey FOREIGN KEY (changed_by_fk) REFERENCES public.ab_user(id);


--
-- TOC entry 3358 (class 2606 OID 3963114)
-- Name: annotation annotation_created_by_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.annotation
    ADD CONSTRAINT annotation_created_by_fk_fkey FOREIGN KEY (created_by_fk) REFERENCES public.ab_user(id);


--
-- TOC entry 3356 (class 2606 OID 3963088)
-- Name: annotation_layer annotation_layer_changed_by_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.annotation_layer
    ADD CONSTRAINT annotation_layer_changed_by_fk_fkey FOREIGN KEY (changed_by_fk) REFERENCES public.ab_user(id);


--
-- TOC entry 3355 (class 2606 OID 3963093)
-- Name: annotation_layer annotation_layer_created_by_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.annotation_layer
    ADD CONSTRAINT annotation_layer_created_by_fk_fkey FOREIGN KEY (created_by_fk) REFERENCES public.ab_user(id);


--
-- TOC entry 3357 (class 2606 OID 3963119)
-- Name: annotation annotation_layer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.annotation
    ADD CONSTRAINT annotation_layer_id_fkey FOREIGN KEY (layer_id) REFERENCES public.annotation_layer(id);


--
-- TOC entry 3309 (class 2606 OID 3962585)
-- Name: clusters clusters_changed_by_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clusters
    ADD CONSTRAINT clusters_changed_by_fk_fkey FOREIGN KEY (changed_by_fk) REFERENCES public.ab_user(id);


--
-- TOC entry 3310 (class 2606 OID 3962580)
-- Name: clusters clusters_created_by_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clusters
    ADD CONSTRAINT clusters_created_by_fk_fkey FOREIGN KEY (created_by_fk) REFERENCES public.ab_user(id);


--
-- TOC entry 3321 (class 2606 OID 3962711)
-- Name: columns columns_changed_by_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.columns
    ADD CONSTRAINT columns_changed_by_fk_fkey FOREIGN KEY (changed_by_fk) REFERENCES public.ab_user(id);


--
-- TOC entry 3322 (class 2606 OID 3962706)
-- Name: columns columns_created_by_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.columns
    ADD CONSTRAINT columns_created_by_fk_fkey FOREIGN KEY (created_by_fk) REFERENCES public.ab_user(id);


--
-- TOC entry 3341 (class 2606 OID 3962893)
-- Name: css_templates css_templates_changed_by_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.css_templates
    ADD CONSTRAINT css_templates_changed_by_fk_fkey FOREIGN KEY (changed_by_fk) REFERENCES public.ab_user(id);


--
-- TOC entry 3340 (class 2606 OID 3962898)
-- Name: css_templates css_templates_created_by_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.css_templates
    ADD CONSTRAINT css_templates_created_by_fk_fkey FOREIGN KEY (created_by_fk) REFERENCES public.ab_user(id);


--
-- TOC entry 3367 (class 2606 OID 3963212)
-- Name: dashboard_email_schedules dashboard_email_schedules_changed_by_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dashboard_email_schedules
    ADD CONSTRAINT dashboard_email_schedules_changed_by_fk_fkey FOREIGN KEY (changed_by_fk) REFERENCES public.ab_user(id);


--
-- TOC entry 3366 (class 2606 OID 3963217)
-- Name: dashboard_email_schedules dashboard_email_schedules_created_by_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dashboard_email_schedules
    ADD CONSTRAINT dashboard_email_schedules_created_by_fk_fkey FOREIGN KEY (created_by_fk) REFERENCES public.ab_user(id);


--
-- TOC entry 3365 (class 2606 OID 3963222)
-- Name: dashboard_email_schedules dashboard_email_schedules_dashboard_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dashboard_email_schedules
    ADD CONSTRAINT dashboard_email_schedules_dashboard_id_fkey FOREIGN KEY (dashboard_id) REFERENCES public.dashboards(id);


--
-- TOC entry 3364 (class 2606 OID 3963227)
-- Name: dashboard_email_schedules dashboard_email_schedules_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dashboard_email_schedules
    ADD CONSTRAINT dashboard_email_schedules_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.ab_user(id);


--
-- TOC entry 3419 (class 2606 OID 3963855)
-- Name: dashboard_roles dashboard_roles_dashboard_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dashboard_roles
    ADD CONSTRAINT dashboard_roles_dashboard_id_fkey FOREIGN KEY (dashboard_id) REFERENCES public.dashboards(id);


--
-- TOC entry 3418 (class 2606 OID 3963860)
-- Name: dashboard_roles dashboard_roles_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dashboard_roles
    ADD CONSTRAINT dashboard_roles_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.ab_role(id);


--
-- TOC entry 3336 (class 2606 OID 3962828)
-- Name: dashboard_slices dashboard_slices_dashboard_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dashboard_slices
    ADD CONSTRAINT dashboard_slices_dashboard_id_fkey FOREIGN KEY (dashboard_id) REFERENCES public.dashboards(id);


--
-- TOC entry 3335 (class 2606 OID 3962833)
-- Name: dashboard_slices dashboard_slices_slice_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dashboard_slices
    ADD CONSTRAINT dashboard_slices_slice_id_fkey FOREIGN KEY (slice_id) REFERENCES public.slices(id);


--
-- TOC entry 3344 (class 2606 OID 3962936)
-- Name: dashboard_user dashboard_user_dashboard_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dashboard_user
    ADD CONSTRAINT dashboard_user_dashboard_id_fkey FOREIGN KEY (dashboard_id) REFERENCES public.dashboards(id);


--
-- TOC entry 3343 (class 2606 OID 3962941)
-- Name: dashboard_user dashboard_user_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dashboard_user
    ADD CONSTRAINT dashboard_user_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.ab_user(id);


--
-- TOC entry 3311 (class 2606 OID 3962606)
-- Name: dashboards dashboards_changed_by_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dashboards
    ADD CONSTRAINT dashboards_changed_by_fk_fkey FOREIGN KEY (changed_by_fk) REFERENCES public.ab_user(id);


--
-- TOC entry 3312 (class 2606 OID 3962601)
-- Name: dashboards dashboards_created_by_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dashboards
    ADD CONSTRAINT dashboards_created_by_fk_fkey FOREIGN KEY (created_by_fk) REFERENCES public.ab_user(id);


--
-- TOC entry 3316 (class 2606 OID 3962657)
-- Name: datasources datasources_created_by_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.datasources
    ADD CONSTRAINT datasources_created_by_fk_fkey FOREIGN KEY (created_by_fk) REFERENCES public.ab_user(id);


--
-- TOC entry 3313 (class 2606 OID 3962629)
-- Name: dbs dbs_changed_by_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dbs
    ADD CONSTRAINT dbs_changed_by_fk_fkey FOREIGN KEY (changed_by_fk) REFERENCES public.ab_user(id);


--
-- TOC entry 3314 (class 2606 OID 3962624)
-- Name: dbs dbs_created_by_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dbs
    ADD CONSTRAINT dbs_created_by_fk_fkey FOREIGN KEY (created_by_fk) REFERENCES public.ab_user(id);


--
-- TOC entry 3375 (class 2606 OID 3963297)
-- Name: druiddatasource_user druiddatasource_user_datasource_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.druiddatasource_user
    ADD CONSTRAINT druiddatasource_user_datasource_id_fkey FOREIGN KEY (datasource_id) REFERENCES public.datasources(id);


--
-- TOC entry 3374 (class 2606 OID 3963302)
-- Name: druiddatasource_user druiddatasource_user_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.druiddatasource_user
    ADD CONSTRAINT druiddatasource_user_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.ab_user(id);


--
-- TOC entry 3417 (class 2606 OID 3963835)
-- Name: dynamic_plugin dynamic_plugin_changed_by_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dynamic_plugin
    ADD CONSTRAINT dynamic_plugin_changed_by_fk_fkey FOREIGN KEY (changed_by_fk) REFERENCES public.ab_user(id);


--
-- TOC entry 3416 (class 2606 OID 3963840)
-- Name: dynamic_plugin dynamic_plugin_created_by_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.dynamic_plugin
    ADD CONSTRAINT dynamic_plugin_created_by_fk_fkey FOREIGN KEY (created_by_fk) REFERENCES public.ab_user(id);


--
-- TOC entry 3342 (class 2606 OID 3962911)
-- Name: favstar favstar_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.favstar
    ADD CONSTRAINT favstar_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.ab_user(id);


--
-- TOC entry 3422 (class 2606 OID 3963944)
-- Name: filter_sets filter_sets_changed_by_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.filter_sets
    ADD CONSTRAINT filter_sets_changed_by_fk_fkey FOREIGN KEY (changed_by_fk) REFERENCES public.ab_user(id);


--
-- TOC entry 3421 (class 2606 OID 3963949)
-- Name: filter_sets filter_sets_created_by_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.filter_sets
    ADD CONSTRAINT filter_sets_created_by_fk_fkey FOREIGN KEY (created_by_fk) REFERENCES public.ab_user(id);


--
-- TOC entry 3420 (class 2606 OID 3963954)
-- Name: filter_sets filter_sets_dashboard_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.filter_sets
    ADD CONSTRAINT filter_sets_dashboard_id_fkey FOREIGN KEY (dashboard_id) REFERENCES public.dashboards(id);


--
-- TOC entry 3320 (class 2606 OID 3963127)
-- Name: columns fk_columns_datasource_id_datasources; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.columns
    ADD CONSTRAINT fk_columns_datasource_id_datasources FOREIGN KEY (datasource_id) REFERENCES public.datasources(id);


--
-- TOC entry 3315 (class 2606 OID 3963469)
-- Name: datasources fk_datasources_cluster_id_clusters; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.datasources
    ADD CONSTRAINT fk_datasources_cluster_id_clusters FOREIGN KEY (cluster_id) REFERENCES public.clusters(id);


--
-- TOC entry 3323 (class 2606 OID 3963132)
-- Name: metrics fk_metrics_datasource_id_datasources; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.metrics
    ADD CONSTRAINT fk_metrics_datasource_id_datasources FOREIGN KEY (datasource_id) REFERENCES public.datasources(id);


--
-- TOC entry 3337 (class 2606 OID 3962851)
-- Name: logs logs_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.logs
    ADD CONSTRAINT logs_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.ab_user(id);


--
-- TOC entry 3325 (class 2606 OID 3962916)
-- Name: metrics metrics_changed_by_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.metrics
    ADD CONSTRAINT metrics_changed_by_fk_fkey FOREIGN KEY (changed_by_fk) REFERENCES public.ab_user(id);


--
-- TOC entry 3324 (class 2606 OID 3962921)
-- Name: metrics metrics_created_by_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.metrics
    ADD CONSTRAINT metrics_created_by_fk_fkey FOREIGN KEY (created_by_fk) REFERENCES public.ab_user(id);


--
-- TOC entry 3348 (class 2606 OID 3962994)
-- Name: query query_database_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.query
    ADD CONSTRAINT query_database_id_fkey FOREIGN KEY (database_id) REFERENCES public.dbs(id);


--
-- TOC entry 3347 (class 2606 OID 3962999)
-- Name: query query_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.query
    ADD CONSTRAINT query_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.ab_user(id);


--
-- TOC entry 3410 (class 2606 OID 3963771)
-- Name: report_execution_log report_execution_log_report_schedule_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.report_execution_log
    ADD CONSTRAINT report_execution_log_report_schedule_id_fkey FOREIGN KEY (report_schedule_id) REFERENCES public.report_schedule(id);


--
-- TOC entry 3412 (class 2606 OID 3963792)
-- Name: report_recipient report_recipient_changed_by_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.report_recipient
    ADD CONSTRAINT report_recipient_changed_by_fk_fkey FOREIGN KEY (changed_by_fk) REFERENCES public.ab_user(id);


--
-- TOC entry 3411 (class 2606 OID 3963797)
-- Name: report_recipient report_recipient_created_by_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.report_recipient
    ADD CONSTRAINT report_recipient_created_by_fk_fkey FOREIGN KEY (created_by_fk) REFERENCES public.ab_user(id);


--
-- TOC entry 3413 (class 2606 OID 3963787)
-- Name: report_recipient report_recipient_report_schedule_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.report_recipient
    ADD CONSTRAINT report_recipient_report_schedule_id_fkey FOREIGN KEY (report_schedule_id) REFERENCES public.report_schedule(id);


--
-- TOC entry 3406 (class 2606 OID 3963747)
-- Name: report_schedule report_schedule_changed_by_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.report_schedule
    ADD CONSTRAINT report_schedule_changed_by_fk_fkey FOREIGN KEY (changed_by_fk) REFERENCES public.ab_user(id);


--
-- TOC entry 3409 (class 2606 OID 3963732)
-- Name: report_schedule report_schedule_chart_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.report_schedule
    ADD CONSTRAINT report_schedule_chart_id_fkey FOREIGN KEY (chart_id) REFERENCES public.slices(id);


--
-- TOC entry 3405 (class 2606 OID 3963752)
-- Name: report_schedule report_schedule_created_by_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.report_schedule
    ADD CONSTRAINT report_schedule_created_by_fk_fkey FOREIGN KEY (created_by_fk) REFERENCES public.ab_user(id);


--
-- TOC entry 3408 (class 2606 OID 3963737)
-- Name: report_schedule report_schedule_dashboard_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.report_schedule
    ADD CONSTRAINT report_schedule_dashboard_id_fkey FOREIGN KEY (dashboard_id) REFERENCES public.dashboards(id);


--
-- TOC entry 3407 (class 2606 OID 3963742)
-- Name: report_schedule report_schedule_database_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.report_schedule
    ADD CONSTRAINT report_schedule_database_id_fkey FOREIGN KEY (database_id) REFERENCES public.dbs(id);


--
-- TOC entry 3415 (class 2606 OID 3963810)
-- Name: report_schedule_user report_schedule_user_report_schedule_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.report_schedule_user
    ADD CONSTRAINT report_schedule_user_report_schedule_id_fkey FOREIGN KEY (report_schedule_id) REFERENCES public.report_schedule(id);


--
-- TOC entry 3414 (class 2606 OID 3963815)
-- Name: report_schedule_user report_schedule_user_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.report_schedule_user
    ADD CONSTRAINT report_schedule_user_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.ab_user(id);


--
-- TOC entry 3393 (class 2606 OID 3963508)
-- Name: rls_filter_roles rls_filter_roles_rls_filter_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rls_filter_roles
    ADD CONSTRAINT rls_filter_roles_rls_filter_id_fkey FOREIGN KEY (rls_filter_id) REFERENCES public.row_level_security_filters(id);


--
-- TOC entry 3392 (class 2606 OID 3963513)
-- Name: rls_filter_roles rls_filter_roles_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rls_filter_roles
    ADD CONSTRAINT rls_filter_roles_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.ab_role(id);


--
-- TOC entry 3395 (class 2606 OID 3963526)
-- Name: rls_filter_tables rls_filter_tables_rls_filter_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rls_filter_tables
    ADD CONSTRAINT rls_filter_tables_rls_filter_id_fkey FOREIGN KEY (rls_filter_id) REFERENCES public.row_level_security_filters(id);


--
-- TOC entry 3394 (class 2606 OID 3963531)
-- Name: rls_filter_tables rls_filter_tables_table_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.rls_filter_tables
    ADD CONSTRAINT rls_filter_tables_table_id_fkey FOREIGN KEY (table_id) REFERENCES public.tables(id);


--
-- TOC entry 3391 (class 2606 OID 3963485)
-- Name: row_level_security_filters row_level_security_filters_changed_by_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.row_level_security_filters
    ADD CONSTRAINT row_level_security_filters_changed_by_fk_fkey FOREIGN KEY (changed_by_fk) REFERENCES public.ab_user(id);


--
-- TOC entry 3390 (class 2606 OID 3963490)
-- Name: row_level_security_filters row_level_security_filters_created_by_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.row_level_security_filters
    ADD CONSTRAINT row_level_security_filters_created_by_fk_fkey FOREIGN KEY (created_by_fk) REFERENCES public.ab_user(id);


--
-- TOC entry 3354 (class 2606 OID 3963057)
-- Name: saved_query saved_query_changed_by_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.saved_query
    ADD CONSTRAINT saved_query_changed_by_fk_fkey FOREIGN KEY (changed_by_fk) REFERENCES public.ab_user(id);


--
-- TOC entry 3353 (class 2606 OID 3963062)
-- Name: saved_query saved_query_created_by_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.saved_query
    ADD CONSTRAINT saved_query_created_by_fk_fkey FOREIGN KEY (created_by_fk) REFERENCES public.ab_user(id);


--
-- TOC entry 3351 (class 2606 OID 3963072)
-- Name: saved_query saved_query_db_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.saved_query
    ADD CONSTRAINT saved_query_db_id_fkey FOREIGN KEY (db_id) REFERENCES public.dbs(id);


--
-- TOC entry 3352 (class 2606 OID 3963067)
-- Name: saved_query saved_query_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.saved_query
    ADD CONSTRAINT saved_query_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.ab_user(id);


--
-- TOC entry 3371 (class 2606 OID 3963250)
-- Name: slice_email_schedules slice_email_schedules_changed_by_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.slice_email_schedules
    ADD CONSTRAINT slice_email_schedules_changed_by_fk_fkey FOREIGN KEY (changed_by_fk) REFERENCES public.ab_user(id);


--
-- TOC entry 3370 (class 2606 OID 3963255)
-- Name: slice_email_schedules slice_email_schedules_created_by_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.slice_email_schedules
    ADD CONSTRAINT slice_email_schedules_created_by_fk_fkey FOREIGN KEY (created_by_fk) REFERENCES public.ab_user(id);


--
-- TOC entry 3369 (class 2606 OID 3963260)
-- Name: slice_email_schedules slice_email_schedules_slice_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.slice_email_schedules
    ADD CONSTRAINT slice_email_schedules_slice_id_fkey FOREIGN KEY (slice_id) REFERENCES public.slices(id);


--
-- TOC entry 3368 (class 2606 OID 3963265)
-- Name: slice_email_schedules slice_email_schedules_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.slice_email_schedules
    ADD CONSTRAINT slice_email_schedules_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.ab_user(id);


--
-- TOC entry 3346 (class 2606 OID 3962954)
-- Name: slice_user slice_user_slice_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.slice_user
    ADD CONSTRAINT slice_user_slice_id_fkey FOREIGN KEY (slice_id) REFERENCES public.slices(id);


--
-- TOC entry 3345 (class 2606 OID 3962959)
-- Name: slice_user slice_user_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.slice_user
    ADD CONSTRAINT slice_user_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.ab_user(id);


--
-- TOC entry 3327 (class 2606 OID 3962763)
-- Name: slices slices_changed_by_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.slices
    ADD CONSTRAINT slices_changed_by_fk_fkey FOREIGN KEY (changed_by_fk) REFERENCES public.ab_user(id);


--
-- TOC entry 3328 (class 2606 OID 3962758)
-- Name: slices slices_created_by_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.slices
    ADD CONSTRAINT slices_created_by_fk_fkey FOREIGN KEY (created_by_fk) REFERENCES public.ab_user(id);


--
-- TOC entry 3326 (class 2606 OID 3963928)
-- Name: slices slices_last_saved_by_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.slices
    ADD CONSTRAINT slices_last_saved_by_fk FOREIGN KEY (last_saved_by_fk) REFERENCES public.ab_user(id);


--
-- TOC entry 3329 (class 2606 OID 3962789)
-- Name: sql_metrics sql_metrics_changed_by_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sql_metrics
    ADD CONSTRAINT sql_metrics_changed_by_fk_fkey FOREIGN KEY (changed_by_fk) REFERENCES public.ab_user(id);


--
-- TOC entry 3330 (class 2606 OID 3962784)
-- Name: sql_metrics sql_metrics_created_by_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sql_metrics
    ADD CONSTRAINT sql_metrics_created_by_fk_fkey FOREIGN KEY (created_by_fk) REFERENCES public.ab_user(id);


--
-- TOC entry 3331 (class 2606 OID 3962779)
-- Name: sql_metrics sql_metrics_table_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sql_metrics
    ADD CONSTRAINT sql_metrics_table_id_fkey FOREIGN KEY (table_id) REFERENCES public.tables(id);


--
-- TOC entry 3404 (class 2606 OID 3963657)
-- Name: sql_observations sql_observations_alert_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sql_observations
    ADD CONSTRAINT sql_observations_alert_id_fkey FOREIGN KEY (alert_id) REFERENCES public.alerts(id);


--
-- TOC entry 3373 (class 2606 OID 3963279)
-- Name: sqlatable_user sqlatable_user_table_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sqlatable_user
    ADD CONSTRAINT sqlatable_user_table_id_fkey FOREIGN KEY (table_id) REFERENCES public.tables(id);


--
-- TOC entry 3372 (class 2606 OID 3963284)
-- Name: sqlatable_user sqlatable_user_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sqlatable_user
    ADD CONSTRAINT sqlatable_user_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.ab_user(id);


--
-- TOC entry 3385 (class 2606 OID 3963409)
-- Name: tab_state tab_state_changed_by_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tab_state
    ADD CONSTRAINT tab_state_changed_by_fk_fkey FOREIGN KEY (changed_by_fk) REFERENCES public.ab_user(id);


--
-- TOC entry 3384 (class 2606 OID 3963414)
-- Name: tab_state tab_state_created_by_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tab_state
    ADD CONSTRAINT tab_state_created_by_fk_fkey FOREIGN KEY (created_by_fk) REFERENCES public.ab_user(id);


--
-- TOC entry 3383 (class 2606 OID 3963419)
-- Name: tab_state tab_state_database_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tab_state
    ADD CONSTRAINT tab_state_database_id_fkey FOREIGN KEY (database_id) REFERENCES public.dbs(id);


--
-- TOC entry 3382 (class 2606 OID 3963424)
-- Name: tab_state tab_state_latest_query_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tab_state
    ADD CONSTRAINT tab_state_latest_query_id_fkey FOREIGN KEY (latest_query_id) REFERENCES public.query(client_id);


--
-- TOC entry 3381 (class 2606 OID 3963429)
-- Name: tab_state tab_state_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tab_state
    ADD CONSTRAINT tab_state_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.ab_user(id);


--
-- TOC entry 3332 (class 2606 OID 3962815)
-- Name: table_columns table_columns_changed_by_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.table_columns
    ADD CONSTRAINT table_columns_changed_by_fk_fkey FOREIGN KEY (changed_by_fk) REFERENCES public.ab_user(id);


--
-- TOC entry 3333 (class 2606 OID 3962810)
-- Name: table_columns table_columns_created_by_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.table_columns
    ADD CONSTRAINT table_columns_created_by_fk_fkey FOREIGN KEY (created_by_fk) REFERENCES public.ab_user(id);


--
-- TOC entry 3334 (class 2606 OID 3962805)
-- Name: table_columns table_columns_table_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.table_columns
    ADD CONSTRAINT table_columns_table_id_fkey FOREIGN KEY (table_id) REFERENCES public.tables(id);


--
-- TOC entry 3389 (class 2606 OID 3963446)
-- Name: table_schema table_schema_changed_by_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.table_schema
    ADD CONSTRAINT table_schema_changed_by_fk_fkey FOREIGN KEY (changed_by_fk) REFERENCES public.ab_user(id);


--
-- TOC entry 3388 (class 2606 OID 3963451)
-- Name: table_schema table_schema_created_by_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.table_schema
    ADD CONSTRAINT table_schema_created_by_fk_fkey FOREIGN KEY (created_by_fk) REFERENCES public.ab_user(id);


--
-- TOC entry 3387 (class 2606 OID 3963456)
-- Name: table_schema table_schema_database_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.table_schema
    ADD CONSTRAINT table_schema_database_id_fkey FOREIGN KEY (database_id) REFERENCES public.dbs(id);


--
-- TOC entry 3386 (class 2606 OID 3963461)
-- Name: table_schema table_schema_tab_state_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.table_schema
    ADD CONSTRAINT table_schema_tab_state_id_fkey FOREIGN KEY (tab_state_id) REFERENCES public.tab_state(id) ON DELETE CASCADE;


--
-- TOC entry 3317 (class 2606 OID 3962690)
-- Name: tables tables_changed_by_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tables
    ADD CONSTRAINT tables_changed_by_fk_fkey FOREIGN KEY (changed_by_fk) REFERENCES public.ab_user(id);


--
-- TOC entry 3318 (class 2606 OID 3962685)
-- Name: tables tables_created_by_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tables
    ADD CONSTRAINT tables_created_by_fk_fkey FOREIGN KEY (created_by_fk) REFERENCES public.ab_user(id);


--
-- TOC entry 3319 (class 2606 OID 3962680)
-- Name: tables tables_database_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tables
    ADD CONSTRAINT tables_database_id_fkey FOREIGN KEY (database_id) REFERENCES public.dbs(id);


--
-- TOC entry 3376 (class 2606 OID 3963334)
-- Name: tag tag_changed_by_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tag
    ADD CONSTRAINT tag_changed_by_fk_fkey FOREIGN KEY (changed_by_fk) REFERENCES public.ab_user(id);


--
-- TOC entry 3377 (class 2606 OID 3963329)
-- Name: tag tag_created_by_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tag
    ADD CONSTRAINT tag_created_by_fk_fkey FOREIGN KEY (created_by_fk) REFERENCES public.ab_user(id);


--
-- TOC entry 3378 (class 2606 OID 3963365)
-- Name: tagged_object tagged_object_changed_by_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tagged_object
    ADD CONSTRAINT tagged_object_changed_by_fk_fkey FOREIGN KEY (changed_by_fk) REFERENCES public.ab_user(id);


--
-- TOC entry 3379 (class 2606 OID 3963360)
-- Name: tagged_object tagged_object_created_by_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tagged_object
    ADD CONSTRAINT tagged_object_created_by_fk_fkey FOREIGN KEY (created_by_fk) REFERENCES public.ab_user(id);


--
-- TOC entry 3380 (class 2606 OID 3963355)
-- Name: tagged_object tagged_object_tag_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tagged_object
    ADD CONSTRAINT tagged_object_tag_id_fkey FOREIGN KEY (tag_id) REFERENCES public.tag(id);


--
-- TOC entry 3339 (class 2606 OID 3962872)
-- Name: url url_changed_by_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.url
    ADD CONSTRAINT url_changed_by_fk_fkey FOREIGN KEY (changed_by_fk) REFERENCES public.ab_user(id);


--
-- TOC entry 3338 (class 2606 OID 3962877)
-- Name: url url_created_by_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.url
    ADD CONSTRAINT url_created_by_fk_fkey FOREIGN KEY (created_by_fk) REFERENCES public.ab_user(id);


--
-- TOC entry 3363 (class 2606 OID 3963175)
-- Name: user_attribute user_attribute_changed_by_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_attribute
    ADD CONSTRAINT user_attribute_changed_by_fk_fkey FOREIGN KEY (changed_by_fk) REFERENCES public.ab_user(id);


--
-- TOC entry 3362 (class 2606 OID 3963180)
-- Name: user_attribute user_attribute_created_by_fk_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_attribute
    ADD CONSTRAINT user_attribute_created_by_fk_fkey FOREIGN KEY (created_by_fk) REFERENCES public.ab_user(id);


--
-- TOC entry 3361 (class 2606 OID 3963185)
-- Name: user_attribute user_attribute_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_attribute
    ADD CONSTRAINT user_attribute_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.ab_user(id);


--
-- TOC entry 3360 (class 2606 OID 3963190)
-- Name: user_attribute user_attribute_welcome_dashboard_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_attribute
    ADD CONSTRAINT user_attribute_welcome_dashboard_id_fkey FOREIGN KEY (welcome_dashboard_id) REFERENCES public.dashboards(id);


-- Completed on 2022-03-11 14:51:15

--
-- PostgreSQL database dump complete
--

