from django import forms
from django.core.validators import EmailValidator
from clan import models
from django.utils.safestring import mark_safe
from django.utils.html import format_html


from django import forms

class Question12(forms.Form):
	statement_1 = forms.BooleanField(required=False, label="Permiten que el programa utilice recursos de la computadora de forma más eficiente ")
	statement_2 = forms.BooleanField(required=False, label="Son muy útiles cuando el programa es corto y sencillo.")
	statement_3 = forms.BooleanField(required=False, label="Es una buena práctica usarlos cuando hay partes que se repiten. ")
	statement_4 = forms.BooleanField(required=False, label="Cuanto más procedimientos, más legible el programa.  ")
	statement_5 = forms.BooleanField(required=False, label="Permiten dividir tareas y trabajar con otros programadores de forma independientemente. ")
	statement_6 = forms.BooleanField(required=False, label="Permiten reutilizar código para problemas similares.  ")
	statement_7 = forms.BooleanField(required=False, label="Permiten resolver un problema complejo en partes más sencillas.")

class Question13(forms.Form):
	statement_1 = forms.BooleanField(required=False, label="La repetición simple va a repetir una serie de instrucciones en base a un número definido por el programador.")
	statement_2 = forms.BooleanField(required=False, label="Repetición simple significa que una instrucción se va a repetir según haga falta. ")
	statement_3 = forms.BooleanField(required=False, label="La repetición condicional significa que una instrucción se va a repetir siempre en cuando se cumpla una condición. ")
	statement_4 = forms.BooleanField(required=False, label="La repetición simple permite automatizar un algoritmo. ")
	statement_5 = forms.BooleanField(required=False, label="La repetición condicional toma como parámetro un número, y la repetición simple toma como parámetro una condición.  ")
	statement_6 = forms.BooleanField(required=False, label="La repetición simple puede dar lugar a un bucle infinito.")



class ExamForm(forms.Form):
	question_1 = forms.ChoiceField(
		choices=[
			(1, 'TRUE'),
			(2, 'FALSE'),
		],
		widget=forms.RadioSelect(),
		label=mark_safe("""
<h4>Teniendo en cuenta que...</h3>
<h5>
<pre>
A = 5
B = 7
</pre>
</h5>
<h4>¿Cúal es el resultado de esta expresión lógica?</h3>
<h5>
<pre>
"A >= 10 and A es par or A < 12 and B es par" 
</pre>
</h5>
		"""),
	)

	question_2 = forms.ChoiceField(
		choices=[
			(1, 'TRUE'),
			(2, 'FALSE'),
		],
		widget=forms.RadioSelect(),
		label=mark_safe("""
<h4>Teniendo en cuenta que...</h3>
<h5>
<pre>
C = 11
</pre>
</h5>
<h4>¿Cúal es el resultado de esta expresión lógica?</h3>
<h5>
<pre>
"(C > 10 or C == 10) and C < 12" 
</pre>
</h5>
		"""),
	)




	question_3 = forms.ChoiceField(
		choices=[
			(1, 'TRUE'),
			(2, 'FALSE'),
		],
		widget=forms.RadioSelect(),
		label=mark_safe("""
<h4>Teniendo en cuenta que...</h3>
<h5>
<pre>
D = 11
F = 21
</pre>
</h5>
<h4>¿Cúal es el resultado de esta expresión lógica?</h3>
<h5>
<pre>
"A == 5 and D > 5 and C > F or F > 11" 
</pre>
</h5>
		"""),
	)






	question_4 = forms.ChoiceField(
		choices=[
			(1, 'TRUE'),
			(2, 'FALSE'),
		],
		widget=forms.RadioSelect(),
		label=mark_safe("""
<h4>Teniendo en cuenta que...</h3>
<h5>
<pre>
A = 8
F = 21
</pre>
</h5>
<h4>¿Cúal es el resultado de esta expresión lógica?</h3>
<h5>
<pre>
"A <= 8 and A es par and A es impar or FALSE or TRUE" 
</pre>
</h5>
		"""),
	)






	question_5 = forms.ChoiceField(
		choices=[
			(1, '14'),
			(2, '15'),
			(3, '16'),
			(4, '17'),
		],
		widget=forms.RadioSelect(),
		label=mark_safe("""
<h4>Observe los siguientes numeros...</h3>
<h5>
<pre>
1 4 5 8 9 12 13 … ?
</pre>
</h5>
<h4>¿Cúal es el número que seguiría a esa secuencia?</h3>

		"""),
	)






	question_6 = forms.ChoiceField(
		choices=[
			(1, '61'),
			(2, '57'),
			(3, '49'),
			(4, '45'),
		],
		widget=forms.RadioSelect(),
		label=mark_safe("""
<h4>Observe los siguientes numeros...</h3>
<h5>
<pre>
1, 5, 13, 25, 41, …?
</pre>
</h5>
<h4>¿Cúal es el número que seguiría a esa secuencia?</h3>

		"""),
	)



	question_7 = forms.ChoiceField(
		choices=[
			(1, '1'),
			(2, '2'),
			(3, '3'),
			(4, '4'),
		],
		widget=forms.RadioSelect(),
		label=mark_safe("""
<h4>Dadas las figuras a, b, c, d...</h3>
<h4>¿Cuál sería la siguiente? </h4> 
<h5> Elija entre 1, 2, 3, 4 </h5>

		"""),
	)






	question_8 = forms.ChoiceField(
		choices=[
			(1, '1'),
			(2, '2'),
			(3, '3'),
			(4, '4'),
		],
		widget=forms.RadioSelect(),
		label=mark_safe("""
<h4>Dadas las figuras a, b, c, d...</h3>
<h4>¿Cuál sería la siguiente? </h4> 
<h5> Elija entre 1, 2, 3, 4 </h5>

		"""),
	)






	question_9 = forms.ChoiceField(
		choices=[
			(1, '-1 y 3'),
			(2, '0 y 3'),
			(3, '1 y 4'),
			(4, '1 y 3'),
			(5, '0 y 4'),
		],
		widget=forms.RadioSelect(),
		label=mark_safe("""
<h3>Observe el siguiente diagrama de flujo y responda:</h3>
<h4>Al momento del terminar el programa… ¿cuánto vale la variable QUESO y la variable C, respectivamente? </h4> 
<h5> Elija la opcion correcta </h5>

		"""),
	)






	question_10 = forms.ChoiceField(
		choices=[
			(1, '3'),
			(2, '4'),
			(3, '5'),
			(4, '9'),
		],
		widget=forms.RadioSelect(),
		label=mark_safe("""
<h3>Observe el siguiente diagrama de flujo y responda:</h3>
<h4>¿Que muestra el algoritmo de la figura si el usuario ingresa sucesivamente 2, 2, 1, 4? </h4> 
<h5> Elija la opcion correcta </h5>

		"""),
	)





	question_11 = forms.ChoiceField(
		choices=[
			(1, '3'),
			(2, '4'),
			(3, '5'),
			(4, '9'),
		],
		widget=forms.ClearableFileInput(),
		label=mark_safe("""
<h3>Observar la siguiente solución de Pilas Bloques... </h3>
		"""),
	)


	question_12 = Question12()
	question_13 = Question13()






	question_14 = forms.ChoiceField(
		choices=[
			(1, 'No, porque el cangrejo en un momento se cae del tablero.'),
			(2, 'Si.'),
			(3, 'Sí, pero podría resolverse de una forma más corta y legible.'),
			(4, 'No, porque quedan globos sin explotar.'),
		],
		widget=forms.RadioSelect(),
		label=mark_safe("""
<h3>Observar el siguiente programa en Pilas-Bloques... </h3>
<h4>Elija la opcion correcta </h4>
		"""),
	)






	question_15 = forms.ChoiceField(
		choices=[
			(1, 'Crearía un solo procedimiento que tome dos parámetros.'),
			(2, 'Crearía dos procedimientos que toman un parámetro.'),
			(3, 'Crearía dos procedimientos que no necesitan parámetros.'),
			(4, 'Tengo otra solución.'),
		],
		widget=forms.RadioSelect(),
		label=mark_safe("""
<h3>Si tuvieras que modificar esa solución... </h3>
<h4> para hacerla más simple y reutilizable...</h4>
<h4> ¿Cómo lo harías?.</h4>
		"""),
	)




	question_15_extra = forms.CharField(
		widget=forms.Textarea(attrs={'rows': 12, 'cols': 70}),
		label="Escribi tu pseudo-codigo acá",
	)



	# Add more questions as needed...

	def __init__(self, *args, **kwargs):
		super(ExamForm, self).__init__(*args, **kwargs)
		self.fields['question_1']
		self.fields['question_2']
		self.fields['question_3']
		self.fields['question_4']
		self.fields['question_5']
		self.fields['question_6']
		self.fields['question_7']
		self.fields['question_8']
		self.fields['question_9']
		self.fields['question_10']
		self.fields['question_11']
		
		self.fields['question_14']
		self.fields['question_15']
		self.fields['question_15_extra']

	def clean(self):
		cleaned_data = super(ExamForm, self).clean()
		# Add custom validation logic if needed
		return cleaned_data




class SubirArchivoForm(forms.Form):
	file = forms.FileField()
	columna_a_plotear = forms.CharField(label="Columna a plotear")