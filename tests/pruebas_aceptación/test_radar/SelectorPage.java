package CucumberSeleniumDemos.test_radar;

import org.openqa.selenium.WebDriver;

public class SelectorPage extends TestRadarPage {
	
	
	public SelectorPage(WebDriver driver, String project_id, String team_id) {
		this.driver = driver;
		this.project_id = project_id;
		this.team_id = team_id;
	}

	public void load() {
		String url = getUrl()+"selector/" + this.project_id + "/" + this.team_id + "/";
		driver.get(url);
	}

	public boolean hasLink(String string) {
		return this.contains(string);
	}
	
	@Override
	public String toString() {
		return "TestRadarPollPage: \n " + this.driver.getPageSource();
	}


}
