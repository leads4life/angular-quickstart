const pages = [
  { path: '/', heading: 'Fresh Flavors' },
  { path: '/menu', heading: 'Explore Our' },
  { path: '/about', heading: 'About' },
  { path: '/private-events', heading: 'Private' },
  { path: '/order-online', heading: 'Order' },
  { path: '/catering', heading: 'Catering' },
  { path: '/gallery', heading: 'Gallery' },
  { path: '/contact', heading: 'Contact' },
];

describe('Golden Wok site', () => {
  pages.forEach(({ path, heading }) => {
    it(`renders ${path}`, () => {
      cy.visit(path);
      cy.get('h1').should('contain', heading);
      cy.get('.site-footer').should('be.visible');
      cy.get('main img').first().should(($img) => {
        expect(($img[0] as HTMLImageElement).naturalWidth).to.be.greaterThan(0);
      });
    });
  });

  it('navigates from the header', () => {
    cy.viewport(1280, 800);
    cy.visit('/');
    cy.get('#site-nav').contains('Menu').click();
    cy.location('pathname').should('eq', '/menu');
    cy.get('#starters').should('exist');
  });
});
