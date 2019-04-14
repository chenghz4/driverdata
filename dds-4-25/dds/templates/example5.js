url = "/api";

$.ajax({
        type: "GET",
        url: url,
        success: store_response(this)
    }
);

url = "/api/censusfield/schema";

$.ajax({
        type: "GET",
        url: url,
        success: store_response(this)
    }
);