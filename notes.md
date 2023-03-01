# Notes
Basic notes that I made whilst working through the fantastic [Cloud Resume Challenge](https://cloudresumechallenge.dev/docs/the-challenge/) by Forrest Brazeal.

I started the challenge in March 2023 as a vehicle for focussing my Cloud learning.

## Safety Net - Creating an AWS Organisation
### Root AWS Account
I already had an AWS account secured with root and MFA, that I had used in the past in the *Original Way*, so I decided to use that as my Organisations Account and follow the *Professional Way*.

Before starting, I created a new Access Key for this project and revoked all previous ones.

I also set up a profile for this access key in my AWS credentials file.

```
[cloudresume]
output = json
region = us-east-1
aws_access_key_id = ######
aws_secret_access_key = ######
```
I then created an environment variable to point to this profile by default, to avoid having to type `--profile` on every aws cli command.

```
SET AWS_PROFILE=cloudresume
```

### Setting up the AWS Organisation
I decided to forego my old habit of doing everything through the AWS Console, and try to learn Infrastructure-As-Code (IAC) as I went along.

Install [org-formation](https://github.com/org-formation/org-formation-cli)
```
npm install -g aws-organization-formation
npx org-formation --help
```
Generate an org-formation template
```
npx org-formation init organization.yml --region us-east-1 
```
This didn't work from corporate network as Node was failing to find local certificate, despite adding entry to the .npmrc file, so I bypassed Node cert checking
```
set NODE_TLS_REJECT_UNAUTHORIZED=0
```
Then I got a template!  I followed [this](https://github.com/org-formation/org-formation-reference) process to set up org-formation.

I enabled SSO on the AWS Account, and then created a CloudFormation [template](cft/iam-setup.yaml) (cft) to create the groups and users on the account. It took several attempts to get the CLI to work validating and executing the template.
```
aws cloudformation validate-template --template-body file://iam-setup.yaml
```
informed me that I needed to set `CAPABILITY_NAMED_IAM` on the create command:
```
aws cloudformation create-stack --stack-name cloud-resume-iam --template-body file://iam-setup.yaml --capabilities CAPABILITY_NAMED_IAM
```
My account already had Admin and Developers groups, so I only created the Auditor and Supporter group.





  


