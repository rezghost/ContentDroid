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
public class GenerationController implements IGenerationController {
    private final GenerationService generationService;

    public GenerationController(GenerationService generationService) {
        this.generationService = generationService;
    }

    /**
     * 
     * {@inheritDoc}
     */
    @PostMapping("/generate")
    public String generateVideo(@RequestBody GenerationRequest request) {
        String videoId = generationService.sendGenerationRequest(request.getPrompt());
        return videoId;
    }

    /**
     * 
     * {@inheritDoc}
     */
    @GetMapping("/status/{id}")
    public String getGenerationStatus(@PathVariable("id") String id) {
        try {
            return generationService.getGenerationStatus(id);
        } catch (Exception e) {
            return new BadRequestException().getMessage();
        }
    }

    /**
     * 
     * {@inheritDoc}
     */
    @GetMapping("/video/{id}")
    public String getGeneratedVideoUri(@PathVariable("id") String id) {
        try {
            return generationService.getGeneratedVideoUri(id);
        } catch (Exception e) { // TODO: catch specific exceptions and return appropriate status codes
            return new BadRequestException().getMessage();
        }
    }
}
