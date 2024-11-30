package com.example.springpostgresdemo.controller;

import com.example.springpostgresdemo.entity.SampleEntity;
import com.example.springpostgresdemo.service.SampleService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import javax.annotation.PostConstruct;
import java.util.List;

@RestController
@RequestMapping("/api/samples")
public class SampleController {

    @Autowired
    private SampleService sampleService;

    @PostConstruct
    public void init() {
        System.out.println("rae preset: Controller initialized");
    }

    @GetMapping
    public List<SampleEntity> getAllSamples() {
        System.out.println("rae preset: Handling GET request");
        return sampleService.getAllSamples();
    }

    @PostMapping
    public SampleEntity createSample(@RequestBody SampleEntity sample) {
        System.out.println("rae preset: Handling POST request");
        return sampleService.saveSample(sample);
    }
}
