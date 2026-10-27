from character import Character
from inventory import Inventory
from userIn import getInput
import math

class Player(Character):
	"""Child class of parent, represents the user's player
    character. Contains an inventory that the player can hold
    gift items in and access during the beginning of the day"""
	def __init__(self, inventory, energy, name = None, traits = None):
		super().__init__(name, traits)
		self.__inventory = inventory
		self.__energy = energy
		self.__maxEnergy = energy
		self.__heldItem = None

	@property
	def inventory(self):
		return self.__inventory

	@property
	def energy(self):
		return self.__energy

	@property
	def heldItem(self):
		return self.__heldItem

	@energy.setter
	def energy(self, energyChange):
		if energyChange >= self.__maxEnergy:
			self.__energy = self.__maxEnergy
		elif energyChange <= 0:
			self.__energy = 0
		else:
			self.__energy = energyChange

	@heldItem.setter
	def heldItem(self, itemToHold):
		if itemToHold:
			if self.__heldItem:
				self.__inventory.add(self.__heldItem)
			self.__heldItem = itemToHold
			

	def checkStats(self):
		threeQuartEn = math.floor(self.__maxEnergy*0.75)
		quarterEn = math.floor(self.__maxEnergy*0.25)
		
		statStr = f"--- {str(self).upper()}'S STATS ---\n"
		for category, trait in self.traits.items():
			statStr += f"{category.upper()}: {trait}\n"
		statStr += "ENERGY: "
		match self.__energy:
			case self.__energy if self.__energy >= threeQuartEn:
				statStr += "Feeling Good!\n"
			case self.__energy if self.__energy in range(quarterEn+1, threeQuartEn):
				statStr += "Could use some rest.\n"
			case self.__energy if (self.__energy <= quarterEn):
				statStr += "About to pass out...\n"
			case _:
				statStr += "You're kind of an anamoly.\n"
		return statStr

	def giveGift(self):
		gift = self.__heldItem
		self.__heldItem = None
		return gift