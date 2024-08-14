import { css } from 'lit';

const globalStyles = css`
  h1 {
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
