const electron = require('electron');

const {app,BrowserWindow,Menu} = electron;
let isLoggedIn = false;
let mainWindow;

//Listen for app ready
app.on('ready',function(){
    //Create new window
    mainWindow = new BrowserWindow({
        width: 400,
        height: 500,
        resizable: false
    });
    //Load window's HTML page
    mainWindow.loadFile('mainWindow.html');
    //Build menue from template
    const mainMenu = Menu.buildFromTemplate(mainMenuTemplate);
    //Insert menu
    Menu.setApplicationMenu(mainMenu);
});
//Create menu template
const mainMenuTemplate = [
    {
        label: 'File',
        submenu:[
            {
                label: 'About'
            }
        ]
    }
];
//Add development tools when not in production mode
if(process.env.NODE_ENV !== 'production'){
    mainMenuTemplate.push(
        {
            label: 'Developer Tools',
            submenu:[
                {
                    label: 'Toggle DevTools',
                    accelerator: process.platform == 'darwin' ? 'Command+I' : 'Ctrl+I',
                    click(item,focusedWindow){
                        focusedWindow.toggleDevTools();
                    }
                },
                {
                    role: 'reload'
                }
            ]
        },
    );
}