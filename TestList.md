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
[X] Get "test pass" event and apply addition logic (send it to New Relic)
[X] Get "push" event and apply addition logic (send it to New Relic)
[] Get "deploy" event and apply addition logic (calculate frequence and send it to New Relic)


## Interface
[X] Interface Timeseries DB

# Refactor List

[] Replace existing script with the new one
[] Add auth token to header when sending post request



[
    {
        'Data': [
            {'ScalarValue': 'test_repo'}, {'ScalarValue': 'push'}, {'ScalarValue': 'event_metadata'}, {'ScalarValue': '2024-01-06 03:09:09.508000000'}, {'ScalarValue': 'test_metadata'}]
    }, 
    {
        'Data': [
            {'ScalarValue': 'test_repo'}, {'ScalarValue': 'push'}, {'ScalarValue': 'event_metadata'}, {'ScalarValue': '2024-01-06 03:09:18.073000000'}, {'ScalarValue': 'test_metadata'}]
    }, 
    {
        'Data': [{'ScalarValue': 'test_repo'}, {'ScalarValue': 'push'}, {'ScalarValue': 'event_metadata'}, {'ScalarValue': '2024-01-06 03:10:00.542000000'}, {'ScalarValue': 'test_metadata'}]
    }
]