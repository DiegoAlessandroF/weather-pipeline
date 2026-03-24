CREATE USER pipeline_user WITH PASSWORD 'pipeline_pass';

GRANT ALL PRIVILEGES ON SCHEMA  raw TO pipeline_user;
GRANT ALL PRIVILEGES ON SCHEMA  staging TO pipeline_user;
GRANT ALL PRIVILEGES ON SCHEMA  mart TO pipeline_user;
