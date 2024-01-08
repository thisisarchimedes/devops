# Architecture


1. Python script that runs in Github Actions and sends JSON events to AWS endpoint (not directly to DB so we can change DB or work directly with webhooks) 
2. API endpoint that receives events from Github Actions and stores them in a DB (need to authenticate and validate input)
2.1. If needed run logic around the input (like recalculate frequency of deployments)
2.2. Send to New Relic


# Test List

## CICD Python Script
[X] Get unsupported event and fail
[X] Get supported event and generate JSON file
[X] Send generated JSON to the API endpoint

## Backend API
[X] Get check authentication
[X] Get payload and validate payload correctness
[X] Get payload and store it in the DB
[X] Get "test pass" event and apply addition logic (record to DB)
[X] Get "push" event and apply addition logic (record to DB)
[] Add "calc_deploy_frequency" event (with ALL as repo name) and write to DB
[] Get "deploy" event and apply addition logic (calculate frequencey for all repos and record to DB)
[] Get "deploy" event and apply addition logic (calculate frequencey a subset of repos and record to DB) - probably need to load config file that define different subsets of repos
[] repeat the above event tests and also send to New Relic


## Interface
[X] Interface Timeseries DB

# Refactor List

[X] Refactor db_connection_timeseris
[] Replace existing script with the new one
[] Add auth token to header when sending post request


# TODO: 

