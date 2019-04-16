$(document).on('mouseover', 'div.item-container', function (e) {
    $(this).addClass('hovered');
});

$(document).on('mouseout', 'div.item-container', function (e) {
    $(this).removeClass('hovered');
});

$(function () {

    $(".js-upload-photos").click(function () {
        $("#fileupload").click();
    });

    $("#fileupload").fileupload({
        dataType: 'json',
        sequentialUploads: true,

        // start: function (e) {
        //     $("#modal-progress").modal("show");
        // },

        stop: function (e) {
            $(".progress-bar").css({ "width": 0 });
            $(".progress-bar").text("");
        },

        progressall: function (e, data) {
            var progress = parseInt(data.loaded / data.total * 100, 10);
            var strProgress = progress + "%";
            $(".progress-bar").css({ "width": strProgress });
            $(".progress-bar").text(strProgress);
        },

        done: function (e, data) {
            if (data.result.is_valid) {
                $(".preview-container").append(
                    "<div class='item-container'><div class='image'><img class='image-style' src='" + data.result.url + "' style='margin: " + data.result.margin + "px 0;'></div><div class='image-name'>" + data.result.name + "</div><div id='delete-image-" + data.result.id + "' class='close-btn'><div class='page-control'><span class='page-control-icon smpdf_3eHO47el2SyBBY'><svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 30 30'><path fill-rule='evenodd' d='M13.582 15.001l-7.875-7.88L5 6.414 6.415 5l.707.707 7.873 7.88 7.874-7.88.707-.707 1.415 1.414-.707.707-7.875 7.88 7.875 7.88.707.708-1.415 1.414-.707-.708-7.874-7.879-7.873 7.88-.707.707L5 23.589l.707-.707 7.875-7.88z'></path></svg></span></div></div></div>"
                )
            }
        }

    });

});

$(document).ready(function () {
    $(".close-btn").click(function () {
        var id = $(this).attr('id');
        $.ajax({
            type: 'DELETE',
            url: "{% url 'dataset:upload' %}",
            data: { 'pk': id },
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-CSRFToken", "{{ csrf_token }}");
            },
            success: function (response) {
            }
        });
    });
});