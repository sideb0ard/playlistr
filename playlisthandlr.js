function showPlaylists(lusername) {
    var playlistUrl = "http://playrrr.com/playlist/";
    xreqHandler(playlistUrl, function()
            {
                if (xreq.readyState==4 && xreq.status==200) {
                    $("#content").append(xreq.responseText);

                } 
            });
}
