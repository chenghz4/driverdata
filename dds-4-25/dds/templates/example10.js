url = "/api/exportjob/";

$.ajax({
        type: "GET",
        url: url,
        success: store_response(this)
    }
);