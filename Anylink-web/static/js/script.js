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
        $("#file_browser").html(response);
      },
      error: function(xhr) {
        //Do Something to handle error
      }
    });
}