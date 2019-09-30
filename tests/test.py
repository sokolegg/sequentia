import unittest
import os
import titanoboa as tnb
import pandas as pd

class TestProjector(unittest.TestCase):

	def setUp(self):
		pass

	def test_demo_missed(self):
		# 2nd january is lacked
		demo = {'date': ['01-01-2019', '01-03-2019', '01-04-2019'],
				'temperature': [1, 3, 4]}
		df = pd.DataFrame(demo)
		df['date'] = pd.to_datetime(df['date'])
		df = df.set_index('date')
		h = tnb.Historical(df)
		daily = h.interpolate('linear')['01-01-2019','01-05-2019',1]
		missed_must_be = 2
		self.assertEqual(daily['temperature'][1], missed_must_be)
		

if __name__ == '__main__':
    unittest.main()