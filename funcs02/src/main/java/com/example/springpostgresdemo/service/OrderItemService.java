package com.example.springpostgresdemo.service;

import com.example.springpostgresdemo.entity.OrderItem;
import com.example.springpostgresdemo.repository.OrderItemRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;
import java.util.logging.Logger;

@Service
public class OrderItemService {

    private static final Logger logger = Logger.getLogger(OrderItemService.class.getName());

    @Autowired
    private OrderItemRepository orderItemRepository;

    public List<OrderItem> getAllOrderItems() {
        List<OrderItem> orderItems = orderItemRepository.findAll();
        logger.info("Raw response from database: " + orderItems);
        return orderItems;
    }

    public Optional<OrderItem> getOrderItemById(Long id) {
        Optional<OrderItem> orderItem = orderItemRepository.findById(id);
        logger.info("Raw response from database: " + orderItem);
        return orderItem;
    }

    public OrderItem createOrderItem(OrderItem orderItem) {
        OrderItem createdOrderItem = orderItemRepository.save(orderItem);
        logger.info("Raw response from database: " + createdOrderItem);
        return createdOrderItem;
    }

    public OrderItem updateOrderItem(Long id, OrderItem orderItemDetails) {
        OrderItem orderItem = orderItemRepository.findById(id).orElseThrow(() -> new RuntimeException("Order item not found"));
        orderItem.setQuantity(orderItemDetails.getQuantity());
        orderItem.setPrice(orderItemDetails.getPrice());
        OrderItem updatedOrderItem = orderItemRepository.save(orderItem);
        logger.info("Raw response from database: " + updatedOrderItem);
        return updatedOrderItem;
    }

    public void deleteOrderItem(Long id) {
        orderItemRepository.deleteById(id);
        logger.info("Deleted order item with id: " + id);
    }
}
