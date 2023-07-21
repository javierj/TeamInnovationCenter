% include('header.tpl')

<h2> Question {{question_index}}. </h2>
<p>
<h3>{{question}}</h3>
</p>
<br/>
<p>

%url = base_url + question_code + str("1")
<a href="{{url}}">
1. I disagree.<br/>
</a>

%url = base_url + question_code + str("2")
<a href="{{url}}">
2. I partially disagree. <br/>
</a>

%url = base_url + question_code + "3"
<a href="{{url}}">
3. I have no opinion. <br/>
</a>

%url = base_url + question_code + "4"
<a href="{{url}}">
4. I partially agree. <br/>
</a>


%url = base_url + question_code + "5"
<a href="{{url}}">
5. I agree. <br/>
</a>

</p>

%# Generate 5 answers with 5 URL.

<h4>
%for i in range(1, 6):
%url = base_url + question_code + str(i)
<!-- <a href="{{url}}"> {{i}} </a> | -->
%end
</h4>


% include('footer.tpl')