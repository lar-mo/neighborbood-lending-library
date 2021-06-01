//////////////////////////////////////
//
// Author: Larry Moiola
// Date: Feb 10, 2021
// Filename: anonymous.spec.js
//
//////////////////////////////////////

const domain_under_test = Cypress.env('host')

describe('Anonymous', () => {

  it('Homepage', () => {

    cy.visit(domain_under_test)

    // Verify all page elements; add check Logout link
    cy.get('section > img')
      .should('have.attr', 'src')
      .should('contain', 'lendingLib_logo2.png')

  }) // end of 'Homepage'

}) // end of 'describe - Anonymous'
