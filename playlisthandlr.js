var playlistUrl = "http://playrrr.com/playlist/";

function showPlaylists(lusername) {
    $.getJSON(playlistUrl, function(data) {
        var items = [];

        $.each(data, function(key,val) {
            //alert("JSON Line: " + val);
            var playlist = jQuery.parseJSON(val);
            // alert( playlist.Name );
            items.push('<li id="' + key + '"><a href="javascript:showPlaylist(' + playlist['Playlist ID'] + ')">' + playlist.Name + '</a></li>');
        });

        $('<ul/>', {
            'class': 'my-new-list',
            html: items.join('')
        }).appendTo("#content"); 
    });
}

function showPlaylist(playlistID) {
    var fullUrl = playlistUrl + playlistID
    $.getJSON(fullUrl, function(data) {
        var items = [];
        alert(data);
    
        //$.each(data, function(key,val) {
            // alert("JSON key: " + val);
            //var playlistItem = jQuery.parseJSON(val);
            // alert("PLAYLIST " + playlist);
            // items.push('<li id="' + key + '"><a href="javascript:showTracklist(' + val + ')">BLAH</a></li>');
        //}); 

        /* $('<ul/>', {
            'class': 'my-new-list',
            html: items.join('')
        }).appendTo("#content"); */
    });
}
    

// $("#content").html(
