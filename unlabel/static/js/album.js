$(document).ready(function () {
    $('.lyrics-form').hide()

    // ADD LYRICS TEXTBOX
    $(".add-lyrics").click(function () {
            $('.lyrics-form').show()
            $('.lyrics pre').hide()

            const song_id = $(this).attr('data-song-id');
            $('.submit-lyrics').attr('data-song-id', song_id)
        }
    )

    // SUBMIT LYRICS
    $('.submit-lyrics').click(function (e) {
        e.preventDefault()
        const ajax_url = $(this).attr('data-ajax-url');
        const song_id = $(this).attr('data-song-id')
        const lyrics = $.trim($('.lyrics-form textarea').val());
        $.ajax({

            url: ajax_url,

            // The data to send (will be converted to a query string)
            data: {
                song_id: song_id,
                lyrics: lyrics
            },

            // Whether this is a POST or GET request
            type: "POST",

            // The type of data we expect back
            dataType: "json",

            headers: {'X-CSRFToken': csrftoken},
        })
            // Code to run if the request succeeds (is done);
            // The response is passed to the function
            .done(function (json) {
                if (json.success === 'success') {
                    // $('.lyrics-form').css('visibility', 'hidden')
                    $('.lyrics-form').hide()
                    $('.lyrics pre').text(lyrics)
                    $('.lyrics pre').show()

                } else {
                    alert("Error: " + json.error)
                }
            })
            // Code to run if the request fails; the raw request and
            // status codes are passed to the function
            .fail(function (xhr, status, errorThrown) {
                alert("Sorry, there was a problem!");
                console.log("Error: " + errorThrown);
                console.log("Status: " + status);
                console.dir(xhr);
            })
            .always(function (xhr, status) {
                // alert("The request is complete!");
            });

    })


    //GET LYRICS
    $(".get-lyrics").click(function () {
        const song_id = $(this).attr('data-song-id');
        const ajax_url = $(this).attr('data-ajax-url');

        $.ajax({

            // The URL for the request
            url: ajax_url,

            // The data to send (will be converted to a query string)
            data: {
                song_id: song_id
            },

            // Whether this is a POST or GET request
            type: "POST",

            // The type of data we expect back
            dataType: "json",

            headers: {'X-CSRFToken': csrftoken},
        })
            // Code to run if the request succeeds (is done);
            // The response is passed to the function
            .done(function (json) {
                if (json.success === 'success') {
                    const song_lyrics = json.song_lyrics;
                    $('.lyrics-form').hide()
                    $('.lyrics pre').show()
                    $('.lyrics pre').text(song_lyrics)

                } else {
                    alert("Error: " + json.error)
                }
            })
            // Code to run if the request fails; the raw request and
            // status codes are passed to the function
            .fail(function (xhr, status, errorThrown) {
                alert("Sorry, there was a problem!");
                console.log("Error: " + errorThrown);
                console.log("Status: " + status);
                console.dir(xhr);
            })
            // Code to run regardless of success or failure;
            .always(function (xhr, status) {
                // alert("The request is complete!");
            });

    })

    $(".post-comment").click(function (){

        const ajax_url = $(this).attr('data-ajax-url');
        const album_id = $(this).attr('data-album-id');
        const comment = $.trim($('.comment-input').val());

        $.ajax({

            // The URL for the request
            url: ajax_url,

            // The data to send (will be converted to a query string)
            data: {
                comment: comment,
                album_id: album_id
            },

            // Whether this is a POST or GET request
            type: "POST",

            // The type of data we expect back
            dataType: "json",

            headers: {'X-CSRFToken': csrftoken},
        })
            // Code to run if the request succeeds (is done);
            // The response is passed to the function
            .done(function (json) {
                if (json.success === 'success') {
                    $('.comment-input').val('')
                    $('.no-comments').css('display', 'none')
                    const comment = json.comment.body;
                    const name = json.comment.name;
                    const image = json.comment.image;
                    const username = json.comment.username;
                    const comment_id = json.comment.id;
                    $('.posts').prepend("<div>\n" +
                        "                    <img src=\"/static/"+ image +"\" alt=\"\"/>\n" +
                        "                    <div>\n" +
                        "                        <a style=\"color: white\" href=\"../../artist/"+ username +"\">\n" +
                        "                            <h3>"+ name +"</h3></a><span\n" +
                        "                            class=\"date\">Just Now</span><br>\n" +
                        "                            <button class=\"edit-comment-button\">Edit</button>\n" +
                        "                            <button data-comment-id=\""+ comment_id +"\"\n" +
                        "                                    data-ajax-url=\"/album/delete_comment/\" class=\"delete-comment\">Delete\n" +
                        "                            </button>\n" +
                        "                            <br>\n" +
                        "                           <p class=\"comment-text\">" + comment + "</p>\n" +
                        "                           <div style=\"display: none\" class=\"edit-comment\">\n" +
                        "                               <input class=\"edit-comment-input\">\n" +
                        "                               <button data-comment-id=\""+ comment_id +"\"\n" +
                        "                                       data-ajax-url=\"/album/edit_comment/\"\n" +
                        "                                        class=\"save-comment\">Save\n" +
                        "                               </button>\n" +
                        "                           </div>\n" +
                        "                    </div>\n" +
                        "                </div>")

                } else {
                    alert("Error: " + json.error)
                }
            })
            // Code to run if the request fails; the raw request and
            // status codes are passed to the function
            .fail(function (xhr, status, errorThrown) {
                alert("Sorry, there was a problem!");
                console.log("Error: " + errorThrown);
                console.log("Status: " + status);
                console.dir(xhr);
            })
            // Code to run regardless of success or failure;
            .always(function (xhr, status) {
                // alert("The request is complete!");
            });
    })

     $(".posts").on("click", '.delete-comment', function (){

        const ajax_url = $(this).attr('data-ajax-url');
        const comment_id = $(this).attr('data-comment-id');

        $.ajax({

            // The URL for the request
            url: ajax_url,

            // The data to send (will be converted to a query string)
            data: {
                comment_id: comment_id,
            },

            // Whether this is a POST or GET request
            type: "POST",

            context: this,

            // The type of data we expect back
            dataType: "json",

            headers: {'X-CSRFToken': csrftoken},
        })
            // Code to run if the request succeeds (is done);
            // The response is passed to the function
            .done(function (json) {
                if (json.success === 'success') {
                    alert('Comment deleted successfully!')
                   $(this).parent().parent().css('display', 'none')

                } else {
                    alert("Error: " + json.error)
                }
            })
            // Code to run if the request fails; the raw request and
            // status codes are passed to the function
            .fail(function (xhr, status, errorThrown) {
                alert("Sorry, there was a problem!");
                console.log("Error: " + errorThrown);
                console.log("Status: " + status);
                console.dir(xhr);
            })
            // Code to run regardless of success or failure;
            .always(function (xhr, status) {
                // alert("The request is complete!");
            });
    })

    $('.posts').on('click', '.edit-comment-button', function () {
        $(this).parent().children('div').css('display', 'block')
        $(this).parent().children('p').css('display', 'none')
        const comment = $(this).parent().children('p').text()
        console.log(comment)
        $(this).parent().children('div').children('input').val(comment)
    })

    $('.posts').on('click','.save-comment', function (){
        const ajax_url = $(this).attr('data-ajax-url');
        const comment_id = $(this).attr('data-comment-id');
        const comment = $(this).parent().children('input').val()

        $.ajax({

            // The URL for the request
            url: ajax_url,

            // The data to send (will be converted to a query string)
            data: {
                comment_id: comment_id,
                comment: comment
            },

            // Whether this is a POST or GET request
            type: "POST",

            // The type of data we expect back
            dataType: "json",

            context: this,

            headers: {'X-CSRFToken': csrftoken},
        })
            // Code to run if the request succeeds (is done);
            // The response is passed to the function
            .done(function (json) {
                if (json.success === 'success') {
                    $(this).parent().parent().children('p').text(comment)
                    $(this).parent().css('display', 'none')
                    $(this).parent().parent().children('p').css('display', 'block')

                } else {
                    alert("Error: " + json.error)
                }
            })
            // Code to run if the request fails; the raw request and
            // status codes are passed to the function
            .fail(function (xhr, status, errorThrown) {
                alert("Sorry, there was a problem!");
                console.log("Error: " + errorThrown);
                console.log("Status: " + status);
                console.dir(xhr);
            })
            // Code to run regardless of success or failure;
            .always(function (xhr, status) {
                // alert("The request is complete!");
            });
    })


});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');
