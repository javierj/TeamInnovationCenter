@team-radar
Feature: realización de encuestas
	
	Scenario: iniciar una encuesta
		Given el proyecto "01" y el equipo "01"
		When empiezo una encuesta
		Then el sistema me muestra la primera pregunta.
		And puedo dar mi opinión en una escala de 1 a 5.
		And 1 significa que estoy muy en desacuerdo.
		And 5 significa que estoy muy de acuerdo.
	
	
	Scenario: finalizar una encuesta
		Given el proyecto "01" y el equipo "01"
		Given una encuesta estándar de 9 preguntas
		When termino la encuesta.
		Then el sistema almacena los resultados de la encuesta para ese equipo.
