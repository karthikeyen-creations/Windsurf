package com.example.springpostgresdemo.controller;

import com.example.springpostgresdemo.service.CommonService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api")
public class CommonController {

    @Autowired
    private CommonService commonService;

    @GetMapping("/data/{condition}")
    public List<Map<String, Object>> getDataAsRecord(@PathVariable String condition) {
        System.out.println("rae preset: Handling GET data as record request");
        return commonService.getDataAsRecord(condition);
    }

    @GetMapping("/json/{condition}")
    public List<String> getDataAsJson(@PathVariable String condition) {
        System.out.println("rae preset: Handling GET data as JSON request");
        return commonService.getDataAsJson(condition);
    }

    @GetMapping("/metadata/{condition}")
    public List<Map<String, Object>> getDataWithMetadata(@PathVariable String condition) {
        System.out.println("rae preset: Handling GET data with metadata request");
        return commonService.getDataWithMetadata(condition);
    }

    @GetMapping("/proc/{condition}")
    public Map<String, Object> getDataWithMetadataProc(@PathVariable String condition) {
        System.out.println("rae preset: Handling GET data with metadata procedure request");
        return commonService.getDataWithMetadataProc(condition);
    }
}
