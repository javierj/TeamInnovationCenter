% include('header.tpl')

<br/>
<h2> Informes disponibles. </h2>
<p>
<h3></h3>
A continuación se muestran los meses y años para los que se han encontrado
respuestas de la encuesta {{survey_type}}.
<br/>
Pulsa en un enlace para ver los resultados de ese mes.

</p>
<br/>

%for year in surveys_overview.begin().keys():
<p>
<strong> {{year}}: </strong>
<br/>
<table>
    <tr> <td> Mes </td> <td> Id </td> <td> Respuestas </td> <td> Información adicional </td>
    %for month in surveys_overview.begin().group(year).keys():

        %for project_id in surveys_overview.begin().group(year).group(month).keys():
            %url = base_url + "/report/" + str(project_id) + "/" + str(project_id) + "/" + str(year) + "/" + str(month) + "/" + survey_type + "/"

            <tr>
                <td><a href="{{url}}"> {{month}} </a>  </td>
                <td> {{project_id}} </td>
                <td> {{surveys_overview.begin().group(year).group(month).group(project_id).counter()}} </td>
                <td> No disponible. </td>
            </tr>
        %end

    %end
</table>
</p>
<hr/>
<p>

%for year in cvs_keys.begin().keys():
    %for project_id in cvs_keys.begin().group(year).keys():
        %url_cvs = base_url + "/cvs/" + str(project_id) + "/" + str(survey_type) + "/"
        <a href="{{url_cvs}}"> Descargar CVS completo de {{project_id}} </a>
        <br/>
</p>

%end

% include('footer.tpl')