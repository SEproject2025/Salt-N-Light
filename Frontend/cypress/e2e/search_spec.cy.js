describe("Search page tests", () => {
  beforeEach(() => {
    // Visit the login page
    cy.visit("/AppLogin");

    // Intercept the login request
    cy.intercept("POST", "/api/token/").as("loginRequest");

    // Login with test credentials
    cy.get("#username").type("testuser1");
    cy.get("#password").type("testpass123");
    cy.get(".btn-submit").click();

    // Wait for the login request to complete
    cy.wait("@loginRequest", { timeout: 10000 }).then((interception) => {
      if (interception.response.statusCode !== 200) {
        throw new Error("Login failed");
      }
    });

    // Wait for navigation to search page
    cy.url().should("eq", "http://localhost:8080/SearchPage");
  });

  it("should show loading state while searching", () => {
    // Mock the search API response with a delay
    cy.intercept("GET", "/api/search/*", (req) => {
      req.reply({
        delay: 1000,
        body: {
          status: 200,
          data: [],
        },
      });
    }).as("searchRequest");

    // Type in the search input
    cy.get('.search-input input[type="text"]').type("David");

    // Verify loading state is shown
    cy.get(".loading-spinner").should("be.visible");

    // Wait for the search request to complete
    cy.wait("@searchRequest");

    // Verify loading state is hidden
    cy.get(".loading-spinner").should("not.exist");
  });

  it("should display search results correctly", () => {
    // Mock the search API response
    cy.intercept("GET", "/api/search/*", {
      statusCode: 200,
      body: [
        {
          user: {
            id: 1,
            first_name: "David",
            last_name: "Kim",
            email: "david@example.com",
            username: "davidkim",
          },
          user_type: "missionary",
          city: "Tokyo",
          state: "Tokyo",
          country: "Japan",
          description: "Test description",
          tags: [{ tag_name: "Teaching" }],
        },
      ],
    }).as("searchRequest");

    // Type in the search input
    cy.get('.search-input input[type="text"]').type("David");

    // Wait for the search request to complete
    cy.wait("@searchRequest");

    // Wait for results to be rendered
    cy.get(".results-grid", { timeout: 10000 }).should("be.visible");
    cy.get(".results-grid").should("not.be.empty");

    // Verify results are displayed correctly
    cy.get(".user-card", { timeout: 10000 }).should("have.length", 1);
    cy.get(".user-card")
      .first()
      .within(() => {
        cy.contains("David Kim").should("exist");
        cy.contains("Tokyo, Japan").should("exist");
        cy.contains("Missionary").should("exist");
        cy.contains("Teaching").should("exist");
      });
  });

  it("should handle API errors gracefully", () => {
    // Mock a failed API response
    cy.intercept("GET", "/api/search/*", {
      statusCode: 500,
      body: { error: "Internal server error" },
    }).as("searchRequest");

    // Type in the search input
    cy.get('.search-input input[type="text"]').type("David");

    // Wait for the search request to complete
    cy.wait("@searchRequest");

    // Verify error message is displayed
    cy.get(".error", { timeout: 10000 }).should("be.visible");
    cy.contains("An error occurred while searching").should("exist");
  });

  it("should show no results message when no matches found", () => {
    // Mock empty results response
    cy.intercept("GET", "/api/search/*", {
      statusCode: 200,
      body: [],
    }).as("searchRequest");

    // Type in the search input
    cy.get('.search-input input[type="text"]').type("nonexistentuser123");

    // Wait for the search request to complete
    cy.wait("@searchRequest");

    // Wait for no results message
    cy.get(".no-results", { timeout: 10000 }).should("be.visible");
    cy.contains("No profiles found").should("exist");
  });

  it("should update results when filters change", () => {
    // Mock initial search response
    cy.intercept("GET", "/api/search/*", {
      statusCode: 200,
      body: [
        {
          user: {
            id: 1,
            first_name: "David",
            last_name: "Kim",
            email: "david@example.com",
            username: "davidkim",
          },
          user_type: "missionary",
          city: "Tokyo",
          state: "Tokyo",
          country: "Japan",
          description: "Test description",
          tags: [{ tag_name: "Teaching" }],
        },
        {
          user: {
            id: 2,
            first_name: "David",
            last_name: "Smith",
            email: "david.smith@example.com",
            username: "davidsmith",
          },
          user_type: "supporter",
          city: "New York",
          state: "NY",
          country: "USA",
          description: "Test description",
          tags: [{ tag_name: "Support" }],
        },
      ],
    }).as("initialSearch");

    // Type in the search input
    cy.get('.search-input input[type="text"]').type("David");

    // Wait for initial search
    cy.wait("@initialSearch");

    // Wait for results to be rendered
    cy.get(".results-grid", { timeout: 10000 }).should("be.visible");
    cy.get(".results-grid").should("not.be.empty");

    // Mock filtered response
    cy.intercept("GET", "/api/search/*", {
      statusCode: 200,
      body: [
        {
          user: {
            id: 1,
            first_name: "David",
            last_name: "Kim",
            email: "david@example.com",
            username: "davidkim",
          },
          user_type: "missionary",
          city: "Tokyo",
          state: "Tokyo",
          country: "Japan",
          description: "Test description",
          tags: [{ tag_name: "Teaching" }],
        },
      ],
    }).as("filteredSearch");

    // Select missionary role
    cy.get('.filter-group select[v-model="searchParams.user_type"]').select(
      "missionary"
    );

    // Wait for filtered search
    cy.wait("@filteredSearch");

    // Wait for filtered results to be rendered
    cy.get(".results-grid", { timeout: 10000 }).should("be.visible");
    cy.get(".results-grid").should("not.be.empty");

    // Verify only missionary results are shown
    cy.get(".user-card", { timeout: 10000 }).should("have.length", 1);
    cy.get(".user-card")
      .first()
      .within(() => {
        cy.contains("Missionary").should("exist");
      });
  });
});
