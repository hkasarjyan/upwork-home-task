require "selenium-webdriver"
require "test/unit"
 
class LoginClass < Test::Unit::TestCase
 
  def setup
    Selenium::WebDriver::Chrome.driver_path = File.join(File.absolute_path('', File.dirname("C://Projects/Selenuim/Drivers")),"Drivers","chromedriver.exe")
    @driver = Selenium::WebDriver.for :chrome
    @driver.get('http://blog.yoniflenner.net/demo')
    @driver.manage.window.maximize    
  end
 
 
  def teardown
    @driver.quit
  end
 
 
  def test_login
    @driver.find_element(:name, "username").send_keys "admin"
    @driver.find_element(:name, "password").send_keys "demo"
    @driver.find_element(:id, "submit").click
    sleep 0.3
    assert(@driver.find_element(:id => "loggedin").text.include?("You Are Logged in"),"Assertion Failed")
    @driver.find_element(:id, "logout").click
  end
end