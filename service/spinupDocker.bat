@echo off

REM Rebuild the service image from the latest source
docker build -t thumbnail_service aspnetcore

docker-compose up -d

pause
