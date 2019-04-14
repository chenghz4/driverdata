data = {
    "query": window.query_uri,
    "export_format":$("select#format").val()
};

url = "/api/exportjob/";

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