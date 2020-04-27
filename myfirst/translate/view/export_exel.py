from translate.models import UserProfile
from django.http import HttpResponse
#Export Data to CSV File
import csv


def export_users_csv(request):
	print("i'm here")
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="users.csv"'

	writer = csv.writer(response)
	writer.writerow(['Location', 'Age', 'Email' ])

	users_profiles = UserProfile.objects.all().values_list('location', 'age', 'mail')
	for user_prof in users_profiles:
		writer.writerow(user_prof)

	return response