url = "/api/query/";

$.ajax({
        type: "GET",
        url: url,
        success: store_response(this)
    }
);