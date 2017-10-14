import re
import requests
from django.core.exceptions import ValidationError


def clean_image_url(value):
	try:
		r = requests.get(value)
		print(value)
		if not r.status_code == requests.codes.ok:
			raise ValidationError("Invalid URL, Please choose another.")
		if not re.compile(r".*\.(jpg|png|gif)$").match(value):
			raise ValidationError("Invalid Image Format. Formats supported : jpg, png, gif")
	except:
		print("in except")
		raise ValidationError("Invalid URL, Please choose another.")
