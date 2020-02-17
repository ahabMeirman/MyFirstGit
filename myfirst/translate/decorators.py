#from flask import request
from django.conf import settings
from django.contrib import messages# success, info, warning, error, debug mehagess

import requests


def check_recaptcha(function):
	def wrap(request, *args, **kwargs):
		request.recaptcha_is_valid = None
		if request.method == 'POST':
			# Ответ с первоначальным результатом валидации каптчи будет содержаться в поле g-recaptcha-response
			recaptcha_response = request.POST.get('g-recaptcha-response')
			
			data = {
				'secret' : settings.GOOGLE_RECAPTCHA_SECRET_KEY,
				'response' : recaptcha_response
			}
			# Именно этот ответ и отправляется с секретным ключом на сервера Google,
			# для верификации сайта и получения окончательного результата верификации пользователя.
			r = requests.post('https://www.google.com/recaptcha/api/siteverify', data = data )
			result = r.json()# принимаем

			if result['success']:
				request.recaptcha_is_valid = True
			else:
				request.recaptcha_is_valid = False
				messages.error(request, 'Invalid reCAPTCHA. Please try again.')
		return function(request, *args, **kwargs) 

	wrap.__doc__ = function.__doc__
	wrap.__name__ = function.__name__
	return wrap