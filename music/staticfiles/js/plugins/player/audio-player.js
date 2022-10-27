$(function () {
    "use strict";
    if ($('.audio-player').length) {
        var myPlayListOtion = '<ul class="more_option"><li><a href="#"><span class="opt_icon" title="Add To Favourites"><span class="icon icon_fav"></span></span></a></li><li><a href="#"><span class="opt_icon" title="Add To Queue"><span class="icon icon_queue"></span></span></a></li><li><a href="#"><span class="opt_icon" title="Download Now"><span class="icon icon_dwn"></span></span></a></li><li><a href="#"><span class="opt_icon" title="Add To Playlist"><span class="icon icon_playlst"></span></span></a></li><li><a href="#"><span class="opt_icon" title="Share"><span class="icon icon_share"></span></span></a></li></ul>';

        var songs = localStorage.getItem('songs');
        songs = JSON.parse(songs);
        // console.log("SONGS IN AUDIO PLAYER:", songs);
        var song_list = []
        if (songs !== null && songs.length > 0) {
            for (var song of songs) {
                // console.log("SONG IN SONGS:", song);
                // delete field.album
                // delete field.created_at
                // delete field.songlist
                // field['options'] = myPlayListOtion
                // song_list.push(field);
                var fields = song.fields;
                delete fields.album;
                delete fields.created_at;
                delete fields.songlist;
                fields['mp3'] = '../../static/media/mp3/' + fields['mp3'];
                fields['oga'] = '../../static/media/mp3/' + fields['oga'];
                fields['options'] = myPlayListOtion;
                song_list.push(fields);
            }
        }


        console.log('song_list: ', song_list);

        var myPlaylist = new jPlayerPlaylist({
            jPlayer: "#jquery_jplayer_1",
            cssSelectorAncestor: "#jp_container_1"
        }, song_list,
            // [{
            //     image: 'assets/images/weekly/song1.jpg',
            //     title: "Adonai",
            //     artist: "Natheniel Bassey",
            //     mp3: "../../static/media/mp3/ADONAI__ __NATHANIEL_BASSEY(128k).mp3",
            //     oga: "../../static/media/mp3/ADONAI__ __NATHANIEL_BASSEY(128k).mp3",
            //     option: myPlayListOtion
            // },
            // {
            //     image: 'assets/images/weekly/song1.jpg',
            //     title: "Covenant Keeping God",
            //     artist: "Victoria Orienze",
            //     mp3: "../../static/media/mp3/Covenant_Keeping_-_Victoria_Orenze_(Lyrics)(128k).mp3",
            //     oga: "../../static/media/mp3/Covenant_Keeping_-_Victoria_Orenze_(Lyrics)(128k).mp3",
            //     option: myPlayListOtion
            // },
            // {
            //     image: 'assets/images/weekly/song1.jpg',
            //     title: "Mighty Warrior",
            //     artist: "Frank Edwards",
            //     mp3: "../../static/media/mp3/Frank_Edwards_-_Mighty_Warrior_ _New_Single_2020(256k).mp3",
            //     oga: "../../static/media/mp3/Frank_Edwards_-_Mighty_Warrior_ _New_Single_2020(256k).mp3",
            //     option: myPlayListOtion
            // },
            // {
            //     image: 'assets/images/weekly/song1.jpg',
            //     title: "Elohim Adonai",
            //     artist: "Apostle Joshua Selman",
            //     mp3: "../../static/media/mp3/Elohim_Adonai_-_Ah_Ah_Ah_Elohim_ _Apostle_Joshua_Selman(128k).mp3",
            //     oga: "../../static/media/mp3/Elohim_Adonai_-_Ah_Ah_Ah_Elohim_ _Apostle_Joshua_Selman(128k).mp3",
            //     option: myPlayListOtion
            // },
            // {
            //     image: 'assets/images/weekly/song1.jpg',
            //     title: "Don’t Let me",
            //     artist: "Mushroom Records",
            //     mp3: "http://www.jplayer.org/audio/mp3/TSP-01-Cro_magnon_man.mp3",
            //     oga: "http://www.jplayer.org/audio/ogg/TSP-01-Cro_magnon_man.ogg",
            //     option: myPlayListOtion
            // }, {
            //     image: 'assets/images/weekly/song2.jpg',
            //     title: "Your Face",
            //     artist: "Ministry",
            //     mp3: "http://www.jplayer.org/audio/mp3/TSP-05-Your_face.mp3",
            //     oga: "http://www.jplayer.org/audio/ogg/TSP-05-Your_face.ogg",
            //     option: myPlayListOtion
            // }, {
            //     image: 'assets/images/weekly/song3.jpg',
            //     title: "Cyber Sonnet",
            //     artist: "You Am I",
            //     mp3: "http://www.jplayer.org/audio/mp3/TSP-07-Cybersonnet.mp3",
            //     oga: "http://www.jplayer.org/audio/ogg/TSP-07-Cybersonnet.ogg",
            //     option: myPlayListOtion
            // }, {
            //     image: 'assets/images/weekly/song4.jpg',
            //     title: "Tempered Song",
            //     artist: "Shelter",
            //     mp3: "http://www.jplayer.org/audio/mp3/Miaow-01-Tempered-song.mp3",
            //     oga: "http://www.jplayer.org/audio/ogg/Miaow-01-Tempered-song.ogg",
            //     option: myPlayListOtion
            // }, {
            //     image: 'assets/images/weekly/song5.jpg',
            //     title: "Hidden",
            //     artist: "Bad Religion",
            //     mp3: "http://www.jplayer.org/audio/mp3/Miaow-02-Hidden.mp3",
            //     oga: "http://www.jplayer.org/audio/ogg/Miaow-02-Hidden.ogg",
            //     option: myPlayListOtion
            // }], 
            {
                swfPath: "js/plugins",
                supplied: "oga, mp3",
                wmode: "window",
                useStateClassSkin: true,
                autoBlur: false,
                smoothPlayBar: true,
                keyEnabled: true,
                playlistOptions: {
                    autoPlay: true
                }
            });
        $("#jquery_jplayer_1").on($.jPlayer.event.ready + ' ' + $.jPlayer.event.play, function (event) {
            console.log("JPPLAYER EVENT READY: ", $.jPlayer.event.ready)
            console.log("JPPLAYER EVENT PLAY: ", $.jPlayer.event.play)
            var current = localStorage.getItem('current');
            // var current = myPlaylist.current;
            console.log("PLAYLIST CURRENT: ", current)
            var playlist = myPlaylist.playlist;
            console.log("PLAYLIST: ", myPlaylist.playlist)
            var fromIndex = current - 3
            var toIndex = 0

            var element = playlist.splice(fromIndex, fromIndex + 1)[0];
            console.log("ELEMENT: ", element)
            playlist.splice(toIndex, 0, element);
            $.each(playlist, function (index, obj) {
                // if (index == current) {
                console.log("INDEX: ", index)
                $(".jp-now-playing").html("<div class='jp-track-name'><span class='que_img'><img src='" + obj.image + "'></span><div class='que_data'>" + obj.title + " <div class='jp-artist-name'>" + obj.artist + "</div></div></div>");
                // }
            });
            $('.knob-wrapper').mousedown(function () {
                $(window).mousemove(function (e) {
                    var angle1 = getRotationDegrees($('.knob')),
                        volume = angle1 / 270

                    if (volume > 1) {
                        $("#jquery_jplayer_1").jPlayer("volume", 1);
                    } else if (volume <= 0) {
                        $("#jquery_jplayer_1").jPlayer("mute");
                    } else {
                        $("#jquery_jplayer_1").jPlayer("volume", volume);
                        $("#jquery_jplayer_1").jPlayer("unmute");
                    }
                });

                return false;
            }).mouseup(function () {
                $(window).unbind("mousemove");
            });


            function getRotationDegrees(obj) {
                var matrix = obj.css("-webkit-transform") ||
                    obj.css("-moz-transform") ||
                    obj.css("-ms-transform") ||
                    obj.css("-o-transform") ||
                    obj.css("transform");
                if (matrix !== 'none') {
                    var values = matrix.split('(')[1].split(')')[0].split(',');
                    var a = values[0];
                    var b = values[1];
                    var angle = Math.round(Math.atan2(b, a) * (180 / Math.PI));
                } else { var angle = 0; }
                return (angle < 0) ? angle + 360 : angle;
            }





            var timeDrag = false;
            $('.jp-play-bar').mousedown(function (e) {
                timeDrag = true;
                updatebar(e.pageX);

            });
            $(document).mouseup(function (e) {
                if (timeDrag) {
                    timeDrag = false;
                    updatebar(e.pageX);
                }
            });
            $(document).mousemove(function (e) {
                if (timeDrag) {
                    updatebar(e.pageX);
                }
            });
            var updatebar = function (x) {
                var progress = $('.jp-progress');
                var position = x - progress.offset().left;
                var percentage = 100 * position / progress.width();
                if (percentage > 100) {
                    percentage = 100;
                }
                if (percentage < 0) {
                    percentage = 0;
                }
                $("#jquery_jplayer_1").jPlayer("playHead", percentage);
                $('.jp-play-bar').css('width', percentage + '%');
            };
            $('#playlist-toggle, #playlist-text, #playlist-wrap li a').unbind().on('click', function () {
                $('#playlist-wrap').fadeToggle();
                $('#playlist-toggle, #playlist-text').toggleClass('playlist-is-visible');
            });
            $('.hide_player').unbind().on('click', function () {
                $('.audio-player').toggleClass('is_hidden');
                $(this).html($(this).html() == '<i class="fa fa-angle-down"></i> HIDE' ? '<i class="fa fa-angle-up"></i> SHOW PLAYER' : '<i class="fa fa-angle-down"></i> HIDE');
            });
            $('body').unbind().on('click', '.audio-play-btn', function () {
                $('.audio-play-btn').removeClass('is_playing');
                $(this).addClass('is_playing');
                var playlistId = $(this).data('playlist-id');
                myPlaylist.play(playlistId);
            });

        });
    }
});