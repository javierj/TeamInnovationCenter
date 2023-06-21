% include('header_web.tpl')

    <form action="/newpoll" method="post">
        <label for="questions_file">Nombre del fichero de preguntas:</label><br>
        <input type="text" id="questions_file" name="questions_file" value="{{str(struct.questions_filename())}}"/>
        <br/>
        %if "questions_file" in errors:
            * {{errors["questions_file"]}} <br/>
        %end
        <br/>
        <label for="poll_name">Nombre de la encuesta:</label>
        <br>
        <input type="text" id="poll_name" name="poll_name" value="{{str(struct.name())}}"/>
        <br>
        %if "poll_name" in errors:
             * {{errors["poll_name"]}} <br/>
        %end
        <br/>
        <label for="num_of_questions">Número de preguntas:</label>
        <br>
        <input type="number" id="num_of_questions" name="num_of_questions" value="{{str(struct.num_of_questions())}}"/>
        <br>
        %if "num_of_questions" in errors:
             * {{errors["num_of_questions"]}} <br/>
        %end
        <br/>
        <label for="questions_in_categories">Preguntas por categoría:</label>
        <br>
        <textarea id="questions_in_categories" name="questions_in_categories" rows="4" cols="60">
{{str(struct.questions_in_categories())}} </textarea>
        <br>
        %if "questions_in_categories" in errors:
            * {{errors["questions_in_categories"]}} <br/>
        %end
        <br/>
        <label for="poll_structure">Estructura:</label>
        <br>
        <textarea id="poll_structure" name="poll_structure" rows="6" cols="60">
{{str(struct.get_test_structure())}} </textarea>
        <br/>
        %if "poll_structure" in errors:
             * {{errors["poll_structure"]}} <br/>
        %end
        <br/>
        <label for="groups">Grupos:</label>
        <br/>
        <textarea id="groups" name="groups" rows="8" cols="60">
{{str(struct.get_groups())}} </textarea>
        <br/>
        %if "groups" in errors:
             * {{errors["poll_structure"]}} <br/>
        %end
        <br/>
        <label for="descriptions">Descripciones:</label>
        <br/>
        <textarea id="descriptions" name="descriptions" rows="10" cols="60">
{{str(struct.description_dict())}} </textarea>
        <br/>
        %if "descriptions" in errors:
             * {{errors["poll_structure"]}} <br/>
        %end
        <br/>

        <input type="checkbox" id="edit_questions" name="edit_questions" value="edit_questions" checked>
        <label for="edit_questions"> Editar fichero de preguntas.</label>
        <br/>
        <br/>
        <input type="submit" value="Submit"/>
        <br/>
        <br/>
        <a href=""/> Salir sin guardar. </a>

    </form>


% include('footer_web.tpl')