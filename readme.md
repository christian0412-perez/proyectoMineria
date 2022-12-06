instrucciones para correr el proyecto:
correr el proyecto con 
python3 servicio.py
despues en un postman o algun programa parecido colocar la siguiente ruta:
http://127.0.0.1:5000/mercadolibre
en el body colocar los siguientes datos:
{
    "producto": "computadoras",
    "limite":10
}
estos son datos de prueba que pueden o no ser cambiados.
se genera un .csv que despues se grafica
despues detener el programa y ejecutar el archivo graph.py con
python3 graph.py
y este programa se encarga de graficar los datos de las predicciones de precios.

miembros del equipo:
Christian Alonso Perez Trujillo 193256 
Pablo David Cruz Cruz 201222
Angel Elias Rodriguez Jimenez 201374
Jose Antonio Camilo Ruiz 201248