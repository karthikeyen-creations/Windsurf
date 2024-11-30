package com.example.springpostgresdemo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class SpringPostgresDemoApplication {

    public static void main(String[] args) {
        System.out.println("rae preset: Starting application");
        SpringApplication.run(SpringPostgresDemoApplication.class, args);
        System.out.println("rae preset: Application started");
    }
}
