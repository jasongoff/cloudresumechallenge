# Chunk 1: Building the Front End
## Steps 2 & 3 - Creating the Static Content
I used my current CV as the basis for the content, but decided to use this as a springboard to learning a bit of CSS.  The resulting HTML and CSS and can be found in the [src](src) folder.

---
## Step 4 - Creating the Static S3 website
I already had a registered domain, Neptune19.com, set up in Route53, so I decided to create a subdomain to serve the resume. [jasongoff.neptune19.com](http://jasongoff.neptune19.com)

I created an S3 bucket to serve the static website.  See [this article](https://docs.aws.amazon.com/AmazonS3/latest/userguide/HostingWebsiteOnS3Setup.html) for a guide.

CloudFormation template: [cft/cloudresume-bucket.yaml](cft/cloudresume-bucket.yaml)

The template was validated and deployed via the AWS CLI:
```
aws cloudformation validate-template --template-body file://cloudresume-bucket.yaml

aws cloudformation deploy --template-file cloudresume-bucket.yaml --stack-name cloud-resume-bucket
```
and to remove it again...
```
aws cloudformation delete-stack --stack-name cloud-resume-bucket
```

---
## Step 5 - Securing with HTTPS and Amazon Cloudfront
Following [this guide](https://aws.amazon.com/blogs/networking-and-content-delivery/amazon-s3-amazon-cloudfront-a-match-made-in-the-cloud/) I used option B first, then tried option C.  Both templates are in the [cft](cft/) folder.

---
## Step 6 - Setting up Amazon Route53 for custom DNS domain routing
As previously mentioned, I already had a registered domain, so decided to create a subdomain in Route53.

I created a new Route53 hosted zone for the subdomain `jasongoff.neptune19.com` following [this guide](https://aws.amazon.com/premiumsupport/knowledge-center/create-subdomain-route-53/).

CloudFormation template: [cft/route53-hostedzone.yaml](cft/route53-hostedzone.yaml).

Finally, in my Route53 hosted zone I created A and CNAME records to point toward the S3 static website by setting them up as an Alias pointing to `s3-website-us-east-1.amazonaws.com`.

Once complete, the [resumé was available](http://jasongoff.neptune19.com/).




Page 68

