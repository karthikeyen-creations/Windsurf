package com.example.springpostgresdemo.service;

import com.example.springpostgresdemo.entity.Product;
import com.example.springpostgresdemo.repository.ProductRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;
import java.util.logging.Logger;

@Service
public class ProductService {

    private static final Logger logger = Logger.getLogger(ProductService.class.getName());

    @Autowired
    private ProductRepository productRepository;

    public List<Product> getAllProducts() {
        List<Product> products = productRepository.findAll();
        logger.info("Raw response from database: " + products);
        return products;
    }

    public Optional<Product> getProductById(Long id) {
        Optional<Product> product = productRepository.findById(id);
        logger.info("Raw response from database: " + product);
        return product;
    }

    public Product createProduct(Product product) {
        Product createdProduct = productRepository.save(product);
        logger.info("Raw response from database: " + createdProduct);
        return createdProduct;
    }

    public Product updateProduct(Long id, Product productDetails) {
        Product product = productRepository.findById(id).orElseThrow(() -> new RuntimeException("Product not found"));
        product.setProductName(productDetails.getProductName());
        product.setPrice(productDetails.getPrice());
        product.setStock(productDetails.getStock());
        Product updatedProduct = productRepository.save(product);
        logger.info("Raw response from database: " + updatedProduct);
        return updatedProduct;
    }

    public void deleteProduct(Long id) {
        productRepository.deleteById(id);
        logger.info("Raw response from database: Product with id " + id + " deleted");
    }
}
