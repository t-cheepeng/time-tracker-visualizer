import unittest
import pandas as pd
import pandas.testing as pt
from src.services import data_service

class TestDataService(unittest.TestCase):
    test_bundle_data = ''

    def setUp(self):
        self.test_bundle_data = pd.read_csv('.\\test\\data\\test_bundle_1.csv')

    def test_sum_time_by_tag(self):
        sum_time_by_tag = data_service.sum_time_by_tag(self.test_bundle_data)
        expected_df = pd.DataFrame({
            'Tags': [
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
            'Duration (decimal)': [
                7.63, 1.51, 3.42, 1.20, 13.46, 4.93, 23.88, 1.20, 7.66
            ]
        })

        pt.assert_frame_equal(sum_time_by_tag, expected_df, check_exact=False)
        
    def test_sum_time(self):
        sum_time = data_service.sum_time(self.test_bundle_data)

        self.assertEqual(64.89, sum_time)
        