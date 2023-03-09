# Chunk 1: Building the Front End
I used my current CV as the basis for the content, but decided to use this as a springboard to learning a bit of CSS.  The resulting HTML and CSS and can be found in the [src](src) folder.

---
## Creating the Static S3 website
I already had a registered domain, Neptune19.com, set up in Route53, so I decided to create a subdomain to serve the resume. [jasongoff.neptune19.com](http://jasongoff.neptune19.com)

The idea here is to create a Route53 entry and a bucketname that are the same as each other, then by certain configuration outlined below, Route53 will route HTTP traffic to your bucket static site!

I created a new Route53 hosted zone `jasongoff.neptune19.com` following [this guide](https://aws.amazon.com/premiumsupport/knowledge-center/create-subdomain-route-53/).

CloudFormation template: [cft/route53-hostedzone.yaml](cft/route53-hostedzone.yaml).

The template was validated and deployed via the AWS CLI:
```
aws cloudformation validate-template --template-body file://route53-hostedzone.yaml

aws cloudformation deploy --template-file route53-hostedzone.yaml --stack-name jasongoff-hosted-zone
```
and to remove it again...
```
aws cloudformation delete-stack --stack-name jasongoff-hosted-zone
```

Once the hosted zone was setup, I then created the S3 bucket to serve the static website.  See [this article](https://docs.aws.amazon.com/AmazonS3/latest/userguide/HostingWebsiteOnS3Setup.html) for a guide.

Finally, in my Route53 hosted zone I created A and CNAME records to point toward the S3 static website by setting them up as an Alias pointing to `s3-website-us-east-1.amazonaws.com`.

Once complete, the [resumé was available](http://jasongoff.neptune19.com/).




Page 68

