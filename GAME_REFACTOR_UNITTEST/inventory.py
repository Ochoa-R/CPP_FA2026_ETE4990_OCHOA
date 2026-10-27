from userIn import getInput
import json

class Inventory():
	"""Class for managing the player's inventory, with functions for adding and
        removing items, opening and closing, and returning whether the
        inventory is opened or closed"""
	def __init__(self, inventory = None):
		self.__inventory = inventory.copy() if inventory else []
		self.__invState = invState = False
		self.__maxLength = 8
		self.__invMenu = [
			{
				"Name": "Description",
				"Desc": "Read an item's description",
				"Func": self.readDesc
			},
			{
				"Name": "Discard",
				"Desc": "Discard an item",
				"Func": self.discard
			},
			{
				"Name": "Gift",
				"Desc": "Bring an item with you as a gift",
				"Func": self.getGift
			}
		]

	def __str__(self):
		if len(self.__inventory) > 0:
			nameList = [item["Name"] for item in self.__inventory]
			invStr = "--- ITEMS ---\n"
			for num, name in enumerate(nameList, start=1):
				invStr += str(num) + '. ' + name + '\n'
			if len(nameList) >= self.__maxLength:
				invStr += "--- FULL ---\n"
			else:
				invStr += "------------\n"
			return invStr
		else:
			return "No Items!\n"

	@property
	def inventory(self):
		return self.__inventory

	@property
	def invState(self):
		return self.__invState

	@property
	def invMenu(self):
		return self.__invMenu

	def open(self):
		print("Opening inventory...\n")
		invState = True

	def close(self):
		print("Returning to Main Menu...\n")
		invState = False

	def checkForItem(self, chosenItem):
		for item in self.__inventory:
			if chosenItem.upper() == item.get("Name").upper():
				return item
		else:
			return None	

	def readDesc(self):
		while True:
			print(self)
			selectedItem = getInput("Choose an item to read the description of: ")
			if item := self.checkForItem(selectedItem):
				print(item["Description"])
				print(item["Effect"]+'\n')
				return
			else:
				print("You don't have that in your inventory.\n")
				return None

	def discard(self):
		while True:
			print(self)
			selectedItem = getInput("Choose an item to discard: ")
			if item := self.checkForItem(selectedItem):
				print(f"{item["Name"]} removed from inventory\n")
				self.__inventory.remove(item)
				return item
			else:
				print("You don't have that in your inventory.\n")
				return None

	def add(self, itemToAdd):
		try:
			match list(itemToAdd.keys()):
				case ["Name", "Description", "Effect"]:
					if len(self.__inventory) >= self.__maxLength:
						while True:
							print("Your inventory is full. Would you like to discard an item?")
							with open("charFiles/nonFuncMenus.json", "r") as file:
								yesNoMenu = json.load(file)["Y/N Prompt"]
							for num, prompt in enumerate(yesNoMenu, start=1):
								print(f"{num}. {prompt}")
							match getInput("Make your choice: ").upper():
								case "YES":
									print("")
									if self.discard():
										break
									else:
										continue
								case "NO":
									print(f"You didn't need the {itemToAdd["Name"]} anyway!\n")
									return itemToAdd
								case _:
									print("Your choice is invalid.\n")
					print(f"{itemToAdd["Name"]} added to inventory\n")
					self.__inventory.append(itemToAdd)
				case _:
					print("Can't add that!\n")
		except AttributeError:
			print("That's not an item!\n")

	def getGift(self):
		while True:
			print(self)
			selectedItem = getInput("Choose a gift to give: ")
			if item := self.checkForItem(selectedItem):
				print(f"You bring the {item["Name"]} for your friend.\n")
				return self.__inventory.pop(self.__inventory.index(item))
			else:
				print("You don't have that in your inventory.")
				return None