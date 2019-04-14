url = "/api/censusfield/";

$.ajax({
        type: "GET",
        url: url,
        success: store_response(this)
    }
);