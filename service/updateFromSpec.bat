@echo on

docker run --rm -v %CD%:/local openapitools/openapi-generator-cli:v6.0.0-beta validate -i /local/api.yaml --recommend

docker run --rm -v %CD%:/local -v %CD%/aspnetcore:/aspnetcore openapitools/openapi-generator-cli:v6.0.0-beta generate -g aspnetcore -i /local/api.yaml --package-name thumbnailService -o aspnetcore -c /local/generatorConfig.json

pause
