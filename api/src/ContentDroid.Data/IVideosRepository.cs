using ContentDroid.Models.VideoGeneration;

namespace ContentDroid.Data;

public interface IVideosRepository
{
    Task<VideoStatus> GetVideoStatusAsync(Guid id);
    Task<Guid> CreateVideoAsync();
    Task<string> GetVideoStorageUriAsync(Guid id);
}
