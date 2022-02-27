@echo on

docker run --rm -v %CD%:/local openapitools/openapi-generator-cli:v5.4.0 validate -i /local/api.yaml --recommend

pause
