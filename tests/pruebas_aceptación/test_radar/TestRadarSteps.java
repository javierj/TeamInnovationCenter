package CucumberSeleniumDemos.test_radar;

import io.cucumber.java.After;
import io.cucumber.java.Before;
import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;

import static org.junit.Assert.*;

public class TestRadarSteps {
	
	TestRadarMainPage mainPage;
	TestRadarPollPage pollPage;
	String project_id;
	String team_id;
	SelectorPage selectorPage;
	ReportPage reportPage;
	private String year;
	private String month;
	
	//--- Given -----------------------------------------
	
	@Given("Test Radar")
	public void test_radar() {
		// Sin código
	}

	@Given("el proyecto {string} y el equipo {string}")
	public void el_proyecto_y_el_equipo(String string, String string2) {
	    this.project_id = string;
	    this.team_id = string2;
	}
	
	@Given("una encuesta estándar de 9 preguntas")
	public void una_encuesta_estandar() {
	    this.empiezo_una_encuesta();
	}
	
	@Given("una encuesta realizada el {string} de {string}")
	public void encuesta_realizada_en(String mes, String año) {
	    this.year = año;
	    this.month = mes;
	}

	@Given("ninguna encuesta realizada el {string} de {string}")
	public void ninguna_encuesta_realizada_en(String mes, String año) {
	    this.encuesta_realizada_en(mes, año);
	}


	//--- When ---------------------------------------------------------
	
	@When("empiezo una encuesta")
	public void empiezo_una_encuesta() {
	    pollPage = mainPage.startPoll(this.project_id, this.team_id);
	    pollPage.load();
	}

	
	@When("Test Radar is on")
	public void test_radar_is_on() {
		//mainPage.load();
	}
	
	@When("termino la encuesta.")
	public void termino_la_encuesta() {
		for(int i= 0; i < 9; i++) {
			//System.out.println("i ="+ i);
			//System.out.println(this.pollPage.toString());
			pollPage.clickOn(" 5 ");
		}
	}
	
	@When("veo los informes disponibles") 
	public void veo_informes_disponibles()
	{
		selectorPage = mainPage.selectReport(this.project_id, this.team_id);
		selectorPage.load();
	}
	
	@When("consulto el informe del proyecto.")
	public void consulto_informe_proyecto()
	{
		reportPage = this.mainPage.reportPage();
		reportPage.load(this.project_id, this.team_id, this.year, this.month);
	}
	
	//----------------------------------------------
	
	@Then("Test radar tells tyou why is Test Improvement Center")
	public void test_radar_tells_tyou_why_is_test_improvement_center() {
		//System.out.println("Then:\n" + this.mainPage);
		assertTrue( mainPage.contains("Team Improvement Center.") );
		assertTrue( mainPage.contains("Mide y mejora la eficacia de tus equipos.") );
	}
	
	@Then("el sistema me muestra la primera pregunta.")
	public void el_sistema_me_muestra_la_primera_pregunta() {
	    // Write code here that turns the phrase above into concrete actions
	    assertTrue( this.pollPage.contains("Pregunta 1.") );
	}
	
	@Then("puedo dar mi opinión en una escala de 1 a 5.")
	public void puedo_dar_mi_opinion() {
	    assertTrue( this.pollPage.contains(" 1 ") );
	    assertTrue( this.pollPage.contains(" 5 ") );
	}
	
	@Then("1 significa que estoy muy en desacuerdo.")
	public void uno_es_muy_desacuerdo() {
	    assertTrue( this.pollPage.contains("1. Es falso / Estoy en desacuerdo.") );
	}
	
	@Then("5 significa que estoy muy de acuerdo.")
	public void cinco_es_muy_de_acuerdo() {
	    assertTrue( this.pollPage.contains("5. Es cierto / Estoy de acuerdo.") );
	}
	
	
	@Then("el sistema almacena los resultados de la encuesta para ese equipo.")
	public void el_sistema_almacena_los_resultados() {
		//System.out.println("Log:\n" + this.pollPage.logToString());
		assertTrue( this.pollPage.toString() , this.pollPage.contains("Gracias por tu participación."));	
	}
	
	@Then("Hay informes para el mes 1 y 2 de 2021.")
	public void ehay_informes() {
		//System.out.println(this.selectorPage.toString());
		assertTrue( this.selectorPage.hasLink("http:/report/G7D/T01/2021/1/"));	
		assertTrue( this.selectorPage.hasLink("http:/report/G7D/T01/2021/2/"));	
	}

	@Then("El factor {string} tiene {string} y {string}.")
	public void  el_factor_tiene_y(String factor, String uno, String dos) {
		System.out.println(factor + "_stats");
		//System.out.println(this.reportPage.toString());
		assertTrue( this.reportPage.contains(factor + "_stats", uno));
		assertTrue( this.reportPage.contains(factor + "_stats", dos));
	}
	
	@Then("el informe indica que no hay ninguna respuesta.")
	public void  informe_no_hay_ninguna_sespuesta() {
		//System.out.println(this.reportPage.toString());
		String expected = "No tenemos registrada ninguna respuesta";
		assertTrue( this.reportPage.contains(expected));
	}
	

	//-------------------------------------------------
	
	@Before()
	public void openPage() {
		mainPage = new TestRadarMainPage();
		mainPage.load();
	}
	
	@After()
	public void closePage() {
		mainPage.close();
	}
}
