from django.core.exceptions import ValidationError

def validator_sms_code(values):
    if len(values) > 6:
        ValidationError('Длина должна быть не больше 6 символов')    
