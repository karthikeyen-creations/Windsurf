package com.example.springpostgresdemo.controller;

import com.example.springpostgresdemo.entity.User;
import com.example.springpostgresdemo.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import javax.annotation.PostConstruct;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/users")
public class UserController {

    @Autowired
    private UserService userService;

    @PostConstruct
    public void init() {
        System.out.println("rae preset: UserController initialized");
    }

    @GetMapping
    public List<User> getAllUsers() {
        System.out.println("rae preset: Handling GET all users request");
        return userService.getAllUsers();
    }

    @GetMapping("/{id}")
    public ResponseEntity<User> getUserById(@PathVariable Long id) {
        System.out.println("rae preset: Handling GET user by ID request");
        return userService.getUserById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    @PostMapping
    public User createUser(@RequestBody User user) {
        System.out.println("rae preset: Handling POST create user request");
        return userService.createUser(user);
    }

    @PutMapping("/{id}")
    public ResponseEntity<User> updateUser(@PathVariable Long id, @RequestBody User userDetails) {
        System.out.println("rae preset: Handling PUT update user request");
        return ResponseEntity.ok(userService.updateUser(id, userDetails));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteUser(@PathVariable Long id) {
        System.out.println("rae preset: Handling DELETE user request");
        userService.deleteUser(id);
        return ResponseEntity.noContent().build();
    }

    @GetMapping("/map")
    public String getUsersAsMap() {
        return userService.getUsersAsMap();
    }

    @GetMapping("/record")
    public List<Map<String, Object>> getUsersAsRecord() {
        return userService.getUsersAsRecord();
    }
}
