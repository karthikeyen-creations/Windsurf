package com.example.springpostgresdemo.controller;

import com.example.springpostgresdemo.entity.Order;
import com.example.springpostgresdemo.service.OrderService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import javax.annotation.PostConstruct;
import java.util.List;

@RestController
@RequestMapping("/api/orders")
public class OrderController {

    @Autowired
    private OrderService orderService;

    @PostConstruct
    public void init() {
        System.out.println("rae preset: OrderController initialized");
    }

    @GetMapping
    public List<Order> getAllOrders() {
        System.out.println("rae preset: Handling GET all orders request");
        return orderService.getAllOrders();
    }

    @GetMapping("/{id}")
    public ResponseEntity<Order> getOrderById(@PathVariable Long id) {
        System.out.println("rae preset: Handling GET order by ID request");
        return orderService.getOrderById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    @PostMapping
    public Order createOrder(@RequestBody Order order) {
        System.out.println("rae preset: Handling POST create order request");
        return orderService.createOrder(order);
    }

    @PutMapping("/{id}")
    public ResponseEntity<Order> updateOrder(@PathVariable Long id, @RequestBody Order orderDetails) {
        System.out.println("rae preset: Handling PUT update order request");
        return ResponseEntity.ok(orderService.updateOrder(id, orderDetails));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteOrder(@PathVariable Long id) {
        System.out.println("rae preset: Handling DELETE order request");
        orderService.deleteOrder(id);
        return ResponseEntity.noContent().build();
    }
}
