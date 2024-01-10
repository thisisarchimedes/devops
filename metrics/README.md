

export API_DEVOPS_EVENT_CATCHER

aws configure

DATABASE_NAME = 'DORAStats'
    TABLE_NAME = 'DORARawEvents'

    DATABASE_NAME = 'DORAStats'
    TABLE_NAME = 'DORARawEventsTest'



     db_connection.write_event_to_db(pd.DataFrame([{
            "Time": [datetime.now()],
            "Repo": 'test_repo',
            "Event": 'calc_deploy_frequency',
            "Metadata": '{test_metadata: value}'
        }]))

        Time must be a string
        Metadata have to be a string
        Every thing is a json string or just a string



        SECRET_STORE_NAME=DevOpsSecretStore


# env var
SECRET_STORE_NAME=DevOpsSecretStore
DEVOPS_DB_NAME="DORAStats"
DEVOPS_TABLE_NAME="DORARawEventsTest"
DEPLOYMENT_FREQ_TIMEFRAME_DAYS=30

# Secret
LOGGER_API_KEY="67aec8303d8caa6b30e56ea2b380affeFFFFNRAL"
SECRET_TOKEN="secret_token_123"
