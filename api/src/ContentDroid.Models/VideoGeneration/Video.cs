namespace ContentDroid.Models.VideoGeneration;

public class Video
{
    public Guid Id { get; set; }

    public string? StorageKey { get; set; }

    public string? FileName { get; set; }

    public long? FileSizeBytes { get; set; }

    public string MimeType { get; set; } = "video/mp4";

    public VideoStatus Status { get; set; } = VideoStatus.Pending;

    public short? Progress { get; set; }

    public string? ErrorCode { get; set; }

    public string? ErrorMessage { get; set; }

    public DateTimeOffset CreatedAt { get; set; }

    public DateTimeOffset? StartedAt { get; set; }

    public DateTimeOffset? CompletedAt { get; set; }

    public DateTimeOffset UpdatedAt { get; set; }
}
