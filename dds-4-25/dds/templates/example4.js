url = "/payments/subscription/1/";

$.ajax({
        type: "DELETE",
        url: url,
        header: {
            "X-CSRFToken": window.csrftoken
        },
        success: store_response(this)
    }
);