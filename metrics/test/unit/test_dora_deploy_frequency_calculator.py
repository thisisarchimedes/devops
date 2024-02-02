import pytest
import pandas as pd

from src.event_processor.calculations.dora_deploy_frequency_calculator import DORADeployFrequencyCalculator

class TestDORADeployFrequencyCalculator:

    def setup_method(self) -> None:
        
        self.test_df = pd.DataFrame({
            'Day': pd.to_datetime([
                '2023-12-12',
                '2023-12-18', '2023-12-19',
                '2023-12-25', '2023-12-27',
                '2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04'
            ]),
            'DeployCount': [1,
                            2, 2,
                            1, 2,
                            1, 1, 1, 3]
        })


    def test_calculate_days_with_deploy_per_week(self):

        start_date = pd.Timestamp('2023-12-01')
        end_date = pd.Timestamp('2024-02-03')

        deploy_freq_calc = DORADeployFrequencyCalculator()
        res = deploy_freq_calc.get_days_with_deploy_per_week_from_daily_deploy_volume(daily_deploy_volume=self.test_df,
                                                                                      start_date=start_date,
                                                                                      end_date=end_date)

        # We expect DataFrame with two columns: 'Week' and 'DaysWithDeploy'.
        assert isinstance(res, pd.DataFrame)
        assert 'Week' in res.columns
        assert 'DaysWithDeploy' in res.columns

        # Expected results based on the provided test data
        expected_weeks = pd.date_range(start='2023-11-27', periods=10, freq='W-MON')
        expected_days_with_deploy = [0, 0, 1, 2, 2, 4, 0, 0, 0, 0]
        for i in range(len(expected_weeks)):
            assert res.iloc[i]['Week'] == expected_weeks[i]
            assert res.iloc[i]['DaysWithDeploy'] == expected_days_with_deploy[i]

        assert len(res) == 10


    def test_deploy_frequency_zero(self):

        start_date = pd.Timestamp('2023-12-01')
        end_date = pd.Timestamp('2024-02-03')

        deploy_freq_calc = DORADeployFrequencyCalculator()
        res = deploy_freq_calc.get_deployment_frequency(daily_deploy_volume=self.test_df,
                                                        start_date=start_date,
                                                        end_date=end_date)
        
        # Test data DaysWithDeploy: 0, 0, 1, 2, 2, 4, 0, 0, 0, 0
        # Deploy frequency should be 0
        assert res == 0

    
    def test_deploy_frequency_two(self):

        start_date = pd.Timestamp('2023-12-12')
        end_date = pd.Timestamp('2024-01-04')

        deploy_freq_calc = DORADeployFrequencyCalculator()
        res = deploy_freq_calc.get_deployment_frequency(daily_deploy_volume=self.test_df,
                                                        start_date=start_date,
                                                        end_date=end_date)
        
        # Test data DaysWithDeploy: 1, 2, 2, 4
        # Deploy frequency should be 2
        assert res == 2
