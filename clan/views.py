from django.shortcuts import render, redirect, get_object_or_404
from django.template import TemplateDoesNotExist
from django.urls import reverse
from django.db.models import Q
from django.views import View, generic
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.utils.html import escape
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from . import models, forms
from functools import wraps
import random
from django.shortcuts import resolve_url
from django.http import HttpResponse
# Create your views here.
# from icecream import ic
import pandas as pd
import seaborn as sns
import matplotlib
matplotlib.use('Agg')
from io import BytesIO
import base64


# //--------------------------------------------------------------------//
# ;;------------------------Generic Template View-----------------------;;
# //--------------------------------------------------------------------//
	
	
class Home(generic.TemplateView):
	template_name="clan/t2_home.html"
	
	
class Datos(generic.TemplateView):
	template_name="clan/t2_datos.html"
	def get(self, request):
		form = forms.SubirArchivoForm()
		contexto = {
					"form": form
					}
		return render(request, self.template_name, contexto)
		
	
	def post(self, request):
		form = forms.SubirArchivoForm(request.POST, request.FILES)
		if form.is_valid():
			uploaded_file = form.cleaned_data['file']
			columna_a_plotear = form.cleaned_data['columna_a_plotear']
			data = pd.read_csv(uploaded_file)      
			
			# Create a Seaborn displot
			sns_plot = sns.displot(data[columna_a_plotear])

			# Convert the Seaborn plot to a Matplotlib figure
			fig = sns_plot.fig

			# Save the Matplotlib figure as an image
			buffer = BytesIO()
			fig.savefig(buffer, format="png")
			buffer.seek(0)

			contexto = {
				"grafico": base64.b64encode(buffer.read()).decode("utf-8")
			}
			buffer.close()
		return render(request, self.template_name, contexto)
	

class Info(generic.TemplateView):
	template_name="clan/t2_info.html"


class Examen(generic.TemplateView):
	template="clan/t2_examen.html"
	
	def get(self, request):
		context = {
					"form":forms.ExamForm
					}
		return render(request, self.template, context)
		
	def post(self, request, *args, **kwargs):
		if request.method == "POST":
			exam_form = forms.ExamForm(request.POST)
			question_12_form = forms.Question12(request.POST)
			question_13_form = forms.Question13(request.POST)



			exam_form.is_valid()
			question_12_form.is_valid()
			question_13_form.is_valid()
			
			
			
			# ic(exam_form.cleaned_data)
			# ic(question_12_form.cleaned_data)
			# ic(question_13_form.cleaned_data)
				
			if exam_form.is_valid() and question_12_form.is_valid() and question_13_form.is_valid():
				# Extract responses from the exam form
				exam_responses = {
					'question_1': exam_form.cleaned_data['question_1'],
					'question_2': exam_form.cleaned_data['question_2'],
					'question_3': exam_form.cleaned_data['question_3'],
					'question_4': exam_form.cleaned_data['question_4'],
					'question_5': exam_form.cleaned_data['question_5'],
					'question_6': exam_form.cleaned_data['question_6'],
					'question_7': exam_form.cleaned_data['question_7'],
					'question_8': exam_form.cleaned_data['question_8'],
					'question_9': exam_form.cleaned_data['question_9'],
					'question_10': exam_form.cleaned_data['question_10'],
					'question_11': exam_form.cleaned_data['question_11'],
					'question_14': exam_form.cleaned_data['question_14'],
					'question_15': exam_form.cleaned_data['question_15'],
					'question_15_extra': exam_form.cleaned_data['question_15_extra'],
				}

				# Extract responses from the Question12 form
				question_12_responses = {
					'statement_1': question_12_form.cleaned_data['statement_1'],
					'statement_2': question_12_form.cleaned_data['statement_2'],
					'statement_3': question_12_form.cleaned_data['statement_3'],
					'statement_4': question_12_form.cleaned_data['statement_4'],
					'statement_5': question_12_form.cleaned_data['statement_5'],
					'statement_6': question_12_form.cleaned_data['statement_6'],
					'statement_7': question_12_form.cleaned_data['statement_7'],
					# Add the rest of the Question12 statements here...
				}

				# Extract responses from the Question13 form
				question_13_responses = {
					'statement_1': question_13_form.cleaned_data['statement_1'],
					'statement_2': question_13_form.cleaned_data['statement_2'],
					'statement_3': question_13_form.cleaned_data['statement_3'],
					'statement_4': question_13_form.cleaned_data['statement_4'],
					'statement_5': question_13_form.cleaned_data['statement_5'],
					'statement_6': question_13_form.cleaned_data['statement_6'],
					'statement_7': question_13_form.cleaned_data['statement_7'],
					# Add the rest of the Question13 statements here...
				}

				# Create or update ExamResult record for the current user
				exam_result, created = ExamResult.objects.get_or_create(user=request.user)

				# Update the ExamResult fields with the responses from the exam form
				for key, value in exam_responses.items():
					setattr(exam_result, key, value)

				# Update the ExamResult fields with the responses from the Question12 form
				for key, value in question_12_responses.items():
					setattr(exam_result, f'question_12_{key}', value)

				# Update the ExamResult fields with the responses from the Question13 form
				for key, value in question_13_responses.items():
					setattr(exam_result, f'question_13_{key}', value)

				exam_result.save()

				return HttpResponse("Form submitted successfully!")
			else:
				print("Formulario invalido")
		else:
			exam_form = forms.ExamForm()
			question_12_form = forms.Question12()
			question_13_form = forms.Question13()

		# Render the forms with error messages or for initial form display
		return render(request, self.template, {
			'exam_form': exam_form,
			'question_12_form': question_12_form,
			'question_13_form': question_13_form,
		})