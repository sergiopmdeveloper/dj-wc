import { css } from 'lit';

const globalStyles = css`
  :host {
    --screen-xl: 1280px;
  }

  h1 {
    margin: 0;
  }

  p {
    margin: 0;
  }

  input {
    width: 100%;
    box-sizing: border-box;
    outline: 0;
    border: 0;
  }

  button {
    cursor: pointer;
    border: 0;
  }

  .section-parent {
    width: 100%;
    padding: 0 1rem;
    margin-bottom: 1rem;
    box-sizing: border-box;
  }

  .section-child {
    max-width: var(--screen-xl);
    margin: 0 auto;
  }
`;

/**
 * Class decorator to add global styles to a component
 * @returns The class decorator
 */
export function addGlobalStyles() {
  return function <T extends { new (...args: any[]): {} }>(constructor: T) {
    return class extends constructor {
      static styles = [globalStyles, (constructor as any).styles || []].flat();
    };
  };
}
