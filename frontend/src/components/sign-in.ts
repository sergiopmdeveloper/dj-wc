import { LitElement, html } from 'lit';
import { customElement } from 'lit/decorators.js';

@customElement('sign-in')
export class SignIn extends LitElement {
  render() {
    return html`<p>Sign in component</p>`;
  }
}
