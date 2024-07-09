import abc
class ArtifactInterface(metaclass=abc.ABCMeta):
	@classmethod
	def __subclasshook__(cls, subclass):
		return (hasattr(subclass,__init__) and
				hasattr(subclass, __repr__) and
				hasattr(subclass, __str__) and
				hasattr(subclass, draw) and
				hasattr(subclass, move) and
				hasattr(subclass, in_range) and
				hasattr(subclass, hit) and
				hasattr(subclass, collision) and
				callable(subclass.__init__) and
				callable(subclass.__repr__) and
				callable(subclass.__str__) and
				callable(subclass.draw) and
				callable(subclass.move) and
				callable(subclass.in_range) and
				callable(subclass.hit) and
				callable(subclass.collision) or
				NotImplemented)

	@abc.abstractmethod
	def __init__():
		"""Constructor"""
		raise NotImplementedError

	@abc.abstractmethod
	def __repr__(self):
		"""callable"""
		raise NotImplementedError

	@abc.abstractmethod
	def __str__(self):
		"""printable"""
		raise NotImplementedError

	@abc.abstractmethod
	def draw(self, surface):
		"""draw artifact"""
		raise NotImplementedError

	@abc.abstractmethod
	def move(self, x_inc=0, y_inc=0):
		"""move artifact"""
		raise NotImplementedError

	@abc.abstractmethod
	def in_range(self, objects):
		"""search in range"""
		raise NotImplementedError

	@abc.abstractmethod
	def hit(self, surface, target):
		"""hit other artifacts"""
		raise NotImplementedError

	@abc.abstractmethod
	def collision(self, objects):
		"""detects collision"""
		raise NotImplementedError