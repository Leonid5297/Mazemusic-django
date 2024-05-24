// Mythium Archive: https://archive.org/details/mythium/
function sendRequest() {
  url = "http://127.0.0.1:8000/my_music/search/all/";
  return fetch(url).then(response => {
    return response.text()
  })
}
jQuery(function ($) {
    sendRequest()
        .then(data => {
            // Здесь tracks доступна и можно использовать jQuery
            console.log(data);
            // ... (дальнейшая обработка с jQuery)
            'use strict'
            var supportsAudio = !!document.createElement('audio').canPlayType;
            if (supportsAudio) {
                // initialize plyr
                var player = new Plyr('#audio1', {
                    controls: [
                        'restart',
                        'play',
                        'progress',
                        'current-time',
                        'duration',
                        'mute',
                        'volume',
                        'download'
                    ]
                });
                // initialize playlist and controls
                var index = 0,
                    playing = false,
                    mediaPath = 'http://localhost:8000/',
               //     mediaPath = 'C:/Users/rebir/django_project/maze_music/my_music\\static/',
                    extension = '',
                    tracks = JSON.parse(data)
                    buildPlaylist = $.each(tracks, function (key, value) {
                        var trackNumber = value.track,
                            trackName = value.name,
                            trackDuration = value.duration;
                        if (trackNumber.toString().length === 1) {
                            trackNumber = '0' + trackNumber;
                        }
                        $('#plList').append('<li> \
                        <div class="plItem"> \
                            <span class="plNum">' + trackNumber + '.</span> \
                            <span class="plTitle">' + trackName + '</span> \
                            <span class="plLength">' + trackDuration + '</span> \
                        </div> \
                    </li>');
                    }),
                    trackCount = tracks.length,
                    npAction = $('#npAction'),
                    npTitle = $('#npTitle'),
                    audio = $('#audio1').on('play', function () {
                        playing = true;
                        npAction.text('Now Playing...');
                    }).on('pause', function () {
                        playing = false;
                        npAction.text('Paused...');
                    }).on('ended', function () {
                        npAction.text('Paused...');
                        if ((index + 1) < trackCount) {
                            index++;
                            loadTrack(index);
                            audio.play();
                        } else {
                            audio.pause();
                            index = 0;
                            loadTrack(index);
                        }
                    }).get(0),
                    btnPrev = $('#btnPrev').on('click', function () {
                        if ((index - 1) > -1) {
                            index--;
                            loadTrack(index);
                            if (playing) {
                                audio.play();
                            }
                        } else {
                            audio.pause();
                            index = 0;
                            loadTrack(index);
                        }
                    }),
                    btnNext = $('#btnNext').on('click', function () {
                        if ((index + 1) < trackCount) {
                            index++;
                            loadTrack(index);
                            if (playing) {
                                audio.play();
                            }
                        } else {
                            audio.pause();
                            index = 0;
                            loadTrack(index);
                        }
                    }),
                    li = $('#plList li').on('click', function () {
                        var id = parseInt($(this).index());
                        if (id !== index) {
                            playTrack(id);
                        }
                    }),
                    loadTrack = function (id) {
                        $('.plSel').removeClass('plSel');
                        $('#plList li:eq(' + id + ')').addClass('plSel');
                        npTitle.text(tracks[id].name);
                        index = id;
                        audio.src = mediaPath + tracks[id].file + extension;
                        console.log(audio.src)
                        updateDownload(id, audio.src);
                    },
                    updateDownload = function (id, source) {
                        player.on('loadedmetadata', function () {
                            $('a[data-plyr="download"]').attr('href', source);
                        });
                    },
                    playTrack = function (id) {
                        loadTrack(id);
                        audio.play();
                    };
                extension = audio.canPlayType('audio/mpeg') ? '.mp3' : audio.canPlayType('audio/ogg') ? '.ogg' : '';
                loadTrack(index);
            } else {
                // no audio support
                $('.column').addClass('hidden');
                var noSupport = $('#audio1').text();
                $('.container').append('<p class="no-support">' + noSupport + '</p>');
            }
        })
        .catch(error => {
            console.error("Ошибка:", error);
        });

});