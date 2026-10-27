from character import Character
import math

class NPC(Character):
	"""Child class of parent, represents a non-player
    character that the player can interact with. Contains
    preferences for items they like and dislike, as well as
    an attachment score that influences the win condition"""
	def __init__(
		self, 
		name = None,
		traits = None,
		preferences = None,
		eventDialogue = None,
		score = 0,
		attachRate = 1
	):
		super().__init__(name, traits)
		self.__prefereces = preferences if preferences else {}
		self.__eventDialogue = eventDialogue if eventDialogue else {}
		self.__score = score
		self.__attachRate = attachRate

	@property
	def score(self):
		return self.__score

	def receiveGift(self, gift):
		match (choicer := gift["Name"]):
			case choicer if choicer in self.__preferences["Likes"]:
				#print(self.__eventDialgoue["Gift"]["Love"])
				print("yay\n")
				self.__score += math.floor(10*self.__attachRate)
			case choicer if choicer in self.__preferences["Dislikes"]:
				#print(self.__eventDialogue["Gift"]["Hate"])
				print("nay\n")
				self.__score -= math.floor(8*(self.__attachRate / 2))
			case _:
				#print(self.__eventDialgoue["Gift"]["Indifference"])
				print("huh?\n")

	def checkStats(self):
		checkPoints = [25, 50, 75, 100]
		statStr = f"--- {str(self).upper()}'S STATS ---\n"
		for category, trait in self.traits.items():
			statStr += f"{category.upper()}: {trait}\n"
		match self.__score:
			case self.__score if self.__score in range(checkPoints[0]):
				statStr += "Maybe you could ask them a few questions?\n"
			case self.__score if self.__score in range(checkPoints[0], checkPoints[1]):
				statStr += "They seem like they want to get to know you better!\n"
			case self.__score if self.__score in range(checkPoints[1], checkPoints[2]):
				statStr += "You're becoming very good friends!\n"
			case self.__score if self.__score in range(checkPoints[2], checkPoints[3]):
				statStr += "They seem to be really into you!\n"
			case self.__score if self.__score >= checkPoints[3]:
				statStr += "Holy fuck.\n"
			case _:
				statStr += "They think you're a weirdo.\n"
		return statStr