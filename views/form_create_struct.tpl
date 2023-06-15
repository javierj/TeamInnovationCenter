% include('header.tpl')

    <form action="/newpoll" method="post">
        <label for="questions_file">Nombre del fichero de preguntas:</label><br>
        <input type="text" id="questions_file" name="questions_file"/>
        <br>
        <label for="poll_name">Nombre de la encuesta:</label>
        <br>
        <input type="text" id="poll_name" name="poll_name"/>
        <br>
        <label for="num_of_questions">Número de preguntas:</label>
        <br>
        <input type="number" id="num_of_questions" name="num_of_questions"/>
        <br>
        <label for="questions_in_categories">Preguntas por categoría:</label>
        <br>
        <textarea id="questions_in_categories" name="questions_in_categories" rows="4" cols="50">
Example: "A":3, "B":1</textarea>
        <br>
        <label for="poll_structure">Estructura:</label>
        <br>
        <textarea id="poll_structure" name="poll_structure" rows="4" cols="50">
Example: "A":"Formación", "B":"Flexibilidad"</textarea>
        <br>
        <label for="groups">Grupos:</label>
        <br>
        <textarea id="groups" name="groups" rows="8" cols="50">
Example: "Formación":[3], "Flexibilidad":[4]</textarea>
        <br>
        <label for="descriptions">Descripciones:</label>
        <br>
        <textarea id="descriptions" name="descriptions" rows="8" cols="50">
Example: "Formación":"Formación.", "Flexibilidad": "Flexibilidad."</textarea>
        <br>
        <input type="submit" value="Submit"/>

    </form>


% include('footer.tpl')