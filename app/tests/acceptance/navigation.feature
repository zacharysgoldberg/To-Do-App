Feature: Test navigation between pages
    We can have a longer description
    That can span a few lines

    Scenario: Homepage can go to receipts
        Given I am on the Homepage
        When I click on the link labeled "Receipts"
        Then I am on the receipts page