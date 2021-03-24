package CucumberSeleniumDemos.test_radar;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;

public class ReportPage  extends TestRadarPage {

	public ReportPage(WebDriver driver) {
		this.driver = driver;
	}

	@Override
	public void load() {
		// TODO Auto-generated method stub
	}

	public void load(String project_id, String team_id) {
		this.project_id = project_id;
		this.team_id = team_id;
		driver.get(this.getUrl() + "report/"+ this.project_id + "/" + this.team_id + "/2021/2/");
		//this.driver.get(url);
	}

	public boolean contains(String id, String uno) {
		//System.out.println()
		WebElement html = this.driver.findElement(By.id(id));
		return html.getText().contains(uno);
	}

}
