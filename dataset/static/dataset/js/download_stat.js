$(".value-button").on("click", function () {

    var $button = $(this);
    var $input = $button.parent().find("input");
    var oldValue = $input.val();
    var url = $('#image').data("url")
    var image_id = $('#image').data("id")
    var type = $input.attr("id");
    var csrf = $('#image').data("csrf");
    var send = true

    if ($button.text() == "+") {
        if (oldValue >= 0) {
            var newVal = parseFloat(oldValue) + 1;
        } else {
            newVal = 0;
            send = false
        }

    } else {
        if (oldValue > 0) {
            var newVal = parseFloat(oldValue) - 1;
        } else {
            newVal = 0;
            send = false
        }
    }
    if (send) {
        $.ajax({
            type: "POST",
            url: url,
            data: {
                'image_id': image_id,
                'type': type,
                'count': newVal,
                'csrfmiddlewaretoken': csrf,
            },
            success: function () {
                $input.val(newVal);
            }
        });
    }
    // $input.val(newVal);

});