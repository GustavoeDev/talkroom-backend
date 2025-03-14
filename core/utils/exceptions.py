from rest_framework.exceptions import APIException

class ValidationError(APIException):
    status_code = 400
    default_detail = 'Parâmentros inválidos para essa requisição.'
    default_code = 'validation_error'