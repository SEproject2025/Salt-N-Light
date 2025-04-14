describe("Search API Tests", () => {
  let authToken;

  beforeEach(() => {
    // Login and get auth token
    cy.request({
      method: "POST",
      url: "http://localhost:8000/api/token/",
      body: {
        username: "testuser1",
        password: "testpass123",
      },
    }).then((response) => {
      expect(response.status).to.eq(200);
      authToken = response.body.access;
    });
  });

  it("should return search results for a valid query", () => {
    cy.request({
      method: "GET",
      url: "http://localhost:8000/api/search/",
      headers: {
        Authorization: `Bearer ${authToken}`,
      },
      qs: {
        q: "David",
        page: 1,
        sort: "recent",
      },
    }).then((response) => {
      // Log the full response for debugging
      cy.log("Search API Response:", JSON.stringify(response.body, null, 2));

      // Verify response structure
      expect(response.status).to.eq(200);
      expect(response.body).to.be.an("array");

      // Verify results array
      if (response.body.length > 0) {
        const firstResult = response.body[0];
        expect(firstResult).to.have.property("user");
        expect(firstResult.user).to.have.property("id");
        expect(firstResult.user).to.have.property("first_name");
        expect(firstResult.user).to.have.property("last_name");
        expect(firstResult).to.have.property("user_type");
        expect(firstResult).to.have.property("city");
        expect(firstResult).to.have.property("country");
        expect(firstResult).to.have.property("tags").and.to.be.an("array");
      }
    });
  });

  it("should return empty results for non-matching query", () => {
    cy.request({
      method: "GET",
      url: "http://localhost:8000/api/search/",
      headers: {
        Authorization: `Bearer ${authToken}`,
      },
      qs: {
        q: "nonexistentuser123",
        page: 1,
        sort: "recent",
      },
    }).then((response) => {
      expect(response.status).to.eq(200);
      expect(response.body).to.be.an("array");
      expect(response.body).to.have.length(0);
    });
  });

  it("should filter by role", () => {
    cy.request({
      method: "GET",
      url: "http://localhost:8000/api/search/",
      headers: {
        Authorization: `Bearer ${authToken}`,
      },
      qs: {
        q: "David",
        user_type: "missionary",
        page: 1,
        sort: "recent",
      },
    }).then((response) => {
      expect(response.status).to.eq(200);
      expect(response.body).to.be.an("array");

      // If there are results, verify they all have the correct user_type
      if (response.body.length > 0) {
        response.body.forEach((result) => {
          expect(result.user_type).to.eq("missionary");
        });
      }
    });
  });
});
