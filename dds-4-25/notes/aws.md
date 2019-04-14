<link rel='stylesheet' href='markdown9.css'/>

Account info
------------

AWS Account ID: `7254-8562-1300`

Canonical User ID: `941328e0783d599dc517790889f0163537b035d770b08038eb1250642b5df1b9`

IAM
---

IAM sign-in: https://725485621300.signin.aws.amazon.com/console

andrew: `AKIAITKKIBHGZSZAP6JA CEfXnfyJi0s9SbpS76ex4pgURwX1Yb8qKKNz1t3t`

password: `Wk)W4Q%pjGDd`

andrew granted PowerUser access:

    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "NotAction": "iam:*",
          "Resource": "*"
        }
      ]
    }

dds: `AKIAIYBLUL5XVYA7FVSQ Lo7ibHUwUqMvuhybKL/PVxf+/FDMJdichM7PW2LL`

dds granted full access to the S3 dds-exports bucket:

    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Sid": "Stmt1394853316000",
          "Effect": "Allow",
          "Action": [
            "s3:*"
          ],
          "Resource": [
            "arn:aws:s3:::dds-exports/*",
            "arn:aws:s3:::dds-exports"
          ]
        }
      ]
    }

dds granted full access to SES:

    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Sid": "Stmt1394853444000",
          "Effect": "Allow",
          "Action": [
            "ses:*"
          ],
          "Resource": [
            "*"
          ]
        }
      ]
    }

SES
---

Added datadrivenshipping.com as a domain
               
Verification records: 

    _amazonses.datadrivenshipping.com. TXT "Q8VUijZQzwAwMJkB+lf2AaGHG1sa/RErewVWBnjXI6I=" - - 1800
    46nokl7n6ufpgnrpo5qxptumiegdxb3b._domainkey.datadrivenshipping.com. CNAME 46nokl7n6ufpgnrpo5qxptumiegdxb3b.dkim.amazonses.com - - 1800 
    bsconsix5i64rdbfqaqbtdntaootryoj._domainkey.datadrivenshipping.com. CNAME bsconsix5i64rdbfqaqbtdntaootryoj.dkim.amazonses.com - - 1800
    rofjbbg43cx5jojbho64pobda4u237vg._domainkey.datadrivenshipping.com. CNAME rofjbbg43cx5jojbho64pobda4u237vg.dkim.amazonses.com - - 1800

Requested production access:

    Use Case Description: To send signup and password reset emails to users

We are required to regularly check https://console.aws.amazon.com/ses/home?region=us-west-2 for bounces/complaints

Production access was approved within 1-2 hours

S3
--

Added bucket "dds-exports" to Northern California region. 

No logging, no notifications, no automatic deletion, no versioning.

Route 53
--------

Created datadrivenshipping.com hosted zone

Nameservers:
    
    ns-483.awsdns-60.com.
    ns-789.awsdns-34.net.
    ns-1179.awsdns-19.org.
    ns-1537.awsdns-00.co.uk.

Copied all records over to Route 53 to prevent disruption of other services
