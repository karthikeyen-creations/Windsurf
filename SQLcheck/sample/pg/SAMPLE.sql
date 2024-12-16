--# SET TERMINATOR #
DROP PROCEDURE SYSPROC.E3RP5020 # -- Dropping the procedure to ensure the latest version is created

CREATE PROCEDURE SYSPROC.E3RP5020
(

IN IN_CMPGN_ID CHAR(25)

,IN IN_CMPGN_NM CHAR(100)
,IN IN_CMPGN_DS VARCHAR(400)
,IN IN_CMPGN_PROMO_CD CHAR(64)
,IN IN_CMPGN_STA_TX CHAR(10)
,IN IN_CREAT_TS TIMESTAMP

,IN IN_LST_UPDT_TS TIMESTAMP

,IN IN_CMPGN_CONTEST_MAX_ENTER_CT SMALLINT
,IN IN_CMPGN_TRGT_REGIS_CT INTEGER
,IN IN_BUS_PRTR_DRCT_OWN_NM  CHAR(50)

,IN IN_CMPGN_STRT_DT DATE
,IN IN_CMPGN_END_DT DATE
,IN IN_DA_PRG_DT DATE

,IN IN_CREAT_BY_USER_TYPE_TX  CHAR(10)
,IN IN_UPDT_BY_USER_TYPE_TX CHAR(10)
,IN IN_ENROLL_SUC_EMAIL_SEND_IN CHAR(01)
,IN IN_ENROLL_SUC_EMAIL_TMPLT_ID CHAR(20)
,IN IN_ENROLL_STA_EMAIL_SEND_IN CHAR(01)
,IN IN_ENROLL_STA_EMAIL_TMPLT_ID CHAR(20)
,IN IN_CMPGN_IM_URL_AD_TX CHAR(254)
,IN IN_EMS_PROMO_ID  CHAR(64)
,IN IN_EMS_EXTNL_PRTR_ID CHAR(64)
,IN IN_CMPGN_LIVE_DT DATE
,OUT SQLCODE_PARM CHAR(010)
,OUT RESP_CD CHAR(014)
,OUT RESP_MSG CHAR(100)
)
DYNAMIC RESULT SETS 0
WITH EXPLAIN
VALIDATE BIND
PACKAGE OWNER PRODSUPT
QUALIFIER VMUS00
LANGUAGE SQL
MODIFIES SQL DATA
CALLED ON NULL INPUT
COMMIT ON RETURN NO
ASUTIME LIMIT 7500000
INHERIT SPECIAL REGISTERS
NOT DETERMINISTIC
DISABLE DEBUG MODE
P1:BEGIN
DECLARE SQLCODE INTEGER;
-- Error handling: Capture SQL exceptions and set response codes and messages accordingly
DECLARE EXIT HANDLER FOR SQLEXCEPTION
BEGIN
SET SQLCODE_PARM = SQLCODE;
SET RESP_CD ='E35020999';
SET RESP_MSG = 'SQL EXCEPTION.CHECK SQLCODE TO FIX.';
END;
SET SQLCODE_PARM ='';
SET RESP_CD ='';
SET RESP_MSG ='';
IF EXISTS(
SELECT 1
FROM GABM_CMPGN
WHERE CMPGN_ID = IN_CMPGN_ID)
THEN
INSERT INTO GABM_CMPGN_AUD
(
AUD_CREAT_TS

,CMPGN_ID

,CMPGN_NM

,CMPGN_DS
,CMPGN_PROMO_CD
,CMPGN_STA_TX


,LST_UPDT_TS
,CMPGN_CONTEST_MAX_ENTER_CT
,CMPGN_TRGT_REGIS_CT
,BUS_PRTR_DRCT_OWN_NM
,CMPGN_STRT_DT
,CMPGN_END_DT

,DA_PRG_DT
,CREAT_BY_USER_TYPE_TX
,UPDT_BY_USER_TYPE_TX
,ENROLL_SUC_EMAIL_SEND_IN
,ENROLL_SUC_EMAIL_TMPLT_ID
,ENROLL_STA_EMAIL_SEND_IN
,ENROLL_STA_EMAIL_TMPLT_ID
,CMPGN_IM_URL_AD_TX
,EMS_EXTNL_PROMO_ID
,EMS_EXTNL_PRTR_ID
)
SELECT
CURRENT_TIMESTAMP
,CMPGN_ID
,CMPGN_NM
,CMPGN_DS
,CMPGN_PROMO_CD
,CMPGN_STA_TX
,CREAT_TS
,LST_UPDT_TS
,CMPGN_CONTEST_MAX_ENTER_CT
,CMPGN_TRGT_REGIS_CT
,BUS_PRTR_DRCT_OWN_NM
,CMPGN_STRT_DT
,CMPGN_END_DT
,DA_PRG_DT

,CREAT_BY_USER_TYPE_TX
,UPDT_BY_USER_TYPE_TX
,ENROLL_SUC_EMAIL_SEND_IN
,ENROLL_SUC_EMAIL_TMPLT_ID
,ENROLL_STA_EMAIL_SEND_IN
,ENROLL_STA_EMAIL_TMPLT_ID
,CMPGN_IM_URL_AD_TX
,EMS_EXTNL_PROMO_ID
,EMS_EXTNL_PRTR_ID

FROM GABM_CMPGN
WHERE CMPGN_ID = IN_CMPGN_ID
FETCH FIRST 1 ROW ONLY;
-- Check the SQLCODE value
CASE
	-- If SQLCODE is 0, the operation was successful
	WHEN SQLCODE = '0' THEN
		SET RESP_CD = 'E35020001'; -- Set response code for success
		SET RESP_MSG = 'AUDIT UPDATED SUCCESSFULLY.'; -- Set response message for success
		SET SQLCODE_PARM = SQLCODE; -- Set SQLCODE parameter to the current SQLCODE value
	-- If SQLCODE is not 0, there was an error
	WHEN SQLCODE <> 0 THEN
		SET RESP_CD = 'E35020901'; -- Set response code for error
		SET RESP_MSG = 'THE SYSTEM CANNOT PROCESS YOUR REQUEST. PLEASE TRY AFTER SOME TIME.'; -- Set response message for error
		LEAVE P1; -- Exit the procedure
END CASE;

UPDATE GABM_CMPGN

SET CMPGN_NM = IN_CMPGN_NM0
,CMPGN_DS = IN_CMPGN_DS
,CMPGN_PROMO_CD = IN_CMPGN_PROMO_CD
,CMPGN_STA_TX = IN_CMPGN_STA_TX
,LST_UPDT_TS = CURRENT_TIMESTAMP
,CMPGN_CONTEST_MAX_ENTER_CT = IN_CMPGN_CONTEST_MAX_ENTER_CT
,CMPGN_TRGT_REGIS_CT =IN_CMPGN_TRGT_REGIS_CT
,BUS_PRTR_DRCT_OWN_NM  =IN_BUS_PRTR_DRCT_OWN_NM
,CMPGN_STRT_DT = IN_CMPGN_STRT_DT
,CMPGN_END_DT = IN_CMPGN_END_DT
,DA_PRG_DT =IN_DA_PRG_DT

,UPDT_BY_USER_TYPE_TX = IN_UPDT_BY_USER_TYPE_TX
,ENROLL_SUC_EMAIL_SEND_IN =IN_ENROLL_SUC_EMAIL_SEND_IN
,ENROLL_SUC_EMAIL_TMPLT_ID =IN_ENROLL_SUC_EMAIL_TMPLT_ID
,ENROLL_STA_EMAIL_SEND_IN =IN_ENROLL_STA_EMAIL_SEND_IN
,ENROLL_STA_EMAIL_TMPLT_ID =IN_ENROLL_STA_EMAIL_TMPLT_ID

,CMPGN_IM_URL_AD_TX = IN_CMPGN_IM_URL_AD_TX
,EMS_EXTNL_PROMO_ID = IN_EMS_EXTNL_PROMO_ID
WHERE CMPGN_ID = IN_CMPGN_ID

-- Check the SQLCODE value and set the response code and message accordingly
CASE
	-- If SQLCODE is 0, the update was successful
	WHEN SQLCODE = '0' THEN
		SET RESP_CD = 'E35020002';
		SET RESP_MSG = 'CMPGN ID SUCCESSFULLY UPDATED.';
		SET SQLCODE_PARM = SQLCODE;
	-- If SQLCODE is not 0, there was an error during the update
	WHEN SQLCODE <> 0 THEN
		SET RESP_CD = 'E35020902';
		SET RESP_MSG = 'THE SYSTEM CANNOT PROCESS YOUR REQUEST. PLEASE TRY AFTER SOME TIME.';
		LEAVE P1;
END CASE;
	-- If SQLCODE is not 0, there was an error
	WHEN SQLCODE <> 0 THEN
		SET RESP_CD = 'E35020902'; -- Set response code for error
		SET RESP_MSG = 'THE SYSTEM CANNOT PROCESS YOUR REQUEST. PLEASE TRY AFTER SOME TIME.'; -- Set response message for error
		LEAVE P1; -- Exit the procedure
END CASE;
ELSE
INSERT INTO GABM_CMPGN
(
CMPGN_ID
,CMPGN_NM
,CMPGN_DS
,CMPGN_PROMO_CD
,CMPGN_STA_TX
,CREAT_TS
,LST_UPDT_TS
,CMPGN_CONTEST_MAX_ENTER_CT
,CMPGN_TRGT_REGIS_CT
,BUS_PRTR_DRCT_OWN_NM
,CMPGN_STRT_DT
,CMPGN_END_DT
,DA_PRG_DT
,CREAT_BY_USER_TYPE_TX
,UPDT_BY_USER_TYPE_TX
,ENROLL_SUC_EMAIL_SEND_IN
,ENROLL_SUC_EMAIL_TMPLT_ID
,ENROLL_STA_EMAIL_SEND_IN
,ENROLL_STA_EMAIL_TMPLT_ID
,CMPGN_IM_URL_AD_TX
,EMS_EXTNL_PROMO_ID
,EMS_EXTNL_PRTR_ID
,CMPGN_LIVE_DT
)
VALUES (
IN_CMPGN_ID
,IN_CMPGN_NM
,IN_CMPGN_DS
,IN_CMPGN_PROMO_CD
,IN_CMPGN_STA_TX
,CURRENT_TIMESTAMP
,CURRENT_TIMESTAMP
,IN_CMPGN_CONTEST_MAX_ENTER_CT
,IN_CMPGN_TRGT_REGIS_CT
,IN_BUS_PRTR_DRCT_OWN_NM
,IN_CMPGN_STRT_DT
,IN_CMPGN_END_DT
,IN_DA_PRG_DT
,IN_CREAT_BY_USER_TYPE_TX
,IN_UPDT_BY_USER_TYPE_TX
,IN_ENROLL_SUC_EMAIL_SEND_IN
,IN_ENROLL_SUC_EMAIL_TMPLT_ID
,IN_ENROLL_STA_EMAIL_SEND_IN
,IN_ENROLL_STA_EMAIL_TMPLT_ID
,IN_CMPGN_IM_URL_AD_TX
,IN_EMS_EXTNL_PROMO_ID
,IN_EMS_EXTNL_PRTR_ID
,CURRENT_TIMESTAMP
,CURRENT_TIMESTAMP
,IN_CMPGN_LIVE_DT
);

CASE
	-- If SQLCODE is 0, the operation was successful
	WHEN SQLCODE = '0' THEN
		SET RESP_CD = 'E35020003'; -- Set response code for success
		SET RESP_MSG = 'CMPGN ID SUCCESSFULLY INSERTED.'; -- Set response message for success
	-- If SQLCODE is not 0, there was an error
	WHEN SQLCODE <> 0 THEN
		SET RESP_CD = 'E35020903'; -- Set response code for error
		SET RESP_MSG = 'THE SYSTEM CANNOT PROCESS YOUR REQUEST. PLEASE TRY AFTER SOME TIME.'; -- Set response message for error
		SET SQLCODE_PARM = SQLCODE; -- Set SQLCODE parameter to the current SQLCODE value
		LEAVE P1; -- Exit the procedure
END CASE;
END IF;
END P1#
GRANT EXECUTE ON PROCEDURE SYSPROC.E3RP5020 TO
XB1459A, XB3375A, XB1916A, XB1914A, XB2347A, JO81SE, JO810MS #