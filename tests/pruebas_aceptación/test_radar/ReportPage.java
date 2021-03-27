package CucumberSeleniumDemos.test_radar;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;

public class ReportPage  extends TestRadarPage {

	public ReportPage(WebDriver driver) {
		this.driver = driver;
	}

	

	public void load(String project_id, String team_id, String year, String month) {
		this.project_id = project_id;
		this.team_id = team_id;
		driver.get(this.getUrl() + "report/"+ this.project_id + "/" + this.team_id + "/" + year + "/" + month +"/");
		//this.driver.get(url);
	}

	public boolean contains(String id, String uno) {
		//System.out.println()
		WebElement html = this.driver.findElement(By.id(id));
		return html.getText().contains(uno);
	}



	@Override
	public void load() {
		//Dont use this
		System.err.print("No uses ReportPage::load");
	}

}
