package com.rezghost.content_droid.controllers;

import com.rezghost.content_droid.models.GenerationRequest;

public interface IGenerationController {
    /**
     * Generates a video based on the provided prompt.
     * 
     * @param request The request containing the prompt and other parameters
     * @return The id of the generated video
     */
    public String generateVideo(GenerationRequest request);

    /**
     * Gets the status of a video generation request by video ID.
     * 
     * @param id The ID of the video to check the status for
     * @return The status of the video generation request
     */
    public String getGenerationStatus(String id);

    /**
     * Gets the URI of the generated video by video ID.
     * 
     * @param id The ID of the video to get the URI for
     * @return The URI of the generated video
     */
    public String getGeneratedVideoUri(String id);
}
