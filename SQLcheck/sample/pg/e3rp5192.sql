CREATE OR REPLACE FUNCTION tgabm00.e3rp5192(
    IN_CMPGN_ID CHAR(25),
    IN_LST_UPDT_BY_PRCS_NM CHAR(10)
) RETURNS TABLE(SQLCODE_PARM CHAR(10), RESP_CD CHAR(14), RESP_MSG CHAR(100)) AS $$
DECLARE
    SQLCODE CHAR(10);
    REC_EXISTS INTEGER;
BEGIN
    SQLCODE_PARM := '';
    RESP_CD := '';
    RESP_MSG := '';

    -- VERIFY IF CAMPAIGN EXIST.
    BEGIN
        SELECT 1 INTO REC_EXISTS
        FROM tgabm00.gabm_cmpgn C
        WHERE C.cmpgn_id = IN_CMPGN_ID
        LIMIT 1;

        SQLCODE := '0';
        RESP_CD := 'E35192000';
        RESP_MSG := 'CAMPAIGN ID FOUND.';
        SQLCODE_PARM := SQLCODE;
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            SQLCODE := '100';
            RESP_CD := 'E35192100';
            RESP_MSG := 'CAMPAIGN ID NOT FOUND.';
            SQLCODE_PARM := SQLCODE;
            RETURN QUERY SELECT SQLCODE_PARM, RESP_CD, RESP_MSG;
        WHEN OTHERS THEN
            SQLCODE := SQLSTATE;
            RESP_CD := 'E35192900';
            RESP_MSG := 'THE SYSTEM CANNOT PROCESS YOUR REQUEST. PLEASE TRY AFTER SOME TIME.';
            SQLCODE_PARM := SQLCODE;
            RETURN QUERY SELECT SQLCODE_PARM, RESP_CD, RESP_MSG;
    END;

    -- UPDATE(DELETE) APPL_CMPNT_RWRD_PARM TABLE
    BEGIN
        UPDATE tgabm00.gabm_appl_cmpnt_rwrd_parm ACRP
        SET act_in = 'N',
            lst_updt_by_prcs_nm = IN_LST_UPDT_BY_PRCS_NM,
            lst_updt_ts = CURRENT_TIMESTAMP
        WHERE rwrd_id IN (
            SELECT CR.rwrd_id
            FROM tgabm00.gabm_cmpgn_rwrd CR
            WHERE CR.cmpgn_id = IN_CMPGN_ID
        );

        SQLCODE := '0';
        RESP_CD := 'E35192001';
        RESP_MSG := 'APPL CMPNT RWRD PARM UPDATED SUCCESSFULLY';
        SQLCODE_PARM := SQLCODE;
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            SQLCODE := '100';
            RESP_CD := 'E35192101';
            RESP_MSG := 'NO ROWS TO UPDATE.';
            SQLCODE_PARM := SQLCODE;
        WHEN OTHERS THEN
            SQLCODE := SQLSTATE;
            RESP_CD := 'E35192901';
            RESP_MSG := 'THE SYSTEM CANNOT PROCESS YOUR REQUEST. PLEASE TRY AFTER SOME TIME.';
            SQLCODE_PARM := SQLCODE;
            RETURN QUERY SELECT SQLCODE_PARM, RESP_CD, RESP_MSG;
    END;

    -- UPDATE(DELETE) GABM_RWRD_APPL_CMPNT TABLE
    BEGIN
        UPDATE tgabm00.gabm_rwrd_appl_cmpnt RAC
        SET act_in = 'N',
            lst_updt_by_prcs_nm = IN_LST_UPDT_BY_PRCS_NM,
            lst_updt_ts = CURRENT_TIMESTAMP
        WHERE rwrd_id IN (
            SELECT CR.rwrd_id
            FROM tgabm00.gabm_cmpgn_rwrd CR
            WHERE CR.cmpgn_id = IN_CMPGN_ID
        );

        SQLCODE := '0';
        RESP_CD := 'E35192002';
        RESP_MSG := 'RWRD APPL CMPNT UPDATED SUCCESSFULLY';
        SQLCODE_PARM := SQLCODE;
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            SQLCODE := '100';
            RESP_CD := 'E35192102';
            RESP_MSG := 'NO ROWS TO UPDATE.';
            SQLCODE_PARM := SQLCODE;
        WHEN OTHERS THEN
            SQLCODE := SQLSTATE;
            RESP_CD := 'E35192902';
            RESP_MSG := 'THE SYSTEM CANNOT PROCESS YOUR REQUEST. PLEASE TRY AFTER SOME TIME.';
            SQLCODE_PARM := SQLCODE;
            RETURN QUERY SELECT SQLCODE_PARM, RESP_CD, RESP_MSG;
    END;

    -- UPDATE(DELETE) GABM_RWRD TABLE
    BEGIN
        UPDATE tgabm00.gabm_rwrd R
        SET act_in = 'N',
            lst_updt_by_prcs_nm = IN_LST_UPDT_BY_PRCS_NM,
            lst_updt_ts = CURRENT_TIMESTAMP
        WHERE rwrd_id IN (
            SELECT CR.rwrd_id
            FROM tgabm00.gabm_cmpgn_rwrd CR
            WHERE CR.cmpgn_id = IN_CMPGN_ID
        );

        SQLCODE := '0';
        RESP_CD := 'E35192003';
        RESP_MSG := 'RWRD DTL UPDATED SUCCESSFULLY.';
        SQLCODE_PARM := SQLCODE;
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            SQLCODE := '100';
            RESP_CD := 'E35192103';
            RESP_MSG := 'NO ROWS TO UPDATE.';
            SQLCODE_PARM := SQLCODE;
        WHEN OTHERS THEN
            SQLCODE := SQLSTATE;
            RESP_CD := 'E35192903';
            RESP_MSG := 'THE SYSTEM CANNOT PROCESS YOUR REQUEST. PLEASE TRY AFTER SOME TIME.';
            SQLCODE_PARM := SQLCODE;
            RETURN QUERY SELECT SQLCODE_PARM, RESP_CD, RESP_MSG;
    END;

    -- UPDATE(DELETE) GABM_CMPGN_RWRD TABLE
    BEGIN
        UPDATE tgabm00.gabm_cmpgn_rwrd CR
        SET act_in = 'N',
            lst_updt_by_prcs_nm = IN_LST_UPDT_BY_PRCS_NM,
            lst_updt_ts = CURRENT_TIMESTAMP
        WHERE cmpgn_id = IN_CMPGN_ID;

        SQLCODE := '0';
        RESP_CD := 'E35192004';
        RESP_MSG := 'CMPGN RWRD DTL UPDATED SUCCESSFULLY.';
        SQLCODE_PARM := SQLCODE;
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            SQLCODE := '100';
            RESP_CD := 'E35192104';
            RESP_MSG := 'NO ROWS TO UPDATE.';
            SQLCODE_PARM := SQLCODE;
        WHEN OTHERS THEN
            SQLCODE := SQLSTATE;
            RESP_CD := 'E35192904';
            RESP_MSG := 'THE SYSTEM CANNOT PROCESS YOUR REQUEST. PLEASE TRY AFTER SOME TIME.';
            SQLCODE_PARM := SQLCODE;
            RETURN QUERY SELECT SQLCODE_PARM, RESP_CD, RESP_MSG;
    END;

    -- UPDATE(DELETE) GABM_CMPGN_CTRY TABLE
    BEGIN
        UPDATE tgabm00.gabm_cmpgn_ctry CC
        SET act_in = 'N',
            lst_updt_by_prcs_nm = IN_LST_UPDT_BY_PRCS_NM,
            lst_updt_ts = CURRENT_TIMESTAMP
        WHERE cmpgn_id = IN_CMPGN_ID;

        SQLCODE := '0';
        RESP_CD := 'E35192005';
        RESP_MSG := 'CMPGN CTRY DTL UPDATED SUCCESSFULLY.';
        SQLCODE_PARM := SQLCODE;
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            SQLCODE := '100';
            RESP_CD := 'E35192105';
            RESP_MSG := 'NO ROWS TO UPDATE.';
            SQLCODE_PARM := SQLCODE;
        WHEN OTHERS THEN
            SQLCODE := SQLSTATE;
            RESP_CD := 'E35192905';
            RESP_MSG := 'THE SYSTEM CANNOT PROCESS YOUR REQUEST. PLEASE TRY AFTER SOME TIME.';
            SQLCODE_PARM := SQLCODE;
            RETURN QUERY SELECT SQLCODE_PARM, RESP_CD, RESP_MSG;
    END;

    -- UPDATE(DELETE) GABM_CMPGN TABLE
    BEGIN
        UPDATE tgabm00.gabm_cmpgn C
        SET cmpgn_end_dt = CURRENT_DATE - INTERVAL '1 day',
            updt_by_user_type_tx = IN_LST_UPDT_BY_PRCS_NM,
            lst_updt_ts = CURRENT_TIMESTAMP
        WHERE cmpgn_id = IN_CMPGN_ID;

        SQLCODE := '0';
        RESP_CD := 'E35192006';
        RESP_MSG := 'CMPGN DTL UPDATED SUCCESSFULLY.';
        SQLCODE_PARM := SQLCODE;
        RETURN QUERY SELECT SQLCODE_PARM, RESP_CD, RESP_MSG;
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            SQLCODE := '100';
            RESP_CD := 'E35192106';
            RESP_MSG := 'NO ROWS TO UPDATE.';
            SQLCODE_PARM := SQLCODE;
            RETURN QUERY SELECT SQLCODE_PARM, RESP_CD, RESP_MSG;
        WHEN OTHERS THEN
            SQLCODE := SQLSTATE;
            RESP_CD := 'E35192906';
            RESP_MSG := 'THE SYSTEM CANNOT PROCESS YOUR REQUEST. PLEASE TRY AFTER SOME TIME.';
            SQLCODE_PARM := SQLCODE;
            RETURN QUERY SELECT SQLCODE_PARM, RESP_CD, RESP_MSG;
    END;
EXCEPTION
    WHEN OTHERS THEN
        SQLCODE := SQLSTATE;
        RESP_CD := 'E35192999';
        RESP_MSG := 'UNEXPECTED ERROR OCCURRED.';
        SQLCODE_PARM := SQLCODE;
        RETURN QUERY SELECT SQLCODE_PARM, RESP_CD, RESP_MSG;
END;
$$ LANGUAGE plpgsql;