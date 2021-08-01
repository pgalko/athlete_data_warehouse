
---
---DB
---
SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;
SET default_tablespace = '';
SET default_with_oids = false;

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;
COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';

CREATE EXTENSION IF NOT EXISTS pgcrypto WITH SCHEMA public;
COMMENT ON EXTENSION pgcrypto IS 'cryptographic functions';




---
---ATHLETE
---
CREATE TABLE public.athlete (
    ath_un character varying(50),
    gc_email character varying(50),
    gc_password character varying(300),
    id integer NOT NULL,
    mfp_username character varying(50),
    mfp_password character varying(300),
    dropbox_access_token character varying(300),
    auto_sync boolean,
    diasend_username character varying(50),
    diasend_password character varying(300),
    glimp_export_link character varying(300),
    libreview_export_link character varying(300),
    mm_export_link character varying(300),
    oura_refresh_token character varying(300)
    strava_refresh_token character varying(300)
);

ALTER TABLE public.athlete OWNER TO postgres;

CREATE SEQUENCE public.athlete_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE public.athlete_id_seq OWNER TO postgres;

ALTER SEQUENCE public.athlete_id_seq OWNED BY public.athlete.id;

---
---DIASEND CGM
---
CREATE TABLE public.diasend_cgm (
    id integer NOT NULL,
    athlete_id integer,
    "timestamp" character varying,
    glucose_nmol_l real,
    data_source character varying(30),
    glucose_nmol_l_15min_avrg real,
    timestamp_gmt character varying
);

ALTER TABLE public.diasend_cgm OWNER TO postgres;

CREATE SEQUENCE public.diasend_cgm_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE public.diasend_cgm_id_seq OWNER TO postgres;

ALTER SEQUENCE public.diasend_cgm_id_seq OWNED BY public.diasend_cgm.id;

---
---FILES
---
CREATE TABLE public.files (
    id bigint NOT NULL,
    data_file_path character varying(256),
    athlete_id integer
);

ALTER TABLE public.files OWNER TO postgres;

CREATE SEQUENCE public.files_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE public.files_id_seq OWNER TO postgres;

ALTER SEQUENCE public.files_id_seq OWNED BY public.files.id;

---
---GARMIN CONNECT BODY COMPOSITION
---
CREATE TABLE public.garmin_connect_body_composition (
    id integer NOT NULL,
    athlete_id integer,
    body_water real,
    muscle_mass_gm integer,
    visceral_fat integer,
    weight_gm real,
    bmi real,
    body_fat real,
    physique_rating character varying,
    timestamp character varying,
    calendar_date character varying,
    metabolic_age character varying,
    bone_mass_gm integer,
    caloric_intake character varying,
    source_type character varying
);

ALTER TABLE public.garmin_connect_body_composition OWNER TO postgres;

CREATE SEQUENCE public.garmin_connect_body_composition_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE public.garmin_connect_body_composition_id_seq OWNER TO postgres;

ALTER SEQUENCE public.garmin_connect_body_composition_id_seq OWNED BY public.garmin_connect_body_composition.id;

---
---GARMIN CONNECT DAILY SUMMARY
---
CREATE TABLE public.garmin_connect_daily_summary (
    id integer NOT NULL,
    athlete_id integer,
    start_gmt character varying(30),
    end_gmt character varying(30),
    activity_level_constant boolean,
    steps integer,
    primary_activity_level character varying(20)
);

ALTER TABLE public.garmin_connect_daily_summary OWNER TO postgres;

CREATE SEQUENCE public.garmin_connect_daily_summary_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE public.garmin_connect_daily_summary_id_seq OWNER TO postgres;

ALTER SEQUENCE public.garmin_connect_daily_summary_id_seq OWNED BY public.garmin_connect_daily_summary.id;

---
---GARMIN CONNECT HRV TRACKING
---
CREATE TABLE public.garmin_connect_hrv_tracking (
    id integer NOT NULL,
    gc_activity_id bigint,
    hrv numeric
);

ALTER TABLE public.garmin_connect_hrv_tracking OWNER TO postgres;

CREATE SEQUENCE public.garmin_connect_hrv_tracking_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE public.garmin_connect_hrv_tracking_id_seq OWNER TO postgres;

ALTER SEQUENCE public.garmin_connect_hrv_tracking_id_seq OWNED BY public.garmin_connect_hrv_tracking.id;

---
---GARMIN CONNEOCT ORIGINAL RECORD
---
CREATE TABLE public.garmin_connect_original_record (
    activity_type character varying(30),
    altitude real,
    cadence real,
    distance real,
    enhanced_altitude real,
    enhanced_speed real,
    fractional_cadence real,
    heart_rate real,
    position_lat numeric(30,1),
    position_long numeric(30,1),
    speed real,
    stance_time real,
    stance_time_balance real,
    step_length real,
    "timestamp" character varying(30),
    vertical_oscillation real,
    vertical_ratio real,
    accumulated_power real,
    left_pedal_smoothness real,
    left_torque_effectiveness real,
    power real,
    right_pedal_smoothness real,
    right_torque_effectiveness real,
    temperature real,
    gc_activity_id bigint,
    id integer NOT NULL,
    swim_stroke character varying,
    avg_speed real,
    avg_swimming_cadence integer,
    event character varying(20),
    event_group character varying(20),
    event_type character varying(20),
    length_type character varying(20),
    message_index integer,
    start_time character varying(30),
    total_calories integer,
    total_elapsed_time real,
    total_strokes integer,
    total_timer_time real,
    lap_id bigint,
    est_core_temp numeric,
    hrv_btb numeric
);

ALTER TABLE public.garmin_connect_original_record OWNER TO postgres;

CREATE SEQUENCE public.garmin_connect_original_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE public.garmin_connect_original_id_seq OWNER TO postgres;

ALTER SEQUENCE public.garmin_connect_original_id_seq OWNED BY public.garmin_connect_original_record.id;

---
---GARMIN CONNEICT ORIGINAL LAP
---
CREATE TABLE public.garmin_connect_original_lap (
    id integer NOT NULL,
    avg_cadence integer,
    avg_cadence_position real[],
    avg_combined_pedal_smoothness real,
    avg_heart_rate integer,
    avg_left_pco real,
    avg_left_pedal_smoothness real,
    avg_left_power_phase real[],
    avg_left_power_phase_peak real[],
    avg_left_torque_effectiveness real,
    avg_power integer,
    avg_power_position real[],
    avg_right_pco real[],
    avg_right_pedal_smoothness real,
    avg_right_power_phase real[],
    avg_right_power_phase_peak real[],
    avg_right_torque_effectiveness real[],
    end_position_lat character varying,
    end_position_long character varying,
    enhanced_avg_speed real,
    enhanced_max_speed real,
    event character varying,
    event_group character varying,
    event_type character varying,
    intensity character varying,
    lap_trigger character varying,
    left_right_balance real,
    max_cadence integer,
    max_cadence_position real[],
    max_heart_rate integer,
    max_power integer,
    max_power_position real[],
    max_speed real,
    message_index integer,
    normalized_power integer,
    sport character varying,
    stand_count real,
    start_position_lat character varying,
    start_position_long character varying,
    start_time character varying,
    time_standing real,
    "timestamp" character varying,
    total_ascent integer,
    total_calories integer,
    total_cycles integer,
    total_descent integer,
    total_distance real,
    total_elapsed_time real,
    total_fat_calories integer,
    total_timer_time real,
    total_work integer,
    gc_activity_id bigint,
    avg_speed real
);

ALTER TABLE public.garmin_connect_original_lap OWNER TO postgres;

CREATE SEQUENCE public.garmin_connect_original_lap_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE public.garmin_connect_original_lap_id_seq OWNER TO postgres;

ALTER SEQUENCE public.garmin_connect_original_lap_id_seq OWNED BY public.garmin_connect_original_lap.id;

---
---GARMIN CONNECT ORIGINAL SESSION
---
CREATE TABLE public.garmin_connect_original_session (
    avg_cadence integer,
    avg_cadence_position real[],
    avg_combined_pedal_smoothness real,
    avg_heart_rate integer,
    avg_left_pco real,
    avg_left_pedal_smoothness real,
    avg_left_power_phase real[],
    avg_left_power_phase_peak real[],
    avg_left_torque_effectiveness real,
    avg_power integer,
    avg_power_position integer[],
    avg_right_pco real,
    avg_right_pedal_smoothness real,
    avg_right_power_phase real[],
    avg_right_power_phase_peak real[],
    avg_right_torque_effectiveness real,
    avg_speed real,
    enhanced_avg_speed real,
    enhanced_max_speed real,
    event character varying,
    event_group character varying,
    event_type character varying,
    first_lap_index integer,
    intensity_factor real,
    left_right_balance real,
    max_cadence integer,
    max_cadence_position real[],
    max_heart_rate integer,
    max_power integer,
    max_power_position integer[],
    max_speed real,
    message_index integer,
    nec_lat character varying,
    nec_long character varying,
    normalized_power integer,
    num_laps integer,
    sport character varying,
    stand_count integer,
    start_position_lat character varying,
    start_position_long character varying,
    start_time character varying,
    sub_sport character varying,
    swc_lat character varying,
    swc_long character varying,
    threshold_power integer,
    time_standing real,
    "timestamp" character varying,
    total_ascent integer,
    total_calories integer,
    total_cycles integer,
    total_descent integer,
    total_distance real,
    total_elapsed_time real,
    total_fat_calories real,
    total_timer_time real,
    total_work bigint,
    training_stress_score real,
    trigger character varying,
    gc_activity_id bigint NOT NULL,
    athlete_id integer,
    hrv_rmssd numeric,
    hrv_sdrr numeric,
    hrv_pnn50 numeric,
    hrv_pnn20 numeric
);


ALTER TABLE public.garmin_connect_original_session OWNER TO postgres;

---
---GARMIN CONNECT WELNESS
---
CREATE TABLE public.garmin_connect_wellness (
    wellness_total_steps real,
    wellness_common_active_calories real,
    wellness_floors_ascended real,
    wellness_max_heart_rate real,
    wellness_min_avg_heart_rate real,
    wellness_average_stress real,
    wellness_resting_heart_rate real,
    wellness_max_stress real,
    wellness_abnormalhr_alerts_count real,
    wellness_max_avg_heart_rate real,
    wellness_total_steps_goal real,
    wellness_user_floors_ascended_goal real,
    wellness_moderate_intensity_minutes real,
    wellness_total_calories real,
    wellness_bodybattery_charged real,
    wellness_floors_descended real,
    wellness_bmr_calories real,
    food_calories_remaining real,
    common_total_calories real,
    wellness_average_steps real,
    wellness_vigorous_intensity_minutes real,
    wellness_total_distance real,
    common_total_distance real,
    wellness_active_calories real,
    food_calories_consumed real,
    id integer NOT NULL,
    athlete_id integer,
    calendar_date date,
    wellness_user_intensity_goal real,
    wellness_min_heart_rate real,
    wellness_body_battery_drained real,
    sleep_duration real
);

ALTER TABLE public.garmin_connect_wellness OWNER TO postgres;

CREATE SEQUENCE public.garmin_connect_wellness_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE public.garmin_connect_wellness_id_seq OWNER TO postgres;

ALTER SEQUENCE public.garmin_connect_wellness_id_seq OWNED BY public.garmin_connect_wellness.id;

---
---WELNESS ACTIVITY TYPE SUMARY
---
CREATE TABLE public.gc_original_wellness_act_type_summary (
    id bigint NOT NULL,
    athlete_id integer,
    active_calories integer,
    active_time real,
    activity_type character varying,
    distance real,
    duration_min integer,
    steps integer,
    "timestamp" character varying
);

ALTER TABLE public.gc_original_wellness_act_type_summary OWNER TO postgres;

CREATE SEQUENCE public.gc_original_wellness_act_type_summary_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE public.gc_original_wellness_act_type_summary_id_seq OWNER TO postgres;

ALTER SEQUENCE public.gc_original_wellness_act_type_summary_id_seq OWNED BY public.gc_original_wellness_act_type_summary.id;

---
---WELNESS ACTIVITY TRACKING
---
CREATE TABLE public.gc_original_wellness_activity_tracking (
    id bigint NOT NULL,
    athlete_id integer,
    activity_type character varying,
    current_activity_type_intensity integer[],
    intensity integer,
    "timestamp" character varying
);

ALTER TABLE public.gc_original_wellness_activity_tracking OWNER TO postgres;

CREATE SEQUENCE public.gc_original_wellness_activity_tracking_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE public.gc_original_wellness_activity_tracking_id_seq OWNER TO postgres;

ALTER SEQUENCE public.gc_original_wellness_activity_tracking_id_seq OWNED BY public.gc_original_wellness_activity_tracking.id;

---
---WELNESS HR TRACKING
---
CREATE TABLE public.gc_original_wellness_hr_tracking (
    id bigint NOT NULL,
    athlete_id integer,
    heart_rate integer,
    timestamp_16 integer,
    "timestamp" character varying
);

ALTER TABLE public.gc_original_wellness_hr_tracking OWNER TO postgres;

CREATE SEQUENCE public.gc_original_wellness_hr_tracking_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE public.gc_original_wellness_hr_tracking_id_seq OWNER TO postgres;

ALTER SEQUENCE public.gc_original_wellness_hr_tracking_id_seq OWNED BY public.gc_original_wellness_hr_tracking.id;

---
---WELLNESS STRESS TRACKING
---
CREATE TABLE public.gc_original_wellness_stress_tracking (
    id bigint NOT NULL,
    athlete_id integer,
    stress_level_time character varying,
    stress_level_value integer,
    "timestamp" character varying
);

ALTER TABLE public.gc_original_wellness_stress_tracking OWNER TO postgres;

CREATE SEQUENCE public.gc_original_wellness_stress_tracking_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE public.gc_original_wellness_stress_tracking_id_seq OWNER TO postgres;

ALTER SEQUENCE public.gc_original_wellness_stress_tracking_id_seq OWNED BY public.gc_original_wellness_stress_tracking.id;

--
--MFP NUTRITION
--
CREATE TABLE public.mfp_nutrition (
    id bigint NOT NULL,
    athlete_id integer,
    date date,
    meal character varying,
    food_item character varying,
    units character varying,
    quantity real,
    fiber real,
    sodium real,
    carbohydrates real,
    calories real,
    fat real,
    protein real
);

ALTER TABLE public.mfp_nutrition OWNER TO postgres;

CREATE SEQUENCE public.mfp_nutrition_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE public.mfp_nutrition_id_seq OWNER TO postgres;

ALTER SEQUENCE public.mfp_nutrition_id_seq OWNED BY public.mfp_nutrition.id;

--
-- MIND MONITOR
--
CREATE TABLE public.mind_monitor_eeg (
    id integer NOT NULL,
    "timestamp" character varying,
    delta_tp9 real,
    delta_af7 real,
    delta_af8 real,
    delta_tp10 real,
    athlete_id integer,
    theta_tp9 real,
    theta_af7 real,
    theta_af8 real,
    theta_tp10 real,
    alpha_tp9 real,
    alpha_af7 real,
    alpha_af8 real,
    alpha_tp10 real,
    beta_tp9 real,
    beta_af7 real,
    beta_af8 real,
    beta_tp10 real,
    gamma_tp9 real,
    gamma_af7 real,
    gamma_af8 real,
    gamma_tp10 real,
    raw_tp9 real,
    raw_af7 real,
    raw_af8 real,
    raw_tp10 real,
    aux_right real,
    accelerometer_x real,
    accelerometer_y real,
    accelerometer_z real,
    gyro_x real,
    gyro_y real,
    gyro_z real,
    head_band_on real,
    hsi_tp9 real,
    hsi_af7 real,
    hsi_af8 real,
    hsi_tp10 real,
    battery real,
    elements character varying,
    timestamp_gmt character varying
);

ALTER TABLE public.mind_monitor_eeg OWNER TO postgres;

CREATE SEQUENCE public.mind_monitor_eeg_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE public.mind_monitor_eeg_id_seq OWNER TO postgres;

ALTER SEQUENCE public.mind_monitor_eeg_id_seq OWNED BY public.mind_monitor_eeg.id;

---
---TIMEZONES
---
CREATE TABLE public.timezones
(
    id integer NOT NULL,
    gc_activity_id bigint,
    timestamp_local character varying,
    timestamp_gmt character varying,
    timezone character varying,
    long_degr numeric,
    lat_degr numeric,
    alt_avrg integer,
    end_time_gmt character varying
);

ALTER TABLE public.timezones OWNER TO postgres;

CREATE SEQUENCE public.timezones_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE public.timezones_id_seq OWNER TO postgres;

ALTER SEQUENCE public.timezones_id_seq OWNED BY public.timezones.id;

---
---GMT_LOCAL_TIME_DIFFERENCE
---

CREATE TABLE public.gmt_local_time_difference
(
    id integer NOT NULL,
    local_date date,
    local_midnight_timestamp timestamp without time zone,
    gmt_midnight_timestamp timestamp without time zone,
    gmt_local_difference interval(6),
    athlete_id integer
);

ALTER TABLE public.gmt_local_time_difference OWNER TO postgres;

CREATE SEQUENCE public.gmt_local_time_difference_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE public.gmt_local_time_difference_id_seq OWNER TO postgres;

ALTER SEQUENCE public.gmt_local_time_difference_id_seq OWNED BY public.gmt_local_time_difference.id;


---
---GC_ORIGINAL_WELLNESS_SLEEP_TRACKING
---
CREATE TABLE public.gc_original_wellness_sleep_tracking
(
    id integer NOT NULL,
    timestamp_gmt character varying,
    timestamp_local character varying,
    activity_tracking_id bigint,
    hr_tracking_id bigint,
    stress_tracking_id bigint
);

ALTER TABLE public.gc_original_wellness_sleep_tracking OWNER TO postgres;

CREATE SEQUENCE public.gc_original_wellness_sleep_tracking_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE public.gc_original_wellness_sleep_tracking_id_seq OWNER TO postgres;

ALTER SEQUENCE public.gc_original_wellness_sleep_tracking_id_seq OWNED BY public.gc_original_wellness_sleep_tracking.id;

---
---WEATHER
---
CREATE TABLE public.weather
(
    id integer NOT NULL,
    athlete_id integer,
    timestamp_gmt character varying,
    temperature numeric,
    dew_point numeric,
    relative_humidity numeric,
    precipitation numeric,
    snow numeric,
    wind_direction numeric,
    wind_speed numeric,
    wind_gust numeric,
    sea_air_pressure numeric,
    total_sunshine numeric,
    condition_code numeric
);

ALTER TABLE public.weather OWNER TO postgres;

CREATE SEQUENCE public.weather_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE public.weather_id_seq OWNER TO postgres;

ALTER SEQUENCE public.weather_id_seq OWNED BY public.weather.id;

--
--OURA READINESS DAILY SUMMARY
--
CREATE TABLE public.oura_readiness_daily_summary( 
  id integer NOT NULL,
  athlete_id integer,
  summary_date character varying,
  period_id integer,
  score integer,
  score_previous_night integer,
  score_sleep_balance integer,
  score_previous_day integer,
  score_activity_balance integer,
  score_resting_hr integer,
  score_hrv_balance integer,
  score_recovery_index integer,
  score_temperature integer,
  rest_mode_state integer
);
  
ALTER TABLE public.oura_readiness_daily_summary OWNER TO postgres;

CREATE SEQUENCE public.oura_readiness_daily_summary_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
	
ALTER TABLE public.oura_readiness_daily_summary_id_seq OWNER TO postgres;

ALTER SEQUENCE public.oura_readiness_daily_summary_id_seq OWNED BY public.oura_readiness_daily_summary.id;

--
--OURA SLEEP DAILY SUMMARY
--
CREATE TABLE public.oura_sleep_daily_summary( 
  id integer NOT NULL,
  athlete_id integer,
  summary_date character varying,
  period_id integer,
  is_longest integer,
  timezone integer,
  bedtime_start character varying,
  bedtime_end character varying,
  score integer,
  score_total integer,
  score_disturbances integer,
  score_efficiency integer,
  score_latency integer,
  score_rem integer,
  score_deep integer,
  score_alignment integer,
  total integer,
  duration integer,
  awake integer,
  light integer,
  rem integer,
  deep integer,
  onset_latency integer,
  restless integer,
  efficiency integer,
  midpoint_time integer,
  hr_lowest integer,
  hr_average real,
  rmssd integer,
  breath_average real,
  temperature_delta real,
  bedtime_end_delta  integer, 
  midpoint_at_delta integer,
  bedtime_start_delta integer,
  temperature_deviation real,
  temperature_trend_deviation real
); 


ALTER TABLE public.oura_sleep_daily_summary OWNER TO postgres;

CREATE SEQUENCE public.oura_sleep_daily_summary_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
	
ALTER TABLE public.oura_sleep_daily_summary_id_seq OWNER TO postgres;

ALTER SEQUENCE public.oura_sleep_daily_summary_id_seq OWNED BY public.oura_sleep_daily_summary.id;

--
--OURA ACTIVITY DAILY SUMMARY
--
CREATE TABLE public.oura_activity_daily_summary( 
  id integer NOT NULL,
  athlete_id integer,
  summary_date character varying,
  day_start character varying,
  day_end character varying,
  timezone integer,
  score integer,
  score_stay_active integer,
  score_move_every_hour integer,
  score_meet_daily_targets integer,
  score_training_frequency integer,
  score_training_volume integer,
  score_recovery_time integer,
  daily_movement integer,
  non_wear integer,
  rest integer,
  inactive integer,
  inactivity_alerts integer,
  low integer,
  medium integer,
  high integer,
  steps integer,
  cal_total integer,
  cal_active integer,
  met_min_inactive integer,
  met_min_low integer,
  met_min_medium integer,
  met_min_high integer,
  average_met real,
  rest_mode_state integer,
  to_target_km real, 
  target_miles real,  
  total integer, 
  to_target_miles real, 
  target_calories integer, 
  target_km real
);
  
ALTER TABLE public.oura_activity_daily_summary OWNER TO postgres;

CREATE SEQUENCE public.oura_activity_daily_summary_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
	
ALTER TABLE public.oura_activity_daily_summary_id_seq OWNER TO postgres;

ALTER SEQUENCE public.oura_activity_daily_summary_id_seq OWNED BY public.oura_activity_daily_summary.id;

--
--OURA ACTIVITY DETAIL
--
CREATE TABLE public.oura_activity_detail(
  id integer NOT NULL,
  oura_activity_id integer,
  timestamp_gmt character varying,
  class_5min integer,
  met_1min real
);

ALTER TABLE public.oura_activity_detail OWNER TO postgres;

CREATE SEQUENCE public.oura_activity_detail_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
	
ALTER TABLE public.oura_activity_detail_id_seq OWNER TO postgres;

ALTER SEQUENCE public.oura_activity_detail_id_seq OWNED BY public.oura_activity_detail.id;
  
--
--OURA SLEEP DETAIL
--
CREATE TABLE public.oura_sleep_detail(
  id integer NOT NULL,
  oura_sleep_id integer,
  timestamp_gmt character varying,
  hypnogram_5min integer,
  hr_5min integer,
  rmssd_5min integer
);

ALTER TABLE public.oura_sleep_detail OWNER TO postgres;

CREATE SEQUENCE public.oura_sleep_detail_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
	
ALTER TABLE public.oura_sleep_detail_id_seq OWNER TO postgres;

ALTER SEQUENCE public.oura_sleep_detail_id_seq OWNED BY public.oura_sleep_detail.id;

--
--STRAVA ACTIVITY SUMMARY
---
CREATE TABLE public.strava_activity_summary(
  id integer NOT NULL,
  athlete_id    integer,
  strava_athlete_id    bigint,
  name  character varying, 
  distance    real,
  moving_time  integer,  
  elapsed_time    integer,
  total_elevation_gain    real,
  type    character varying,
  workout_type    integer,
  strava_activity_id    bigint,
  external_id    character varying,
  upload_id    bigint,
  start_date    character varying,
  start_date_local    character varying,
  timezone    character varying,
  utc_offset   integer,
  start_latitude    numeric,
  start_longitude   numeric,
  end_latitude    numeric,
  end_longitude    numeric,
  location_city    character varying,
  location_state    character varying,
  location_country    character varying,
  map  character varying,
  summary_polyline    character varying,   
  trainer    boolean,
  commute    boolean,
  manual    boolean,
  gear_id    character varying,
  average_speed  real,  
  max_speed    real,
  average_cadence    real,
  average_temp    real,
  average_watts    real,
  weighted_average_watts    real,
  kilojoules    real,
  device_watts    boolean,
  average_heartrate   real,
  max_heartrate    real,
  max_watts    real,
  elev_high    real,
  elev_low    real,
  suffer_score   real
);

ALTER TABLE public.strava_activity_summary OWNER TO postgres;

CREATE SEQUENCE public.strava_activity_summary_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
	
ALTER TABLE public.strava_activity_summary_id_seq OWNER TO postgres;

ALTER SEQUENCE public.strava_activity_summary_id_seq OWNED BY public.strava_activity_summary.id;

--
--STRAVA ACTIVITY STREAMS
--
CREATE TABLE public.strava_activity_streams(
  id integer NOT NULL,
  activity_id    integer,
  time_gmt    character varying,
  distance    real,
  latitude    numeric,
  longitude    numeric,
  altitude    real,
  velocity_smooth    real,
  heartrate    integer,
  cadence    integer,
  watts    integer,
  temp    integer,
  moving    boolean,
  grade_smooth    real
);

ALTER TABLE public.strava_activity_streams OWNER TO postgres;

CREATE SEQUENCE public.strava_activity_streams_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
	
ALTER TABLE public.strava_activity_streams_id_seq OWNER TO postgres;

ALTER SEQUENCE public.strava_activity_streams_id_seq OWNED BY public.strava_activity_streams.id;



--
--AUTO INCREMENTS
--
ALTER TABLE ONLY public.athlete ALTER COLUMN id SET DEFAULT nextval('public.athlete_id_seq'::regclass);

ALTER TABLE ONLY public.diasend_cgm ALTER COLUMN id SET DEFAULT nextval('public.diasend_cgm_id_seq'::regclass);

ALTER TABLE ONLY public.files ALTER COLUMN id SET DEFAULT nextval('public.files_id_seq'::regclass);

ALTER TABLE ONLY public.garmin_connect_body_composition ALTER COLUMN id SET DEFAULT nextval('public.garmin_connect_body_composition_id_seq'::regclass);

ALTER TABLE ONLY public.garmin_connect_daily_summary ALTER COLUMN id SET DEFAULT nextval('public.garmin_connect_daily_summary_id_seq'::regclass);

ALTER TABLE ONLY public.garmin_connect_hrv_tracking ALTER COLUMN id SET DEFAULT nextval('public.garmin_connect_hrv_tracking_id_seq'::regclass);

ALTER TABLE ONLY public.garmin_connect_original_lap ALTER COLUMN id SET DEFAULT nextval('public.garmin_connect_original_lap_id_seq'::regclass);

ALTER TABLE ONLY public.garmin_connect_original_record ALTER COLUMN id SET DEFAULT nextval('public.garmin_connect_original_id_seq'::regclass);

ALTER TABLE ONLY public.garmin_connect_wellness ALTER COLUMN id SET DEFAULT nextval('public.garmin_connect_wellness_id_seq'::regclass);

ALTER TABLE ONLY public.gc_original_wellness_act_type_summary ALTER COLUMN id SET DEFAULT nextval('public.gc_original_wellness_act_type_summary_id_seq'::regclass);

ALTER TABLE ONLY public.gc_original_wellness_activity_tracking ALTER COLUMN id SET DEFAULT nextval('public.gc_original_wellness_activity_tracking_id_seq'::regclass);

ALTER TABLE ONLY public.gc_original_wellness_hr_tracking ALTER COLUMN id SET DEFAULT nextval('public.gc_original_wellness_hr_tracking_id_seq'::regclass);

ALTER TABLE ONLY public.gc_original_wellness_stress_tracking ALTER COLUMN id SET DEFAULT nextval('public.gc_original_wellness_stress_tracking_id_seq'::regclass);

ALTER TABLE ONLY public.mfp_nutrition ALTER COLUMN id SET DEFAULT nextval('public.mfp_nutrition_id_seq'::regclass);

ALTER TABLE ONLY public.mind_monitor_eeg ALTER COLUMN id SET DEFAULT nextval('public.mind_monitor_eeg_id_seq'::regclass);

ALTER TABLE ONLY public.timezones ALTER COLUMN id SET DEFAULT nextval('public.timezones_id_seq'::regclass);

ALTER TABLE ONLY public.gmt_local_time_difference ALTER COLUMN id SET DEFAULT nextval('public.gmt_local_time_difference_id_seq'::regclass);

ALTER TABLE ONLY public.gc_original_wellness_sleep_tracking ALTER COLUMN id SET DEFAULT nextval('public.gc_original_wellness_sleep_tracking_id_seq'::regclass);

ALTER TABLE ONLY public.weather ALTER COLUMN id SET DEFAULT nextval('public.weather_id_seq'::regclass);

ALTER TABLE ONLY public.oura_readiness_daily_summary ALTER COLUMN id SET DEFAULT nextval('public.oura_readiness_daily_summary_id_seq'::regclass);

ALTER TABLE ONLY public.oura_sleep_daily_summary ALTER COLUMN id SET DEFAULT nextval('public.oura_sleep_daily_summary_id_seq'::regclass);

ALTER TABLE ONLY public.oura_activity_daily_summary ALTER COLUMN id SET DEFAULT nextval('public.oura_activity_daily_summary_id_seq'::regclass);

ALTER TABLE ONLY public.oura_activity_detail ALTER COLUMN id SET DEFAULT nextval('public.oura_activity_detail_id_seq'::regclass);

ALTER TABLE ONLY public.oura_sleep_detail ALTER COLUMN id SET DEFAULT nextval('public.oura_sleep_detail_id_seq'::regclass);

ALTER TABLE ONLY public.strava_activity_summary ALTER COLUMN id SET DEFAULT nextval('public.strava_activity_summary_id_seq'::regclass);

ALTER TABLE ONLY public.strava_activity_streams ALTER COLUMN id SET DEFAULT nextval('public.strava_activity_streams_id_seq'::regclass);


--
--PRIMARY KEYS
---
ALTER TABLE ONLY public.athlete
    ADD CONSTRAINT athlete_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.diasend_cgm
    ADD CONSTRAINT diasent_cgm_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.files
    ADD CONSTRAINT files_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.garmin_connect_body_composition
    ADD CONSTRAINT garmin_connect_body_composition_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.garmin_connect_daily_summary
    ADD CONSTRAINT garmin_connect_daily_summary_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.garmin_connect_hrv_tracking
    ADD CONSTRAINT garmin_connect_hrv_tracking_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.garmin_connect_original_lap
    ADD CONSTRAINT garmin_connect_original_lap_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.garmin_connect_original_record
    ADD CONSTRAINT garmin_connect_original_record_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.garmin_connect_original_session
    ADD CONSTRAINT garmin_connect_original_session_pkey PRIMARY KEY (gc_activity_id);

ALTER TABLE ONLY public.garmin_connect_wellness
    ADD CONSTRAINT garmin_connect_wellness_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.gc_original_wellness_act_type_summary
    ADD CONSTRAINT gc_original_wellness_act_type_summary_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.gc_original_wellness_activity_tracking
    ADD CONSTRAINT gc_original_wellness_activity_tracking_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.gc_original_wellness_hr_tracking
    ADD CONSTRAINT gc_original_wellness_hr_tracking_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.gc_original_wellness_stress_tracking
    ADD CONSTRAINT gc_original_wellness_stress_tracking_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.mfp_nutrition
    ADD CONSTRAINT mfp_nutrition_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.mind_monitor_eeg
    ADD CONSTRAINT mind_monitor_eeg_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.timezones
    ADD CONSTRAINT timezones_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.gmt_local_time_difference
    ADD CONSTRAINT gmt_local_time_difference_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.gc_original_wellness_sleep_tracking
    ADD CONSTRAINT gc_original_wellness_sleep_tracking_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.weather
    ADD CONSTRAINT weather_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.oura_readiness_daily_summary
    ADD CONSTRAINT oura_readiness_daily_summary_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.oura_sleep_daily_summary
    ADD CONSTRAINT oura_sleep_daily_summary_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.oura_activity_daily_summary
    ADD CONSTRAINT oura_activity_daily_summary_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.oura_activity_detail
    ADD CONSTRAINT oura_activity_detail_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.oura_sleep_detail
    ADD CONSTRAINT oura_sleep_detail_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.strava_activity_summary
    ADD CONSTRAINT strava_activity_summary_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.strava_activity_streams
    ADD CONSTRAINT strava_activity_streams_pkey PRIMARY KEY (id);

--
--UNIQUES
--
ALTER TABLE ONLY public.files
    ADD CONSTRAINT unique_data_file_path UNIQUE (data_file_path);

ALTER TABLE ONLY public.diasend_cgm
    ADD CONSTRAINT unique_diasend_cgm UNIQUE (athlete_id, "timestamp", data_source);

ALTER TABLE ONLY public.gc_original_wellness_act_type_summary
    ADD CONSTRAINT unique_gc_original_wellness_act_type_summary UNIQUE (athlete_id, activity_type, "timestamp");

ALTER TABLE ONLY public.gc_original_wellness_activity_tracking
    ADD CONSTRAINT unique_gc_original_wellness_activity_tracking UNIQUE (athlete_id, "timestamp");

ALTER TABLE ONLY public.gc_original_wellness_hr_tracking
    ADD CONSTRAINT unique_gc_original_wellness_hr_tracking UNIQUE (athlete_id, "timestamp");

ALTER TABLE ONLY public.gc_original_wellness_stress_tracking
    ADD CONSTRAINT unique_gc_original_wellness_stress_tracking UNIQUE (athlete_id, "timestamp");

ALTER TABLE ONLY public.garmin_connect_original_lap
    ADD CONSTRAINT "unique_original_lap_timestamp-gc_activity_id" UNIQUE (gc_activity_id, "timestamp");

ALTER TABLE ONLY public.garmin_connect_original_record
    ADD CONSTRAINT "unique_original_record_timestamp-lap_id" UNIQUE ("timestamp", lap_id);

ALTER TABLE ONLY public.garmin_connect_wellness
    ADD CONSTRAINT unique_wellness_calendar_date UNIQUE (calendar_date);

ALTER TABLE ONLY public.garmin_connect_body_composition
    ADD CONSTRAINT unique_bodycomposition_athlete_id_timestamp UNIQUE (athlete_id, timestamp);

ALTER TABLE ONLY public.garmin_connect_daily_summary
    ADD CONSTRAINT unique_daily_summary_athlete_id_start_gmt UNIQUE (athlete_id, start_gmt);

ALTER TABLE ONLY public.mind_monitor_eeg
    ADD CONSTRAINT unique_mind_monitor_eeg UNIQUE ("timestamp", athlete_id);

ALTER TABLE ONLY public.timezones
    ADD CONSTRAINT unique_timezones UNIQUE (gc_activity_id, timestamp_gmt);

ALTER TABLE ONLY public.gmt_local_time_difference
    ADD CONSTRAINT unique_gmt_local_time_difference_local_date UNIQUE (local_date);

ALTER TABLE ONLY public.gc_original_wellness_sleep_tracking
    ADD CONSTRAINT unique_gc_original_wellness_sleep_timestamp_gmt UNIQUE (timestamp_gmt);

ALTER TABLE ONLY public.weather
    ADD CONSTRAINT unique_weather_athlete_id_timestamp_gmt UNIQUE (athlete_id, timestamp_gmt);

ALTER TABLE ONLY public.oura_readiness_daily_summary	
	ADD CONSTRAINT unique_oura_readiness_daily_summary UNIQUE (summary_date,period_id);

ALTER TABLE ONLY public.oura_sleep_daily_summary	
	ADD CONSTRAINT unique_oura_sleep_daily_summary UNIQUE (summary_date,period_id);

ALTER TABLE ONLY public.oura_activity_daily_summary	
	ADD CONSTRAINT unique_oura_activity_daily_summary UNIQUE (summary_date);

ALTER TABLE ONLY public.oura_activity_detail	
	ADD CONSTRAINT unique_oura_activity_detail UNIQUE (timestamp_gmt);

ALTER TABLE ONLY public.oura_sleep_detail	
	ADD CONSTRAINT unique_oura_sleep_detail UNIQUE (timestamp_gmt);

ALTER TABLE ONLY public.strava_activity_summary	
	ADD CONSTRAINT unique_strava_activity_summary UNIQUE (start_date);

ALTER TABLE ONLY public.strava_activity_streams	
	ADD CONSTRAINT unique_strava_activity_streams UNIQUE (time_gmt);

--
--INDEXES
--
CREATE INDEX fki_fk_bodycomposition_athlete_id ON public.garmin_connect_body_composition USING btree (athlete_id);

CREATE INDEX fki_fk_daily_summary_athlete_id ON public.garmin_connect_daily_summary USING btree (athlete_id);

CREATE INDEX fki_fk_files_athlete_id ON public.files USING btree (athlete_id);

CREATE INDEX fki_fk_original_gc_activity_id ON public.garmin_connect_original_record USING btree (gc_activity_id);

CREATE INDEX fki_fk_original_lap_gc_activity_id ON public.garmin_connect_original_lap USING btree (gc_activity_id);

CREATE INDEX fki_fk_original_record_lap_id ON public.garmin_connect_original_record USING btree (lap_id);

CREATE INDEX fki_fk_original_session_athleyte_id ON public.garmin_connect_original_session USING btree (athlete_id);

CREATE INDEX fki_fk_wellness__athlete_id ON public.garmin_connect_wellness USING btree (athlete_id);

CREATE INDEX pki_original_lap_id ON public.garmin_connect_original_lap USING btree (id);

CREATE INDEX fki_gc_original_activity_tracking_id_timestamp ON public.gc_original_wellness_activity_tracking USING btree ("timestamp" COLLATE pg_catalog."default", id);

CREATE INDEX fki_gc_original_hr_tracking_timestamp_id ON public.gc_original_wellness_hr_tracking USING btree ("timestamp" COLLATE pg_catalog."default", id);

CREATE INDEX fki_gc_original_stress_tracking_id_timestamp ON public.gc_original_wellness_stress_tracking USING btree ("timestamp" COLLATE pg_catalog."default", id);

---
--FOREIGN KEYS
---
ALTER TABLE ONLY public.garmin_connect_body_composition
    ADD CONSTRAINT fk_bodycomposition_athlete_id FOREIGN KEY (athlete_id) REFERENCES public.athlete(id);

ALTER TABLE ONLY public.garmin_connect_daily_summary
    ADD CONSTRAINT fk_daily_summary_athlete_id FOREIGN KEY (athlete_id) REFERENCES public.athlete(id);

ALTER TABLE ONLY public.diasend_cgm
    ADD CONSTRAINT fk_diasend_cgm_athlete_id FOREIGN KEY (athlete_id) REFERENCES public.athlete(id);

ALTER TABLE ONLY public.files
    ADD CONSTRAINT fk_files_athlete_id FOREIGN KEY (athlete_id) REFERENCES public.athlete(id);

ALTER TABLE ONLY public.gc_original_wellness_act_type_summary
    ADD CONSTRAINT fk_gc_original_wellness_act_type_summary_athlete_id FOREIGN KEY (athlete_id) REFERENCES public.athlete(id);

ALTER TABLE ONLY public.gc_original_wellness_activity_tracking
    ADD CONSTRAINT fk_gc_original_wellness_activity_tracking_athlete_id FOREIGN KEY (athlete_id) REFERENCES public.athlete(id);

ALTER TABLE ONLY public.gc_original_wellness_hr_tracking
    ADD CONSTRAINT fk_gc_original_wellness_hr_tracking_athlete_id FOREIGN KEY (athlete_id) REFERENCES public.athlete(id);

ALTER TABLE ONLY public.gc_original_wellness_stress_tracking
    ADD CONSTRAINT fk_gc_original_wellness_stress_tracking_athlete_id FOREIGN KEY (athlete_id) REFERENCES public.athlete(id);

ALTER TABLE ONLY public.garmin_connect_hrv_tracking
    ADD CONSTRAINT fk_hrv_activity_id FOREIGN KEY (gc_activity_id) REFERENCES public.garmin_connect_original_session(gc_activity_id);

ALTER TABLE ONLY public.mfp_nutrition
    ADD CONSTRAINT fk_mfp_nutrition_athlete_id FOREIGN KEY (athlete_id) REFERENCES public.athlete(id);

ALTER TABLE ONLY public.mind_monitor_eeg
    ADD CONSTRAINT fk_mind_monitor_eeg_athlete_id FOREIGN KEY (athlete_id) REFERENCES public.athlete(id);

ALTER TABLE ONLY public.garmin_connect_original_lap
    ADD CONSTRAINT fk_original_lap_gc_activity_id FOREIGN KEY (gc_activity_id) REFERENCES public.garmin_connect_original_session(gc_activity_id);

ALTER TABLE ONLY public.garmin_connect_original_record
    ADD CONSTRAINT fk_original_record_lap_id FOREIGN KEY (lap_id) REFERENCES public.garmin_connect_original_lap(id);

ALTER TABLE ONLY public.garmin_connect_original_session
    ADD CONSTRAINT fk_original_session_athlete_id FOREIGN KEY (athlete_id) REFERENCES public.athlete(id);

ALTER TABLE ONLY public.garmin_connect_wellness
    ADD CONSTRAINT fk_wellness_athlete_id FOREIGN KEY (athlete_id) REFERENCES public.athlete(id);

ALTER TABLE ONLY public.timezones
    ADD CONSTRAINT fk_timezones_activity_id FOREIGN KEY (gc_activity_id) REFERENCES public.garmin_connect_original_session (gc_activity_id);

ALTER TABLE ONLY public.gmt_local_time_difference
    ADD CONSTRAINT fk_gmt_local_time_difference_athlete_id FOREIGN KEY (athlete_id) REFERENCES public.athlete(id);

ALTER TABLE ONLY public.gc_original_wellness_sleep_tracking
    ADD CONSTRAINT fk_gc_original_wellness_sleep_act_track FOREIGN KEY (activity_tracking_id) REFERENCES public.gc_original_wellness_activity_tracking (id);

ALTER TABLE ONLY public.gc_original_wellness_sleep_tracking
    ADD CONSTRAINT fk_gc_original_wellness_sleep_hr_track FOREIGN KEY (hr_tracking_id) REFERENCES public.gc_original_wellness_hr_tracking (id);

ALTER TABLE ONLY public.gc_original_wellness_sleep_tracking
    ADD CONSTRAINT fk_gc_original_wellness_sleep_stress_track FOREIGN KEY (stress_tracking_id) REFERENCES public.gc_original_wellness_stress_tracking (id);

ALTER TABLE ONLY public.weather
    ADD CONSTRAINT fk_weather_athlete_id FOREIGN KEY (athlete_id) REFERENCES public.athlete (id);

ALTER TABLE ONLY public.oura_readiness_daily_summary
    ADD CONSTRAINT fk_oura_readiness_daily_summary_athlete_id FOREIGN KEY (athlete_id) REFERENCES public.athlete(id);

ALTER TABLE ONLY public.oura_sleep_daily_summary
    ADD CONSTRAINT fk_oura_sleep_daily_summary_athlete_id FOREIGN KEY (athlete_id) REFERENCES public.athlete(id);

ALTER TABLE ONLY public.oura_activity_daily_summary
    ADD CONSTRAINT fk_oura_activity_daily_summary_athlete_id FOREIGN KEY (athlete_id) REFERENCES public.athlete(id);

ALTER TABLE ONLY public.oura_activity_detail
    ADD CONSTRAINT fk_oura_activity_detail_activity_summary_id FOREIGN KEY (oura_activity_id) REFERENCES public.oura_activity_daily_summary(id);

ALTER TABLE ONLY public.oura_sleep_detail
    ADD CONSTRAINT fk_oura_sleep_detail_sleep_summary_id FOREIGN KEY (oura_sleep_id) REFERENCES public.oura_sleep_daily_summary(id);

ALTER TABLE ONLY public.strava_activity_summary
    ADD CONSTRAINT fk_strava_activity_summary_athlete_id FOREIGN KEY (athlete_id) REFERENCES public.athlete(id);

ALTER TABLE ONLY public.strava_activity_streams
    ADD CONSTRAINT fk_strava_activity_streams_strava_activity_id FOREIGN KEY (activity_id) REFERENCES public.strava_activity_summary(id);

