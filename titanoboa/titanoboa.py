import pandas as pd

class Interpolation:

	def __init__(self, historical, column, method):
		self.historical = historical
		self.column = column
		self.method = method

	def apply(self, axes):
		joined = pd.concat([self.historical.raw, axes.points])
		print(joined)
		cleared = joined.groupby(joined.index).first()
		interpolated = cleared.interpolate(self.method)
		return interpolated

class Extrapolation:

	def __init__(self, historical, column, method):
		self.historical = historical
		self.column = column
		self.method = method


class TimeAxes():

	def __init__(self, historical, expanding):
		self.historical = historical
		self.start = pd.to_datetime(expanding[0] if expanding[0] is not None else self.historical.raw.index.min())
		self.end = pd.to_datetime(expanding[1] if expanding[1] is not None else self.historical.raw.index.max())
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

class Historical:

	def convert_raw(self, raw):
		if isinstance(raw, pd.DataFrame):
			return raw
		else:
			return pd.DataFrame(raw)

	def __init__(self, raw):
		self.raw = self.convert_raw(raw)
		empty_filling = zip(self.raw.columns, [None]*len(self.raw.columns))
		self.interpolates = {'temperature' : 'linear'} #{empty_filling}
		self.extrapolates = {empty_filling}

	def __getitem__(self, expanding):
		axes = TimeAxes(self, expanding)
		interpolated = Interpolation(self, None, 'linear').apply(axes)
		return interpolated

	def interpolate(self, method, columns=None):
		return self


