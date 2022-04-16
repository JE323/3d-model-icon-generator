@echo on

docker run --rm -v %CD%:/local openapitools/openapi-generator-cli:v6.0.0-beta validate -i /local/api.yaml --recommend

pause
