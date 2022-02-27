# thumbnailService - ASP.NET Core 5.0 Server

Service for generating thumbnails from 3D models

## Run

Linux/OS X:

```
sh build.sh
```

Windows:

```
build.bat
```
## Run in Docker

```
cd src/thumbnailService
docker build -t thumbnailservice .
docker run -p 5000:8080 thumbnailservice
```
