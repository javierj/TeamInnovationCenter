package CucumberSeleniumDemos.test_radar;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.firefox.FirefoxDriver;

public class TestRadarMainPage extends TestRadarPage {
	
	public void load() {
		System.setProperty("webdriver.chrome.driver", "/code/JavaWorkspaces/BDD_Workspace/CucumberSeleniumDemos/driver/chromedriver_win32/chromedriver.exe");
		 driver = new ChromeDriver();
		 //driver.get("http://javierj.pythonanywhere.com");
		 //this.log("Main page: ");
		 driver.get(this.getUrl());
	}


	public TestRadarPollPage startPoll(String project_id, String team_id) {
		return new TestRadarPollPage(driver, project_id, team_id);
	}


	public SelectorPage selectReport(String project_id, String team_id) {
		return new SelectorPage(driver, project_id, team_id);
	}
	
	public ReportPage reportPage() {
		return new ReportPage(driver);
	}
}
