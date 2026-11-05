/**
 * CLIENT-API.JS - PUENTE CLIENTE-SERVIDOR CON EL BACKEND DE PYTHON
 * Conecta la interfaz visual y el visor 3D WebGL con los motores en Python.
 */

class PythonSimulatorBridge {
  constructor() {
    this.isPythonBackendAvailable = false;
    this.checkConnection();
  }

  async checkConnection() {
    try {
      const res = await fetch('/api/hardware/recognition', { method: 'GET' });
      if (res.ok) {
        this.isPythonBackendAvailable = true;
        console.log("✓ Backend en Python conectado y listo.");
      }
    } catch(e) {
      this.isPythonBackendAvailable = false;
      console.log("ℹ Modo cliente local (Inicia 'python main.py' para activar el motor Python completo).");
    }
  }

  // VS Code Engine
  async executeCode(code, language) {
    if (!this.isPythonBackendAvailable) return null;
    try {
      const res = await fetch('/api/vscode/execute', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code, language })
      });
      return await res.json();
    } catch(e) {
      return null;
    }
  }

  // Linux Terminal
  async executeLinuxCommand(command) {
    if (!this.isPythonBackendAvailable) return null;
    try {
      const res = await fetch('/api/terminal/linux', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ command })
      });
      return await res.json();
    } catch(e) {
      return null;
    }
  }

  // Windows Terminal
  async executeWindowsCommand(command) {
    if (!this.isPythonBackendAvailable) return null;
    try {
      const res = await fetch('/api/terminal/windows', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ command })
      });
      return await res.json();
    } catch(e) {
      return null;
    }
  }

  // Web Studio
  async previewWebStudio(html, css, js) {
    if (!this.isPythonBackendAvailable) return null;
    try {
      const res = await fetch('/api/web/preview', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ html, css, js })
      });
      return await res.json();
    } catch(e) {
      return null;
    }
  }

  // Hardware Recognition Quiz
  async validateQuiz(compId, answerIndex) {
    if (!this.isPythonBackendAvailable) return null;
    try {
      const res = await fetch('/api/hardware/recognition/quiz', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ comp_id: compId, answer_index: answerIndex })
      });
      return await res.json();
    } catch(e) {
      return null;
    }
  }

  // Hardware Placement Validation
  async validatePlacement(partId, slotId) {
    if (!this.isPythonBackendAvailable) return null;
    try {
      const res = await fetch('/api/hardware/placement/validate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ part_id: partId, slot_id: slotId })
      });
      return await res.json();
    } catch(e) {
      return null;
    }
  }

  // Hardware Upgrade Action
  async upgradeAction(action, slotKey) {
    if (!this.isPythonBackendAvailable) return null;
    try {
      const endpoint = action === 'unmount' ? '/api/hardware/upgrade/unmount' : '/api/hardware/upgrade/install';
      const res = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ slot_key: slotKey })
      });
      return await res.json();
    } catch(e) {
      return null;
    }
  }

  // Hardware Maintenance Tool
  async applyMaintenanceTool(tool) {
    if (!this.isPythonBackendAvailable) return null;
    try {
      const res = await fetch('/api/hardware/maintenance/tool', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ tool })
      });
      return await res.json();
    } catch(e) {
      return null;
    }
  }
}

window.pythonBridge = new PythonSimulatorBridge();
