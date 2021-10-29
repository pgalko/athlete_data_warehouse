
--
-- CREATE CONSOLIDATED 1MIN INTERVALS DATA VIEW 
--
CREATE OR REPLACE VIEW public.view_consolidated_data_streams AS
    SELECT DISTINCT athlete.id AS athlete_id,
        time_interval_min.timestamp_gmt,
        gmt_local_time_difference.gmt_local_difference as utc_offset,
        -- Garmin Connect Activity
        garmin_connect_original_record.heart_rate as gc_actvt_hr,
        garmin_connect_original_record.enhanced_speed as gc_actvt_speed,
        garmin_connect_original_record.distance as gc_actvt_distance,
        garmin_connect_original_record.enhanced_altitude as gc_actvt_altitude,
        garmin_connect_original_record.cadence as gc_actvt_cadence,
        garmin_connect_original_record.power as gc_actvt_power,
        garmin_connect_original_record.temperature as gc_actvt_temperature,
		-- Strava Activity
		strava_activity_streams.heartrate as strava_actvt_hr,
        strava_activity_streams.velocity_smooth as strava_actvt_speed,
        strava_activity_streams.distance as strava_actvt_distance,
        strava_activity_streams.altitude as strava_actvt_altitude,
        strava_activity_streams.cadence as strava_actvt_cadence,
        strava_activity_streams.watts as strava_actvt_power,
        strava_activity_streams.temp as strava_actvt_temperature,
		strava_activity_streams.grade_smooth as strava_actv_grade,
        -- Garmin Connect Wellness
        gc_original_wellness_activity_tracking.activity_type as gc_well_actvt_type,
        gc_original_wellness_activity_tracking.intensity as gc_well_intensity,
        gc_original_wellness_hr_tracking.heart_rate as gc_well_hr,
        gc_original_wellness_stress_tracking.stress_level_value as gc_well_stress,
        CASE
            WHEN gc_original_wellness_sleep_tracking.timestamp_gmt IS NOT NULL THEN True
            ELSE False
        END AS gc_well_sleeping,
        -- Oura
        oura_activity_detail.met_1min as oura_act_met,
        oura_activity_detail.class_5min as oura_act_intensity,
        oura_sleep_detail.hypnogram_5min as oura_hypnogram,
        oura_sleep_detail.hr_5min as oura_sleep_hr,
        oura_sleep_detail.rmssd_5min as oura_rmssd,
        -- MyFitnessPall
        STRING_AGG(mfp_nutrition.food_item,',') as nutr_food_items,
        SUM(mfp_nutrition.calories) as nutr_calories,
        SUM(mfp_nutrition.protein) as nutr_protein,
        SUM(mfp_nutrition.carbohydrates) as nutr_carbs,
        SUM(mfp_nutrition.fat) as nutr_fat,
        SUM(mfp_nutrition.fiber) as nutr_fiber,
        SUM(mfp_nutrition.sodium) as nutr_sodium,
        -- Glimp, FreestyleLibre
        diasend_cgm.glucose_nmol_l as glu_glucose,
        diasend_cgm.glucose_nmol_l_15min_avrg as glu_glucose_15m_avrg,
        diasend_cgm.ketone_nmol_l as glu_ketones,
        --EEG
        to_char((((mind_monitor_eeg.alpha_tp9+mind_monitor_eeg.alpha_af7+mind_monitor_eeg.alpha_af8+mind_monitor_eeg.alpha_tp10)/4)+1)*50,'FM999.00')::real as eeg_avg_alpha,
        to_char((((mind_monitor_eeg.beta_tp9+mind_monitor_eeg.beta_af7+mind_monitor_eeg.beta_af8+mind_monitor_eeg.beta_tp10)/4)+1)*50,'FM999.00')::real as eeg_avg_beta,
        to_char((((mind_monitor_eeg.gamma_tp9+mind_monitor_eeg.gamma_af7+mind_monitor_eeg.gamma_af8+mind_monitor_eeg.gamma_tp10)/4)+1)*50,'FM999.00')::real eeg_avg_gamma,
        to_char((((mind_monitor_eeg.delta_tp9+mind_monitor_eeg.delta_af7+mind_monitor_eeg.delta_af8+mind_monitor_eeg.delta_tp10)/4)+1)*50,'FM999.00')::real as eeg_avg_delta,
        -- Weather
        weather.temperature as wthr_temp,
        weather.dew_point as wthr_dew_point,
        weather.relative_humidity as wthr_humidity,
        weather.precipitation as wthr_precip,
        weather.snow as wthr_snow,
        weather.wind_direction as wthr_wind_dir,
        weather.wind_speed as wthr_wind_speed,
        weather.wind_gust as wthr_wind_gust,
        weather.sea_air_pressure as wthr_air_press,
        weather.total_sunshine as wthr_tot_sunsh,
        weather.condition_code as wthr_cond_code	
    FROM public.athlete
        --Timestamps
        LEFT JOIN public.time_interval_min ON time_interval_min.athlete_id = athlete.id
        LEFT JOIN public.gmt_local_time_difference ON gmt_local_time_difference.local_date::text = left(time_interval_min.timestamp_gmt,-9)
        --Garmin Connect Wellness
        LEFT JOIN public.gc_original_wellness_activity_tracking ON gc_original_wellness_activity_tracking.timestamp = time_interval_min.timestamp_gmt
        LEFT JOIN public.gc_original_wellness_hr_tracking ON gc_original_wellness_hr_tracking.timestamp = time_interval_min.timestamp_gmt
        LEFT JOIN public.gc_original_wellness_stress_tracking ON gc_original_wellness_stress_tracking.timestamp = time_interval_min.timestamp_gmt
        LEFT JOIN public.gc_original_wellness_sleep_tracking ON gc_original_wellness_sleep_tracking.timestamp_gmt = time_interval_min.timestamp_gmt
        --Garmin Connect Activity
        LEFT JOIN public.garmin_connect_original_record ON garmin_connect_original_record.timestamp = time_interval_min.timestamp_gmt
		--Strava Activity
        LEFT JOIN public.strava_activity_streams ON strava_activity_streams.time_gmt = time_interval_min.timestamp_gmt
        -- Oura
        LEFT JOIN public.oura_activity_detail ON oura_activity_detail.timestamp_gmt = time_interval_min.timestamp_gmt 
        LEFT JOIN public.oura_sleep_detail ON CONCAT(left(oura_sleep_detail.timestamp_gmt, -2), '00') = time_interval_min.timestamp_gmt
        -- Nutrition
        -- This is based on MFP defaults (breakfast,lunch,dinner etc) or customised meal labeling (eg '6am-9am','9am-12pm','12pm-3pm'etc). 
        -- Can be customised in MFP settings and they allow up to 6 meal labels per day.
        LEFT JOIN public.mfp_nutrition ON CASE 
            WHEN meal = '6am-9am' THEN CONCAT(date::text,' 07:30:00')
            WHEN meal = 'Breakfast' THEN CONCAT(date::text,' 07:30:00')
            WHEN meal = '9am-12pm' THEN CONCAT(date::text,' 10:30:00')
            WHEN meal = '12pm-3pm' THEN CONCAT(date::text,' 13:30:00')
            WHEN meal = 'Lunch' THEN CONCAT(date::text,' 12:30:00')
            WHEN meal = '3pm-6pm' THEN  CONCAT(date::text,' 16:30:00')
            WHEN meal = 'Snack' THEN CONCAT(date::text,' 15:30:00')
            WHEN meal = '6pm-9pm' THEN  CONCAT(date::text,' 19:30:00')
            WHEN meal = 'Dinner' THEN CONCAT(date::text,' 19:30:00')
            WHEN meal = '9pm-12am' THEN CONCAT(date::text,' 22:30:00')
        -- Convert GMT timestamp to local
        END = (time_interval_min.timestamp_gmt::timestamp + gmt_local_time_difference.gmt_local_difference)::text
        -- Glimp, FreestyleLibre
        LEFT JOIN public.diasend_cgm ON concat(left(diasend_cgm.timestamp_gmt, -2), '00') = time_interval_min.timestamp_gmt
        -- EEG
        LEFT JOIN public.mind_monitor_eeg ON left(mind_monitor_eeg.timestamp_gmt, -7) = time_interval_min.timestamp_gmt
        -- Weather
        LEFT JOIN public.weather ON weather.timestamp_gmt = time_interval_min.timestamp_gmt
	--WHERE time_interval_min.timestamp_gmt::timestamp > '2021-10-01 00:00:00'::timestamp
    GROUP BY athlete.id,time_interval_min.timestamp_gmt,gmt_local_time_difference.gmt_local_difference,gc_original_wellness_activity_tracking.activity_type,gc_original_wellness_activity_tracking.intensity,
            gc_original_wellness_hr_tracking.heart_rate,gc_original_wellness_stress_tracking.stress_level_value,oura_activity_detail.met_1min,
            oura_activity_detail.class_5min,oura_sleep_detail.hypnogram_5min,oura_sleep_detail.hr_5min,oura_sleep_detail.rmssd_5min,
            gc_original_wellness_sleep_tracking.timestamp_gmt,diasend_cgm.glucose_nmol_l,diasend_cgm.glucose_nmol_l_15min_avrg,diasend_cgm.glucose_nmol_l_15min_avrg,
            diasend_cgm.ketone_nmol_l,	weather.temperature,weather.dew_point,weather.relative_humidity,weather.precipitation,weather.snow,weather.wind_direction,
            weather.wind_speed,weather.wind_gust,weather.sea_air_pressure,weather.total_sunshine,weather.condition_code,garmin_connect_original_record.heart_rate,
            garmin_connect_original_record.enhanced_speed,garmin_connect_original_record.distance,garmin_connect_original_record.enhanced_altitude,garmin_connect_original_record.cadence,
            garmin_connect_original_record.power,garmin_connect_original_record.temperature,mind_monitor_eeg.alpha_tp9,mind_monitor_eeg.alpha_af7,mind_monitor_eeg.alpha_af8,
            mind_monitor_eeg.alpha_tp10,mind_monitor_eeg.beta_tp9,mind_monitor_eeg.beta_af7,mind_monitor_eeg.beta_af8,mind_monitor_eeg.beta_tp10,mind_monitor_eeg.gamma_tp9,
            mind_monitor_eeg.gamma_af7,mind_monitor_eeg.gamma_af8,mind_monitor_eeg.gamma_tp10,mind_monitor_eeg.delta_tp9,mind_monitor_eeg.delta_af7,mind_monitor_eeg.delta_af8,
            mind_monitor_eeg.delta_tp10,strava_activity_streams.heartrate,strava_activity_streams.velocity_smooth,strava_activity_streams.distance,strava_activity_streams.altitude,strava_activity_streams.cadence,
			strava_activity_streams.watts,strava_activity_streams.temp,strava_activity_streams.grade_smooth
    ORDER BY time_interval_min.timestamp_gmt DESC --LIMIT 525600 ; -- 1 years of data at 1 min intervals
