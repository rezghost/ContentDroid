package com.rezghost.content_droid.controllers;

import org.apache.coyote.BadRequestException;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import com.rezghost.content_droid.models.GenerationRequest;
import com.rezghost.content_droid.services.GenerationService;

@RestController
public class GenerationController {
    private final GenerationService generationService;

    public GenerationController(GenerationService generationService) {
        this.generationService = generationService;
    }

    @PostMapping("/generate")
    public String generate(@RequestBody GenerationRequest request) {
        String videoId = generationService.sendGenerationRequest(request.getPrompt());
        return videoId;
    }

    @GetMapping("/status/{id}")
    public String getStatus(@PathVariable String id) {
        try {
            return generationService.getGenerationStatus(id);
        } catch (Exception e) {
            return new BadRequestException().getMessage();
        }
    }
}
