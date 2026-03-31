using ContentDroid.Models.VideoGeneration;
using Dapper;
using Npgsql;

namespace ContentDroid.Data;

public class VideosRepository(NpgsqlDataSource dataSource) : IVideosRepository
{
    private readonly NpgsqlDataSource _dataSource = dataSource;

    public async Task<Guid> CreateVideoAsync()
    {
        await using var connection = await _dataSource.OpenConnectionAsync();

        var videoId = connection.Query<Guid>(
            """
            INSERT INTO videos
            DEFAULT VALUES
            RETURNING id;
            """
        );

        return videoId.Single();
    }

    public async Task<VideoStatus> GetVideoStatusAsync(Guid id)
    {
        await using var connection = await _dataSource.OpenConnectionAsync();

        var rawStatus = await connection.QuerySingleAsync<string>(
            """
            SELECT status::text FROM videos
            WHERE id = @Id;
            """,
            new { Id = id }
        );

        if (Enum.TryParse<VideoStatus>(rawStatus, ignoreCase: true, out var videoStatus))
        {
            return videoStatus;
        }

        throw new InvalidOperationException($"Unknown video status '{rawStatus}' returned from the database.");
    }

    public async Task<string> GetVideoStorageUriAsync(Guid id)
    {
        await using var connection = await _dataSource.OpenConnectionAsync();
        var sql = """
            SELECT storage_uri FROM videos
            WHERE id = @Id;
            """;

        var storageUri = connection.Query<string>(sql, new { Id = id }).Single();
        return storageUri;
    }
}
