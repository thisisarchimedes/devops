

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