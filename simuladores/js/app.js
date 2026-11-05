/**
 * APP.JS - CONTROLADOR PRINCIPAL DE LA SUITE DE SIMULADORES
 * Gestión de módulos, navegación responsiva para Android/Linux/Windows,
 * atajos globales, notificaciones toast y soporte PWA offline
 */

document.addEventListener('DOMContentLoaded', () => {
  // Inicialización de los 4 simuladores de software
  const vsCodeSim = new VSCodeSimulator();
  const linuxTerm = new LinuxTerminal();
  const winTerm = new WindowsTerminal();
  const webStudio = new WebStudio();

  // Inicialización de los 4 simuladores dedicados de hardware
  let simRecog = null;
  let simPlace = null;
  let simUpgrade = null;
  let simClean = null;

  try {
    simRecog = new HardwareRecognitionSim();
    simPlace = new HardwarePlacementSim();
    simUpgrade = new HardwareUpgradeSim();
    simClean = new HardwareMaintenanceSim();
  } catch (err) {
    console.error("Error inicializando simuladores de hardware:", err);
  }

  // Sistema Global de Toasts
  const toastContainer = document.getElementById('toastContainer');
  window.showAppToast = (message, type = 'info') => {
    if (!toastContainer) return;
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    let icon = 'ℹ️';
    if (type === 'success') icon = '✅';
    if (type === 'warning') icon = '⚠️';
    if (type === 'error') icon = '❌';

    toast.innerHTML = `<span>${icon}</span> <span>${message}</span>`;
    toastContainer.appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateY(10px)';
      toast.style.transition = 'all 0.3s ease';
      setTimeout(() => toast.remove(), 300);
    }, 3500);
  };

  // Gestión de Pestañas de Módulos
  const navTabs = document.querySelectorAll('.nav-tab');
  const moduleViews = document.querySelectorAll('.module-view');

  function switchModule(moduleName) {
    navTabs.forEach(tab => {
      const isActive = tab.dataset.module === moduleName;
      tab.classList.toggle('active', isActive);
      if (isActive) {
        tab.scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' });
      }
    });

    moduleViews.forEach(view => {
      const isTarget = view.id === `view-${moduleName}`;
      view.classList.toggle('active', isTarget);
    });

    // Enfoques específicos al entrar al módulo
    if (moduleName === 'linux-term') {
      setTimeout(() => linuxTerm.input && linuxTerm.input.focus(), 100);
    } else if (moduleName === 'windows-term') {
      setTimeout(() => winTerm.input && winTerm.input.focus(), 100);
    } else if (moduleName === 'vscode') {
      setTimeout(() => vsCodeSim.textarea && vsCodeSim.textarea.focus(), 100);
    } else if (moduleName === 'web-studio') {
      webStudio.renderPreview();
    } else if (moduleName.startsWith('sim-')) {
      // Ajuste inmediato del viewport Three.js al cambiar de pestaña
      setTimeout(() => window.dispatchEvent(new Event('resize')), 50);
    }
  }

  navTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      const mod = tab.dataset.module;
      switchModule(mod);
      try {
        history.replaceState(null, null, `#${mod}`);
      } catch(e) {}
    });
  });

  // Restaurar módulo desde hash en URL
  const hash = window.location.hash.replace('#', '');
  if (hash && document.getElementById(`view-${hash}`)) {
    switchModule(hash);
  }

  // Pantalla Completa
  const btnFullscreen = document.getElementById('btnFullscreen');
  if (btnFullscreen) {
    btnFullscreen.addEventListener('click', () => {
      if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen().catch(() => {});
      } else {
        if (document.exitFullscreen) document.exitFullscreen();
      }
    });
  }

  // Modal de Ayuda
  const btnHelp = document.getElementById('btnHelpModal');
  const btnCloseHelp = document.getElementById('btnCloseHelp');
  const helpModal = document.getElementById('helpModal');

  if (btnHelp && helpModal) {
    btnHelp.addEventListener('click', () => {
      helpModal.style.display = 'flex';
    });
  }

  if (btnCloseHelp && helpModal) {
    btnCloseHelp.addEventListener('click', () => {
      helpModal.style.display = 'none';
    });
  }

  if (helpModal) {
    helpModal.addEventListener('click', (e) => {
      if (e.target === helpModal) helpModal.style.display = 'none';
    });
  }

  // Atajos de teclado globales
  window.addEventListener('keydown', (e) => {
    if (e.key === 'F1') {
      e.preventDefault();
      if (helpModal) helpModal.style.display = 'flex';
    } else if (e.key === 'Escape') {
      if (helpModal && helpModal.style.display === 'flex') {
        helpModal.style.display = 'none';
      }
    }
  });

  // Registro de Service Worker para uso 100% Offline (PWA en Android, Windows y Linux)
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
      navigator.serviceWorker.register('sw.js').catch(err => {
        console.log('SW registration note:', err);
      });
    });
  }

  window.showAppToast('Suite de Simuladores cargada con éxito. Compatible con Android, Linux y Windows.', 'success');
});
