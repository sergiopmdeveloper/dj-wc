import { LitElement, css, html } from 'lit';
import { customElement, property } from 'lit/decorators.js';
import { addGlobalStyles } from './globalStyles';

@customElement('email-confirmation')
@addGlobalStyles()
export class EmailConfirmation extends LitElement {
  @property({ attribute: 'email' })
  email: string = '';

  static styles = css`
    main {
      height: 100vh;
      display: flex;
      justify-content: center;
      align-items: center;
      padding: 0 1rem;
    }

    div {
      text-align: center;
    }

    h1 {
      font-size: 2rem;
      margin-bottom: 1rem;
    }

    p {
      font-size: 1.2rem;
    }
  `;

  render() {
    return html`
      <main>
        <div>
          <h1>Activate your account</h1>

          <p>
            You have successfully registered. Please check your email
            <strong>${this.email}</strong> for a confirmation link.
          </p>
        </div>
      </main>
    `;
  }
}
