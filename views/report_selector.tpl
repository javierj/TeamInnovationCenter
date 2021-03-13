% include('header.tpl')

<br/>
<h2> Informes disponibles. </h2>
<p>
<h3></h3>
A continuación se muestran los meses y años para los que se han encontrado
encuestas del proyecto {{org_id}}/{{project_id}}.
<br/>
Pulsa en un enlace para ver los resultados de ese mes.

</p>
<br/>

%for year in surveys_overview.begin().keys():
<p>
<strong> {{year}}: </strong>
<br/>
<table>
    <tr> <td> Mes </td> <td> Tipo de encuestas </td> <td> Número de encuestas </td> <td> Información adicional </td>
    %for month in surveys_overview.begin().group(year).keys():
        %url = base_url + "/" + str(year) + "/" + str(month) + "/"
        %for survey_type in surveys_overview.begin().group(year).group(month).keys():
            <tr>
                <td><a href="{{url}}"> {{month}} </a>  </td>
                <td> {{survey_type}} </td>
                <td> {{surveys_overview.begin().group(year).group(month).group(survey_type).counter()}} </td>
                <td> Aún no disponible </td>
            </tr>
        %end

    %end
</table>
</p>
%end

% include('footer.tpl')