using System.Text.Json.Serialization;
using ContentDroid.Api.Services;
using ContentDroid.Data.Extensions;
using ContentDroid.Models.Configuration;
using Serilog;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddOpenApi();
builder.Services.AddControllers().AddJsonOptions(options =>
{
    options.JsonSerializerOptions.Converters.Add(new JsonStringEnumConverter());
});

builder.Services.AddLogging(builder =>
{
    builder.AddSerilog(new LoggerConfiguration()
        .MinimumLevel.Information()
        .WriteTo.Console()
        .CreateLogger(), dispose: true);
});

builder.Services.Configure<RabbitMQConfig>(builder.Configuration.GetSection("RabbitMQ"));
builder.Services.Configure<PostgresConfig>(builder.Configuration.GetSection("Postgres"));
builder.Services.AddTransient<IVideoGenerationService, VideoGenerationService>();
builder.Services.AddDataAccess(builder.Configuration);


var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    app.MapOpenApi();

    app.UseSwaggerUI(options =>
    {
        options.SwaggerEndpoint("/openapi/v1.json", "ContentDroid API v1");
    });
}

app.MapControllers();

app.Run();
