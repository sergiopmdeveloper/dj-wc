import { LitElement, css, html } from 'lit';
import { customElement, property } from 'lit/decorators.js';
import { addGlobalStyles } from '../globalStyles';

@customElement('user-info-form')
@addGlobalStyles()
export class UserInfoForm extends LitElement {
  @property({ attribute: 'first-name' })
  firstName: string = '';

  @property({ attribute: 'last-name' })
  lastName: string = '';

  static styles = css`
    h1 {
      color: black;
      margin-bottom: 1.5rem;
    }

    form > div {
      display: flex;
      flex-direction: column;
      gap: 0.25rem;
      margin-bottom: 1rem;
    }

    form > div:last-of-type {
      margin-bottom: 1.5rem;
    }

    input {
      border-bottom: 1px solid black;
      padding: 0.5rem 0;
    }

    button {
      width: 100%;
      font-size: 1rem;
      padding: 0.5rem 0;
    }
  `;

  render() {
    return html`
      <div class="section-parent">
        <div class="section-child">
          <h1>User info</h1>
          <form>
            <div>
              <label for="first-name">First name</label>

              <input
                type="text"
                id="first-name"
                name="first-name"
                placeholder="First name..."
                .value=${this.firstName}
              />
            </div>

            <div>
              <label for="last-name">Last name</label>
              <input
                type="text"
                id="last-name"
                name="last-name"
                placeholder="Last name..."
                .value=${this.lastName}
              />
            </div>

            <button type="submit">Save</button>
          </form>
        </div>
      </div>
    `;
  }
}
