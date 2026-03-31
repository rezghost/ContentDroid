using ContentDroid.Api.Services;
using ContentDroid.Models.VideoGeneration;
using Microsoft.AspNetCore.Mvc;

namespace ContentDroid.Api.Controllers;

[ApiController]
[Route("api/v1/videos")]
public class VideoController(IVideoGenerationService videoGenerationService) : ControllerBase
{
    private readonly IVideoGenerationService _videoGenerationService = videoGenerationService;

    [HttpPost("generate")]
    [ProducesResponseType(typeof(Guid), StatusCodes.Status201Created)]
    public async Task<IActionResult> GenerateTextVideo([FromBody] TextVideoGenerationRequest request)
    {
        var videoId = await _videoGenerationService.GenerateTextVideoAsync(request);

        return Created(videoId.ToString(), videoId);
    }

    [HttpGet("{videoId}/status")]
    [ProducesResponseType(typeof(VideoStatus), StatusCodes.Status200OK)]
    public async Task<IActionResult> GetVideoStatus(Guid videoId)
    {
        var status = await _videoGenerationService.GetVideoStatusAsync(videoId);
        return Ok(status);
    }

    [HttpGet("{videoId}/uri")]
    [ProducesResponseType(typeof(string), StatusCodes.Status200OK)]
    public async Task<IActionResult> GetVideoStorageUri(Guid videoId)
    {
        var uri = await _videoGenerationService.GetVideoStorageUriAsync(videoId);
        return Ok(uri);
    }
}