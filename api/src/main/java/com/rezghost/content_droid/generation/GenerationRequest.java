package com.rezghost.content_droid.generation;

public class GenerationRequest {
    private String prompt;

    public GenerationRequest() {
    }

    public GenerationRequest(String prompt) {
        this.prompt = prompt;
    }

    public String getPrompt() {
        return this.prompt;
    }

    public void setPrompt(String prompt) {
        this.prompt = prompt;
    }
}
