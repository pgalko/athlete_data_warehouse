--
-- CREATE CONSOLIDATED 1DAY SUMMARY DATA VIEW 
--
CREATE OR REPLACE VIEW public.view_consolidated_data_summary AS
    SELECT DISTINCT athlete.id AS athlete_id,
            --Timestamps
            gmt_local_time_difference.local_date,
            --
            --ACTIVITY
            --
            -- Garmin Connect Activity (comment out if using Strava)
            SUM(DISTINCT garmin_connect_original_session.total_elapsed_time) as gc_actvt_elapsed_time,
            SUM(DISTINCT garmin_connect_original_session.total_distance) as gc_actvt_distance,
            SUM(DISTINCT garmin_connect_original_session.total_ascent)::int as gc_actvt_total_ascent,
            AVG(DISTINCT garmin_connect_original_session.avg_heart_rate)::int as gc_actvt_avg_hr,
            MAX(DISTINCT garmin_connect_original_session.max_heart_rate)::int as gc_actvt_max_hr,
            SUM(DISTINCT garmin_connect_original_session.total_calories)::int as gc_actvt_total_calories,
            ROUND(AVG(DISTINCT garmin_connect_original_session.hrv_rmssd),5) as gc_actvt_hrv_rmssd,
            ROUND(AVG(DISTINCT garmin_connect_original_session.hrv_sdrr),5) as gc_actvt_hrv_sdrr,
            ROUND(AVG(DISTINCT garmin_connect_original_session.hrv_pnn50),5) as gc_actvt_hrv_pnn50,
            ROUND(AVG(DISTINCT garmin_connect_original_session.hrv_pnn20),5) as gc_actvt_hrv_pnn20,
            -- Strava Activity (comment out if using Garmin Conect)
            aggr_strava_activity_summary.strava_actvt_elapsed_time,
            aggr_strava_activity_summary.strava_actvt_distance,
            aggr_strava_activity_summary.strava_actvt_elevation_gain,
            aggr_strava_activity_summary.strava_actvt_avg_temp,
            aggr_strava_activity_summary.strava_actvt_avg_heartrate,
            aggr_strava_activity_summary.strava_actvt_max_heartrate,
            aggr_strava_activity_summary.strava_actvt_elev_high,
            aggr_strava_activity_summary.strava_actvt_suffer_score,
            --ROUND(aggr_strava_activity_summary.strava_actvt_atl,2) as strava_actvt_atl,
            --ROUND(aggr_strava_activity_summary.strava_actvt_ctl,2) as strava_actvt_ctl,
            --ROUND(aggr_strava_activity_summary.strava_actvt_ctl,2) - ROUND(aggr_strava_activity_summary.strava_actvt_atl,2) as strava_actvt_tsb,
            
            -- Oura Activity
            oura_activity_daily_summary.score as oura_actvt_score,
            oura_activity_daily_summary.score_stay_active as oura_actvt_score_stay_active,
            oura_activity_daily_summary.score_move_every_hour as oura_actvt_score_move_every_hour,
            oura_activity_daily_summary.score_training_frequency as oura_actvt_score_training_frequency,
            oura_activity_daily_summary.score_training_volume as oura_actvt_score_training_volume,
            oura_activity_daily_summary.score_recovery_time as oura_actvt_score_recovery_time,
            oura_activity_daily_summary.daily_movement as oura_actvt_daily_movement,
            oura_activity_daily_summary.rest as oura_actvt_rest,
            oura_activity_daily_summary.inactive as oura_actvt_inactive,
            oura_activity_daily_summary.low as oura_actvt_low,
            oura_activity_daily_summary.medium as oura_actvt_med,
            oura_activity_daily_summary.high as oura_actvt_high,
            oura_activity_daily_summary.steps as oura_actvt_steps,
            oura_activity_daily_summary.cal_active as oura_actvt_cal_active,
            oura_activity_daily_summary.met_min_inactive as oura_actvt_met_min_inactive,
            oura_activity_daily_summary.met_min_low as oura_actvt_met_min_low,
            oura_activity_daily_summary.met_min_medium as oura_actvt_met_min_medium,
            oura_activity_daily_summary.met_min_high as oura_actvt_met_min_high,
            oura_activity_daily_summary.average_met as oura_actvt_average_met,
            --
            --WELLNESS
            --
            --Garmin Connect Wellness
            garmin_connect_wellness.wellness_total_steps as gc_well_total_steps,
            garmin_connect_wellness.wellness_total_distance as gc_well_total_distance,
            garmin_connect_wellness.wellness_floors_ascended as gc_well_floors_ascended,
            garmin_connect_wellness.wellness_floors_descended as gc_well_floors_descended,
            garmin_connect_wellness.wellness_max_heart_rate as gc_well_max_hr,
            garmin_connect_wellness.wellness_min_heart_rate as gc_well_min_hr,
            garmin_connect_wellness.wellness_min_avg_heart_rate as gc_well_min_avg_hr,
            garmin_connect_wellness.wellness_resting_heart_rate as gc_well_resting_hr,
            garmin_connect_wellness.wellness_max_avg_heart_rate as gc_well_max_avg_hr,
            garmin_connect_wellness.wellness_average_stress as gc_well_avg_stress,
            garmin_connect_wellness.wellness_max_stress as gc_well_max_stress,
            garmin_connect_wellness.sleep_duration as gc_well_sleep_duration,
            garmin_connect_wellness.wellness_bodybattery_charged as gc_well_battery_charge,
            garmin_connect_wellness.wellness_body_battery_drained as gc_well_battery_drained,
            garmin_connect_wellness.wellness_moderate_intensity_minutes as gc_well_moderate_intensity_minutes,
            garmin_connect_wellness.wellness_vigorous_intensity_minutes as gc_well_vigorous_intensity_minutes,
            garmin_connect_wellness.wellness_total_calories as gc_well_total_calories,
            garmin_connect_wellness.wellness_bmr_calories as gc_well_bmr_calories,
            garmin_connect_wellness.food_calories_remaining as gc_well_food_calories_remaining,
            garmin_connect_wellness.food_calories_consumed as gc_well_food_calories_consumed,
            garmin_connect_wellness.common_total_calories as gc_well_common_total_calories,
            garmin_connect_wellness.wellness_active_calories as gc_well_active_calories,
            --Garmin Connect Body Composition
            ROUND(AVG(DISTINCT garmin_connect_body_composition.body_water::numeric),2) as gc_bc_body_water,
            AVG(DISTINCT garmin_connect_body_composition.muscle_mass_gm)::int as gc_bc_muscle_mass,
            AVG(DISTINCT garmin_connect_body_composition.weight_gm)::int as gc_bc_weight,
            ROUND(AVG(DISTINCT garmin_connect_body_composition.bmi::numeric),2) as gc_bc_bmi,
            ROUND(AVG(DISTINCT garmin_connect_body_composition.body_fat::numeric),2) as gc_bc_body_fat,
            AVG(DISTINCT garmin_connect_body_composition.bone_mass_gm)::int as gc_bc_bone_mass,
            --Oura Readiness Daily Summary
            oura_readiness_daily_summary.score as oura_readnss_score,
            oura_readiness_daily_summary.score_previous_night as oura_readnss_score_prev_night,
            oura_readiness_daily_summary.score_previous_day as oura_readnss_score_previous_day,
            oura_readiness_daily_summary.score_sleep_balance as oura_readnss_score_sleep_balance,
            oura_readiness_daily_summary.score_activity_balance as oura_readnss_score_activity_balance,
            oura_readiness_daily_summary.score_resting_hr as oura_readnss_score_resting_hr,
            oura_readiness_daily_summary.score_hrv_balance as oura_readnss_score_hrv_ballance,
            oura_readiness_daily_summary.score_recovery_index as oura_readnss_score_recovery_index,
            oura_readiness_daily_summary.score_temperature as oura_readnss_score_temperature,
            --
            -- SLEEP
            --
            -- Oura Sleep Daily Summary
            oura_sleep_daily_summary.bedtime_start::timestamp+gmt_local_time_difference.gmt_local_difference as oura_sleep_bedtime_start,
            oura_sleep_daily_summary.bedtime_end::timestamp+gmt_local_time_difference.gmt_local_difference as oura_sleep_bedtime_end,
            oura_sleep_daily_summary.score as oura_sleep_score,
            oura_sleep_daily_summary.score_total as oura_sleep_score_total,
            oura_sleep_daily_summary.score_disturbances as oura_sleep_score_disturbances,
            oura_sleep_daily_summary.score_efficiency as oura_sleep_score_efficiency,
            oura_sleep_daily_summary.score_latency as oura_sleep_score_latency,
            oura_sleep_daily_summary.score_rem as oura_sleep_score_rem,
            oura_sleep_daily_summary.score_deep as oura_sleep_score_deep,
            oura_sleep_daily_summary.score_alignment as oura_sleep_score_alignment,
            oura_sleep_daily_summary.total as oura_sleep_total_asleep,
            oura_sleep_daily_summary.duration as oura_sleep_total_in_bed,
            oura_sleep_daily_summary.awake as oura_sleep_awake,
            oura_sleep_daily_summary.light as oura_sleep_light,
            oura_sleep_daily_summary.rem as oura_sleep_rem,
            oura_sleep_daily_summary.deep as oura_sleep_deep,
            oura_sleep_daily_summary.onset_latency as oura_sleep_onset_latency,
            oura_sleep_daily_summary.restless as oura_sleep_restless,
            oura_sleep_daily_summary.efficiency as oura_sleep_efficiency,
            oura_sleep_daily_summary.midpoint_time as oura_sleep_midpoint_time,
            oura_sleep_daily_summary.hr_lowest as oura_sleep_hr_lowest,
            oura_sleep_daily_summary.hr_average as oura_sleep_hr_average,
            oura_sleep_daily_summary.rmssd as oura_sleep_rmssd,
            oura_sleep_daily_summary.breath_average as oura_sleep_breath_average,
            oura_sleep_daily_summary.temperature_deviation as oura_sleep_temperature_deviation,
            oura_sleep_daily_summary.temperature_trend_deviation as oura_sleep_temperature_temperature_trend_deviation,
            oura_sleep_daily_summary.bedtime_end_delta as oura_sleep_bedtime_end_delta,
            oura_sleep_daily_summary.bedtime_start_delta as oura_sleep_bedtime_start_delta,
            oura_sleep_daily_summary.midpoint_at_delta as oura_sleep_midpoint_at_delta,
            --
            --NUTRITION
            --
            --MFP Nutrition
            aggr_mfp_nutrition.nutr_food_items,
            aggr_mfp_nutrition.nutr_food_items_count,
            aggr_mfp_nutrition.nutr_daily_calories,
            aggr_mfp_nutrition.nutr_daily_carbs,
            aggr_mfp_nutrition.nutr_daily_protein,
            aggr_mfp_nutrition.nutr_daily_fat,
            aggr_mfp_nutrition.nutr_daily_fiber,
            aggr_mfp_nutrition.nutr_daily_sodium,
            --
            --BG,Ketones
            --
            --Glimp,FreestyleLibre BG, Ketones
            ROUND(aggr_diasend_cgm.bg_1min_avrg::numeric,2) as bg_1min_glu_avrg,
            ROUND(aggr_diasend_cgm.bg_15min_avrg::numeric,2) as bg_15min_glu_avrg,
            ROUND(aggr_diasend_cgm.keto_avrg::numeric,2) as bg_keto_avrg,
            ROUND(aggr_diasend_cgm.bg_15min_stddev::numeric,2) as bg_glu_stddev,
            ROUND((aggr_diasend_cgm.bg_15min_stddev::numeric/aggr_diasend_cgm.bg_15min_avrg::numeric)*100,2) as bg_glu_variability_perc,
            aggr_diasend_cgm.bg_1min_max as bg_glu_1min_max,
            aggr_diasend_cgm.bg_1min_min as bg_glu_1min_min,
            aggr_diasend_cgm.bg_15min_max as bg_glu_15min_max,
            aggr_diasend_cgm.bg_15min_min as bg_glu_15min_min,
            aggr_diasend_cgm.keto_max as bg_keto_max,
            aggr_diasend_cgm.keto_min as bg_keto_min,
            --
            --EEG
            --
            --Mind Monitor
            ROUND(aggr_mind_monitor_eeg.average_alpha::numeric,2) as eeg_average_alpha,
            ROUND(aggr_mind_monitor_eeg.average_beta::numeric,2) as eeg_average_beta,
            ROUND(aggr_mind_monitor_eeg.average_gamma::numeric,2) as eeg_average_gamma,
            ROUND(aggr_mind_monitor_eeg.average_delta::numeric,2) as eeg_average_delta,
            ROUND(aggr_mind_monitor_eeg.average_theta::numeric,2) as eeg_average_theta,
            EXTRACT(EPOCH FROM DATE_TRUNC('second',aggr_mind_monitor_eeg.eeg_duration))::numeric AS eeg_session_duration,
            --
            --WEATHER
            --
            --Meteostat
            aggr_weather.weather_min_temperature as weather_min_temp,
            aggr_weather.weather_max_temperature as weather_max_temp,
            ROUND(aggr_weather.weather_avg_temperature::numeric,1) as weather_avg_temp,
            ROUND(aggr_weather.weather_avg_dew_point::numeric,1) as weather_avg_dew_point,
            ROUND(aggr_weather.weather_avg_humidity::numeric,1) as weather_avg_humidity,
            ROUND(aggr_weather.weather_avg_precipitation::numeric,1) as weather_avg_precipitation,
            ROUND(aggr_weather.weather_avg_snow::numeric,1) as weather_avg_snow,
            ROUND(aggr_weather.weather_avg_wind_direction::numeric,1) as weather_avg_wind_direction,
            ROUND(aggr_weather.weather_avg_wind_speed::numeric,1) as weather_avg_wind_speed,
            ROUND(aggr_weather.weather_avg_wind_gust::numeric,1) as weather_avg_wind_gust,
            ROUND(aggr_weather.weather_avg_air_pressure::numeric,1) as weather_avg_air_pressure,
            ROUND(aggr_weather.weather_stddev_air_pressure::numeric,1) as weather_stddev_air_pressure,
            ROUND(aggr_weather.weather_avg_tot_sunshine::numeric,1) as weather_avg_tot_sunshine
            --
            --CUSTOM (Uncomment-Modify the below section to match your custom tables)
            --
            --HRV4 Training
            --CASE WHEN cstm_hrv4_training.hr = '-' THEN 0 ELSE cstm_hrv4_training.hr::numeric END AS hrv4t_hr,
            --CASE WHEN cstm_hrv4_training.avnn = '-' THEN 0 ELSE cstm_hrv4_training.avnn::numeric END AS hrv4t_avnn,
            --CASE WHEN cstm_hrv4_training.sdnn = '-' THEN 0 ELSE cstm_hrv4_training.sdnn::numeric END AS hrv4t_sdnn,
            --CASE WHEN cstm_hrv4_training.rmssd = '-' THEN 0 ELSE cstm_hrv4_training.rmssd::numeric END AS hrv4t_rmssd,
            --CASE WHEN cstm_hrv4_training.pnn50 = '-' THEN 0 ELSE cstm_hrv4_training.pnn50::numeric END AS hrv4t_pnn50,
            --CASE WHEN cstm_hrv4_training.hrv4t_recovery_points = '-' THEN 0 ELSE cstm_hrv4_training.hrv4t_recovery_points::numeric END AS hrv4t_recovery_points,
            --CASE WHEN cstm_hrv4_training.training_performance = '-' THEN 0 ELSE cstm_hrv4_training.training_performance::numeric END AS hrv4t_training_performance,
            --CASE WHEN cstm_hrv4_training.physical_condition = '-' THEN 0 ELSE cstm_hrv4_training.physical_condition::numeric END AS hrv4t_physical_condition,
            --CASE WHEN cstm_hrv4_training.trainingrpe = '-' THEN 0 ELSE cstm_hrv4_training.trainingrpe::numeric END AS hrv4t_trainingrpe,
            --CASE WHEN cstm_hrv4_training.trainingmotivation = '-' THEN 0 ELSE cstm_hrv4_training.trainingmotivation::numeric END AS hrv4t_training_motivation,
            --CASE WHEN cstm_hrv4_training.sleep_quality = '-' THEN 0 ELSE cstm_hrv4_training.sleep_quality::numeric END AS hrv4t_sleep_quality,
            --CASE WHEN cstm_hrv4_training.mental_energy = '-' THEN 0 ELSE cstm_hrv4_training.mental_energy::numeric END AS hrv4t_mental_energy,
            --CASE WHEN cstm_hrv4_training.muscle_soreness = '-' THEN 0 ELSE cstm_hrv4_training.muscle_soreness::numeric END AS hrv4t_muscle_soreness,
            --CASE WHEN cstm_hrv4_training.fatigue = '-' THEN 0 ELSE cstm_hrv4_training.fatigue::numeric END AS hrv4t_fatigue,
            --cstm_hrv4_training.traveling AS hrv4t_traveling,
            --cstm_hrv4_training.sickness AS hrv4t_sickness,
            --cstm_hrv4_training.alcohol AS hrv4t_alcohol,
            --CASE WHEN cstm_hrv4_training.current_lifestyle = ' -' THEN 0 ELSE cstm_hrv4_training.current_lifestyle::numeric END AS hrv4t_current_lifestyle,
            --cstm_hrv4_training.vo2max::numeric AS hrv4t_vo2max
			                                 
    FROM public.athlete
            --Timestamps
            LEFT JOIN public.gmt_local_time_difference ON gmt_local_time_difference.athlete_id = athlete.id
            --Garmin Connect Activity
            LEFT JOIN public.garmin_connect_original_session ON (garmin_connect_original_session.timestamp::timestamp+gmt_local_time_difference.gmt_local_difference)::date = gmt_local_time_difference.local_date
            --Strava Activity
            LEFT JOIN
                (SELECT start_date_local::date,
                    SUM(strava_activity_summary.elapsed_time) as strava_actvt_elapsed_time,
                    SUM(strava_activity_summary.distance) as strava_actvt_distance,
                    SUM(strava_activity_summary.total_elevation_gain) as strava_actvt_elevation_gain,
                    AVG(strava_activity_summary.average_temp)::int as strava_actvt_avg_temp,
                    AVG(strava_activity_summary.average_heartrate)::int as strava_actvt_avg_heartrate,
                    MAX(strava_activity_summary.max_heartrate) as strava_actvt_max_heartrate,
                    MAX(strava_activity_summary.elev_high) as strava_actvt_elev_high,
                    SUM(strava_activity_summary.suffer_score) as strava_actvt_suffer_score
                    --calculate ATL and CTL using "ema" aggregate and "ema_func" function
                    --ema(SUM(strava_activity_summary.suffer_score::numeric), 0.1428 /* alpha as 1/7 */) over (order by start_date_local::date asc) as strava_actvt_atl,
                    --ema(SUM(strava_activity_summary.suffer_score::numeric), 0.0238 /* alpha as 2/42 */) over (order by start_date_local::date asc) as strava_actvt_ctl
                FROM public.strava_activity_summary GROUP  BY start_date_local::date) aggr_strava_activity_summary  
            ON aggr_strava_activity_summary.start_date_local::date = gmt_local_time_difference.local_date
            --Oura Activity
            LEFT JOIN public.oura_activity_daily_summary ON oura_activity_daily_summary.summary_date::date = gmt_local_time_difference.local_date
            --Garmin Connect Wellness
            LEFT JOIN public.garmin_connect_wellness ON garmin_connect_wellness.calendar_date::date = gmt_local_time_difference.local_date
            --Garmin Connect Body Composition
            LEFT JOIN public.garmin_connect_body_composition ON (garmin_connect_body_composition.timestamp::timestamp+gmt_local_time_difference.gmt_local_difference)::date = gmt_local_time_difference.local_date
            --Oura Readiness Daily Summary
            LEFT JOIN public.oura_readiness_daily_summary ON oura_readiness_daily_summary.summary_date::date = gmt_local_time_difference.local_date
            --Oura Sleep Daily Summary
            LEFT JOIN public.oura_sleep_daily_summary ON oura_sleep_daily_summary.summary_date::date = gmt_local_time_difference.local_date
            -- MFP Nutrition
            LEFT JOIN 
                (SELECT date,
                        STRING_AGG(mfp_nutrition.food_item,',') as nutr_food_items,
                        COUNT(mfp_nutrition.meal) as nutr_food_items_count,
                        SUM(mfp_nutrition.calories) as nutr_daily_calories,
                        SUM(mfp_nutrition.carbohydrates) as nutr_daily_carbs,
                        SUM(mfp_nutrition.protein) as nutr_daily_protein,
                        SUM(mfp_nutrition.fat) as nutr_daily_fat,
                        SUM(mfp_nutrition.fiber) as nutr_daily_fiber,
                        SUM(mfp_nutrition.sodium) as nutr_daily_sodium 
                FROM public.mfp_nutrition GROUP  BY date) aggr_mfp_nutrition  
            ON aggr_mfp_nutrition.date = gmt_local_time_difference.local_date
            --BG,Ketones
            LEFT JOIN 
                (SELECT timestamp::date,
                        AVG(diasend_cgm.glucose_nmol_l) as bg_1min_avrg,
                        AVG(diasend_cgm.glucose_nmol_l_15min_avrg) as bg_15min_avrg,
                        STDDEV(diasend_cgm.glucose_nmol_l_15min_avrg) as bg_15min_stddev,
                        MAX(diasend_cgm.glucose_nmol_l) as bg_1min_max,
                        MIN(diasend_cgm.glucose_nmol_l) as bg_1min_min,
                        MAX(diasend_cgm.glucose_nmol_l_15min_avrg) as bg_15min_max,
                        MIN(diasend_cgm.glucose_nmol_l_15min_avrg) as bg_15min_min,
                        AVG(diasend_cgm.ketone_nmol_l) as keto_avrg,
                        MAX(diasend_cgm.ketone_nmol_l) as keto_max,
                        MIN(diasend_cgm.ketone_nmol_l) as keto_min
                FROM public.diasend_cgm GROUP  BY timestamp::date) aggr_diasend_cgm  
            ON aggr_diasend_cgm.timestamp::date = gmt_local_time_difference.local_date
            --Mind Monitor
            LEFT JOIN 
                (SELECT timestamp::date,
                        AVG((((nullif(mind_monitor_eeg.alpha_tp9,'NaN')+nullif(mind_monitor_eeg.alpha_af7,'NaN')+nullif(mind_monitor_eeg.alpha_af8,'NaN')+nullif(mind_monitor_eeg.alpha_tp10,'NaN'))/4)+1)*50) as average_alpha,
                        AVG((((nullif(mind_monitor_eeg.beta_tp9,'NaN')+nullif(mind_monitor_eeg.beta_af7,'NaN')+nullif(mind_monitor_eeg.beta_af8,'NaN')+nullif(mind_monitor_eeg.beta_tp10,'NaN'))/4)+1)*50) as average_beta,
                        AVG((((nullif(mind_monitor_eeg.gamma_tp9,'NaN')+nullif(mind_monitor_eeg.gamma_af7,'NaN')+nullif(mind_monitor_eeg.gamma_af8,'NaN')+nullif(mind_monitor_eeg.gamma_tp10,'NaN'))/4)+1)*50) as average_gamma,
                        AVG((((nullif(mind_monitor_eeg.delta_tp9,'NaN')+nullif(mind_monitor_eeg.delta_af7,'NaN')+nullif(mind_monitor_eeg.delta_af8,'NaN')+nullif(mind_monitor_eeg.delta_tp10,'NaN'))/4)+1)*50) as average_delta,
                        AVG((((nullif(mind_monitor_eeg.theta_tp9,'NaN')+nullif(mind_monitor_eeg.theta_af7,'NaN')+nullif(mind_monitor_eeg.theta_af8,'NaN')+nullif(mind_monitor_eeg.theta_tp10,'NaN'))/4)+1)*50) as average_theta,
                        MAX(timestamp::timestamp)-MIN(timestamp::timestamp) as eeg_duration
                FROM public.mind_monitor_eeg GROUP  BY timestamp::date) aggr_mind_monitor_eeg  
            ON aggr_mind_monitor_eeg.timestamp::date = gmt_local_time_difference.local_date
            --Meteostat
            LEFT JOIN 
                (SELECT timestamp_gmt::date,
                        MIN(weather.temperature) as weather_min_temperature,
                        MAX(weather.temperature) as weather_max_temperature,
                        AVG(weather.temperature) as weather_avg_temperature,
                        AVG(weather.dew_point) as weather_avg_dew_point,
                        AVG(weather.relative_humidity) as weather_avg_humidity,
                        AVG(weather.precipitation) as weather_avg_precipitation,
                        AVG(nullif(weather.snow,'NaN')) as weather_avg_snow,
                        AVG(weather.wind_direction) as weather_avg_wind_direction,
                        AVG(weather.wind_speed) as weather_avg_wind_speed,
                        AVG(nullif(weather.wind_gust,'NaN')) as weather_avg_wind_gust,
                        AVG(weather.sea_air_pressure) as weather_avg_air_pressure,
                        STDDEV(weather.sea_air_pressure) as weather_stddev_air_pressure,
                        AVG(nullif(weather.total_sunshine,'NaN')) as weather_avg_tot_sunshine      
                FROM public.weather GROUP  BY timestamp_gmt::date) aggr_weather  
            ON aggr_weather.timestamp_gmt::date = gmt_local_time_difference.local_date

        --(Uncomment-Modify the below section to match your custom tables)
        --Custom (hrv4training)
        --LEFT JOIN public.cstm_hrv4_training ON cstm_hrv4_training.date::date = gmt_local_time_difference.local_date
			           
    GROUP BY athlete.id, gmt_local_time_difference.local_date,gmt_local_time_difference.gmt_local_difference,aggr_strava_activity_summary.strava_actvt_elapsed_time,aggr_strava_activity_summary.strava_actvt_distance,
            aggr_strava_activity_summary.strava_actvt_elevation_gain,aggr_strava_activity_summary.strava_actvt_avg_temp,aggr_strava_activity_summary.strava_actvt_avg_heartrate,aggr_strava_activity_summary.strava_actvt_max_heartrate,
            aggr_strava_activity_summary.strava_actvt_elev_high,aggr_strava_activity_summary.strava_actvt_suffer_score,
	    --aggr_strava_activity_summary.strava_actvt_atl,aggr_strava_activity_summary.strava_actvt_ctl,
            oura_activity_daily_summary.score,oura_activity_daily_summary.score_stay_active,oura_activity_daily_summary.score_move_every_hour,
            oura_activity_daily_summary.score_training_frequency,oura_activity_daily_summary.score_training_volume,oura_activity_daily_summary.score_recovery_time,oura_activity_daily_summary.daily_movement,
            oura_activity_daily_summary.rest,oura_activity_daily_summary.inactive,oura_activity_daily_summary.low,oura_activity_daily_summary.medium,oura_activity_daily_summary.high,
            oura_activity_daily_summary.steps,oura_activity_daily_summary.cal_active,oura_activity_daily_summary.met_min_inactive,oura_activity_daily_summary.met_min_low,oura_activity_daily_summary.met_min_medium,
            oura_activity_daily_summary.met_min_high,oura_activity_daily_summary.average_met,garmin_connect_wellness.wellness_total_steps,garmin_connect_wellness.wellness_total_distance,garmin_connect_wellness.wellness_floors_ascended,
            garmin_connect_wellness.wellness_floors_descended,garmin_connect_wellness.wellness_max_heart_rate,garmin_connect_wellness.wellness_min_heart_rate,garmin_connect_wellness.wellness_min_avg_heart_rate,
            garmin_connect_wellness.wellness_average_stress,garmin_connect_wellness.wellness_resting_heart_rate,garmin_connect_wellness.wellness_max_stress,garmin_connect_wellness.sleep_duration,garmin_connect_wellness.wellness_max_avg_heart_rate,
            garmin_connect_wellness.wellness_moderate_intensity_minutes,garmin_connect_wellness.wellness_total_calories,garmin_connect_wellness.wellness_bodybattery_charged,garmin_connect_wellness.wellness_body_battery_drained,
            garmin_connect_wellness.wellness_bmr_calories,garmin_connect_wellness.food_calories_remaining,garmin_connect_wellness.common_total_calories,garmin_connect_wellness.wellness_vigorous_intensity_minutes,
            garmin_connect_wellness.wellness_active_calories,garmin_connect_wellness.food_calories_consumed,oura_readiness_daily_summary.score,oura_readiness_daily_summary.score_previous_night,oura_readiness_daily_summary.score_previous_day,
            oura_readiness_daily_summary.score_sleep_balance,oura_readiness_daily_summary.score_activity_balance,oura_readiness_daily_summary.score_resting_hr,oura_readiness_daily_summary.score_hrv_balance,
            oura_readiness_daily_summary.score_recovery_index,oura_readiness_daily_summary.score_temperature,oura_sleep_daily_summary.bedtime_start,oura_sleep_daily_summary.bedtime_end,oura_sleep_daily_summary.score,
            oura_sleep_daily_summary.score_total,oura_sleep_daily_summary.score_disturbances,oura_sleep_daily_summary.score_efficiency,oura_sleep_daily_summary.score_latency,oura_sleep_daily_summary.score_rem,
            oura_sleep_daily_summary.score_deep,oura_sleep_daily_summary.score_alignment,oura_sleep_daily_summary.total,oura_sleep_daily_summary.duration,oura_sleep_daily_summary.awake,
            oura_sleep_daily_summary.light,oura_sleep_daily_summary.rem,oura_sleep_daily_summary.deep,oura_sleep_daily_summary.onset_latency,oura_sleep_daily_summary.restless,oura_sleep_daily_summary.efficiency,
            oura_sleep_daily_summary.midpoint_time,oura_sleep_daily_summary.hr_lowest,oura_sleep_daily_summary.hr_average,oura_sleep_daily_summary.rmssd,oura_sleep_daily_summary.breath_average,oura_sleep_daily_summary.temperature_deviation,
            oura_sleep_daily_summary.bedtime_start_delta,oura_sleep_daily_summary.bedtime_end_delta,oura_sleep_daily_summary.midpoint_at_delta,oura_sleep_daily_summary.temperature_trend_deviation,
            aggr_mfp_nutrition.nutr_food_items,aggr_mfp_nutrition.nutr_food_items_count,aggr_mfp_nutrition.nutr_daily_calories,aggr_mfp_nutrition.nutr_daily_carbs,
            aggr_mfp_nutrition.nutr_daily_protein,aggr_mfp_nutrition.nutr_daily_fat,aggr_mfp_nutrition.nutr_daily_fiber,aggr_mfp_nutrition.nutr_daily_sodium,aggr_diasend_cgm.bg_1min_avrg,aggr_diasend_cgm.bg_15min_avrg,aggr_diasend_cgm.bg_15min_stddev,
            aggr_diasend_cgm.bg_1min_max,aggr_diasend_cgm.bg_1min_min,aggr_diasend_cgm.bg_15min_max,aggr_diasend_cgm.bg_15min_min,aggr_diasend_cgm.keto_avrg,aggr_diasend_cgm.keto_max,aggr_diasend_cgm.keto_min,
            aggr_mind_monitor_eeg.average_alpha,aggr_mind_monitor_eeg.average_beta,aggr_mind_monitor_eeg.average_gamma,aggr_mind_monitor_eeg.average_delta,aggr_mind_monitor_eeg.average_theta,aggr_mind_monitor_eeg.eeg_duration,
            aggr_weather.weather_min_temperature,aggr_weather.weather_max_temperature,aggr_weather.weather_avg_temperature,aggr_weather.weather_avg_dew_point,aggr_weather.weather_avg_humidity,aggr_weather.weather_avg_precipitation,
            aggr_weather.weather_avg_snow,aggr_weather.weather_avg_wind_direction,aggr_weather.weather_avg_wind_speed,aggr_weather.weather_avg_wind_gust,aggr_weather.weather_avg_air_pressure,aggr_weather.weather_stddev_air_pressure,
            aggr_weather.weather_avg_tot_sunshine
            --(Uncomment-Modify the below section to match your custom tables)
            --,cstm_hrv4_training.hr,cstm_hrv4_training.avnn,cstm_hrv4_training.sdnn,cstm_hrv4_training.rmssd,cstm_hrv4_training.pnn50,cstm_hrv4_training.hrv4t_recovery_points,
            --cstm_hrv4_training.training_performance,cstm_hrv4_training.physical_condition,cstm_hrv4_training.trainingrpe,cstm_hrv4_training.trainingmotivation,cstm_hrv4_training.sleep_quality,cstm_hrv4_training.mental_energy,
	    --cstm_hrv4_training.muscle_soreness,cstm_hrv4_training.fatigue,cstm_hrv4_training.traveling,cstm_hrv4_training.sickness,cstm_hrv4_training.alcohol,cstm_hrv4_training.current_lifestyle,cstm_hrv4_training.vo2max         
    ORDER BY gmt_local_time_difference.local_date DESC;


