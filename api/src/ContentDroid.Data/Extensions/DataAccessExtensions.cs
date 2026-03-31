using ContentDroid.Models.Configuration;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Npgsql;

namespace ContentDroid.Data.Extensions;

public static class DataAccessExtensions
{
    public static IServiceCollection AddDataAccess(this IServiceCollection services, IConfiguration configuration)
    {
        var postgresConfig = new PostgresConfig();
        configuration.GetSection("Postgres").Bind(postgresConfig);

        var connectionString = $"Host={postgresConfig.Host};Port={postgresConfig.Port};Database={postgresConfig.Database};Username={postgresConfig.User};Password={postgresConfig.Password}";

        services.AddSingleton(NpgsqlDataSource.Create(connectionString));
        services.AddTransient<IVideosRepository, VideosRepository>();

        return services;
    }
}