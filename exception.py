class ShortenerBaseError(Exception):
    pass

class NotFoundLongUrl(ShortenerBaseError):
    pass

class SlugAlredyExistError(ShortenerBaseError):
    pass