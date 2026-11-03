import threading
import time
import json
from pathlib import Path
import matplotlib.pyplot as plt
import lab_9_loggers_ochoa as logs
from lab_9_parsers_ochoa import executeLogStorage

def monitorFile(filePath, stopEvent, interval=10):
	logPath = Path(filePath)
	lastModified = None
	prevData = None
	while True:
		try:
			modified = logPath.stat().st_mtime
			if modified != lastModified:
				try:
					with logPath.open("r", encoding='utf-8') as file:
						currentData = json.load(file)
				except json.JSONDecodeError:
					time.sleep(0.1)
					continue
				if currentData != prevData:
					printSummary(currentData)
					plotSummary(currentData)
					prevData = currentData
		except FileNotFoundError:
			print(f"no such file {filePath} exists")

		stopEvent.wait(interval)

def printSummary(logData):
	levels = ["INFO", "DEBUG", "WARNING", "ERROR", "CRITICAL"]
	messageSum = {}
	criticalMessages = []
	for level in levels:
		messageSum.update({level: 0})
		try:
			messageSum[level] += sum(logData[level].values())
			if level == "CRITICAL":
				criticalMessages += [
					message for message in logData[level].keys()
				]
		except KeyError:
			continue
	
	print(f"\n--- LOG SUMMARY | {time.asctime(time.gmtime())} ---")
	for level, amount in messageSum.items():
		print(f"{level}: {amount}")
	print("\n--- CRITICAL MESSAGES ---")
	for message in criticalMessages:
		print(message)
	
def plotSummary(logData):
	levels = ["INFO", "DEBUG", "WARNING", "ERROR", "CRITICAL"]
	messageSum = {}
	for level in levels:
		messageSum.update({level: 0})
		try:
			messageSum[level] += sum(logData[level].values())
		except KeyError:
			continue
	x = list(messageSum.keys())
	y = list(messageSum.values())
	plt.bar(x, y)
	plt.title('Error Messages')
	plt.ylabel('Amount')
	plt.show()

def startMonitor(fileName, stopEvent):
	stopEvent = threading.Event()
	logFile = fileName
	monitorThread = threading.Thread(target=monitorFile, args=(logFile, stopEvent), daemon=True)
	monitorThread.start()
	return monitorThread

if __name__ == "__main__":
	filePath = "logData.json"
	stopEvent = threading.Event()
	logList = logs.getLogs() 
	thread = startMonitor(filePath, stopEvent)
	try:
		while True:
			for log in logList:
				logs.writeWarnings(log)
			executeLogStorage(Path.cwd())
			time.sleep(13)
	except KeyboardInterrupt:
		stopEvent.set()
		thread.join(timeout=2)
		print("Monitoring Operations Ceased")
