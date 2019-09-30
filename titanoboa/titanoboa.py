import pandas as pd 

class Historical:

	def convert_raw(self, raw):
		if isinstance(raw, pd.DataFrame):
			return raw
		else:
			return pd.DataFrame(raw)

	def __init__(self, raw):
		self.raw = self.convert_raw(raw)
		empty_filling = zip(self.raw.columns, [None]*len(self.raw.columns))
		self.interpolates = {empty_filling}
		self.extrapolates = {empty_filling}

	def __getitem__(self, expanding):
		print(expanding)
		step = 1 # expanding one day parser
		start = pd.to_datetime(expanding[0] if expanding[0] is not None else self.raw.index.min())
		end = pd.to_datetime(expanding[1] if expanding[1] is not None else self.raw.index.max())
		dates = []
		d = start
		while d < end:
			dates.append(d)
			d = d + pd.DateOffset(step)
		print(dates)
		expanded = pd.DataFrame(index=dates, data={'temperature': [None]*len(dates)})
		joined = pd.concat([self.raw, expanded])
		print(joined)
		cleared = joined.groupby(joined.index).first()
		print(len(cleared))
		assert len(cleared) == len(expanded)
		return cleared.interpolate('linear')

	def interpolate(self, method, columns=None):
		self.raw.interpolate(method)
		return self


