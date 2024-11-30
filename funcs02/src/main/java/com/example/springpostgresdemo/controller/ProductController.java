package com.example.springpostgresdemo.controller;

import com.example.springpostgresdemo.entity.Product;
import com.example.springpostgresdemo.service.ProductService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import javax.annotation.PostConstruct;
import java.util.List;

@RestController
@RequestMapping("/api/products")
public class ProductController {

    @Autowired
    private ProductService productService;

    @PostConstruct
    public void init() {
        System.out.println("rae preset: ProductController initialized");
    }

    @GetMapping
    public List<Product> getAllProducts() {
        System.out.println("rae preset: Handling GET all products request");
        return productService.getAllProducts();
    }

    @GetMapping("/{id}")
    public ResponseEntity<Product> getProductById(@PathVariable Long id) {
        System.out.println("rae preset: Handling GET product by ID request");
        return productService.getProductById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    @PostMapping
    public Product createProduct(@RequestBody Product product) {
        System.out.println("rae preset: Handling POST create product request");
        return productService.createProduct(product);
    }

    @PutMapping("/{id}")
    public ResponseEntity<Product> updateProduct(@PathVariable Long id, @RequestBody Product productDetails) {
        System.out.println("rae preset: Handling PUT update product request");
        return ResponseEntity.ok(productService.updateProduct(id, productDetails));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteProduct(@PathVariable Long id) {
        System.out.println("rae preset: Handling DELETE product request");
        productService.deleteProduct(id);
        return ResponseEntity.noContent().build();
    }
}
