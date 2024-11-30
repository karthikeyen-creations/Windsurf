package com.example.springpostgresdemo.service;

import com.example.springpostgresdemo.entity.User;
import com.example.springpostgresdemo.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.logging.Logger;

@Service
public class UserService {

    private static final Logger logger = Logger.getLogger(UserService.class.getName());

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private JdbcTemplate jdbcTemplate;

    public List<User> getAllUsers() {
        List<User> users = userRepository.findAll();
        logger.info("Raw response from database: " + users);
        return users;
    }

    public Optional<User> getUserById(Long id) {
        Optional<User> user = userRepository.findById(id);
        logger.info("Raw response from database: " + user);
        return user;
    }

    public User createUser(User user) {
        User createdUser = userRepository.save(user);
        logger.info("Raw response from database: " + createdUser);
        return createdUser;
    }

    public User updateUser(Long id, User userDetails) {
        User user = userRepository.findById(id).orElseThrow(() -> new RuntimeException("User not found"));
        user.setUsername(userDetails.getUsername());
        user.setEmail(userDetails.getEmail());
        User updatedUser = userRepository.save(user);
        logger.info("Raw response from database: " + updatedUser);
        return updatedUser;
    }

    public void deleteUser(Long id) {
        userRepository.deleteById(id);
        logger.info("Raw response from database: User with id " + id + " deleted");
    }

    public String getUsersAsMap() {
        String sql = "SELECT tgabm00.get_users_as_map();";
        String result = jdbcTemplate.queryForObject(sql, String.class);
        logger.info("Raw response from database: " + result);
        return result;
    }

    public List<Map<String, Object>> getUsersAsRecord() {
        String sql = "SELECT * FROM tgabm00.get_users_as_record() AS result(key TEXT, value1 TEXT, value2 TEXT);";
        List<Map<String, Object>> result = jdbcTemplate.queryForList(sql);
        logger.info("Raw response from database: " + result);
        return result;
    }
}
