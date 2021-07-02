import unittest
import pandas as pd
import pandas.testing as pt
from src.services import data_service
import src.constants as const

class TestDataService(unittest.TestCase):
    test_bundle_data = ''

    def setUp(self):
        # Bundle 1 is not representative of actual user data. There exist overlapping timings
        self.test_bundle_data = pd.read_csv('.\\test\\data\\test_bundle_1.csv')
        self.test_bundle_data.rename(columns=const.col_name_map, inplace=True)

    def test_sum_time_by_tag(self):
        sum_time_by_tag = data_service.sum_time_by_criteria(self.test_bundle_data, [const.tags])
        expected_df = pd.DataFrame({
            const.tags: [
                'Downtime (Watching Shows, Gaming, Resting, Taking a Break)',
                'Exercising (Run, Swim, Workout)',
                'Hobbies (Music, Cooking)',
                'M18+ (You know what :)',
                'Primary Work (Job, Studying)',
                'Side Projects (Other Coding Projects)',
                'Sleep',
                'Socialising (Chatting, Hanging Out)',
                'Surviving (Groceries, Eating, Hygiene)'
            ],
            const.time_in_decmial: [
                7.63, 1.51, 3.42, 1.20, 13.46, 4.93, 23.88, 1.20, 7.66
            ]
        })

        pt.assert_frame_equal(sum_time_by_tag, expected_df, check_exact=False)
        
    def test_sum_time(self):
        sum_time = data_service.sum_time(self.test_bundle_data)

        self.assertEqual(64.89, sum_time)
    
    def test_sum_time_by_workweek(self):
        workweek = data_service.sum_time_by_workweek(self.test_bundle_data, sum_by_workweek=True)
        non_workweek = data_service.sum_time_by_workweek(self.test_bundle_data, sum_by_workweek=False)
        
        exp_workweek_df = pd.DataFrame({
            const.tags: [
                'Downtime (Watching Shows, Gaming, Resting, Taking a Break)',
                'Exercising (Run, Swim, Workout)',
                'Hobbies (Music, Cooking)',
                'M18+ (You know what :)',
                'Primary Work (Job, Studying)',
                'Side Projects (Other Coding Projects)',
                'Sleep',
                'Socialising (Chatting, Hanging Out)',
                'Surviving (Groceries, Eating, Hygiene)'
            ],
            const.time_in_decmial: [
                7.63, 1.51, 3.42, 1.20, 13.46, 4.93, 23.88, 1.20, 7.66
            ]
        })
        exp_non_workweek_df = pd.DataFrame({
            const.tags: [
                'Sleep',
                'Surviving (Groceries, Eating, Hygiene)'
            ],
            const.time_in_decmial: [
                7.73, 0.10
            ]
        })

        pt.assert_frame_equal(workweek, exp_workweek_df, check_exact=False)
        pt.assert_frame_equal(
            non_workweek, exp_non_workweek_df, check_exact=False)
