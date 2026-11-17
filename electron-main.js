const { app, BrowserWindow, screen, ipcMain } = require('electron');
const path = require('path');

let win;

function createWindow() {
  const { width, height } = screen.getPrimaryDisplay().workAreaSize;

  win = new BrowserWindow({
    x: Math.round(width * 0.65),
    y: Math.round(height * 0.15),   // arranca un poco abajo del borde superior
    width: 420,
    height: 640,
    minWidth: 340,
    minHeight: 400,
    frame: false,
    transparent: true,
    alwaysOnTop: true,
    resizable: true,
    movable: true,
    skipTaskbar: false,
    focusable: true,
    hasShadow: false,
    roundedCorners: false,
    webPreferences: {
      contextIsolation: false,
      nodeIntegration: false,
      sandbox: false
    },
    titleBarStyle: 'hidden',
    trafficLightPosition: { x: -100, y: -100 }
  });

  win.loadFile(path.join(__dirname, 'index.html'));

  // Permitir mover la ventana desde el renderer (CSS -webkit-app-region: drag)
  // y también desde IPC si se necesita
  ipcMain.on('window-move', (_, { dx, dy }) => {
    if (win) {
      const [x, y] = win.getPosition();
      win.setPosition(x + dx, y + dy);
    }
  });

  win.on('closed', () => { win = null; });
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) createWindow();
});

ipcMain.on('window-close', () => win?.close());
ipcMain.on('window-minimize', () => win?.minimize());