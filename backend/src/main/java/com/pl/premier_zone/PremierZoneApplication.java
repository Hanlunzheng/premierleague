package com.pl.premier_zone;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.ComponentScan;

@SpringBootApplication
@ComponentScan(basePackages = "com.pl.premier_zone")
public class PremierZoneApplication {

    public static void main(String[] args) {
        SpringApplication.run(PremierZoneApplication.class, args);
    }

} 