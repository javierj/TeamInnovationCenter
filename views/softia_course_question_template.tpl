% include('header.tpl')

<h2> Pregunta {{question_index}}. </h2>
<p>
<h3>{{question}}</h3>
</p>
<br/>

<h3>
<p>

%url = base_url + question_code + str("1")
<a href="{{url}}">
1. Doble Grado Ingeniería Informática-Tecnologías Informáticas y Matemáticas. <br/>
</a>

%url = base_url + question_code + str("2")
<a href="{{url}}">
2. Grado en Ingeniería de la Salud. <br/>
</a>

%url = base_url + question_code + "3"
<a href="{{url}}">
3. Grado en Ingeniería Informática (cualquier especialidad). <br/>
</a>

%url = base_url + question_code + "4"
<a href="{{url}}">
4. Master del área de Ingeniería Informática. <br/>
</a>


%url = base_url + question_code + "5"
<a href="{{url}}">
5. Doctorado. <br/>
</a>

</p>
</h3>

%# Generate 5 answers with 5 URL.

<h4>
%for i in range(1, 6):
%url = base_url + question_code + str(i)
<!-- <a href="{{url}}"> {{i}} </a> | -->
%end
</h4>


% include('footer.tpl')