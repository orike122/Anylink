//imports
const electron = require('electron');
const regedit = require('regedit');
const fs = require('fs');
const path = require('path');
const forge = require('node-forge');
const request = require('request');


process.env.NODE_ENV = 'production'
//globals
const {app,BrowserWindow,Menu,ipcMain} = electron;
var isLoggedIn = false;
let mainWindow;

//Listen for app ready
app.on('ready',function(){
    //Create new window
    mainWindow = new BrowserWindow({
        width: 400,
        height: 500,
        resizable: false,
        webPreferences: {
            nodeIntegration: true
        }
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
function check_reg(callback){
    //check registry for important values
    regedit.list(['HKCU\\SOFTWARE\\Anylink'], function(lserr,result){
        if(lserr) console.log(lserr);
        var res = result['HKCU\\SOFTWARE\\Anylink'];
        key_path = res.values['key_path'].value;
        has_init = res.values['has_init'].value;
        callback(key_path,has_init);
    });
}
function write_user_reg(user){
    //Write value to registry
    var val = {
        'HKCU\\SOFTWARE\\Anylink': {
            'user': {
                value: user,
                type: 'REG_SZ'
            }
        }
    };
    regedit.putValue(val,function(err){
        if(err) console.log(err);
    });
}
function set_has_init(num){
    //Write value to registry
    var val = {
        'HKCU\\SOFTWARE\\Anylink': {
            'has_init': {
                value: num,
                type: 'REG_DWORD'
            }
        }
    };
    regedit.putValue(val,function(err){
        if(err) console.log(err);
    });
}
ipcMain.on('key:open',function(e){
    //when event key:open

    if(isLoggedIn){
        check_reg(function(key_path,has_init){
            if(has_init){
                var pub_key = fs.readFileSync(path.join(key_path,'key.pub'));
            }
            else{
                //create key pair
                var pair = forge.pki.rsa.generateKeyPair(2048);
                var pub_key = forge.ssh.publicKeyToOpenSSH(pair.publicKey);
                var pkey = forge.ssh.privateKeyToOpenSSH(pair.privateKey);

                //write to file key pair
                fs.writeFileSync(path.join(key_path,'key.pub'),pub_key);
                fs.writeFileSync(path.join(key_path,'key'),pkey);

                //change settings in registry
                set_has_init(1);
            }
            mainWindow.webContents.send("key:expose",pub_key);
        });
    }
});
ipcMain.on('cred:submit',function(e,cred){
    //when event cred:submit

    //send's an ajax prot request
    request.post(
        {url: 'https://anylinknow.tk/validate_user',
        json:{
            email: cred.email,
            passh: cred.passh
        }},
        function(err,response,body){;
            if(err) console.log(err);
            if(body){
                if(body.valid){
                    isLoggedIn = true;
                    mainWindow.webContents.send("tab:enable");
                    write_user_reg(cred.email);
                }
                else{
                    isLoggedIn = false;
                }
            }
        });
    
});