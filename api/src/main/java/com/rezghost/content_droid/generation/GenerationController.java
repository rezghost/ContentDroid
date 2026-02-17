package com.rezghost.content_droid.generation;

import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class GenerationController {
    @PostMapping("/generate")
    public String generate(@RequestBody GenerationRequest request) {
        return "Hello, " + request.getPrompt() + "!";
    }
}
