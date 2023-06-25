% include('header_web.tpl')

    <form action="/edit/questions/{{survey_name}}" method="post" accept-charset="UTF-8">
        <input type="hidden" id="survey_name" name="survey_name" value="{{survey_name}}" />
        <label for="questions_file">Preguntas de {{survey_name}}:</label><br>

        <textarea id="questions_text" name="questions_text" rows="20" cols="90" wrap="virtual">
{{questions_txt}}</textarea>
        <br>

        <input type="submit" value="Submit"/>
        <br/>
        <a href="/dashboard/{{survey_name}}/"> Salir sin guardar. </a>

    </form>


% include('footer_web.tpl')