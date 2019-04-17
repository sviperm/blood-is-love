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
            $(".drag-n-drop-area").addClass('d-none');
            $(".preview-container").removeClass('d-none');
            $(".upload-more").removeClass('d-none');
            if (data.result.is_valid) {
                $(".preview-container").append(data.result.html_item)
            }
        }

    });

});

$(document).on('hidden.bs.modal', '#modal_error', function () {
    $(this).remove();
});

$(document).on('click', 'button.close-btn', function () {
    var pk = $(this).data("pk");
    var url = $(this).data("url");
    var csrf = $(this).data("csrf");
    var parent = $(this).parent('div.item-container');

    $.ajax({
        type: 'POST',
        dataType: "json",
        url: url,
        data: {
            'pk': pk,
            'csrfmiddlewaretoken': csrf,
        },
        success: function (response) {
            if (response.success) {
                $(parent).remove();
                if ($('.preview-container').children().length == 0) {
                    $(".preview-container").addClass('d-none');
                    $(".upload-more").addClass('d-none');
                    $(".drag-n-drop-area").removeClass('d-none');
                }
            } else {
                // console.log(response);
                $(parent).addClass('container-error');
                $(".preview-container").append(response.html_modal_error)
                $("#modal_error").modal("show");
            }
        }
    });
});
