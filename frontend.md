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

aws cloudformation deploy --template-file cloudresume-bucket.yaml --stack-name jasongoff-neptune19-bucket
```
and to remove it again...
```
aws cloudformation delete-stack --stack-name jasongoff-neptune19-bucket
```
If you want to check which stacks are currently deployed
```
aws cloudformation list-stacks --stack-status-filter CREATE_COMPLETE
```
Remove the filter to see all stacked, including deleted ones.

---
## Step 5a (really step 6!) - Adding the Route53 Domain
In order to create a certificate to use with HTTPS, the domain must be registered in the same account using Route53 to create a Hosted Zone.

As previously mentioned, I already had a registered domain, so decided to create a subdomain in Route53.

I created a new Route53 hosted zone for the subdomain `jasongoff.neptune19.com` following [this guide](https://aws.amazon.com/premiumsupport/knowledge-center/create-subdomain-route-53/).

CloudFormation template: [cft/route53-hostedzone.yaml](cft/route53-hostedzone.yaml).

```
aws cloudformation validate-template --template-body file://route53-hostedzone.yaml

aws cloudformation deploy --template-file route53-hostedzone.yaml --stack-name jasongoff-neptune19-route53
```
and to remove it again...
```
aws cloudformation delete-stack --stack-name jasongoff-neptune19-route53
```

---
## Step 5b - Securing with HTTPS and Amazon Cloudfront
Firstly I had to obtain a certificate using Amazon Certificate Manager (ACM).  I did this via the console in my account that was hosting the Route53 Domain. 

Following [this guide](https://aws.amazon.com/blogs/networking-and-content-delivery/amazon-s3-amazon-cloudfront-a-match-made-in-the-cloud/) I used option B to create a Cloudfront distribution for my existing bucket. 

I then enhanced the template to add HTTPS/TLS encryption.  Under the DistributionConfig, I added CNAMEs and Certificate info.
```
      DistributionConfig:
        CNAMEs:
          - jasongoff.neptune19.com
        ...
        other settings
        ...
        ViewerCertificate:
          AcmCertificateArn: arn:aws:acm:us-east-1:1234567890:certificate/267a1f8e-d36a-40cf-9e52-07ef2d2a9999
          CloudFrontDefaultCertificate: false
          MinimumProtocolVersion: TLSv1
          SslSupportMethod: sni-only          
```
I also changed the ViewerProtocolPolicy to https-only.
```
        DefaultCacheBehavior:
          ...
          other settings
          ...
          ViewerProtocolPolicy: 'https-only'
```
The final template is in the [cft](cft/) folder.
```
aws cloudformation validate-template --template-body file://cloudfront-option-b.yaml

aws cloudformation deploy --template-file cloudfront-option-b.yaml --stack-name jasongoff-neptune19-cloudfront
```
and to remove it again...
```
aws cloudformation delete-stack --stack-name jasongoff-neptune19-cloudfront
```
---
## Step 6 - Setting up Amazon Route53 for custom DNS domain routing

Finally, in my Route53 hosted zone I created A records to point toward the Cloudfront distribution by setting them up as an Alias pointing to my CloudFront Distribution `https://d2nkm3yfbzeb17.cloudfront.net`.  See [this guide](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-to-cloudfront-distribution.html) for details.

_Only if you have a subdomain:_
I then checked the 4 nameservers set up in my subdomain hosted zone and added an NS record to my main domain entry (neptune19.com).  See [this guide](https://aws.amazon.com/premiumsupport/knowledge-center/create-subdomain-route-53/) for a refresher of what this means!

Once complete, the [resumé was available](https://jasongoff.neptune19.com/).
