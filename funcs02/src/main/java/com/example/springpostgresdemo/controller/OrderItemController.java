package com.example.springpostgresdemo.controller;

import com.example.springpostgresdemo.entity.OrderItem;
import com.example.springpostgresdemo.service.OrderItemService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import javax.annotation.PostConstruct;
import java.util.List;

@RestController
@RequestMapping("/api/order-items")
public class OrderItemController {

    @Autowired
    private OrderItemService orderItemService;

    @PostConstruct
    public void init() {
        System.out.println("rae preset: OrderItemController initialized");
    }

    @GetMapping
    public List<OrderItem> getAllOrderItems() {
        System.out.println("rae preset: Handling GET all order items request");
        return orderItemService.getAllOrderItems();
    }

    @GetMapping("/{id}")
    public ResponseEntity<OrderItem> getOrderItemById(@PathVariable Long id) {
        System.out.println("rae preset: Handling GET order item by ID request");
        return orderItemService.getOrderItemById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    @PostMapping
    public OrderItem createOrderItem(@RequestBody OrderItem orderItem) {
        System.out.println("rae preset: Handling POST create order item request");
        return orderItemService.createOrderItem(orderItem);
    }

    @PutMapping("/{id}")
    public ResponseEntity<OrderItem> updateOrderItem(@PathVariable Long id, @RequestBody OrderItem orderItemDetails) {
        System.out.println("rae preset: Handling PUT update order item request");
        return ResponseEntity.ok(orderItemService.updateOrderItem(id, orderItemDetails));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteOrderItem(@PathVariable Long id) {
        System.out.println("rae preset: Handling DELETE order item request");
        orderItemService.deleteOrderItem(id);
        return ResponseEntity.noContent().build();
    }
}
