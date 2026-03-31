namespace ContentDroid.Models.Configuration;

public class RabbitMQConfig
{
    public required string TextVideoQueueName { get; set; }
    public required string RabbitHost { get; set; }
    public int RabbitPort { get; set; }
    public required string RabbitUser { get; set; }
    public required string RabbitPassword { get; set; }
    public required string RabbitVhost { get; set; }
}