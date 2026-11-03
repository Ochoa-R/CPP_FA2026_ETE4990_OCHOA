import json
import re
from pathlib import Path

def logReader(logFile):
	try:
		with open(logFile, "r") as file:
			return [line.strip() for line in file]
	except FileNotFoundError:
		return None

def logFinder(findPath):
	try:
		if findPath.exists():		
			for logFile in findPath.rglob('*.log'):
				if logFile:
					yield logReader(logFile)
	except AttributeError:
		return None

def logParser(logLines):
	pattern = r"^(.*?)\s--\s(.*?)\s--\s(.*?)\s--\s(.*)$"
	splitter = r"\s--\s"
	collection = []
	for log in logLines:
		for message in log:
			result = re.split(splitter, re.match(pattern, message).group(0))
			if result not in collection:
				collection.append(result)
				yield result

def messageCounter(messages):
	levels = ["INFO", "DEBUG", "WARNING", "ERROR", "CRITICAL"]
	messageDict = {}
	for message in messages:
		for level in levels:
			if level in message:
				if level not in messageDict.keys():
					messageDict.update({level: {}})
				if message[-1] not in messageDict[level].keys():
					messageDict[level].update({message[-1]: 0})
				messageDict[level][message[-1]] += 1
	return messageDict

def logStore(logData):
	try:
		with open("logData.json", "r+") as file:
			json.dump(logData, file, indent=4)
	except FileNotFoundError:
		with open("logData.json", "w") as file:
			json.dump(logData, file, indent=4)

def executeLogStorage(path):
	logStore(messageCounter(logParser(logFinder(path))))
