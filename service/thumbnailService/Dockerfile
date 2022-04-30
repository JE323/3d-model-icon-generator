#See https://aka.ms/containerfastmode to understand how Visual Studio uses this Dockerfile to build your images for faster debugging.

# Container we use for final publish
FROM mcr.microsoft.com/dotnet/aspnet:6.0.4-bullseye-slim AS base
WORKDIR /app
ENV ASPNETCORE_URLS http://+:80
EXPOSE 80
#EXPOSE 443

# Build container
FROM mcr.microsoft.com/dotnet/sdk:6.0.202-bullseye-slim AS build

# Copy the code into the container
WORKDIR /src
COPY ["src/thumbnailService/thumbnailService.csproj", "thumbnailService/"]

RUN dotnet clean "thumbnailService/thumbnailService.csproj"
# NuGet restore
RUN dotnet restore "thumbnailService/thumbnailService.csproj"
COPY ["src/thumbnailService/", "thumbnailService/"]

# Build the API
WORKDIR "thumbnailService"
RUN dotnet build "thumbnailService.csproj" -c Release -o /app/build

# Publish it
FROM build AS publish
RUN dotnet publish "thumbnailService.csproj" -c Release -o /app/publish

# Make the final image for publishing
FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "thumbnailService.dll"]
