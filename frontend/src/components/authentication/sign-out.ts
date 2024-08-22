import axios from 'axios';
import { LitElement, css, html } from 'lit';
import { customElement } from 'lit/decorators.js';
import { addGlobalStyles } from '../globalStyles';

@customElement('sign-out')
@addGlobalStyles()
export class SignOut extends LitElement {
  static styles = css`
    button {
      font-size: 1rem;
      color: darkred;
      background-color: lightcoral;
      padding: 0.5rem;
    }
  `;

  render() {
    return html`<button @click=${this.signOut}>Sign Out</button>`;
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
