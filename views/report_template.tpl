% include('header.tpl')

%#Definiciones d elos factors evaluados en las encuestas.

%defs = dict()
%defs['Precondiciones'] = "Recoge todos los factores higiénicos de motivación (o motivaciones extrínsecas)."
%defs['Seguridad sicológica'] = "Poder expresar opiniones sin miedo a represalias."
%defs['Compromiso con el trabajo'] = "Las personas de las que depende mi trabajo adquieren compromisos y los cumplen."
%defs['Perfiles y responsabilidad'] = "Toma de decisiones clara, responsables definidas y tareas claras."
%defs['Resultados significativos'] = "Me importa mi trabajo y me siento implicado haciéndolo."
%defs['Propósito e impacto'] = "El trabajo que realizo tiene una utilidad y un impacto."

<br/>

<h2> <span aria-hidden="true" class="octicon octicon-link">Informe Team Radar.</span></h2>
<p> Se muestran {{report.get_answers_len()}} encuestras.
<br/>
Las encuestas mostradas son del mes {{report.get_month()}} del año {{report.get_year()}}.
</p>

%for factor_name, factor in report.iter_factors():

    <h3>{{factor_name}}:</h3>
    <p> {{defs[factor_name]}} </p>
    <p>
    %# Tabla de respuestas a las preguntas.
    <table>
		    <tr>
            <td> <strong> Pregunta </strong> </td>
            <td> <strong> Respuestas </strong> </td>
            </tr>

            %for q_id in question_answer.questions_id(factor_name):
            <tr>
                <td> {{question_answer.question_text(q_id)}} </td>
                <td> {{question_answer.question_answers(q_id)}} </td>
             </tr>
            %end

	</table>

    <br/>

	    <table>
		    <tr> <td></td>
		    %for i in range(1, len(factor.means())+1):
		    <td> <strong> Pregunta {{i}} </strong> </td>
		    %end
		    </tr>
		    <tr>
		    <td> <em> Media </em> </td>
		    %for i in factor.means():
		    <td style="text-align:center"> {{i}} </td>
		    %end
		    </tr>
		    <tr>
		    <td> <em> Desviación </em> </td>
		    %for i in factor.mads():
		    <td style="text-align:center"> {{i}} </td>
		    %end
		    </tr>
        </table>
 </p>

 <p>
 <strong>
 Media total: {{factor.total_mean()}}
 <br/>
 Desviación media total: {{factor.total_mad()}}
 </strong>
 </p>

<p>
<strong> Análisis:  </strong> {{factor.get_analysis()}}
</p>

<p>
Evolución temporal:

<table>
    <tr>
        <td> Año </td> <td> Mes </td> <td> Encuestas </td><td> Valor medio </td> <td> Desviación media </td>
    </tr>
    %for i in range(0, factor.historical_series()):
    <tr>
        %for info in factor.get_historical_serie(i):
            <td> {{info}} </td>
        %end
    </tr>
    %end

</table>
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