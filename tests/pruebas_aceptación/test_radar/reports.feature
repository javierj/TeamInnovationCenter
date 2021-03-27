Feature: reports

	Descripción
	

	@team-radar
	Scenario: mostrar factores.
		Given el proyecto "TEST" y el equipo "TEST"
		And una encuesta realizada el "2" de "2021"
		When consulto el informe del proyecto.
		Then El factor "Precondiciones" tiene "Media total: 2." y "Desviación media total: 0.".

	@team-radar
	Scenario: no hay resultados.
		Given el proyecto "TEST" y el equipo "TEST"
		And ninguna encuesta realizada el "2" de "2020"
		When consulto el informe del proyecto.
		Then el informe indica que no hay ninguna respuesta.

	@developer
	Scenario: mostrar preguntas y respuestas. 
		Given el proyecto de pruebas "TEST", "TEST".
		And una encuesta realizada en "Febrero".
		When consulto el informe del proyecto.
		Then Veo la pregunta "Considero que mi sueldo no refleja mi valía en el trabajo que hago." con una respuesta de "5".
		
	@team-radar
	Scenario: selector de encuestas
		Given el proyecto "G7D" y el equipo "T01"
		When veo los informes disponibles
		Then Hay informes para el mes 1 y 2 de 2021.
		