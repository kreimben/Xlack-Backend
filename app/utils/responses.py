import logging

from fastapi.responses import JSONResponse


class CommonResponse(JSONResponse):
    """
    This is case of response ins common case.
    Don't use this response directly.
    """
    ...


class SuccessResponse(CommonResponse):
    def __init__(self,
                 status_code: int = 200,
                 message: str = 'Success!',
                 **kwargs):
        self.param = {
            'success': True,
            'message': message
        }

        self.param.update(kwargs)
        logging.debug(f'CommonResponse param: {self.param}')

        super().__init__(content=self.param, status_code=status_code)


class FailureResponse(CommonResponse):
    def __init__(self,
                 status_code: int,
                 message: str = 'Failed!',
                 **kwargs):
        self.param = {
            'success': False,
            'message': message
        }
        self.param.update(kwargs)
        logging.debug(f'CommonResponse param: {self.param}')

        super().__init__(content=self.param, status_code=status_code)
