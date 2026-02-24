package com.rezghost.content_droid.services;

public interface IGenerationService {

    /**
     * Sends a generation request with the given prompt.
     * 
     * @param prompt The prompt to be sent for generation
     * @return A unique identifier for the generation request
     */
    String sendGenerationRequest(String prompt);

    /**
     * Gets status of video generation by video ID.
     * 
     * @param videoId The video ID to retrieve status for
     * @return The status of the video generation
     */
    String getGenerationStatus(String videoId);

    /**
     * Gets URI of generated video by video ID.
     * 
     * @param videoId The video ID to retrieve URI for
     * @return The URI of the generated video
     */
    String getGeneratedVideoUri(String videoId);
}
