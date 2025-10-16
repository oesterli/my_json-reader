import { LitElement, html, css } from "lit";
import { customElement, state } from "lit/decorators.js";

@customElement("my-app")
export class MyApp extends LitElement {
  @state() private data: any = null;
  @state() private loading = false;
  @state() private error: string | null = null;

  static styles = css`
    :host {
      display: block;
      font-family: system-ui, sans-serif;
      padding: 1.5rem;
      color: #333;
    }

    button {
      padding: 0.5rem 1rem;
      border: none;
      border-radius: 8px;
      background-color: #0078d7;
      color: white;
      cursor: pointer;
    }

    button:hover {
      background-color: #005fa3;
    }

    pre {
      background: #f4f4f4;
      padding: 1rem;
      border-radius: 8px;
      overflow-x: auto;
    }
  `;

  render() {
    return html`
      <h1>📡 API-Daten mit Lit + TypeScript</h1>
      <button @click=${this._fetchData}>API abrufen</button>

      ${this.loading
        ? html`<p>Lade Daten...</p>`
        : this.error
        ? html`<p style="color:red;">Fehler: ${this.error}</p>`
        : this.data
        ? html`<pre>${JSON.stringify(this.data, null, 2)}</pre>`
        : html`<p>Noch keine Daten geladen.</p>`}
    `;
  }

  private async _fetchData() {
    this.loading = true;
    this.error = null;
    this.data = null;

    try {
      // Beispiel-API: JSONPlaceholder (kannst du anpassen)
      // const res = await fetch("https://jsonplaceholder.typicode.com/posts/1");
      const res = await fetch("http://localhost:8000/api/v1/");
      if (!res.ok) throw new Error(`HTTP-Fehler: ${res.status}`);
      this.data = await res.json();
    } catch (err: any) {
      this.error = err.message;
    } finally {
      this.loading = false;
    }
  }
}
