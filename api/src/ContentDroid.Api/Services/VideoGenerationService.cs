using ContentDroid.Data;
using ContentDroid.Models.Configuration;
using ContentDroid.Models.VideoGeneration;
using Microsoft.Extensions.Options;

namespace ContentDroid.Api.Services;

public class VideoGenerationService(IOptions<RabbitMQConfig> deploymentConfig, IVideosRepository videosRepository, IVideosQueueService videosQueueService) : IVideoGenerationService
{
    private readonly RabbitMQConfig _rabbitMQConfig = deploymentConfig.Value;
    private readonly IVideosRepository _videosRepository = videosRepository;
    private readonly IVideosQueueService _videosQueueService = videosQueueService;

    /// <inheritdoc/>
    public async Task<Guid> GenerateTextVideoAsync(TextVideoGenerationRequest request)
    {
        var videoId = await _videosRepository.CreateVideoAsync();

        var queueRequest = new TextVideoGenerationRequest
        {
            VideoId = videoId,
            Dialogue = request.Dialogue
        };

        await _videosQueueService.QueueTextVideoAsync(queueRequest);

        return videoId;
    }

    /// <inheritdoc/>
    public async Task<VideoStatus> GetVideoStatusAsync(Guid videoId)
    {
        var videoStatus = await _videosRepository.GetVideoStatusAsync(videoId);
        return videoStatus;
    }

    /// <inheritdoc/>
    public async Task<string> GetVideoStorageUriAsync(Guid videoId)
    {
        var storageUri = await _videosRepository.GetVideoStorageUriAsync(videoId);
        return storageUri;
    }
}