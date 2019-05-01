$("#ask_delete_button").click(function () {
    $('#delete_modal').appendTo("body")
    $('#delete_modal').modal('show')
});

$("#confirm_delete_button").click(function () {
    $('#delete_modal').modal('hide')
    var pk = $(this).data("pk");
    var url = $(this).data("url");
    var csrf = $(this).data("csrf");
    var type = $(this).data("type");
    var parent = $(this).parent('div.item-container');
    $.ajax({
        type: 'POST',
        dataType: "json",
        url: url,
        data: {
            'pk': pk,
            'csrfmiddlewaretoken': csrf,
            'type': type,
        },
        success: function (response) {
            if (response.success) {
                window.location.replace(response.redirect_url);
            } else {
                alert("Ошибка при удалении");
            }
        },
        error: function (response) {
            alert("Ошибка при удалении");
        }

    });
});