package com.example;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.ApplicationListener;
import org.springframework.context.event.ContextRefreshedEvent;

@SpringBootApplication
public class PostgresDemoApplication implements ApplicationListener<ContextRefreshedEvent> {

    private static final Logger logger = LoggerFactory.getLogger(PostgresDemoApplication.class);

    public static void main(String[] args) {
        SpringApplication.run(PostgresDemoApplication.class, args);
        logger.info("Application started...");
    }

    @Override
    public void onApplicationEvent(ContextRefreshedEvent event) {
        logger.info("Context refreshed...");
    }
}
