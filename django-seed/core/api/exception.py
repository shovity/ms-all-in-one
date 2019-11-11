

class Redirect(Exception):
    """Message is url for redirect"""
    pass


class Unauthorized(Exception):
    """On self.auth fail"""
    pass


class Forbidden(Exception):
    """On self.auth fail"""
    pass


class NotFound(Exception):
    """Resource not found"""
    pass