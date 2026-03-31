using System.Text;
using ContentDroid.Models.Configuration;
using ContentDroid.Models.VideoGeneration;
using RabbitMQ.Client;

namespace ContentDroid.Api.Services;

public class VideosQueueService : IVideosQueueService
{
    private readonly RabbitMQConfig _rabbitConfig;
    private readonly ConnectionFactory _connectionFactory;
    private readonly ILogger<VideosQueueService> _logger;

    public VideosQueueService(RabbitMQConfig rabbitConfig, ILogger<VideosQueueService> logger)
    {
        _rabbitConfig = rabbitConfig;
        _logger = logger;
        _connectionFactory = new ConnectionFactory
        {
            HostName = _rabbitConfig.RabbitHost,
            Port = _rabbitConfig.RabbitPort,
            UserName = _rabbitConfig.RabbitUser,
            Password = _rabbitConfig.RabbitPassword,
            VirtualHost = _rabbitConfig.RabbitVhost
        };
    }

    /// <inheritdoc/>
    public async Task QueueTextVideoAsync(TextVideoGenerationRequest request)
    {
        using var connection = await _connectionFactory.CreateConnectionAsync();
        using var channel = await connection.CreateChannelAsync();

        await channel.QueueDeclareAsync(
            queue: _rabbitConfig.TextVideoQueueName,
            durable: true,
            exclusive: false,
            autoDelete: false,
            arguments: new Dictionary<string, object?> { { "x-queue-type", "quorum" }
        });

        var body = Encoding.UTF8.GetBytes(request.Dialogue);
        await channel.BasicPublishAsync(exchange: string.Empty, routingKey: _rabbitConfig.TextVideoQueueName, body: body);
        _logger.LogInformation("Enqueued text video generation request for: {VideoId}", request.VideoId);
    }
}