package com.rezghost.content_droid.generation;

import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class GenerationController {
    private final GenerationService generationService;

    public GenerationController(GenerationService generationService) {
        this.generationService = generationService;
    }

    @PostMapping("/generate")
    public String generate(@RequestBody GenerationRequest request) {
        generationService.sendGenerationRequest(request.getPrompt());
        return "Generation request sent for prompt: " + request.getPrompt();
    }
}
