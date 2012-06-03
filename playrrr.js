var lusername;
var password;

// AJAX HANDLER AND CALLBACK
var xreq = new XMLHttpRequest();
function xreqHandler(url,afunckd)
{
    xreq.onreadystatechange=afunckd;
    xreq.open("GET",url,true);
    xreq.send();
}


function innit()
{
    if  (readCookie('username') && readCookie('password')) {
        lusername = readCookie('username');
        password = readCookie('password');
        $("#content").html("<h1>" + lusername + "</h1>");
        //$("#content").append(playlists);
        showPlaylists(lusername);
    }
    else {
        document.getElementById("content")
        .innerHTML="<input id=\"lusername\" onfocus=\"this.value=''\" value=\"UserName\"/></input></br></br><input id=\"pword\" value=\"Password\"></input><br/><br/><button id=\"parpbutton\" type=\"button\" onclick=\"authMeBaby()\">pARP</button>";  
    }
}

function authMeBaby() {
    lusername = document.getElementById('lusername').value;
    pword = document.getElementById('pword').value;
    createCookie('username',lusername);
    createCookie('password',pword);
    window.location = "/";
}


function createCookie(name,value) {
    
    var name = name;
    var value = value;
    var days = 7;
    
    if (days) {
        var date = new Date();
        date.setTime(date.getTime()+(days*24*60*60*1000));
        var expires = "; expires="+date.toGMTString();
    }
    else var expires = "";
    document.cookie = name+"="+value+expires+"; path=/";
}

function readCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
    }
    return null;
}

function eraseCookie(name) {
    createCookie(name,"",-1);
}


function signShit(argz)
{
    // :LASTFM SIGNING ALGO - 1. Order parameters. 2. Append secret 3. md5 hash the whole thing
    // STAGE1 - ORDER PARAMS
    // alert("ARGSSS: " + argz);
    var sortedArgz = argz.sort();
    var sig='';
    for (t in sortedArgz)
    {
        sig += sortedArgz[t].replace(/=/g, "");
    }
    sig += secret;
    return hex_md5(sig);
}

