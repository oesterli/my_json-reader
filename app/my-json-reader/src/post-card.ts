// src/post-card.ts
import { LitElement, html, css } from "lit";
import { customElement, property } from "lit/decorators.js";

@customElement("post-card")
export class PostCard extends LitElement {
  @property({ type: String }) title = "";
  @property({ type: String }) body = "";

  static styles = css`
    :host {
      display: block;
      border: 1px solid #ccc;
      border-radius: 8px;
      padding: 1rem;
      margin: 0.5rem 0;
      box-shadow: 1px 1px 5px rgba(0,0,0,0.05);
    }
    h3 {
      margin: 0 0 0.5rem 0;
      color: #0078d7;
    }
  `;

  render() {
    return html`
      <h3>${this.title}</h3>
      <p>${this.body}</p>
    `;
  }
}
