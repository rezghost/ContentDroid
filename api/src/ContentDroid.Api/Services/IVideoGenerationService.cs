using ContentDroid.Models.VideoGeneration;

namespace ContentDroid.Api.Services;

public interface IVideoGenerationService
{
    /// <summary>
    /// Generates a video based on the provided text dialogue.  
    /// </summary>
    /// <param name="request">The request containing the text dialogue <see cref="TextVideoGenerationRequest"/></param>
    /// <returns>Task</returns>
    Task<Guid> GenerateTextVideoAsync(TextVideoGenerationRequest request);

    /// <summary>
    /// Gets the status of a video.
    /// </summary>
    /// <param name="videoId">The ID of the video.</param>
    /// <returns>The status of the video. <see cref="VideoStatus"/> </returns>
    Task<VideoStatus> GetVideoStatusAsync(Guid videoId);

    /// <summary>
    /// Gets the storage URI of a video.
    /// </summary>
    /// <param name="videoId">The ID of the video.</param>
    /// <returns>The storage URI of the video.</returns>
    Task<string> GetVideoStorageUriAsync(Guid videoId);
}