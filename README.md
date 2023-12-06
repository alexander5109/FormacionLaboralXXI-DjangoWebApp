# PseudoWebsite Applicacion
Practicando django

# 1. Descargar el proyecto
1. Ir a [Entregas](https://github.com/ecthelion5109/selingdjango2023/releases/tag/entregas).
2. Hacer click para descargar el archivo comprimido mas nuevo. Usualmente esta subido en formado .rar o .7z.
3. Extraerlo con 7zip/WinRar o algun programa parecido. 

# 2. Crear entorno con la configuraciones del proyecto.
1. Abrir una terminal de cmd/powershell/bash sobre:	`selingDjango2023`
2. Crear un entorno en python 3.11 mediante:	`python -m venv venv`
3. Activar ese entorno mediante:	`venv/scripts/activate`
4. Descargar la misma version de django del proyecto mediante:	`pip install -r requirements.txt`
	
# 3. Correr la aplicacion.
1. Abrir una terminal de cmd/powershell/bash sobre:	`selingDjango2023`
2. Activar el entorno si no se encuentra activado:	`venv/scripts/activate`
3. Correr servidor:	`python manage.py runserver`

	
# Forma automatica de hacer los mencionados pasos:
1. Abrir `run_creador_de_entorno.cmd` y esperar.
2. Abrir `run_server.bat` y ver la pagina en el servidor.
	
# Notas:
	- Las templates tienen nombre según como se heredan; 
		* "0000_" es la template master.
		* "0001_" son las intermedias.
		* "t2_" son las templates finales.
	- Las views de CRUD para "centros_de_formacion/" estan hechas aplicando views generidas de django. Por lo que tienen menos particularidades.
	- Las views de CRUD para "<str:tables>/" son hijas de una clase llamada MyViewMaster que calcula si son views para ver los estudiantes, o para ver los cursos.  Tiene una docena de properties que calculan la form, el model y otras utilidades. 
	- Esas views tambien heredan desde MyLoginRequiredMixin que a su vez es hija del LoginRequiredMixin de django. Le agregue un par de propiedades para no repetir urls.