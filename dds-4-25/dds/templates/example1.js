data = {
    "stripe_token": window.stripetoken,
    "plan_type": "monthly"
};

url = "/payments/subscription/";

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