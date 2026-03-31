namespace ContentDroid.Models.VideoGeneration;

public class TextVideoGenerationRequest
{
    public required Guid VideoId { get; set; }
    public required string Dialogue { get; set; }
}
