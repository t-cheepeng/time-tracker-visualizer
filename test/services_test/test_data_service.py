import unittest
from numpy import float64
import pandas as pd
import pandas.testing as pt
import src.constants as const
from src.services import data_service

class TestDataService(unittest.TestCase):
    test_bundle_data_1 = ''
    test_bundle_data_2 = ''

    def setUp(self):
        # Bundle 1 is not representative of actual user data. There exist overlapping timings
        self.test_bundle_data_1 = pd.read_csv('.\\test\\data\\test_bundle_1.csv')
        self.test_bundle_data_1.rename(columns=const.col_name_map, inplace=True)

        # Bundle 2 contains carryover entries
        self.test_bundle_data_2 = pd.read_csv('.\\test\\data\\test_bundle_2.csv')
        self.test_bundle_data_2.rename(columns=const.col_name_map, inplace=True)

    def test_sum_time_by_tag(self):
        sum_time_by_tag = data_service.sum_time_by_criteria(self.test_bundle_data_1, [const.tags])
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
                7.63, 1.51, 3.42, 1.20, 13.46, 4.93, 31.61, 1.20, 7.76
            ]
        })

        pt.assert_frame_equal(sum_time_by_tag, expected_df, check_exact=False)
        
    def test_sum_time(self):
        sum_time = data_service.sum_time(self.test_bundle_data_1)

        self.assertEqual(72.72, sum_time)
    
    def test_sum_time_by_workweek(self):
        workweek = data_service.sum_time_by_workweek(self.test_bundle_data_1, sum_by_workweek=True)
        non_workweek = data_service.sum_time_by_workweek(self.test_bundle_data_1, sum_by_workweek=False)
        
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

    def test_split_carryovers(self):
        df = data_service.split_carryovers(self.test_bundle_data_2)
        # Weird bug where object comparison cause the frames to be unequal even though they have same value
        df[[const.start_time, const.end_time]] = df[[const.start_time, const.end_time]].astype(str)
        df[const.time_in_decmial] = df[const.time_in_decmial].astype(float64)
        mask = df[[const.start_date, const.start_time, const.end_date,
                   const.end_time, const.time_in_hours, const.time_in_decmial]]
        
        exp_df = pd.DataFrame({
            const.start_date: ['08/06/2021', '08/06/2021', '09/06/2021', '30/06/2021', '01/07/2021'],
            const.start_time: ['00:04:25', '23:53:31', '00:00:00', '23:30:00', '00:00:00'],
            const.end_date: ['08/06/2021', '08/06/2021',
                               '09/06/2021', '30/06/2021', '01/07/2021'],
            const.end_time: ['08:03:23', '23:59:59', '08:03:58', '23:59:59', '08:00:00'],
            const.time_in_hours: ['07:58:58', '00:06:28', '08:03:58', '00:29:59', '08:00:00'],
            const.time_in_decmial: [7.98, 0.11, 8.07, 0.50, 8.00],
        })

        pt.assert_frame_equal(mask, exp_df, check_exact=False)

