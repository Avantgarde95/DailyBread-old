class BaseError(Exception):
    pass


# ----------------------------------
# data

class DataLoadError(BaseError):
    pass


# ----------------------------------
# downloader

class ConnectionError(BaseError):
    pass


class InvalidDateError(BaseError):
    pass


# ----------------------------------
# dbhandler

class DBStoreError(BaseError):
    pass


class DBLookupError(BaseError):
    pass


class DBDeleteError(BaseError):
    pass


class DBKeyListError(BaseError):
    pass


# ----------------------------------
# siteopener

class SiteOpenError(BaseError):
    pass
