% include('header.tpl')

%#Definiciones d elos factors evaluados en las encuestas.

%defs = dict()
%defs['Precondiciones'] = "Recoge todos los factores higiénicos de motivación (o motivaciones extrínsecas)."
%defs['Seguridad sicológica'] = "Poder expresar opiniones sin miedo a represalias."
%defs['Dependabilidad'] = "Las personas de las que depende mi trabajo adquieren compromisos y los cumplen."
%defs['Estructura y claridad'] = "Toma de decisiones clara, responsables definidas y tareas claras."
%defs['Significado'] = "Me importa mi trabajo y me siento implicado haciéndolo."
%defs['Impacto'] = "El trabajo que realizo tiene una utilidad y un impacto."

<br/>

<h2> <span aria-hidden="true" class="octicon octicon-link">Informe Team Radar.</span></h2>
<p> Las últimas encuestas realizadas son del mes {{date_info['month']}} del año {{date_info['year']}}.
</p>

%for char, data in data_report.items():

    <h3>{{char}}:</h3>
    <p> {{defs[char]}} </p>
    <p>
    %# Tabla de respuestas a las preguntas.
    <table>
		    <tr>
		    %for i in range(1, len(data['answer'][0])+1):
		    <td> <strong> Respuestas pregunta {{i}} </strong> </td>
		    %end
		    </tr>
		    %for answer_row in data['answer']:
		    <tr>
		        %for answer in answer_row:
		        <td style="text-align:center>{{answer}}</td>
		        %end
		    </tr>
		    %end
	</table>

    <br/>

	    <table>
		    <tr> <td></td>
		    %for i in range(1, len(data['mean'])+1):
		    <td> <strong> Pregunta {{i}} </strong> </td>
		    %end
		    </tr>
		    <tr>
		    <td> <em> Media </em> </td>
		    %for i in data['mean']:
		    <td style="text-align:center"> {{i}} </td>
		    %end
		    </tr>
		    <tr>
		    <td> <em> Desviación </em> </td>
		    %for i in data['mad']:
		    <td style="text-align:center"> {{i}} </td>
		    %end
		    </tr>
        </table>
 </p>
<p>
<strong> Análisis:  </strong> {{data['analysis']}}
</p>
<br/>
%end



%# Comentario.

<p>
<hr/>
<strong> Este informe se ha generado de manera automática </strong>
<br/>
Puedes solicitar un informe elaborado a mano más detallado, rellenando el siguiente formulario (Google Form)
 para recibir el informe con el resultado de las encuestas. Tienes un informe de ejemplo elaborado a mano
   <A href="./files/InformeEjemplo.pdf">  aquí </a>.

</p>
<hr/>
<iframe src="https://docs.google.com/forms/d/e/1FAIpQLSdO6iuXwFtZNsFjtxJkjNKUQGDGaX2Ru14tyfpClmEEginn-w/viewform?embedded=true" width="640" height="1000" frameborder="0" marginheight="0" marginwidth="0">Cargando…</iframe>

<hr/>

<center><img src="./images/img01.jpg"/></center>
<hr/>
<h2>
<span aria-hidden="true" class="octicon octicon-link">Contacto</span></h2>
<p> Este proyecto de investigación se desarrolla bajo el paraguas del grupo de investigación en Ingeniería Web y Testing Temprano (IWT2) de la Universidad de Sevilla </p>
<p> Su principal responsable es Javier Gutiérrez y puedes contactar con él vía correo electrónico: javier arroba us.es o Twitter: arroba iwt2_javier </p>

% include('footer.tpl')