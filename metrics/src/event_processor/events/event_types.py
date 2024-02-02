from dataclasses import dataclass

@dataclass
class EventTypes:
    CALC_DEPLOY_FREQUENCY = 'calc_deploy_frequency'
    CALC_DEPLOY_LEAD_TIME = 'calc_deploy_lead_time'
    DEPLOY = 'deploy'
    PUSH = 'push'
    TEST_PASS = 'test_pass'
    TEST_RUN = 'test_run'