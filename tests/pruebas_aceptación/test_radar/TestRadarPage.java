package CucumberSeleniumDemos.test_radar;

import org.openqa.selenium.WebDriver;

public abstract class TestRadarPage {
	WebDriver driver;
	StringBuffer log = new StringBuffer();
	
	String project_id;
	String team_id;
	
	String url = "http://127.0.0.1:8080/";
	//String url = "http://javierj.pythonanywhere.com";

	public Boolean contains(String string) {
		return driver.getPageSource().contains(string);
	}

	public void close() {
		driver.quit();
		log = new StringBuffer();
	}
	
	public void log(String text) {
		this.log.append(text);
	}
	
	public String logToString() {
		return this.log.toString();
	}
	
	public abstract void load();

	protected String getUrl() {
		//return "http://javierj.pythonanywhere.com/" + string + "/"+this.project_id+"/"+this.team_id+"/";
		return this.url;
	}

	public String toString() {
		return "Page: \n " + this.driver.getPageSource();
	}
}
