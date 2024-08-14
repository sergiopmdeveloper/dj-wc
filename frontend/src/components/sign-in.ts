import { LitElement, css, html } from 'lit';
import { customElement } from 'lit/decorators.js';
import { addGlobalStyles } from './globalStyles';

@customElement('sign-in')
@addGlobalStyles()
export class SignIn extends LitElement {
  static styles = css`
    main {
      height: 100vh;
      display: flex;
      justify-content: center;
      align-items: center;
    }

    main > div {
      width: 25rem;
      background-color: #f9f9f9;
      box-sizing: border-box;
      border-radius: 0.5rem;
      padding: 1.5rem;
    }

    h1 {
      font-weight: 700;
      margin-bottom: 1.5rem;
    }

    form > div {
      display: flex;
      gap: 0.25rem;
      flex-direction: column;
      margin-bottom: 1rem;
    }

    form > div:last-of-type {
      margin-bottom: 1.5rem;
    }

    input {
      padding: 0.5rem 0 0.5rem 0.5rem;
    }

    button {
      width: 100%;
      font-size: 1rem;
      padding: 0.5rem 0;
    }
  `;

  render() {
    return html`
      <main>
        <div>
          <h1>Sign in</h1>

          <form>
            <div>
              <label for="email">Email</label>
              <input type="text" id="email" name="email" />
            </div>

            <div>
              <label for="password">Password</label>
              <input type="password" id="password" name="password" />
            </div>

            <button type="submit">Send</button>
          </form>
        </div>
      </main>
    `;
  }
}
