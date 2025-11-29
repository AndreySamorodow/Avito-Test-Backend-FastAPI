class ShortenerBaseError(Exception):
    pass

class NotFoundLongUrl(ShortenerBaseError):
    pass

class SlugAlredyExistError(ShortenerBaseError):
    pass

class URLNotValid(ShortenerBaseError):
    pass

class CustomSlugNotValid(ShortenerBaseError):
    pass