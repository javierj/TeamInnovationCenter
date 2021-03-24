package CucumberSeleniumDemos.test_radar;

import java.util.concurrent.TimeUnit;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;

public class TestRadarPollPage extends TestRadarPage {
	
	public TestRadarPollPage(WebDriver driver, String project_id, String team_id) {
		this.driver = driver;
		this.project_id = project_id;
		this.team_id = team_id;
	}

	public void load() {
		String url = getUrl() + "test/" + this.project_id + "/" + this.team_id + "/";
		driver.get(url);
		
	}

	public void clickOn(String string) {
		this.driver.findElement(By.xpath("//a[text()='"+string+"']")).click(); 
		this.log.append("Click on: "+string);
		//driver.manage().timeouts().implicitlyWait(20, TimeUnit.SECONDS);
		try {
			Thread.sleep(1000);
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	@Override
	public String toString() {
		return "TestRadarPollPage: \n " + this.driver.getPageSource();
	}

}
