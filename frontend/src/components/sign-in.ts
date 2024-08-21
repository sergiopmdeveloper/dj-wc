import axios, { AxiosError } from 'axios';
import { LitElement, css, html } from 'lit';
import { customElement, property } from 'lit/decorators.js';
import { addGlobalStyles } from './globalStyles';

@customElement('sign-in')
@addGlobalStyles()
export class SignIn extends LitElement {
  @property({ attribute: 'csrf-token' })
  csrfToken: string = '';

  @property({ attribute: 'sending' })
  sending: boolean = false;

  @property({ attribute: 'errors' })
  errors: string[] = [];

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

    p {
      font-size: 0.8rem;
      color: red;
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
      <main>
        <div>
          <h1>Sign in</h1>

          <form @submit=${this.signIn}>
            <div>
              <label for="email">Email</label>
              <input type="text" id="email" name="email" autocomplete="email" />
            </div>

            <div>
              <label for="password">Password</label>
              <input type="password" id="password" name="password" />
            </div>

            ${this.errors.length
              ? html`<div>
                  ${this.errors.map((error) => html`<p>${error}</p>`)}
                </div>`
              : ''}

            <button type="submit" ?disabled=${this.sending}>
              ${this.sending ? 'Sending...' : 'Send'}
            </button>
          </form>
        </div>
      </main>
    `;
  }

  /**
   * Handles the sign in form submission

   * @param {Event} e - The submit event from the form
   * @returns {Promise<void>} - The promise that resolves when the request is successful
   * @throws {AxiosError} When the request fails
   */
  async signIn(e: Event): Promise<void> {
    e.preventDefault();

    this.sending = true;

    const form = e.target as HTMLFormElement;
    const formData = new FormData(form);

    try {
      await axios.post(`${window.location.origin}/sign-in`, formData, {
        headers: {
          'X-CSRFToken': this.csrfToken,
        },
      });

      this.errors = [];
      window.location.href = '/';
    } catch (error) {
      const axiosError = error as AxiosError;

      if (
        axiosError.response?.status === 422 ||
        axiosError.response?.status === 401
      ) {
        const responseData = axiosError.response.data as SignInErrorData;
        this.errors = responseData.errors;
      }
    } finally {
      this.sending = false;
    }
  }
}

interface SignInErrorData {
  errors: string[];
}
