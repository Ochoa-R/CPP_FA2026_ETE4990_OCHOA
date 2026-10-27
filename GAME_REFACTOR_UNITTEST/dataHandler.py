import json
from userIn import getInput
from player import Player
from nonplayer import NPC
from inventory import Inventory

def createNewPlayer():
	"""Initiates the creation of  a new character upon
	starting a new save file. Will automatically save to the 
	selected empty file upon completion"""
	print("It's a new day...\n")
	with open("charFiles/playerFormat.json", "r") as file:
		playerTraits = json.load(file)["Traits"]
	while True:
		playerName = getInput("What's your name?: ").upper()
		for trait, value in playerTraits.items():
			value = getInput(f"What's your {trait}?: ")
		print("\nYour name is: " + playerName)
		print("--- and your stats are --- ")
		for trait, value in playerTraits.items():
			print(f"{trait.upper()}: {value}")
		print("Is this okay?")
		while True:
			with open("charFiles/nonFuncMenus.json", "r") as file:
				yesNoMenu = json.load(file)["Y/N Prompt"]
			for num, prompt in enumerate(yesNoMenu, start=1):
				print(f"{num}. {prompt}")
			match getInput("Make your choice: ").upper():
				case "YES":
					print("Very well. It's time to wake up...\n")
					return Player(Inventory(), 12, playerName, playerTraits)
				case "NO":
					print("Let's try that again...\n")
					break
				case _:
					print("Your choice is invalid.\n")

def loadNPCData(npcName):
	try:
		with open("charFiles/npcs.json", "r") as dataFile:
			npcData = json.load(dataFile)[npcName]
		#with open("charFiles/npcDialogue.json", "r") as talkFile:
		#	npcDialogue = json.load(talkFile)[npcName]
		try:
			with open("charFiles/scoreSave.json", "r") as saveFile:
				scoreMods = json.load(saveFile)[npcName]
			return NPC(
				npcName, 
				npcData["Traits"], 
				npcData["Preferences"],
				{},
				scoreMods["Score"], 
				scoreMods["AttachRate"]
			)
		except (FileNotFoundError, KeyError):
			return NPC(
				npcName,
				npcData["Traits"],
				npcData["Preferences"],
				{},
				0,
				npcData["AttachRate"]
			)
	except (FileNotFoundError, KeyError):
		return None