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
    if (type == 'file'){
        $.ajax({
          dataType: 'native',
          url: "/file_browser",
          type: "get"
          xhrFields: {
            responseType: 'blob'
          },
          success: function(blob){
            console.log(blob.size);
              var link=document.createElement('a');
              link.href=window.URL.createObjectURL(blob);
              link.download=name;
              document.body.appendChild(link);
              link.click();
          }
        });
    }
    else {
        $.ajax({
          url: "/file_browser",
          type: "get",
          data: {jsdata: type+','+name},
          success: function(response) {
            $("#file_browser").html(response);
          },
          error: function(xhr) {
            //Do Something to handle error
          }
        });
    }
}