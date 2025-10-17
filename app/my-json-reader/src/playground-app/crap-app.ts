import { LitElement, html, css } from "lit";
import { customElement, state } from "lit/decorators.js";

@customElement("crap-app")
export class CrapApp extends LitElement {
  @state() private data: any = null;


  static styles = css`
    h1 {
      display: block;
      font-family: system-ui, sans-serif;
      padding: 1.5rem;
      color: #333;
    }
    div {
        background-color: green;
    }
  `;

  render() {
    return html`
      <h1>💩Crap-App💩</h1>
      <div></div>
    `;
  }
}