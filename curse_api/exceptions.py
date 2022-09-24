class APIBanned(Exception):
    pass


class BadRequest(Exception):  # 400
    pass


class Forbidden(Exception):  # 403
    pass


class NotFound(Exception):  # 404
    pass


class MethodNotAllowed(Exception):  # 405
    pass


class ImATeapot(Exception):  # 418
    pass


class InternalServerError(Exception):  # 500
    pass


def _raise(status_code: int):  # template
    match status_code:
        case 200:
            return True
        case 400:
            raise BadRequest(
                "The server cannot or will not process the request due to something that is perceived to be a client error."
            )
        case 403:
            raise Forbidden("The client does not have access rights to the content")
        case 404:
            raise NotFound("The server can not find the requested resource.")
        case 500:
            raise InternalServerError(
                "The server has encountered a situation it does not know how to handle."
            )
        case 418:
            raise ImATeapot(
                "The server refuses to brew coffee because it is, permanently, a teapot."
            )
        case _:
            raise Exception(f"I don't know what went wrong")
