# importing necessary modules
from userIn import getInput
from character import Character
from player import Player
from nonplayer import NPC
from inventory import Inventory
import dataHandler as dh
import random as rd
import json

# importing unittest modules
from unittest.mock import patch
import unittest as ut

# Character unittest
class TestCharacter(ut.TestCase):
    def setUp(self):
        self.charEmpty = Character()
        self.charArg = Character("John", {"Age": 45})

    def testPrivateVariables(self):
        self.assertNotIn("name", self.charEmpty.__dict__)
        self.assertNotIn("traits", self.charEmpty.__dict__)

    def testNoNameReturnsEmptyString(self):
        result = str(self.charEmpty)
        self.assertIsInstance(result, str)
        self.assertEqual(len(result), 0)

    def testNoTraitsReturnsEmptyDict(self):
        self.assertEqual(self.charEmpty.traits, {})

    def testPassedNameReturnsUsefulString(self):
        result = str(self.charArg)
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)

    def testTraitsProperty(self):
        self.assertEqual(self.charArg.traits, {"Age": 45})
        self.assertEqual(self.charArg.traits["Age"], 45)

# Inventory unittest
class TestInventory(ut.TestCase):
	def setUp(self):
		with open("charFiles/gameItems.json", "r") as file:
			self.itemList = json.load(file)
		self.invEmpty = Inventory()
		self.invFull = Inventory(self.itemList)
		self.menuList = [
			{
				"Name": "Description",
				"Desc": "Read an item's description",
				"Func": self.invEmpty.readDesc
			},
			{
				"Name": "Discard",
				"Desc": "Discard an item",
				"Func": self.invEmpty.discard
			},
			{
				"Name": "Gift",
				"Desc": "Bring an item with you as a gift",
				"Func": self.invEmpty.getGift
			}
		]
		self.dummyItem = {
			"Name": "Pear", 
			"Description": "Kind of like an apple.",
			"Effect": "Liked by those who take their nutrition seriously!"
		}

	def testPrivateVariables(self):
		self.assertNotIn("inventory", self.invEmpty.__dict__)
		self.assertNotIn("invState", self.invEmpty.__dict__)
		self.assertNotIn("invMenu", self.invEmpty.__dict__)

	def testInventoryProperty(self):
		self.assertEqual(self.invEmpty.inventory, [])
		self.assertEqual(self.invFull.inventory, self.itemList)

	def testInvStateProperty(self):
		self.assertEqual(self.invEmpty.invState, False)

	def testInvMenuProperty(self):
		self.assertEqual(self.invEmpty.invMenu, self.menuList)

	def testNoItemsReturnsNoItems(self):
		result = str(self.invEmpty).strip()
		self.assertIsInstance(result, str)
		self.assertEqual(result, "No Items!")

	def testInvStateFalseByDefault(self):
		self.assertFalse(self.invEmpty.invState)

	def testInventoryIsCopy(self):
		self.assertIsNot(self.invFull.inventory, self.itemList)

	def testFullInventoryHasFullIndicator(self):
		self.assertIn("FULL", str(self.invFull))

	def testNotFullInventoryHasNoFullIndicator(self):
		self.invFull.inventory.remove(self.dummyItem)
		self.assertNotIn("FULL", str(self.invFull))

	def testCheckForItemReturnsCorrectItem(self):
		self.assertEqual(self.invFull.checkForItem("Pear"), self.dummyItem)

	def testCheckForItemReturnsNoneWhenInvalidInput(self):
		self.assertIsNone(self.invFull.checkForItem("Chilly Cheese Hamburger"))

	#def testAddRaisesAttributeErrorWhenInvalidItem(self):
	#	with self.assertRaises(AttributeError):
	#		self.invEmpty.add("Bingus")

	def testReadDescReturnsNoneWhenInvalidItem(self):
		#with patch('__main__.getInput') as mock:
		with patch('inventory.getInput') as mock:
			mock.return_value = "Flubbernuts"
			result = self.invEmpty.readDesc()
		self.assertIsNone(result)
		mock.assert_called_once_with("Choose an item to read the description of: ")

	def testDiscardReturnsNoneWhenInvalidItem(self):
		#with patch('__main__.getInput') as mock:
		with patch('inventory.getInput') as mock:
			mock.return_value = "Flubbernuts"
			result = self.invEmpty.discard()
		self.assertIsNone(result)
		mock.assert_called_once_with("Choose an item to discard: ")

	def testDiscardReturnsItemWhenValidItem(self):
		#with patch('__main__.getInput') as mock:
		with patch('inventory.getInput') as mock:
			mock.return_value = "Pear"
			result = self.invFull.discard()
		self.assertEqual(result, self.dummyItem)
		mock.assert_called_once_with("Choose an item to discard: ")

# Player unittest
class TestPlayer(ut.TestCase):
	def setUp(self):
		with open("charFiles/gameItems.json", "r") as file:
			self.itemList = json.load(file)
		self.nullPlayer = Player(Inventory(), 0)
		self.pregPlayer = Player(Inventory(self.itemList), 12, "Test Player", {"Hair Color": "Brown"})
		self.dummyItem = {
			"Name": "Pear", 
			"Description": "Kind of like an apple.",
			"Effect": "Liked by those who take their nutrition seriously!"
		}

	def testPrivateVariables(self):
		self.assertNotIn("inventory", self.nullPlayer.__dict__)
		self.assertNotIn("energy", self.nullPlayer.__dict__)
		self.assertNotIn("maxEnergy", self.nullPlayer.__dict__)
		self.assertNotIn("heldItem", self.nullPlayer.__dict__)

	def testInventoryProperty(self):
		self.assertIsInstance(self.nullPlayer.inventory, Inventory)

	def testEnergyProperty(self):
		self.assertEqual(self.nullPlayer.energy, 0)
		self.assertEqual(self.pregPlayer.energy, 12)

	def testHeldItemProperty(self):
		self.assertIsNone(self.nullPlayer.heldItem)

	def testEnergySetterDoesNotExceedMaxEnergy(self):
		maxRange = self.pregPlayer.energy + 1
		for i in range(maxRange):
			self.nullPlayer.energy += rd.randint(1, 100)
		for i in range(maxRange):
			self.pregPlayer.energy += rd.randint(1, 100)
		self.assertEqual(self.nullPlayer.energy, 0)
		self.assertEqual(self.pregPlayer.energy, 12)

	def testEnergySetterDoesNotGoBelowZero(self):
		maxRange = self.pregPlayer.energy + 1
		for i in range(maxRange):
			self.nullPlayer.energy -= rd.randint(1, 100)
		for i in range(maxRange):
			self.pregPlayer.energy -= rd.randint(1, 100)
		self.assertEqual(self.nullPlayer.energy, 0)
		self.assertEqual(self.pregPlayer.energy, 0)

	def testHeldItemSetterNoCallAddIfIsNone(self):
		with patch.object(self.nullPlayer.inventory, 'add') as mock:
			self.nullPlayer.heldItem = self.dummyItem
		mock.assert_not_called()

	def testHeldItemDoesNotChangeIfAssignedNullValue(self):
		self.nullPlayer.heldItem = self.dummyItem
		self.nullPlayer.heldItem = None
		self.assertEqual(self.nullPlayer.heldItem, self.dummyItem)
		self.nullPlayer.heldItem = 0
		self.assertEqual(self.nullPlayer.heldItem, self.dummyItem)
		self.nullPlayer.heldItem = False
		self.assertEqual(self.nullPlayer.heldItem, self.dummyItem)

	def testHeldItemSetterCallsAddIfFilled(self):
		with patch.object(self.nullPlayer.inventory, 'add') as mock:
			self.nullPlayer.heldItem = self.dummyItem
			self.nullPlayer.heldItem = self.dummyItem
		mock.assert_called_once()

	def testCheckStatsChangesEnergyMessage(self):
		self.assertIn("Feeling Good!", self.pregPlayer.checkStats())
		self.pregPlayer.energy = self.pregPlayer.energy // 2
		self.assertIn("Could use some rest.", self.pregPlayer.checkStats())
		self.pregPlayer.energy = self.pregPlayer.energy // 2
		self.assertIn("About to pass out...", self.pregPlayer.checkStats())

	def testCheckStatsExecutesFirstCaseWhenEnergyNull(self):
		self.assertIn("Feeling Good!", self.nullPlayer.checkStats())

	def testCheckStatsShowsStats(self):
		self.assertIn("HAIR COLOR: Brown", self.pregPlayer.checkStats())

if __name__ == '__main__':
    ut.main(argv=['first-arg-is-ignored'], exit=False)