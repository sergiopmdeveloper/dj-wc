import axios from 'axios';
import { LitElement, css, html } from 'lit';
import { customElement, property } from 'lit/decorators.js';
import { addGlobalStyles } from '../globalStyles';

@customElement('app-header')
@addGlobalStyles()
export class AppHeader extends LitElement {
  @property({ attribute: 'user-id' })
  userId: string = '';

  static styles = css`
    div {
      height: 4rem;
      background-color: black;
    }

    header {
      height: 100%;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    h1 {
      color: white;
      font-size: 1.5rem;
    }

    button {
      height: 2rem;
      font-size: 1rem;
      color: white;
      background-color: grey;
      border-radius: 0.25rem;
      padding: 0.5rem;

      &:hover {
        filter: brightness(0.9);
      }
    }
  `;

  render() {
    return html`
      <div class="section-parent">
        <header class="section-child">
          <h1>Brand</h1>
          ${this.userId
            ? html` <button @click=${this.signOut}>Sign out</button> `
            : ''}
        </header>
      </div>
    `;
  }

  /**
   * Signs the user out
   */
  signOut() {
    axios.get(`${window.location.origin}/sign-out`).then(() => {
      window.location.href = '/sign-in';
    });
  }
}
