import pandas as pd

class Interpolation:

	def __init__(self, historical, column, method):
		self.historical = historical
		self.column = column
		self.method = method

	def apply(self, axes):
		joined = pd.concat([self.historical, axes.points])
		cleared = joined.groupby(joined.index).first()
		interpolated = cleared.interpolate(self.method, limit_direction='both')
		return interpolated

	def __getitem__(self, expanding):
		axes = TimeAxes(self, expanding)
		interpolated = self.apply(axes)
		return Historical(interpolated)

class Extrapolation:

	def __init__(self, historical, column, method):
		self.historical = historical
		self.column = column
		self.method = method


class TimeAxes():

	def __init__(self, historical, expanding):
		self.historical = historical
		self.start = pd.to_datetime(expanding[0] if expanding[0] is not None else self.historical.index.min())
		self.end = pd.to_datetime(expanding[1] if expanding[1] is not None else self.historical.index.max())
		self.step = expanding[2]
		self.points = self.build()

	def build(self):
		dates = []
		d = self.start
		while d < self.end:
			dates.append(d)
			d = d + pd.DateOffset(self.step)
		print(dates)
		expanded = pd.DataFrame(index=dates, data=None)
		return expanded

class Historical(pd.DataFrame):

	def __init__(self, data):
		super().__init__(data)
		empty_filling = zip(self.columns, [None]*len(self.columns))
		self.interpolates = {'temperature' : 'linear'} #{empty_filling}
		self.extrapolates = {empty_filling}

	def interpolate(self, method, columns=None):
		return Interpolation(self, method=method, column=None)

	def expand(self, *expanding):
		for e in expanding:
			df = self
			if e in ['weekday', 'month', 'year']:
				df[e] = getattr(self.index, e)
		return df


