Feature: Look of the day
  As a professional who wants to get dressed quickly
  I want three ready outfits when I open the app
  So that I decide what to wear in one tap

  Background:
    Given I am signed in
    And my closet has at least 9 garments

  Scenario: Looks are ready when I open the notification
    Given my 3 looks for today were generated
    When I tap the morning notification
    Then I see the Today screen
    And I see 3 looks in a horizontal carousel

  Scenario: Looks are still loading
    Given my looks for today are not ready yet
    When I open the Today screen
    Then I see a skeleton with the same layout as the looks

  Scenario: Closet below the minimum
    Given my closet has 5 garments
    When I open the Today screen
    Then I see "4 more pieces to unlock your looks"
    And I see a button to open the camera

  Scenario: Choose a look
    Given I see the 3 looks
    When I swipe to option 2
    And I tap "Wear option 2"
    Then option 2 is saved in my wear history
