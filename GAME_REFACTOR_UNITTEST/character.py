class Character():
	"""Parent class that holds the stats of the given
	player or NPC character"""
	def __init__(self, name = None, traits = None):
		self.__name = name if name else ""
		self.__traits = traits if traits else {}
	def __str__(self):
		return self.__name

	@property
	def traits(self):
		return self.__traits