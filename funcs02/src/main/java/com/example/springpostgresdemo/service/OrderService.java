package com.example.springpostgresdemo.service;

import com.example.springpostgresdemo.entity.Order;
import com.example.springpostgresdemo.repository.OrderRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;
import java.util.logging.Logger;

@Service
public class OrderService {

    private static final Logger logger = Logger.getLogger(OrderService.class.getName());

    @Autowired
    private OrderRepository orderRepository;

    public List<Order> getAllOrders() {
        List<Order> orders = orderRepository.findAll();
        logger.info("Raw response from database: " + orders);
        return orders;
    }

    public Optional<Order> getOrderById(Long id) {
        Optional<Order> order = orderRepository.findById(id);
        logger.info("Raw response from database: " + order);
        return order;
    }

    public Order createOrder(Order order) {
        Order createdOrder = orderRepository.save(order);
        logger.info("Raw response from database: " + createdOrder);
        return createdOrder;
    }

    public Order updateOrder(Long id, Order orderDetails) {
        Order order = orderRepository.findById(id).orElseThrow(() -> new RuntimeException("Order not found"));
        order.setTotalAmount(orderDetails.getTotalAmount());
        order.setOrderDate(orderDetails.getOrderDate());
        Order updatedOrder = orderRepository.save(order);
        logger.info("Raw response from database: " + updatedOrder);
        return updatedOrder;
    }

    public void deleteOrder(Long id) {
        orderRepository.deleteById(id);
        logger.info("Order deleted from database with id: " + id);
    }
}
