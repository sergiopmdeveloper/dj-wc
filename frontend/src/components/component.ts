import { LitElement, css, html } from 'lit';
import { customElement, property } from 'lit/decorators.js';

@customElement('component-test')
export class MyComponent1 extends LitElement {
  @property() name = 'World';

  static styles = css`
    p {
      color: red;
    }
  `;

  render() {
    return html`<p>Hello, ${this.name} from Component 1!</p>`;
  }
}
