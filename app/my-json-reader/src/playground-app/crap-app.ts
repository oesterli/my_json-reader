import { LitElement, html, css } from "lit";
import { customElement, state, property} from "lit/decorators.js";

@customElement("crap-app")
export class CrapApp extends LitElement {
 
  // Property only internally availble
  @state() private check: boolean = true;
 
 // Publicly availble property
 @property({ type: String }) name = 'Default name';

 // Define styles for this element 
  static styles = css`
    .overall-wrapper {
      background-color: beige;
    }

    h1 {
      display: block;
      font-family: system-ui, sans-serif;
      padding: 1.5rem;
      color: #333;
    }
    .info {
        background-color: green;
    }
  `;

// Render element
  render() {
    return html`
      <div class=overall-wrapper>
        <h1>💩Crap-App💩</h1>
        <div class=info>${this.name}</div>
        <div>Inital state: ${this.check}</div>
        <div ${this._check()}> State changed: ${this.check}</div>
      </div>

    `;
  }

// Define a function
private _check() {
  this.check = false;
}
  


}