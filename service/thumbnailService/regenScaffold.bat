cd src/thumbnailService

dotnet ef dbcontext scaffold "Host=localhost;Port=5432;Database=database;Username=postgres;Password=admin" -f -o "Entities/Sql" --context-dir "Context" -c "ModelThumbnailDBContext" --no-pluralize Npgsql.EntityFrameworkCore.PostgreSQL

pause
