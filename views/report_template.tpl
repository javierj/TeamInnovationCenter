% include('header.tpl')

<br/>
<h2> <span aria-hidden="true" class="octicon octicon-link">Informe.</span></h2>
<p> Se han encontrado {{report.get_answers_len()}} encuestras.
<br/>
Las encuestas mostradas son del mes {{report.get_month()}} del año {{report.get_year()}}.
</p>

<br/>
    <!-- Gráfico -->
    <h3> Resumen: </h3>
    <div>
        <canvas id="myChart" style="border:1px solid"></canvas>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
        const labels = [
            %for factor_name, _ in report.iter_factors():
            '{{factor_name}}',
            %end
            'Sin uso'
        ];
        const factor_ok = 'rgba(75, 192, 192, 0.2)';
        const border_factor_ok = 'rgb(75, 192, 192)';
        const factor_bad = 'rgba(255, 99, 132, 0.2)';
        const border_factor_bad = 'rgb(255, 99, 132)';
        const mad_ok = 'rgba(54, 162, 235, 0.2)';
        const border_mad_ok = 'rgb(54, 162, 235)';
        const mad_bad = 'rgba(255, 159, 64, 0.2)';
        const border_mad_bad = 'rgb(255, 159, 64)';
        const data = {
            labels: labels,
            datasets: [{
                axis: 'y',
                label: '',
                data: [
                    %for _, factor in report.iter_factors():
                        {{factor.total_mean()}},
                    %end
                    ],
                    fill: false,
                    backgroundColor: [
                        %for _, factor in report.iter_factors():
                            %if factor.total_mean() >= 2.5:
                                factor_ok,
                            %end
                            %if factor.total_mean() < 2.5:
                                factor_bad,
                            %end
                        %end
                    ],
                    borderColor: [
                        %for _, factor in report.iter_factors():
                            %if factor.total_mean() >= 2.5:
                                border_factor_ok,
                            %end
                            %if factor.total_mean() < 2.5:
                                border_factor_bad,
                            %end
                        %end
                    ],
                    borderWidth: 1
                },
                {
	                axis: 'y',
                    label: '',
                    data: [
                        %for _, factor in report.iter_factors():
                            {{factor.total_mad()}},
                        %end
                    ],
                    fill: false,
                    backgroundColor: [
                        %for _, factor in report.iter_factors():
                            %if factor.total_mad() > 1:
                                mad_bad,
                            %end
                            %if factor.total_mad() <= 1:
                                mad_ok,
                            %end
                        %end
                    ],
                    borderColor: [
                        %for _, factor in report.iter_factors():
                            %if factor.total_mad() > 1:
                                border_mad_bad,
                            %end
                            %if factor.total_mad() <= 1:
                                border_mad_ok,
                            %end
                        %end
                    ],
                    borderWidth: 1
                }]
            };
        const config = {
    type: 'bar',
    data,
    options: {
    indexAxis: 'y',
    }
    };

 var myChart = new Chart(
    document.getElementById('myChart'),
    config
  );
    </script>

<p>
    La primera barra de cada factor es el valor medio y la segunda barra es la desviación media.
    <br/>
    Una barra azul o verde indica un valor adecuado y una barra roja o naranja indica un valor a mejorar.
</p>

<br/>
<br/>

%for factor_name, factor in report.iter_factors():

    <h3>{{factor_name}}:</h3>
    <p> {{defs[factor_name]}} </p>

    <div id="{{factor_name}}_stats">

    <p style="font-size:20px">
        <strong>
            Media total: {{factor.total_mean()}}
            <br/>
            Desviación media total: {{factor.total_mad()}}
        </strong>
    </p>
    </div>

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


 </p>

<p>
<!--
<strong> Análisis:  </strong> {{factor.get_analysis()}}
-->
</p>

<p>
<strong> Evolución temporal: </strong>

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

<br/> <hr/> <br/>

%end

<p>
<a href="{{base_url}}/cvs/{{report.get_project_id()}}/{{report.get_struct_name()}}/"> Descargar todos los datos en CVS. </a>
</p>


%# Comentario.

<p>
<hr/>
<strong> Este informe se ha generado de manera automática </strong>

<hr/>

<!--
<h2>
<span aria-hidden="true" class="octicon octicon-link">Contacto</span>
</h2>
<p> Este proyecto de investigación se desarrolla bajo el paraguas del grupo de investigación en Ingeniería Web y
Testing Temprano (IWT2) de la Universidad de Sevilla </p>
<p> Su principal responsable es Javier Gutiérrez y puedes contactar con él vía correo electrónico: javier arroba us.es
o Twitter: arroba iwt2_javier </p>
-->
% include('footer.tpl')