import unittest
import os
import sequentia as seq
import pandas as pd

class TestProjector(unittest.TestCase):

	def setUp(self):
		demo = {'date': ['01-01-2019', '01-03-2019', '01-04-2019'],
				'temperature': [1, 3, 4]}
		df = pd.DataFrame(demo)
		df['date'] = pd.to_datetime(df['date'])
		df = df.set_index('date')
		self.df = df

	def test_demo_missed(self):
		# 2nd january is lacked
		h = seq.Historical(self.df)
		daily = h.interpolate('linear')['12-31-2018','01-06-2019',1]
		missed_must_be = 2
		print(daily.head())
		self.assertEqual(daily['temperature']['01-02-2019'], missed_must_be)

	def test_expand(self):
		h = seq.Historical(self.df).expand('month', 'year')
		print(h.head())
		
	# def test_fragmentation(self):
	# 	demo = {'date': ['01-01-2019', '01-03-2019', '01-04-2019'],
	# 			'temperature': [1, 3, 4]}
	# 	h = tnb.Historical(df)
	# 	f = h.fragmentate(['28days','1day'], names=['past', 'target'])[::'1day']
	# 	past_aggr = {
	# 		'weekly': lambda x: x[::7],
	# 		'max': lambda x: x.max(),
	# 		'std': lambda x: x.std()
	# 	}
	# 	result = f.apply(past=past_aggr, target=lambda x: x[0])
	# 	result = 


if __name__ == '__main__':
    unittest.main()