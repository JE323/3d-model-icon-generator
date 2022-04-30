# thumbnailService - ASP.NET Core 6.0 Server

Service for generating thumbnails from 3D models

## Run

Windows:

```
build.bat
```


Linux/OS X:

```
sh build.sh
```

## Run in Docker

```
cd src/thumbnailService
docker build -t thumbnailservice .
docker run -p 5000:8080 thumbnailservice
```
