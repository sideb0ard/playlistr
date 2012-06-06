function showPlaylists(lusername) {
    var playlistUrl = "http://playrrr.com/playlist/";
    $.getJSON(playlistUrl, function(data) {
        var items = [];

        $.each(data, function(key,val) {
            //alert("JSON Line: " + val);
            var playlist = jQuery.parseJSON(val);
            // alert( playlist.Name );
            items.push('<li id="' + key + '"><a href="' + playlistUrl + playlist['Playlist ID'] + '">' + playlist.Name + '</a></li>');
        });

        $('<ul/>', {
            'class': 'my-new-list',
            html: items.join('')
        }).appendTo("#content"); 
    });
}

// $("#content").html(
