% include('header.tpl')

<br/>
<h2> Pregunta {{question_index}}. </h2>
<p>
<h3>{{question}}</h3>
</p>
<br/>
<p>
1. Es cierto / Estoy de acuerdo. <br/>
2. A veces es cierto / Estoy parcialmente de acuerdo. <br/>
3. No tengo criterio. <br/>
4. A veces es falso / Estoy parcialmente en desacuerdo. <br/>
5. Es falso / Estoy en desacuerdo. <br/>
</p>
%# Generate 5 answers with 5 URL.

<h4>
%for i in range(1, 6):
%url = base_url + question_code + str(i)
<a href="{{url}}"> {{i}} </a> |
%end
</h4>


% include('footer.tpl')