package com.example.springpostgresdemo.service;

import com.example.springpostgresdemo.entity.SampleEntity;
import com.example.springpostgresdemo.repository.SampleRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import javax.annotation.PostConstruct;
import java.util.List;

@Service
public class SampleService {

    @Autowired
    private SampleRepository sampleRepository;

    @PostConstruct
    public void init() {
        System.out.println("rae preset: Service initialized");
    }

    public List<SampleEntity> getAllSamples() {
        System.out.println("rae preset: Fetching all samples");
        return sampleRepository.findAll();
    }

    public SampleEntity saveSample(SampleEntity sample) {
        System.out.println("rae preset: Saving sample");
        return sampleRepository.save(sample);
    }
}
