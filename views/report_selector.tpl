% include('header.tpl')

<br/>
<h2> Informes disponibles. </h2>
<p>
<h3></h3>
A continuación se muestran los meses y años para los que se ha encontrado
encuestas del proyecto {{org_id}}/{{project_id}}.
<br/>
Pulsa en un enlace para ver los resultados de ese mes.

</p>
<br/>

%for year, months in month_year.items():
<p>
<strong> {{year}}: </strong>
<br/>
<table>
    <tr> <td> Mes </td> <td> Información adicional </td>
    %for month in months:
    %url = base_url + "/" + str(year) + "/" + str(month) + "/"
    <tr> <td>
        <a href="{{url}}"> {{month}} </a>
    </td> <td> Aún no disponible </td> </tr>
    %end
</table>

</p>
%end



% include('footer.tpl')