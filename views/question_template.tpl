% include('header.tpl')

<br/>
<h2> Pregunta X. </h2>
<p>
<h3>{{question}}</h3>
</p>
<br/>
<p>
</p>
%# Generate 5 answers with 5 URL.

<h4>
%for i in range(1, 6):
%url = base_url + question_code + str(i)
<a href="{{url}}"> {{i}} </a> |
%end
</h4>


% include('footer.tpl')