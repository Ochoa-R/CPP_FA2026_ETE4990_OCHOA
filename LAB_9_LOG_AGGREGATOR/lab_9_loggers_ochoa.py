import logging
import random as rd

def createLog(logName, logLevel, handlerFile):
	logFormat = logging.Formatter(
		fmt=("%(asctime)s -- %(name)s -- %(levelname)s"" -- %(message)s")
	)

	logging.basicConfig(level=logging.INFO, force=True)
	log = logging.getLogger(logName)
	log.setLevel(logLevel)

	handler = logging.handlers.TimedRotatingFileHandler(
		filename=handlerFile,
		when="D",
		backupCount=1
	)
	handler.setFormatter(logFormat)
	log.addHandler(handler)

	return log

def writeWarnings(logger):
	info = [
    "Application started",
    "Configuration loaded",
    "User logged in",
    "Request completed",
    "File read successfully",
    "Connection established",
    "Task completed",
    "Cache refreshed",
    "Session created",
    "Application stopped"
	]

	debug = [
    "Entering function process_data",
    "Variable count set to 10",
    "Payload contents inspected",
    "Loop iteration started",
    "Database query parameters logged",
    "Cache lookup performed",
    "Response object created",
    "Token expiration checked",
    "Execution path selected",
    "Temporary value calculated"
	]

	warning = [
    "Disk space is running low",
    "Configuration value is missing",
    "Connection is unstable",
    "Request took longer than expected",
    "Cache entry is expired",
    "Retry attempt required",
    "Deprecated feature detected",
    "Memory usage is elevated",
    "Input is partially incomplete",
    "Background task is delayed"
	]

	error = [
    "File cannot be found",
    "Unable to connect to database",
    "Invalid user input",
    "Request failed",
    "Permission denied",
    "Unable to write to disk",
    "Authentication failed",
    "Unexpected response received",
    "Data validation failed",
    "Operation timed out"
	]

	critical = [
    "Data corrupted",
    "Database is unavailable",
    "Security breach detected",
    "System overheating",
    "Application crash detected",
    "Storage device failure",
    "Service is completely unavailable",
    "Memory exhaustion detected",
    "Critical configuration failure",
    "Computer engaging self-combustion mode"
	]

	for _ in range(rd.randrange(0,2)):
		logger.info(info[rd.randrange(len(info))])
	for _ in range(rd.randrange(0,2)):
		logger.debug(info[rd.randrange(len(debug))])
	for _ in range(rd.randrange(0,2)):
		logger.warning(warning[rd.randrange(len(warning))])
	for _ in range(rd.randrange(0,2)):
		logger.error(error[rd.randrange(len(error))])
	for _ in range(rd.randrange(0,2)):
		logger.critical(error[rd.randrange(len(critical))])

def getLogs():
	mainLog = createLog("main", logging.INFO, "main.log")
	appLog = createLog("../myApps/app", logging.WARNING, "app.log")
	appUtilLog = createLog("../myApps/app.utils", logging.ERROR, "appUtils.log")
	appUtilDbLog = createLog("../myApps/app.utils.db", logging.CRITICAL, "appUtilsDb.log")
	gameDataLog = createLog("../myApps/games/game.bin", logging.INFO, "gameBin.log")
	gameImageLog = createLog("../myApps/games/game.cue", logging.WARNING, "gameCue.log")
	gameSaveLog = createLog("../myApps/games/game.game_1.mcd", logging.ERROR, "gameCard.log")

	return [mainLog, appLog, appUtilLog, appUtilDbLog, gameDataLog, gameImageLog, gameSaveLog]
