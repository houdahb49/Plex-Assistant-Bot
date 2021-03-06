import sqlite3
import datetime
from backend import constants

###############
# USERS TABLE #
###############

# Gets the 'users' table entry for the supplied telegram ID
def getUser(id):
    db = sqlite3.connect(constants.DB_FILE, detect_types=sqlite3.PARSE_DECLTYPES)
    db_cursor = db.cursor()
    db_cursor.execute("PRAGMA foreign_keys = ON")
    db_cursor.execute('SELECT * FROM users WHERE telegram_id = ?', (str(id),))
    user = db_cursor.fetchone()
    db.close()
    return user

# Get all user rows from 'users' table
def getUsers():
    db = sqlite3.connect(constants.DB_FILE, detect_types=sqlite3.PARSE_DECLTYPES)
    db_cursor = db.cursor()
    db_cursor.execute("PRAGMA foreign_keys = ON")
    db_cursor.execute('SELECT * FROM users')
    users = db_cursor.fetchall()
    db.close()
    return users

# Get the 'users' table entries with the status code supplied
def getUsersWithStatus(status):
    db = sqlite3.connect(constants.DB_FILE, detect_types=sqlite3.PARSE_DECLTYPES)
    db_cursor = db.cursor()
    db_cursor.execute("PRAGMA foreign_keys = ON")
    db_cursor.execute('SELECT * FROM users WHERE status = ?', (str(status),))
    users = db_cursor.fetchall()
    db.close()
    return users

# Get the admins from the 'users' table
def getAdmins():
    db = sqlite3.connect(constants.DB_FILE, detect_types=sqlite3.PARSE_DECLTYPES)
    db_cursor = db.cursor()
    db_cursor.execute("PRAGMA foreign_keys = ON")
    admins = []
    for admin in db_cursor.execute('SELECT * FROM users WHERE status = ?', (constants.ACCOUNT_STATUS_ADMIN,)):
        admins.append(admin[0])
    db.close()
    return admins

# Checks if the supplied user ID is registered
def isUserRegistered(id):
    db = sqlite3.connect(constants.DB_FILE, detect_types=sqlite3.PARSE_DECLTYPES)
    db_cursor = db.cursor()
    db_cursor.execute("PRAGMA foreign_keys = ON")
    db_cursor.execute('SELECT * FROM users WHERE telegram_id = ?', (id,))
    if(db_cursor.fetchone() is not None):
        db.close()
        return True
    db.close()
    return False

# Checks if the supplied user ID is <status>
def isUserStatus(id, status):
    db = sqlite3.connect(constants.DB_FILE, detect_types=sqlite3.PARSE_DECLTYPES)
    db_cursor = db.cursor()
    db_cursor.execute("PRAGMA foreign_keys = ON")
    db_cursor.execute('SELECT * FROM users WHERE telegram_id = ? AND status = ?', (id,status))
    if(db_cursor.fetchone() is not None):
        db.close()
        return True
    db.close()
    return False

###############
# SHOWS TABLE #
###############

# Get the list of shows that are active in the database
def getDatabaseShows():
    db = sqlite3.connect(constants.DB_FILE, detect_types=sqlite3.PARSE_DECLTYPES)
    db_cursor = db.cursor()
    db_cursor.execute("PRAGMA foreign_keys = ON")
    shows = []
    for show in db_cursor.execute('SELECT * FROM television'):
        shows.append([show[0], show[1]])
    return shows

# Get a tuple/row containing the information for the show matching the TVDB ID
def getShow(id):
    db = sqlite3.connect(constants.DB_FILE, detect_types=sqlite3.PARSE_DECLTYPES)
    db_cursor = db.cursor()
    db_cursor.execute("PRAGMA foreign_keys = ON")
    db_cursor.execute('SELECT * FROM television WHERE tvdb_id = ?', (id,))
    show = db_cursor.fetchone()
    db.close()
    return show

def getShowByName(name):
    db = sqlite3.connect(constants.DB_FILE, detect_types=sqlite3.PARSE_DECLTYPES)
    db_cursor = db.cursor()
    db_cursor.execute("PRAGMA foreign_keys = ON")
    db_cursor.execute('SELECT * FROM television WHERE name = ?', (name,))
    show = db_cursor.fetchone()
    db.close()
    return show

def getShowsSearch(text):
    db = sqlite3.connect(constants.DB_FILE)
    db_cursor = db.cursor()
    db_cursor.execute("PRAGMA foreign_keys = ON")
    db_cursor.execute('SELECT * FROM television WHERE name LIKE ?', ("%"+text+"%",))
    shows = db_cursor.fetchall()
    db.close()
    return shows

def getShowsWatchedByUser(id):
    db = sqlite3.connect(constants.DB_FILE, detect_types=sqlite3.PARSE_DECLTYPES)
    db_cursor = db.cursor()
    db_cursor.execute("PRAGMA foreign_keys = ON")
    db_cursor.execute("""SELECT * FROM television WHERE 
        tvdb_id IN (SELECT media_id FROM notifiers WHERE telegram_id = ? AND media_type = ?)
    """, (id, constants.NOTIFIER_MEDIA_TYPE_TELEVISION))
    shows = db_cursor.fetchall()
    db.close()
    return shows

def getShowsWatchedSearch(id, text):
    db = sqlite3.connect(constants.DB_FILE, detect_types=sqlite3.PARSE_DECLTYPES)
    db_cursor = db.cursor()
    db_cursor.execute("PRAGMA foreign_keys = ON")
    db_cursor.execute("""SELECT * FROM television WHERE 
        tvdb_id IN (SELECT media_id FROM notifiers WHERE telegram_id = ? AND media_type = ?) AND
        name LIKE ?
    """, (id, constants.NOTIFIER_MEDIA_TYPE_TELEVISION, "%"+text+"%"))
    shows = db_cursor.fetchall()
    db.close()
    return shows

################
# MOVIES TABLE #
################

# Get the list of movies taht are active in the database
def getDatabaseMovies():
    db = sqlite3.connect(constants.DB_FILE)
    db_cursor = db.cursor()
    db_cursor.execute("PRAGMA foreign_keys = ON")
    movies = []
    for movie in db_cursor.execute('SELECT * FROM movies'):
        movies.append([movie[0], movie[1]])
    return movies

# Get a tuple/row containing the information for the movie matching the TMDB ID
def getMovie(id):
    db = sqlite3.connect(constants.DB_FILE, detect_types=sqlite3.PARSE_DECLTYPES)
    db_cursor = db.cursor()
    db_cursor.execute("PRAGMA foreign_keys = ON")
    db_cursor.execute('SELECT * FROM movies WHERE tmdb_id = ?', (id,))
    movie = db_cursor.fetchone()
    db.close()
    return movie

def getMovieByName(name):
    db = sqlite3.connect(constants.DB_FILE, detect_types=sqlite3.PARSE_DECLTYPES)
    db_cursor = db.cursor()
    db_cursor.execute("PRAGMA foreign_keys = ON")
    db_cursor.execute('SELECT * FROM movies WHERE name = ?', (name,))
    movie = db_cursor.fetchone()
    db.close()
    return movie

def getMoviesSearch(text):
    db = sqlite3.connect(constants.DB_FILE, detect_types=sqlite3.PARSE_DECLTYPES)
    db_cursor = db.cursor()
    db_cursor.execute("PRAGMA foreign_keys = ON")
    db_cursor.execute('SELECT * FROM movies WHERE name LIKE ?', ("%"+text+"%",))
    movies = db_cursor.fetchall()
    db.close()
    return movies

def getMoviesWatchedByUser(id):
    db = sqlite3.connect(constants.DB_FILE, detect_types=sqlite3.PARSE_DECLTYPES)
    db_cursor = db.cursor()
    db_cursor.execute("PRAGMA foreign_keys = ON")
    db_cursor.execute("""SELECT * FROM movies WHERE 
        tmdb_id IN (SELECT media_id FROM notifiers WHERE telegram_id = ? and media_type = ?)
    """, (id, constants.NOTIFIER_MEDIA_TYPE_MOVIE))
    movies = db_cursor.fetchall()
    db.close()
    return movies

def getMoviesWatchedSearch(id, text):
    db = sqlite3.connect(constants.DB_FILE, detect_types=sqlite3.PARSE_DECLTYPES)
    db_cursor = db.cursor()
    db_cursor.execute("PRAGMA foreign_keys = ON")
    db_cursor.execute("""SELECT * FROM movies WHERE 
        tmdb_id IN (SELECT media_id FROM notifiers WHERE telegram_id = ? and media_type = ?) AND
        name LIKE ?
    """, (id, constants.NOTIFIER_MEDIA_TYPE_MOVIE, "%"+text+"%"))
    movies = db_cursor.fetchall()
    db.close()
    return movies

##################
# NOTIFIER TABLE #
##################

def getNotifier(id):
    db = sqlite3.connect(constants.DB_FILE, detect_types=sqlite3.PARSE_DECLTYPES)
    db_cursor = db.cursor()
    db_cursor.execute("PRAGMA foreign_keys = ON")
    db_cursor.execute('SELECT * FROM notifiers WHERE watch_id = ?', (id,))
    notifier = db_cursor.fetchone()
    db.close()
    return notifier

def getNotifiers():
    db = sqlite3.connect(constants.DB_FILE, detect_types=sqlite3.PARSE_DECLTYPES)
    db_cursor = db.cursor()
    db_cursor.execute("PRAGMA foreign_keys = ON")
    db_cursor.execute('SELECT * FROM notifiers')
    notifiers = db_cursor.fetchall()
    db.close()
    return notifiers
    
def getNotifierForUser(id, media_id, media_type):
    db = sqlite3.connect(constants.DB_FILE, detect_types=sqlite3.PARSE_DECLTYPES)
    db_cursor = db.cursor()
    db_cursor.execute("PRAGMA foreign_keys = ON")
    db_cursor.execute("""SELECT * FROM notifiers WHERE
        telegram_id = ? AND
        media_id = ? AND
        media_type = ?
    """, (id, media_id, media_type))
    notifier = db_cursor.fetchone()
    db.close()
    return notifier

def getNotifiersForUser(id):
    db = sqlite3.connect(constants.DB_FILE, detect_types=sqlite3.PARSE_DECLTYPES)
    db_cursor = db.cursor()
    db_cursor.execute("PRAGMA foreign_keys = ON")
    db_cursor.execute('SELECT * FROM notifiers WHERE telegram_id = ?', (id,))
    notifiers = db_cursor.fetchall()
    db.close()
    return notifiers

def getTelevisionNotifiersForUser(id):
    db = sqlite3.connect(constants.DB_FILE, detect_types=sqlite3.PARSE_DECLTYPES)
    db_cursor = db.cursor()
    db_cursor.execute("PRAGMA foreign_keys = ON")
    db_cursor.execute('SELECT * FROM notifiers WHERE media_type = ? AND telegram_id = ?', (constants.NOTIFIER_MEDIA_TYPE_TELEVISION, id))
    notifiers = db_cursor.fetchall()
    db.close()
    return notifiers

def getMoviesNotifiersForUser(id):
    db = sqlite3.connect(constants.DB_FILE, detect_types=sqlite3.PARSE_DECLTYPES)
    db_cursor = db.cursor()
    db_cursor.execute("PRAGMA foreign_keys = ON")
    db_cursor.execute('SELECT * FROM notifiers WHERE media_type = ? AND telegram_id = ?', (constants.NOTIFIER_MEDIA_TYPE_MOVIE, id))
    notifiers = db_cursor.fetchall()
    db.close()
    return notifiers

def getUsersImmediateUpdate(media_id, media_type):
    db = sqlite3.connect(constants.DB_FILE, detect_types=sqlite3.PARSE_DECLTYPES)
    db_cursor = db.cursor()
    db_cursor.execute("PRAGMA foreign_keys = ON")
    db_cursor.execute("""SELECT telegram_id FROM notifiers WHERE
        media_id = ? AND
        media_type = ? AND
        frequency = ?
    """, (media_id, media_type, constants.NOTIFIER_FREQUENCY_IMMEDIATELY))
    users = db_cursor.fetchall()
    db.close()
    return users

def getNotifiersForUserDaily(id, media_type):
    db = sqlite3.connect(constants.DB_FILE, detect_types=sqlite3.PARSE_DECLTYPES)
    db_cursor = db.cursor()
    db_cursor.execute("PRAGMA foreign_keys = ON")
    db_cursor.execute("""SELECT * FROM notifiers WHERE
        telegram_id = ? AND
        frequency = ? AND
        media_type = ?
    """, (id, constants.NOTIFIER_FREQUENCY_DAILY, media_type))
    notifiers = db_cursor.fetchall()
    db.close()
    return notifiers

def getNotifiersForUserWeekly(id, media_type):
    db = sqlite3.connect(constants.DB_FILE, detect_types=sqlite3.PARSE_DECLTYPES)
    db_cursor = db.cursor()
    db_cursor.execute("PRAGMA foreign_keys = ON")
    db_cursor.execute("""SELECT * FROM notifiers WHERE
        telegram_id = ? AND
        frequency = ? AND
        media_type = ?
    """, (id, constants.NOTIFIER_FREQUENCY_WEEKLY, media_type))
    notifiers = db_cursor.fetchall()
    db.close()
    return notifiers

###################
# METADATA TABLES #
###################

def getMetadata(id, media_type):
    db = sqlite3.connect(constants.DB_FILE, detect_types=sqlite3.PARSE_DECLTYPES)
    db_cursor = db.cursor()
    db_cursor.execute("PRAGMA foreign_keys = ON")
    if(int(media_type) == constants.NOTIFIER_MEDIA_TYPE_TELEVISION):
        db_cursor.execute("SELECT * FROM metadata_television WHERE metadata_id = ?", (id,))
    elif(int(media_type) == constants.NOTIFIER_MEDIA_TYPE_MOVIE):
        db_cursor.execute("SELECT * FROM metadata_movies WHERE metadata_id = ?", (id,))
    metadata = db_cursor.fetchone()
    db.close()
    return metadata

def getMetadataPastDay(media_type, media_id, upgrade):
    db = sqlite3.connect(constants.DB_FILE, detect_types=sqlite3.PARSE_DECLTYPES)
    db_cursor = db.cursor()
    db_cursor.execute("PRAGMA foreign_keys = ON")
    utc_time = datetime.datetime.utcnow().timestamp()-constants.daysToSeconds(1)
    if(int(media_type) == constants.NOTIFIER_MEDIA_TYPE_TELEVISION):
        db_cursor.execute("""SELECT * FROM metadata_television WHERE
            download_time > ? AND
            tvdb_id = ? AND
            is_upgrade = ?
        """, (utc_time, media_id, upgrade))
    elif(int(media_type) == constants.NOTIFIER_MEDIA_TYPE_MOVIE):
        db_cursor.execute("""SELECT * FROM metadata_movies WHERE
            download_time > ? AND
            tmdb_id = ? AND
            is_upgrade = ?
        """, (utc_time, media_id, upgrade))
    metadata = db_cursor.fetchall()
    db.close()
    return metadata

def getMetadataPastWeek(media_type, media_id, upgrade):
    db = sqlite3.connect(constants.DB_FILE, detect_types=sqlite3.PARSE_DECLTYPES)
    db_cursor = db.cursor()
    db_cursor.execute("PRAGMA foreign_keys = ON")
    utc_time = datetime.datetime.utcnow().timestamp()-constants.weeksToSeconds(1)
    if(int(media_type) == constants.NOTIFIER_MEDIA_TYPE_TELEVISION):
        db_cursor.execute("""SELECT * FROM metadata_television WHERE
            download_time > ? AND
            tvdb_id = ? AND
            is_upgrade = ?
        """, (utc_time, media_id, upgrade))
    elif(int(media_type) == constants.NOTIFIER_MEDIA_TYPE_MOVIE):
        db_cursor.execute("""SELECT * FROM metadata_movies WHERE
            download_time > ? AND
            tmdb_id = ? AND
            is_upgrade = ?
        """, (utc_time, media_id, upgrade))
    metadata = db_cursor.fetchall()
    db.close()
    return metadata
