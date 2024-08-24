import axios from 'axios';
import { LitElement, css, html } from 'lit';
import { customElement, property, state } from 'lit/decorators.js';
import { addGlobalStyles } from '../globalStyles';

@customElement('user-info-form')
@addGlobalStyles()
export class UserInfoForm extends LitElement {
  @property({ attribute: 'csrf-token' })
  csrfToken: string = '';

  @property({ attribute: 'first-name' })
  firstName: string = '';

  @property({ attribute: 'last-name' })
  lastName: string = '';

  @state()
  private currentFirstName: string = '';

  @state()
  private currentLastName: string = '';

  @state()
  private sending: boolean = false;

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

    button:disabled {
      cursor: not-allowed;
    }
  `;

  render() {
    return html`
      <div class="section-parent">
        <div class="section-child">
          <h1>User info</h1>
          <form @submit=${this.updateUserInfo}>
            <div>
              <label for="first-name">First name</label>

              <input
                type="text"
                id="first-name"
                name="first-name"
                placeholder="First name..."
                .value=${this.firstName}
                @input=${this.handleInputChange}
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
                @input=${this.handleInputChange}
              />
            </div>

            <button
              type="submit"
              ?disabled=${this.isFormUnchanged() || this.sending}
            >
              Save
            </button>
          </form>
        </div>
      </div>
    `;
  }

  willUpdate(changedProperties: Map<string, any>) {
    if (
      changedProperties.has('firstName') &&
      this.firstName !== this.currentFirstName
    ) {
      this.currentFirstName = this.firstName;
    }
    if (
      changedProperties.has('lastName') &&
      this.lastName !== this.currentLastName
    ) {
      this.currentLastName = this.lastName;
    }
  }

  /**
   * Updates the current first name and last
   * name values when the input fields change
   *
   * @param {Event} e - The input event
   */
  private handleInputChange(e: Event) {
    const target = e.target as HTMLInputElement;

    if (target.id === 'first-name') {
      this.currentFirstName = target.value;
    } else if (target.id === 'last-name') {
      this.currentLastName = target.value;
    }
  }

  /**
   * Checks if the form is unchanged
   *
   * @returns {boolean} - True if the form is unchanged, false otherwise
   */
  private isFormUnchanged(): boolean {
    return (
      this.currentFirstName === this.firstName &&
      this.currentLastName === this.lastName
    );
  }

  /**
   * Handles the user info form submission
   *
   * @param {Event} e - The submit event from the form
   */
  async updateUserInfo(e: Event) {
    e.preventDefault();

    this.sending = true;

    const form = e.target as HTMLFormElement;
    const formData = new FormData(form);

    try {
      await axios.post(`${window.location.origin}/user`, formData, {
        headers: {
          'X-CSRFToken': this.csrfToken,
        },
      });

      this.firstName = this.currentFirstName;
      this.lastName = this.currentLastName;
    } catch (error) {
      console.error(error);
    } finally {
      this.sending = false;
    }
  }
}
