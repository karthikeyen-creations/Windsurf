DROP PROCEDURE SYSPROC.E3RP5020; -- Dropping the procedure to ensure the latest version is created

CREATE OR REPLACE FUNCTION tgabm00.e3rp5020(
    IN_CMPGN_ID CHAR(25),
    IN_CMPGN_NM CHAR(100),
    IN_CMPGN_DS VARCHAR(400),
    IN_CMPGN_PROMO_CD CHAR(64),
    IN_CMPGN_STA_TX CHAR(10),
    IN_CREAT_TS TIMESTAMP,
    IN_LST_UPDT_TS TIMESTAMP,
    IN_CMPGN_CONTEST_MAX_ENTER_CT SMALLINT,
    IN_CMPGN_TRGT_REGIS_CT INTEGER,
    IN_BUS_PRTR_DRCT_OWN_NM CHAR(50),
    IN_CMPGN_STRT_DT DATE,
    IN_CMPGN_END_DT DATE,
    IN_DA_PRG_DT DATE,
    IN_CREAT_BY_USER_TYPE_TX CHAR(10),
    IN_UPDT_BY_USER_TYPE_TX CHAR(10),
    IN_ENROLL_SUC_EMAIL_SEND_IN CHAR(1),
    IN_ENROLL_SUC_EMAIL_TMPLT_ID CHAR(20),
    IN_ENROLL_STA_EMAIL_SEND_IN CHAR(1),
    IN_ENROLL_STA_EMAIL_TMPLT_ID CHAR(20),
    IN_CMPGN_IM_URL_AD_TX CHAR(254),
    IN_EMS_EXTNL_PROMO_ID CHAR(64),
    IN_EMS_EXTNL_PRTR_ID CHAR(64),
    IN_CMPGN_LIVE_DT DATE
)
RETURNS TABLE(SQLCODE_PARM CHAR(10), RESP_CD CHAR(14), RESP_MSG CHAR(100)) AS $$
DECLARE
    SQLCODE CHAR(10);
BEGIN
    SQLCODE_PARM := '';
    RESP_CD := '';
    RESP_MSG := '';

    BEGIN
        IF EXISTS (SELECT 1 FROM tgabm00.gabm_cmpgn WHERE cmpgn_id = IN_CMPGN_ID) THEN
            BEGIN
                INSERT INTO tgabm00.gabm_cmpgn_aud (
                    aud_creat_ts, cmpgn_id, cmpgn_nm, cmpgn_ds, cmpgn_promo_cd, cmpgn_sta_tx,
                    creat_ts, lst_updt_ts, cmpgn_contest_max_enter_ct, cmpgn_trgt_regis_ct,
                    bus_prtr_drct_own_nm, cmpgn_strt_dt, cmpgn_end_dt, da_prg_dt,
                    creat_by_user_type_tx, updt_by_user_type_tx, enroll_suc_email_send_in,
                    enroll_suc_email_tmplt_id, enroll_sta_email_send_in, enroll_sta_email_tmplt_id,
                    cmpgn_im_url_ad_tx, ems_extnl_promo_id, ems_extnl_prtr_id
                )
                SELECT
                    CURRENT_TIMESTAMP, cmpgn_id, cmpgn_nm, cmpgn_ds, cmpgn_promo_cd, cmpgn_sta_tx,
                    creat_ts, lst_updt_ts, cmpgn_contest_max_enter_ct, cmpgn_trgt_regis_ct,
                    bus_prtr_drct_own_nm, cmpgn_strt_dt, cmpgn_end_dt, da_prg_dt,
                    creat_by_user_type_tx, updt_by_user_type_tx, enroll_suc_email_send_in,
                    enroll_suc_email_tmplt_id, enroll_sta_email_send_in, enroll_sta_email_tmplt_id,
                    cmpgn_im_url_ad_tx, ems_extnl_promo_id, ems_extnl_prtr_id
                FROM tgabm00.gabm_cmpgn
                WHERE cmpgn_id = IN_CMPGN_ID
                LIMIT 1;

                SQLCODE := '0';
                                  RESP_CD := 'E35020001';
                    RESP_MSG := 'AUDIT UPDATED SUCCESSFULLY.';
                EXCEPTION 
                WHEN NO_DATA_FOUND THEN

                WHEN OTHERS THEN
                    SQLCODE := SQLSTATE;
                    SQLCODE_PARM := SQLCODE;
                    RESP_CD := 'E35020901';
                    RESP_MSG := 'THE SYSTEM CANNOT PROCESS YOUR REQUEST. PLEASE TRY AFTER SOME TIME.';
                    RETURN QUERY SELECT SQLCODE_PARM, RESP_CD, RESP_MSG;
            END;
            BEGIN
                UPDATE tgabm00.gabm_cmpgn
                SET
                    cmpgn_nm = IN_CMPGN_NM,
                    cmpgn_ds = IN_CMPGN_DS,
                    cmpgn_promo_cd = IN_CMPGN_PROMO_CD,
                    cmpgn_sta_tx = IN_CMPGN_STA_TX,
                    lst_updt_ts = CURRENT_TIMESTAMP,
                    cmpgn_contest_max_enter_ct = IN_CMPGN_CONTEST_MAX_ENTER_CT,
                    cmpgn_trgt_regis_ct = IN_CMPGN_TRGT_REGIS_CT,
                    bus_prtr_drct_own_nm = IN_BUS_PRTR_DRCT_OWN_NM,
                    cmpgn_strt_dt = IN_CMPGN_STRT_DT,
                    cmpgn_end_dt = IN_CMPGN_END_DT,
                    da_prg_dt = IN_DA_PRG_DT,
                    updt_by_user_type_tx = IN_UPDT_BY_USER_TYPE_TX,
                    enroll_suc_email_send_in = IN_ENROLL_SUC_EMAIL_SEND_IN,
                    enroll_suc_email_tmplt_id = IN_ENROLL_SUC_EMAIL_TMPLT_ID,
                    enroll_sta_email_send_in = IN_ENROLL_STA_EMAIL_SEND_IN,
                    enroll_sta_email_tmplt_id = IN_ENROLL_STA_EMAIL_TMPLT_ID,
                    cmpgn_im_url_ad_tx = IN_CMPGN_IM_URL_AD_TX,
                    ems_extnl_promo_id = IN_EMS_EXTNL_PROMO_ID,
                    ems_extnl_prtr_id = IN_EMS_EXTNL_PRTR_ID
                WHERE cmpgn_id = IN_CMPGN_ID;

                SQLCODE := '0';
                EXCEPTION WHEN OTHERS THEN
                    SQLCODE := SQLSTATE;
                    SQLCODE_PARM := SQLCODE;
                    RESP_CD := 'E35020999';
                    RESP_MSG := 'SQL EXCEPTION. CHECK SQLCODE TO FIX.';
                    RETURN QUERY SELECT SQLCODE_PARM, RESP_CD, RESP_MSG;
            END;

            CASE
                WHEN SQLCODE = '0' THEN
                    RESP_CD := 'E35020002';
                    RESP_MSG := 'CMPGN ID SUCCESSFULLY UPDATED.';
                    SQLCODE_PARM := SQLCODE;
                ELSE
                    RESP_CD := 'E35020902';
                    RESP_MSG := 'THE SYSTEM CANNOT PROCESS YOUR REQUEST. PLEASE TRY AFTER SOME TIME.';
                    RETURN QUERY SELECT SQLCODE_PARM, RESP_CD, RESP_MSG;
            END CASE;
        ELSE
            BEGIN
                INSERT INTO tgabm00.gabm_cmpgn (
                    cmpgn_id, cmpgn_nm, cmpgn_ds, cmpgn_promo_cd, cmpgn_sta_tx, creat_ts, lst_updt_ts,
                    cmpgn_contest_max_enter_ct, cmpgn_trgt_regis_ct, bus_prtr_drct_own_nm, cmpgn_strt_dt,
                    cmpgn_end_dt, da_prg_dt, creat_by_user_type_tx, updt_by_user_type_tx, enroll_suc_email_send_in,
                    enroll_suc_email_tmplt_id, enroll_sta_email_send_in, enroll_sta_email_tmplt_id,
                    cmpgn_im_url_ad_tx, ems_extnl_promo_id, ems_extnl_prtr_id, cmpgn_live_dt
                )
                VALUES (
                    IN_CMPGN_ID, IN_CMPGN_NM, IN_CMPGN_DS, IN_CMPGN_PROMO_CD, IN_CMPGN_STA_TX, CURRENT_TIMESTAMP,
                    CURRENT_TIMESTAMP, IN_CMPGN_CONTEST_MAX_ENTER_CT, IN_CMPGN_TRGT_REGIS_CT, IN_BUS_PRTR_DRCT_OWN_NM,
                    IN_CMPGN_STRT_DT, IN_CMPGN_END_DT, IN_DA_PRG_DT, IN_CREAT_BY_USER_TYPE_TX, IN_UPDT_BY_USER_TYPE_TX,
                    IN_ENROLL_SUC_EMAIL_SEND_IN, IN_ENROLL_SUC_EMAIL_TMPLT_ID, IN_ENROLL_STA_EMAIL_SEND_IN,
                    IN_ENROLL_STA_EMAIL_TMPLT_ID, IN_CMPGN_IM_URL_AD_TX, IN_EMS_EXTNL_PROMO_ID, IN_EMS_EXTNL_PRTR_ID,
                    IN_CMPGN_LIVE_DT
                );

                SQLCODE := '0';
                EXCEPTION WHEN OTHERS THEN
                    SQLCODE := SQLSTATE;
                    SQLCODE_PARM := SQLCODE;
                    RESP_CD := 'E35020999';
                    RESP_MSG := 'SQL EXCEPTION. CHECK SQLCODE TO FIX.';
                    RETURN QUERY SELECT SQLCODE_PARM, RESP_CD, RESP_MSG;
            END;

            CASE
                WHEN SQLCODE = '0' THEN
                    RESP_CD := 'E35020003';
                    RESP_MSG := 'CMPGN ID SUCCESSFULLY INSERTED.';
                    SQLCODE_PARM := SQLCODE;
                ELSE
                    RESP_CD := 'E35020903';
                    RESP_MSG := 'THE SYSTEM CANNOT PROCESS YOUR REQUEST. PLEASE TRY AFTER SOME TIME.';
                    RETURN QUERY SELECT SQLCODE_PARM, RESP_CD, RESP_MSG;
            END CASE;
        END IF;
    EXCEPTION WHEN OTHERS THEN
        SQLCODE := SQLSTATE;
        SQLCODE_PARM := SQLCODE;
        RESP_CD := 'E35020999';
        RESP_MSG := 'SQL EXCEPTION. CHECK SQLCODE TO FIX.';
        RETURN QUERY SELECT SQLCODE_PARM, RESP_CD, RESP_MSG;
    END;

    RETURN QUERY SELECT SQLCODE_PARM, RESP_CD, RESP_MSG;
END;
$$ LANGUAGE plpgsql;