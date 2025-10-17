// src/api-view.ts
import { LitElement, html, css } from "lit";
import { customElement, property, state } from "lit/decorators.js";
import { ApiService } from "./api-service";
import "./post-card"; // Import der Unterkomponente

@customElement("api-view")
export class ApiView extends LitElement {
  @property({ type: String }) url = "";

  @state() private data: any[] = [];
  @state() private loading = false;
  @state() private error: string | null = null;

  private apiService = new ApiService();

  static styles = css`
    :host {
      display: block;
      margin: 1rem 0;
    }
  `;

  connectedCallback() {
    super.connectedCallback();
    this._loadData();
  }

  private async _loadData() {
    if (!this.url) return;
    this.loading = true;
    this.error = null;
    this.data = [];

    try {
      const result = await this.apiService.fetchData(this.url);
      // Wenn result ein Array ist, direkt verwenden, sonst Array mit einem Objekt
      this.data = Array.isArray(result) ? result : [result];
    } catch (err: any) {
      this.error = err.message;
    } finally {
      this.loading = false;
    }
  }

  render() {
    if (this.loading) return html`<p>Lade Daten...</p>`;
    if (this.error) return html`<p style="color:red;">Fehler: ${this.error}</p>`;
    if (!this.data.length) return html`<p>Keine Daten vorhanden.</p>`;

    return html`
      ${this.data.map(
        (item) => html`<post-card .title=${item.message}></post-card>`
      )}
    `;
  }
}
