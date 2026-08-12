<template>
  <div id="app-wrapper">
    <header id="top-bar">
      <h1 id="title">🔐 Deterministic Password Manager</h1>
    </header>

    <div id="main">
      <!-- Left Panel -->
      <div id="left-panel">

        <div class="card" id="intro">
          <h3>About</h3>
          <p>
            A deterministic password manager derives passwords from the inputs you provide — no passwords are stored.
            Use the counter to handle forced resets, and the custom settings to meet specific domain requirements.
          </p>
        </div>

        <div class="card" id="displayPassword" v-if="showPassword">
          <h3>Generated Password</h3>
          <div class="password-box">{{ finalPassword }}</div>
        </div>

        <div class="card" id="defaultDiv">
          <h3>Password Generator</h3>
          <div class="form-group">
            <label>Username</label>
            <input type="text" v-model="username" placeholder="e.g. john@example.com" required>
          </div>
          <div class="form-group">
            <label>Master Password</label>
            <input type="password" v-model="masterPassword" placeholder="Your secret master password" required>
          </div>
          <div class="form-group">
            <label>Domain</label>
            <input type="text" v-model="domain" placeholder="e.g. github.com" required>
          </div>
          <div class="form-group">
            <label>Counter</label>
            <input type="text" v-model="counter" placeholder="e.g. 0" required>
          </div>
          <button class="btn btn-primary" @click="generateDefault">Generate Default Password</button>
        </div>

        <div class="card" id="customDiv">
          <h3>Custom Password Settings</h3>
          <div class="form-row">
            <div class="form-group">
              <label>Length</label>
              <input type="text" v-model="length" placeholder="Default">
            </div>
            <div class="form-group">
              <label>Symbols</label>
              <input type="text" v-model="symbols" placeholder="Default">
            </div>
          </div>
          <div class="checkbox-row">
            <label class="checkbox-label">
              <input type="checkbox" v-model="uppercase">
              <span>Uppercase</span>
            </label>
            <label class="checkbox-label">
              <input type="checkbox" v-model="lowercase">
              <span>Lowercase</span>
            </label>
            <label class="checkbox-label">
              <input type="checkbox" v-model="numbers">
              <span>Numbers</span>
            </label>
          </div>
          <button class="btn btn-secondary" @click="generateCustom">Generate Custom Password</button>
        </div>

      </div>

      <!-- Right Panel -->
      <div id="right-panel">
        <div class="card" id="displaySavedSpecifications">
          <div id="specs-header">
            <h3>Saved Specifications</h3>
            <button class="btn btn-outline" @click="getSavedSpecifications">Refresh</button>
          </div>

          <div v-if="specifications.length === 0" class="empty-state">
            No specifications saved yet. Click Refresh to load.
          </div>

          <div
            v-for="(spec, index) in specifications"
            :key="index"
            class="spec-entry"
          >
            <div class="spec-heading">Entry {{ index + 1 }}</div>
            <div class="spec-grid">
              <span class="spec-key">Username</span><span class="spec-val">{{ spec.username }}</span>
              <span class="spec-key">Domain</span><span class="spec-val">{{ spec.domain }}</span>
              <span class="spec-key">Count</span><span class="spec-val">{{ spec.count }}</span>
              <span class="spec-key">Length</span><span class="spec-val">{{ spec.length === -1 ? 'N/A' : spec.length }}</span>
              <span class="spec-key">Symbols</span><span class="spec-val">{{ spec.symbols === '' ? 'N/A' : spec.symbols }}</span>
              <span class="spec-key">Uppercase</span><span class="spec-val">{{ spec.uppercase === 1 ? 'Yes' : 'No' }}</span>
              <span class="spec-key">Lowercase</span><span class="spec-val">{{ spec.lowercase === 1 ? 'Yes' : 'No' }}</span>
              <span class="spec-key">Numbers</span><span class="spec-val">{{ spec.numbers === 1 ? 'Yes' : 'No' }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
const BASE_URL = "http://localhost:8080/";

export default {
  name: 'MainPage',
  data() {
    return {
      username: '',
      masterPassword: '',
      domain: '',
      counter: '',
      length: '',
      symbols: '',
      uppercase: false,
      lowercase: false,
      numbers: false,
      finalPassword: '',
      showPassword: false,
      specifications: []
    };
  },
  methods: {
    generateDefault() {
      let bodyString = "username=" + encodeURIComponent(this.username);
      bodyString += "&password=" + encodeURIComponent(this.masterPassword);
      bodyString += "&domain=" + encodeURIComponent(this.domain);
      bodyString += "&counter=" + encodeURIComponent(this.counter);

      fetch(BASE_URL + 'defaults', {
        method: "POST",
        body: bodyString,
        credentials: "include",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded"
        }
      }).then(response => {
        console.log("Server responded from default POST!", response);
        response.json().then(data => {
          console.log(data);
          this.displayPassword(data);
        });
      });
    },

    generateCustom() {
      let bodyString = "username=" + encodeURIComponent(this.username);
      bodyString += "&password=" + encodeURIComponent(this.masterPassword);
      bodyString += "&domain=" + encodeURIComponent(this.domain);
      bodyString += "&counter=" + encodeURIComponent(this.counter);
      bodyString += "&length=" + (this.length === '' ? 'default' : encodeURIComponent(this.length));
      bodyString += "&symbols=" + (this.symbols === '' ? 'default' : encodeURIComponent(this.symbols));
      bodyString += "&uppercase=" + encodeURIComponent(this.uppercase);
      bodyString += "&lowercase=" + encodeURIComponent(this.lowercase);
      bodyString += "&numbers=" + encodeURIComponent(this.numbers);

      console.log(bodyString);

      fetch(BASE_URL + 'customs', {
        method: "POST",
        body: bodyString,
        credentials: "include",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded"
        }
      }).then(response => {
        console.log("Server responded from custom POST!", response);
        response.json().then(data => {
          console.log(data);
          this.displayPassword(data);
        });
      });
    },

    getSavedSpecifications() {
      fetch(BASE_URL + 'specifications', {
        method: "GET",
        credentials: "include",
        headers: {}
      }).then(response => {
        console.log("Server responded from specifications GET", response);
        response.json().then(data => {
          console.log(data);
          this.specifications = data;
        });
      });
    },

    displayPassword(data) {
      this.finalPassword = data["encryptedPassword"];
      this.showPassword = true;
    }
  }
};
</script>

<style>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
  font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
}

body {
  background-color: #f0f2f5;
  min-height: 100vh;
}

#app-wrapper {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* ── Header ── */
#top-bar {
  background: linear-gradient(135deg, #1a73e8, #0d47a1);
  padding: 20px 40px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.2);
}

#title {
  color: #ffffff;
  font-size: 1.8rem;
  font-weight: 600;
  letter-spacing: 0.5px;
}

/* ── Two-column layout ── */
#main {
  display: flex;
  flex: 1;
  gap: 24px;
  padding: 28px;
  align-items: flex-start;
}

#left-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 20px;
  min-width: 0;
}

#right-panel {
  width: 380px;
  flex-shrink: 0;
}

/* ── Cards ── */
.card {
  background: #ffffff;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.08), 0 4px 16px rgba(0,0,0,0.06);
}

.card h3 {
  font-size: 1rem;
  font-weight: 600;
  color: #1a73e8;
  text-transform: uppercase;
  letter-spacing: 0.8px;
  margin-bottom: 14px;
  padding-bottom: 10px;
  border-bottom: 2px solid #e8f0fe;
}

#intro p {
  color: #555;
  line-height: 1.65;
  font-size: 0.93rem;
}

/* ── Password result box ── */
.password-box {
  background: #e8f0fe;
  border: 2px dashed #1a73e8;
  border-radius: 8px;
  padding: 14px 18px;
  font-family: "Courier New", Courier, monospace;
  font-size: 1.1rem;
  font-weight: 600;
  color: #0d47a1;
  word-break: break-all;
  letter-spacing: 1px;
}

/* ── Form elements ── */
.form-group {
  display: flex;
  flex-direction: column;
  margin-bottom: 14px;
}

.form-group label {
  font-size: 0.82rem;
  font-weight: 600;
  color: #444;
  margin-bottom: 5px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.form-group input[type="text"],
.form-group input[type="password"] {
  padding: 9px 12px;
  border: 1.5px solid #d0d7de;
  border-radius: 7px;
  font-size: 0.95rem;
  color: #222;
  transition: border-color 0.2s, box-shadow 0.2s;
  outline: none;
}

.form-group input[type="text"]:focus,
.form-group input[type="password"]:focus {
  border-color: #1a73e8;
  box-shadow: 0 0 0 3px rgba(26,115,232,0.15);
}

.form-row {
  display: flex;
  gap: 14px;
}

.form-row .form-group {
  flex: 1;
}

/* ── Checkboxes ── */
.checkbox-row {
  display: flex;
  gap: 20px;
  margin-bottom: 18px;
  flex-wrap: wrap;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 7px;
  cursor: pointer;
  font-size: 0.92rem;
  color: #333;
  font-weight: 500;
}

.checkbox-label input[type="checkbox"] {
  width: 17px;
  height: 17px;
  accent-color: #1a73e8;
  cursor: pointer;
}

/* ── Buttons ── */
.btn {
  display: inline-block;
  padding: 10px 22px;
  border: none;
  border-radius: 8px;
  font-size: 0.93rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s, transform 0.1s, box-shadow 0.2s;
  letter-spacing: 0.3px;
}

.btn:active {
  transform: scale(0.97);
}

.btn-primary {
  background: #1a73e8;
  color: #fff;
  width: 100%;
  margin-top: 4px;
}

.btn-primary:hover {
  background: #1557b0;
  box-shadow: 0 2px 8px rgba(26,115,232,0.35);
}

.btn-secondary {
  background: #34a853;
  color: #fff;
  width: 100%;
  margin-top: 4px;
}

.btn-secondary:hover {
  background: #267a3b;
  box-shadow: 0 2px 8px rgba(52,168,83,0.35);
}

.btn-outline {
  background: transparent;
  color: #1a73e8;
  border: 1.5px solid #1a73e8;
  padding: 7px 16px;
  font-size: 0.85rem;
}

.btn-outline:hover {
  background: #e8f0fe;
}

/* ── Saved Specifications panel ── */
#specs-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 14px;
  padding-bottom: 10px;
  border-bottom: 2px solid #e8f0fe;
}

#specs-header h3 {
  margin-bottom: 0;
  padding-bottom: 0;
  border-bottom: none;
}

.empty-state {
  color: #999;
  font-size: 0.9rem;
  text-align: center;
  padding: 30px 0;
}

.spec-entry {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 14px;
  margin-bottom: 12px;
  border-left: 4px solid #1a73e8;
}

.spec-heading {
  font-weight: 700;
  font-size: 0.88rem;
  color: #1a73e8;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 10px;
}

.spec-grid {
  display: grid;
  grid-template-columns: 90px 1fr;
  gap: 4px 10px;
}

.spec-key {
  font-size: 0.82rem;
  font-weight: 600;
  color: #666;
  text-transform: uppercase;
  letter-spacing: 0.4px;
}

.spec-val {
  font-size: 0.88rem;
  color: #222;
  word-break: break-all;
}

/* ── Responsive ── */
@media (max-width: 800px) {
  #main {
    flex-direction: column;
    padding: 16px;
  }
  #right-panel {
    width: 100%;
  }
}
</style>
