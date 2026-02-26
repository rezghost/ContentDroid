package com.rezghost.content_droid.services;

import java.util.Map;
import java.util.UUID;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;
import com.google.gson.Gson;
import com.rezghost.content_droid.models.VideoEntity;
import com.rezghost.content_droid.models.VideoStatus;
import com.rezghost.content_droid.repository.VideosRepository;

import jakarta.annotation.PostConstruct;

@Service
public class GenerationService implements IGenerationService {

    private Connection connection;
    private Channel channel;
    private Logger logger;
    private final VideosRepository videosRepository;
    private final String queueName;
    private final String rabbitHost;
    private final int rabbitPort;
    private final String rabbitUser;
    private final String rabbitPassword;
    private final String rabbitVhost;
    private final Gson gson = new Gson();

    public GenerationService(
            VideosRepository videosRepository,
            @Value("${app.rabbitmq.queue-name:videos}") String queueName,
            @Value("${app.rabbitmq.host:localhost}") String rabbitHost,
            @Value("${app.rabbitmq.port:5672}") int rabbitPort,
            @Value("${app.rabbitmq.username:guest}") String rabbitUser,
            @Value("${app.rabbitmq.password:guest}") String rabbitPassword,
            @Value("${app.rabbitmq.vhost:/}") String rabbitVhost) {
        this.videosRepository = videosRepository;
        this.queueName = queueName;
        this.rabbitHost = rabbitHost;
        this.rabbitPort = rabbitPort;
        this.rabbitUser = rabbitUser;
        this.rabbitPassword = rabbitPassword;
        this.rabbitVhost = rabbitVhost;
    }

    @PostConstruct
    public void init() throws Exception {
        ConnectionFactory factory = new ConnectionFactory();
        factory.setHost(rabbitHost);
        factory.setPort(rabbitPort);
        factory.setUsername(rabbitUser);
        factory.setPassword(rabbitPassword);
        factory.setVirtualHost(rabbitVhost);
        factory.setAutomaticRecoveryEnabled(true);

        this.connection = factory.newConnection();
        this.channel = connection.createChannel();
        this.channel.queueDeclare(queueName, true, false, false, null);
        this.logger = LoggerFactory.getLogger(GenerationService.class);
    }

    /**
     * 
     * {@inheritDoc}
     */
    @Transactional
    public String sendGenerationRequest(String prompt) {
        try {
            VideoEntity savedVideo = videosRepository.save(VideoEntity.newPending());
            String guid = savedVideo.getId().toString();
            String jsonPayload = gson.toJson(Map.of("id", guid, "prompt", prompt));

            channel.basicPublish("", queueName, null, jsonPayload.getBytes(java.nio.charset.StandardCharsets.UTF_8));
            logger.info("[x] Sent: " + guid);

            return guid;
        } catch (Exception e) {
            e.printStackTrace();
        }

        return "";
    }

    /**
     * 
     * {@inheritDoc}
     */
    public String getGenerationStatus(String videoId) {
        UUID id = UUID.fromString(videoId);
        VideoEntity video = videosRepository.findById(id).orElseThrow();

        return video.getStatus().toString();
    }

    /**
     * 
     * {@inheritDoc}
     */
    public String getGeneratedVideoUri(String videoId) {
        UUID id = UUID.fromString(videoId);
        VideoEntity video = videosRepository.findById(id).orElseThrow();

        if (video.getStatus() != VideoStatus.COMPLETE) {
            throw new IllegalStateException("Video generation is not completed yet.");
        }

        return video.getStorageKey();
    }
}
