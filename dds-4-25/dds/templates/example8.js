data = {
    "query": window.query_uri,
    "field": "/api/censusfield/10/",
    "type": "eq",
    "value": "LAS VEGAS"
};

url = "/api/queryfilter/";

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