import { LitElement, html, css } from "lit";
import { customElement, property, state } from "lit/decorators.js";

@customElement("post-card")
export class PostCard extends LitElement {
  @property({ type: Object }) data: any = {};
  @state() private expandedPaths = new Set<string>(); // speichert geöffnete Knoten

  static styles = css`
  :host {
    display: block;
    border: 1px solid #ccc;
    border-radius: 8px;
    padding: 0.75rem;
    margin: 0.5rem 0;
    background: #fff;
    font-family: "Courier New", monospace;
    font-size: 0.85rem;
    box-shadow: 1px 1px 5px rgba(0, 0, 0, 0.05);
    line-height: 1.3; /* kompakterer Zeilenabstand */
  }

  h3 {
    margin: 0 0 0.5rem 0;
    color: #0078d7;
    font-size: 1rem;
  }

  .json-container {
    background: #f9f9f9;
    border-radius: 6px;
    padding: 0.5rem;
    overflow-y: auto;
    max-height: 300px;
    /*white-space: pre;*/ 
  }

  .key { color: #0078d7; }
  .string { color: #d14; }
  .number { color: #098658; }
  .boolean { color: #b58900; }
  .null { color: #999; }

  .toggle {
    cursor: pointer;
    user-select: none;
    color: #666;
  }
  .toggle:hover { color: #000; }

  .indent {
    margin-left: 1rem; /* etwas kleinere Einrückung */
  }

  /* Optional: Abstände zwischen Zeilen entfernen */
  .indent > div {
    margin: 0;
    padding: 0;
  }

  /* Wenn du möchtest, kannst du den Text vertikal noch enger setzen */
  .json-container div {
    line-height: 1.2;
  }
`;


  render() {
    return html`
      <h3>📄 API Response</h3>
      <div class="json-container">
        ${this._renderJson(this.data, "")}
      </div>
    `;
  }

  private _togglePath(path: string) {
    if (this.expandedPaths.has(path)) {
      this.expandedPaths.delete(path);
    } else {
      this.expandedPaths.add(path);
    }
    this.requestUpdate();
  }

  private _renderJson(data: any, path: string): unknown {
    if (data === null) {
      return html`<span class="null">null</span>`;
    }

    if (Array.isArray(data)) {
      const isExpanded = this.expandedPaths.has(path);
      return html`
        <span class="toggle" @click=${() => this._togglePath(path)}>
          [${isExpanded ? "▼" : "▶"} Array(${data.length})]
        </span>
        ${isExpanded
          ? html`
              <div class="indent">
                ${data.map((item, i) =>
                  html`<div>${this._renderJson(item, `${path}[${i}]`)}</div>`
                )}
              </div>
              <div>] </div>
            `
          : ""}
      `;
    }

    if (typeof data === "object") {
      const isExpanded = this.expandedPaths.has(path);
      const keys = Object.keys(data);
      return html`
        <span class="toggle" @click=${() => this._togglePath(path)}>
          {${isExpanded ? "▼" : "▶"} Object(${keys.length})}
        </span>
        ${isExpanded
          ? html`
              <div class="indent">
                ${keys.map(
                  (key) => html`
                    <div>
                      <span class="key">"${key}"</span>: 
                      ${this._renderJson(data[key], `${path}.${key}`)}
                    </div>
                  `
                )}
              </div>
              <div>}</div>
            `
          : ""}
      `;
    }

    // Primitive Werte
    if (typeof data === "string") {
      return html`<span class="string">"${data}"</span>`;
    }
    if (typeof data === "number") {
      return html`<span class="number">${data}</span>`;
    }
    if (typeof data === "boolean") {
      return html`<span class="boolean">${data}</span>`;
    }

    return html`<span>${String(data)}</span>`;
  }
}
