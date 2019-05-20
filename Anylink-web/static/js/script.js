function hashpass() {
  var pwdObj = document.getElementById('inputpasswordh');
  var hashObj = new jsSHA("SHA-256", "TEXT", {numRounds: 1});
  hashObj.update(pwdObj.value);
  var hash = hashObj.getHash("HEX");
  pwdObj.value = hash;
  document.getElementById('inputpasswordh').hidden = "true";
  document.getElementById('inputmailh').hidden = "true";
}

function send_path(type,name) {
    $.ajax({
        url: "/file_browser",
        type: "get",
        data: {jsdata: type+','+name},
        success: function(response) {
            console.log('success')
            console.log(type)
            $("#file_browser").html(response);
            if (type == 'file'){
                console.log('open win')
                var win = window.open('/download_file', '_blank');
                if (win) {
                    //Browser has allowed it to be opened
                    console.log('focus win')
                    win.focus();
                } else {
                    //Browser has blocked it
                    alert('Please allow popups for this website');
                }
            }
        },
        error: function(xhr) {
        //Do Something to handle error
        }
        console.log('end')
    });
}
