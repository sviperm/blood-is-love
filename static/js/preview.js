$("#id_file").on('change', function () {
    $(this).next('.form-control-file').addClass("selected");

    //Get count of selected files
    var countFiles = $(this)[0].files.length;

    var imgPath = $(this)[0].value;
    var extn = imgPath.substring(imgPath.lastIndexOf('.') + 1).toLowerCase();
    var image_holder = $("#image_holder");
    var image_list = $("#image_list");
    image_holder.empty();
    image_list.empty();

    $('input[type="file"]').each(function () {
        if ($('input[type="file"]').val() != "") {
            $('#upload_images').attr({
                disabled: false,
            });
            $('#color_picker_btn').attr({
                disabled: false,
            });
        } else {
            $('#upload_images').attr({
                disabled: true,
            });
            $('#color_picker_btn').attr({
                disabled: true,
            });
        }
    });

    // TODO: добавить разрешения
    if (extn == "gif" || extn == "png" || extn == "jpg" || extn == "jpeg" || extn == "bmp") {

        //loop for each file selected for uploaded.
        for (var i = 0; i < countFiles; i++) {
            (function (count, self) {
                var reader = new FileReader()
                reader.onload = function (e) {
                    if (count == 0) {
                        $("<a />", {
                            "id": "image-link-" + count,
                            "class": "list-group-item list-group-item-action active",
                            "href": "#image-" + count,
                            html: "<i class='far fa-image'></i> " + self.files[count].name,
                        }).appendTo(image_list);
                    } else {
                        $("<a />", {
                            "class": "list-group-item list-group-item-action ",
                            "href": "#image-" + count,
                            html: "<i class='far fa-image'></i> " + self.files[count].name,
                        }).appendTo(image_list);
                    }
                    $("<h4 />", {
                        "id": "image-" + count,
                        text: self.files[count].name,
                    }).appendTo(image_holder);
                    $("<img />", {
                        "src": e.target.result,
                        "class": "scroll-img"
                    }).appendTo(image_holder);
                }
                reader.readAsDataURL(self.files[count])
            })(i, this);
        }
        $('#preview_block').removeClass("d-none");
    } else {
        $(this).next('.form-control-file').removeClass("selected");
        $('#preview_block').addClass("d-none");
    }
});

$('#clear_list').on('click', function () {
    $("#id_file").val('');
    $("#image_holder").empty();
    $("#image_list").empty();
    $('.form-control-file').removeClass("selected");
    $('#preview_block').addClass("d-none");
});

$('#upload_images').on('click', function () {
    $('input[type="file"]').each(function () {
        if ($('input[type="file"]').val() != "") {
            $('#upload_images').attr({
                'class': 'btn btn-primary',
                disabled: true,
            });
            $('#color_picker_btn').attr({
                disabled: true,
            });
            $('#clear_list').attr({
                disabled: true,
            });
            $('#upload_images').html('<span class="spinner-grow spinner-grow-sm" role="status" aria-hidden="true"></span> Запустить');
            // $('#upload_images').html('<span class="spinner-grow spinner-grow-sm" role="status" aria-hidden="true"></span> Думаю...');
            $('form').submit();
        }
    });

});

$(document).ready(function () {
    $('.range-picker').jRange({
        from: 0,
        to: 150,
        step: 5,
        scale: [0, 30, 60, 90, 120, 150],
        format: '%s',
        width: 265,
        showLabels: true,
        snap: true
    });
});

$(document).ready(function () {
    $('.range-slider-h').jRange({
        from: 0,
        to: 180,
        step: 1,
        format: '%s',
        scale: [0, 36, 72, 108, 144, 180],
        width: 265,
        showLabels: true,
        isRange: true
    });
});

$(document).ready(function () {
    $('.range-slider-s, .range-slider-v').jRange({
        from: 0,
        to: 255,
        step: 1,
        format: '%s',
        scale: [0, 51, 102, 153, 204, 255],
        width: 265,
        showLabels: true,
        isRange: true
    });
});


$(document).on('click', '.dropdown-menu', function (e) {
    e.stopPropagation();
});
