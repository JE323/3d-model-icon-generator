:: Generated by: https://openapi-generator.tech
::

@echo off

dotnet restore src\thumbnailService
dotnet build src\thumbnailService
echo Now, run the following to start the project: dotnet run -p src\thumbnailService\thumbnailService.csproj --launch-profile web.
echo.
