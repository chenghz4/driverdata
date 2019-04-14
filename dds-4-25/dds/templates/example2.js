url = "/api/account/";

$.ajax({
        type: "GET",
        url: url,
        success: store_response(this)
    }
);