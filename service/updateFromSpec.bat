@echo on

docker run --rm -v %CD%:/local openapitools/openapi-generator-cli:v5.4.0 validate -i /local/api.yaml --recommend

docker run --rm -v %CD%:/local -v %CD%/aspnetcore:/aspnetcore openapitools/openapi-generator-cli:v5.4.0 generate -g aspnetcore -i /local/api.yaml --package-name thumbnailService -o aspnetcore -c /local/generatorConfig.json

pause
