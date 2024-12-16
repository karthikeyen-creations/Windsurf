--#SET TERMINATOR #
CREATE PROCEDURE SYSPROC.E3RP5192

(
IN IN_CMPGN_ID CHAR(25)
,IN IN_LST_UPDT_BY_PRCS_NM CHAR(10)
,OUT SQLCODE_PARM CHAR(10)
,OUT RESP_CD CHAR(14)
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
DECLARE REC_EXISTS INTEGER;
DECLARE EXIT HANDLER FOR SQLEXCEPTION
BEGIN

SET SQLCODE_PARM = SQLCODE;

SET RESP_CD ='E35192999';

SET RESP_MSG = 'SQL EXCEPTION.CHECK SQLCODE TO FIX.';
END;
SET SQLCODE_PARM ='';
SET RESP_CD ='';
SET RESP_MSG ='';

-- VERIFY IF CAMPAIGN EXIST.
SELECT 1
INTO REC_EXISTS
FROM GABM_CMPGN C

WHERE C.CMPGN_ID = IN_CMPGN_ID
FETCH FIRST 1 ROW ONLY
WITH UR;
CASE
WHEN SQLCODE = '0' THEN
SET RESP_CD ='E35192000';

SET RESP_MSG = 'CAMPAIGN ID FOUND.';
SET SQLCODE_PARM = SQLCODE;
WHEN SQLCODE = '100' THEN
SET RESP_CD ='E35192100';
SET RESP_MSG ='CAMPAIGN ID NOT FOUND.';
SET SQLCODE_PARM = SQLCODE;
LEAVE P1;WHEN SQLCODE <> '0' THEN
SET RESP_CD ='E35192900';

SET RESP_MSG = 'THE SYSTEM CANNOT PROCESS YOUR REQUEST. 
 PLEASE TRY AFTER SOME TIME. ';
SET SQLCODE_PARM = SQLCODE;
LEAVE P1;

END CASE;

-- UPDATE(DELETE) APPL_CMPNT_RWRD_| PARM TABLE

UPDATE GABM_APPL_CMPNT_RWRD_PARM ACRP

SET ACRP.ACT_IN ='N'
,ACRP.LST_UPDT_BY_PRCS_NM = IN_LST_UPDT_BY_PRCS_NM
,ACRP.LST_UPDT_TS = CURRENT_TIMESTAMP

WHERE ACRP.RWRD_ID IN
(SELECT CR.RWRD_ID
FROM GABM_CMPGN_RWRD CR
WHERE CR.CMPGN_ID = IN_CMPGN_ID);

CASE

WHEN SQLCODE ='0' THEN
SET RESP_CD ='E35192001';
SET RESP_MSG ='APPL CMPNT RWRD PARM UPDATED SUCCESSFULLY';

SET SQLCODE_PARM = SQLCODE;

WHEN SQLCODE = '100' THEN
SET RESP_CD ='E35192101';
SET RESP_MSG ='NO ROWS TO UPDATE.';SET SQLCODE_PARM = SQLCODE;
WHEN SQLCODE <> 0 THEN
SET RESP_CD ='E35192901';
SET RESP_MSG = 'THE SYSTEM CANNOT PROCESS YOUR REQUEST. 
 PLEASE TRY AFTER SOME TIME.';
SET SQLCODE_PARM = SQLCODE;
LEAVE P1;
END CASE;

UPDATE GABM_RWRD_APPL_CMPNT RAC

SET RAC.ACT_IN ='N'
,RAC.LST_UPDT_BY_PRCS_NM = IN_LST_UPDT_BY_PRCS_NM
,RAC.LST_UPDT_TS = CURRENT_TIMESTAMP

WHERE RAC.RWRD_ID IN
(SELECT CR.RWRD_ID
FROM GABM_CMPGN_RWRD CR
WHERE CR.CMPGN_ID = IN_CMPGN_ID);

CASE

WHEN SQLCODE ='0' THEN
SET RESP_CD ='E35192002';
SET RESP_MSG = 'RWRD APPL CMPNT UPDATED SUCCESSFULLY';
SET SQLCODE_PARM = SQLCODE;

WHEN SQLCODE = '100' THEN
SET RESP_CD ='E35192102';
SET RESP_MSG = 'NO ROWS TO UPDATE.';SET SQLCODE_PARM = SQLCODE;
WHEN SQLCODE <> 0 THEN
SET RESP_CD ='E35192902';
SET RESP_MSG = 'THE SYSTEM CANNOT PROCESS YOUR REQUEST. PLEASE TRY AFTER SOME TIME.';
SET SQLCODE_PARM = SQLCODE;
LEAVE P1;
END CASE;

-- UPDATE(DELETE) GABM_RWRD TABLE

UPDATE GABM_RWRD R

SET R.ACT_IN ='N'
,R.LST_UPDT_BY_PRCS_NM = IN_LST_UPDT_BY_PRCS_NM
,R.LST_UPDT_TS = CURRENT_TIMESTAMP

WHERE R.RWRD_ID IN
(SELECT CR.RWRD_ID
FROM GABM_CMPGN_RWRD CR
WHERE CR.CMPGN_ID = IN_CMPGN_ID);

CASE

WHEN SQLCODE ='0' THEN
SET RESP_CD ='E35192003';
SET RESP_MSG = 'RWRD DTL UPDATED SUCCESSFULLY.';
SET SQLCODE_PARM = SQLCODE;

WHEN SQLCODE = '100' THEN
SET RESP_CD ='E35192103';
SET RESP_MSG = 'NO ROWS TO UPDATE.';SET SQLCODE_PARM = SQLCODE;
WHEN SQLCODE <> 0 THEN
SET RESP_CD ='E35192903';
SET RESP_MSG = 'THE SYSTEM CANNOT PROCESS YOUR REQUEST. PLEASE TRY AFTER SOME TIME.';
SET SQLCODE_PARM = SQLCODE;
LEAVE P1;
END CASE;

UPDATE GABM_CMPGN_RWRD CR

SET CR.ACT_IN ='N'
,CR.LST_UPDT_BY_PRCS_NM=IN_LST_UPDT_BY_PRCS_NM
,CR.LST_UPDT_TS = CURRENT_TIMESTAMP

WHERE CR.CMPGN_ID = IN_CMPGN_ID;

CASE

WHEN SQLCODE ='0' THEN
SET RESP_CD ='E35192004';
SET RESP_MSG = 'CMPGN RWRD DTL UPDATED SUCCESSFULLY.';
SET SQLCODE_PARM = SQLCODE;

WHEN SQLCODE = '100' THEN
SET RESP_CD ='E35192104';
SET RESP_MSG ='NO ROWS TO UPDATE.';
SET SQLCODE_PARM = SQLCODE;

WHEN SQLCODE <> 0 THEN
SET RESP_CD ='E35192904';SET RESP_MSG = 'THE SYSTEM CANNOT PROCESS YOUR REQUEST. PLEASE TRY AFTER SOME TIME.';
SET SQLCODE_PARM = SQLCODE;
LEAVE P1;
END CASE;

UPDATE GABM_CMPGN_CTRY CC

SET CC.ACT_IN ='N'
,CC.LST_UPDT_BY_PRCS_NM =IN_LST_UPDT_BY_PRCS_NM
,CC.LST_UPDT_TS = CURRENT_TIMESTAMP

WHERE CC.CMPGN_ID = IN_CMPGN_ID;

CASE

WHEN SQLCODE ='0' THEN
SET RESP_CD ='E35192005';
SET RESP_MSG = 'CMPGN CTRY DTL UPDATED SUCCESSFULLY.';
SET SQLCODE_PARM = SQLCODE;

WHEN SQLCODE = '100' THEN
SET RESP_CD ='E35192105';
SET RESP_MSG ='NO ROWS TO UPDATE.';
SET SQLCODE_PARM = SQLCODE;

WHEN SQLCODE <> 0 THEN
SET RESP_CD ='E35192905';
SET RESP_MSG = 'THE SYSTEM CANNOT PROCESS YOUR REQUEST. PLEASE TRY AFTER SOME TIME.';

SET SQLCODE_PARM = SQLCODE;LEAVE P1;
END CASE;

UPDATE GABM_CMPGN C

SET C.CMPGN_END_DT =CURRENT_DATE - 1 DAY
,C.UPDT_BY_USER_TYPE_TX = IN_LST_UPDT_BY_PRCS_NM
,C.LST_UPDT_TS = CURRENT_TIMESTAMP

WHERE C.CMPGN_ID = IN_CMPGN_ID;

CASE

WHEN SQLCODE ='0' THEN
SET RESP_CD ='E35192006';
SET RESP_MSG = 'CMPGN DTL UPDATED SUCCESSFULLY.';
SET SQLCODE_PARM = SQLCODE;
LEAVE P1;

WHEN SQLCODE = '100' THEN
SET RESP_CD ='E35192106';
SET RESP_MSG ='NO ROWS TO UPDATE.';
SET SQLCODE_PARM = SQLCODE;
LEAVE P1;

WHEN SQLCODE <> 0 THEN
SET RESP_CD ='E35192906';
SET RESP_MSG = 'THE SYSTEM CANNOT PROCESS YOUR REQUEST. PLEASE TRY AFTER SOME TIME.';

SET SQLCODE_PARM = SQLCODE;
LEAVE P1;
END CASE;

END P1#
GRANT EXECUTE ON PROCEDURE SYSPROC.E3RP5192 TO XB1459A, XB3375A, XB1916A, XB1914A, XB2347A, J081SE, J0810MS #