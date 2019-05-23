const electron = require('electron');

const {app,BrowserWindow} = electron;

let mainWindow;

//Listen for app ready
app.on('ready',function(){
    //Create new window
    mainWindow = new BrowserWindow({});
    //Load window's HTML page
    mainWindow.loadFile('mainWindow.html');
});