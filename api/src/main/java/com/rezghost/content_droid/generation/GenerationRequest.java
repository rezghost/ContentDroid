package com.rezghost.content_droid.generation;

public class GenerationRequest {
    private String prompt;
    private String voice;
    private String backgroundVideoType;

    public GenerationRequest() {
    }

    public GenerationRequest(String prompt, String voice, String backgroundVideoType) {
        this.prompt = prompt;
        this.voice = voice;
        this.backgroundVideoType = backgroundVideoType;
    }

    public String getPrompt() {
        return this.prompt;
    }

    public String getVoice() {
        return this.voice;
    }

    public String getBackgroundVideoType() {
        return this.backgroundVideoType;
    }
}
