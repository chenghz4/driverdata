data = {
    "name": "Companies in Las Vegas",
    "sort_by": "/api/censusfield/2/"
};

url = "/api/query/";

$.ajax({
        type: "POST",
        accepts: "application/json",
        contentType: "application/json",
        data: JSON.stringify(data),
        url: url,
        header: {
            "X-CSRFToken": window.csrftoken
        },
        success: store_response(this)
    }
);