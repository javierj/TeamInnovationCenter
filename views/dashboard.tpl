% include('header_web.tpl')

<h2> Dashboard de la encuesta {{survey_name}}.</h2>
<p>
Enlace de la encuesta:
    <a href="{{base_url}}/poll/{{survey_name}}/01/"> {{base_url}}/poll/{{survey_name}}/01/</a>
<br/>
Enlace de prueba (no guarda los resultados):
    <a href = "{{base_url}}/poll/{{survey_name}}/01/0000"> http://127.0.0.1/poll/{{survey_name}}/01/0000 </a>
</p>
<hr/>
<p>
Consultar respuestas:  <a href = "{{base_url}}/report/poll/{{survey_name}}/"> {{base_url}}/report/poll/{{survey_name}}/ </a>
</p>
<hr/>
<p>
Editar estructura de la encuesta: TODO
<br/>
Editar preguntas de la encuesta:
    <a href = "{{base_url}}/edit/questions/{{survey_name}}"> {{base_url}}/edit/questions/{{survey_name}} </a>
</p>
<a href="/"> Volver a página principal. </a>


% include('footer_web.tpl')