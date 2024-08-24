import { LitElement, css, html } from 'lit';
import { customElement, property } from 'lit/decorators.js';
import { addGlobalStyles } from '../globalStyles';

@customElement('use-toast')
@addGlobalStyles()
export class UseToast extends LitElement {
  @property({ attribute: 'type' })
  type: ToastType = 'warning';

  @property({ attribute: 'message' })
  message: string = '';

  @property({ attribute: 'visible' })
  visible: boolean = true;

  static styles = css`
    span {
      position: absolute;
      font-size: 0.75rem;
      border-radius: 0.25rem;
      padding: 0.5rem;
      right: 0.75rem;
      bottom: 0.75rem;
    }

    .success {
      background-color: lightgreen;
      color: darkgreen;
    }

    .error {
      background-color: lightcoral;
      color: darkred;
    }

    .warning {
      background-color: lightyellow;
      color: darkorange;
    }
  `;

  render() {
    return html`${this.visible
      ? html`<span class="${this.type}">${this.message}</span>`
      : ''}`;
  }

  connectedCallback() {
    super.connectedCallback();
    this.hideToast();
  }

  /**
   * Hide the toast after 3 seconds
   */
  hideToast() {
    setTimeout(() => {
      this.visible = false;
    }, 3000);
  }
}

type ToastType = 'success' | 'error' | 'warning';
