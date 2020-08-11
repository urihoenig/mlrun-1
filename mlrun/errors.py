from http import HTTPStatus

import requests


class MLRunBaseError(Exception):
    """
    A base class from which all other exceptions inherit.
    If you want to catch all errors that the MLRun SDK might raise,
    catch this base exception.
    """

    pass


class MLRunHTTPError(MLRunBaseError, requests.HTTPError):
    def __init__(
        self, message: str, response: requests.Response = None, status_code: int = None
    ):

        # because response object is probably with an error, it returns False, so we
        # should use 'is None' specifically
        if response is None:
            response = requests.Response()
        if status_code:
            response.status_code = status_code

        requests.HTTPError.__init__(self, message, response=response)


class MLRunDataStoreError(MLRunHTTPError):
    error_status_code = None

    def __init__(self, message: str, response: requests.Response = None):
        super(MLRunDataStoreError, self).__init__(
            message, response=response, status_code=self.error_status_code
        )


def raise_for_status(response: requests.Response):
    """
    Raise a specific MLRunSDK error depending on the given response status code.
    If no specific error exists, raises an MLRunHTTPError
    """
    try:
        response.raise_for_status()
    except requests.HTTPError as exc:
        try:
            raise STATUS_ERRORS[response.status_code](
                str(exc), response=response
            ) from exc
        except KeyError:
            raise MLRunHTTPError(str(exc), response=response) from exc


# Specific Errors


class UnauthorizedError(MLRunDataStoreError):
    error_status_code = HTTPStatus.UNAUTHORIZED.value


class AccessDeniedError(MLRunDataStoreError):
    error_status_code = HTTPStatus.FORBIDDEN.value


class NotFoundError(MLRunDataStoreError):
    error_status_code = HTTPStatus.NOT_FOUND.value


STATUS_ERRORS = {
    HTTPStatus.UNAUTHORIZED.value: UnauthorizedError,
    HTTPStatus.FORBIDDEN.value: AccessDeniedError,
    HTTPStatus.NOT_FOUND.value: NotFoundError,
}
