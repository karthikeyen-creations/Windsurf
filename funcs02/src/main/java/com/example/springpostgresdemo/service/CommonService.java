package com.example.springpostgresdemo.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.SqlOutParameter;
import org.springframework.jdbc.core.SqlParameter;
import org.springframework.jdbc.core.simple.SimpleJdbcCall;
import org.springframework.stereotype.Service;

import java.sql.Types;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.logging.Logger;

@Service
public class CommonService {

    private static final Logger logger = Logger.getLogger(CommonService.class.getName());

    @Autowired
    private JdbcTemplate jdbcTemplate;

    public List<Map<String, Object>> getDataAsRecord(String condition) {
        String sql = "SELECT * FROM tgabm00.get_data_as_record(?) AS result(key TEXT, value1 TEXT, value2 TEXT);";
        List<Map<String, Object>> result = jdbcTemplate.queryForList(sql, new Object[]{condition});
        logger.info("Raw response from database: " + result);
        return result;
    }

    public List<String> getDataAsJson(String condition) {
        String sql = "SELECT * FROM tgabm00.get_data_as_json(?);";
        List<String> result = jdbcTemplate.queryForList(sql, new Object[]{condition}, String.class);
        logger.info("Raw response from database: " + result);
        return result;
    }

    public List<Map<String, Object>> getDataWithMetadata(String condition) {
        String sql = "SELECT * FROM tgabm00.get_data_with_metadata(?);";
        List<Map<String, Object>> result = jdbcTemplate.queryForList(sql, new Object[]{condition});
        logger.info("Raw response from database: " + result);
        return result;
    }

    public Map<String, Object> getDataWithMetadataProc(String condition) {
        SimpleJdbcCall jdbcCall = new SimpleJdbcCall(jdbcTemplate)
                .withSchemaName("tgabm00")
                .withProcedureName("get_data_with_metadata_proc")
                .declareParameters(
                        new SqlParameter("condition", Types.VARCHAR),
                        new SqlOutParameter("result", Types.OTHER)
                );

        Map<String, Object> inParams = new HashMap<>();
        inParams.put("condition", condition);

        Map<String, Object> result = jdbcCall.execute(inParams);
        logger.info("Raw response from database: " + result);
        return result;
    }
}
