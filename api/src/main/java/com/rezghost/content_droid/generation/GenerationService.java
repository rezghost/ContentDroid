package com.rezghost.content_droid.generation;

import org.springframework.stereotype.Service;

import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;

import jakarta.annotation.PostConstruct;

@Service
public class GenerationService {

    private static final String QUEUE_NAME = "videos";
    private Connection connection;
    private Channel channel;

    @PostConstruct
    public void init() throws Exception {
        ConnectionFactory factory = new ConnectionFactory();
        factory.setHost("localhost");

        this.connection = factory.newConnection();
        this.channel = connection.createChannel();
        this.channel.queueDeclare(QUEUE_NAME, true, false, false, null);
    }

    public void sendGenerationRequest(String prompt) {
        try {
            channel.basicPublish("", QUEUE_NAME, null, prompt.getBytes());
            System.out.println("[x] Sent: " + prompt);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}