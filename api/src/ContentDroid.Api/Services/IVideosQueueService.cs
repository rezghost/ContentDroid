using ContentDroid.Models.VideoGeneration;

namespace ContentDroid.Api.Services;

public interface IVideosQueueService
{
    /// <summary>
    /// Enqueues a text video generation request.
    /// </summary>
    /// <param name="request">The text video generation request. <see cref="TextVideoGenerationRequest"/> </param>
    /// <returns>Task</returns>
    Task QueueTextVideoAsync(TextVideoGenerationRequest request);
}