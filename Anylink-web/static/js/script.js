function hashpass() {
  var pwdObj = document.getElementById('inputpasswordh');
  var hashObj = new jsSHA("SHA-256", "TEXT", {numRounds: 1});
  hashObj.update(pwdObj.value);
  var hash = hashObj.getHash("HEX");
  pwdObj.value = hash;
  document.getElementById('inputpasswordh').hidden = "true";
  document.getElementById('inputmailh').hidden = "true";
}

function set_type(var type) {
    elmnt =document.getElementById(type)
    elmnt.value = 'TRUE'
}