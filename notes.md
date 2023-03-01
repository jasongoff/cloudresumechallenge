# Notes
Basic notes that I made whilst working through the fantastic [Cloud Resume Challenge](https://cloudresumechallenge.dev/docs/the-challenge/) by Forrest Brazeal.

I started the challenge in March 2023 as a vehicle for focussing my Cloud learning.

# Safety Net - Creating an AWS Organisation
## Root AWS Account
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

## Setting up the AWS Organisation - org-formation
I decided to forego my old habit of doing everything through the AWS Console, and try to learn Infrastructure-As-Code (IAC) as I went along.

Install [org-formation](https://github.com/org-formation/org-formation-cli)
```
npm install -g aws-organization-formation
npx org-formation --help
```
Generate an org-formation template
```
npx org-formation init organization.yml --region us-east-1 --cross-account-role-name OrganizationFormationBuildAccessRole --print-stack --verbose
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

Then I realised the guide didn't mean IAM groups, it meant SSO groups! 

```
aws cloudformation delete-stack --stack-name cloud-resume-iam
```

 OK then.  Google-Fu drew a blank on how to create SSO Groups with CFTs, so back to the console for those.  

## Information Gathered for step 4.

|Parameter|Description|My Setting|
|--|--|--|
|SSO start URL|Go to AWS SSO -> Settings -> User Portal -> User Portal URL|https://d-9067ada9ca.awsapps.com/start|
|{{sso-instance-arn}}|Go to AWS SSO -> Settings -> ARN|arn:aws:sso:::instance/ssoins-7223a1d999336e35|
|{{sso-admin-group-id}}|Go to AWS SSO -> Groups -> Administrator -> Details -> Group ID|f4487468-5031-70db-b28d-57a641cae0be|
|{{sso-auditor-group-id}}|Go to AWS SSO -> Groups -> Auditor -> Details -> Group ID|d438f498-d0f1-7023-04bf-2e5932d1ae7c|
|{{sso-developer-group-id}}|Go to AWS SSO -> Groups -> Developer -> Details -> Group ID|d408d4d8-a041-7090-41c5-cf0b8126e6f2|
|{{sso-supporter-group-id}}|Go to AWS SSO -> Groups -> Supporter -> Details -> Group ID|141874d8-4061-70c7-5fe1-d746cabb8a45|
|{{management-account-id}}|12 digit identifier of the management account|284148388796|
|{{state-bucket-name}}|S3 bucket where the IaC state will be stored|organization-formation-state-284148388796-prd|
|{{organization-name}}|Alias of the management account|jasongoff|
|{{primary-aws-region}}|The primary AWS region to deploy to|us-east-1|
|{{management-root-email-address}}|Email address used to register the management account|jason@goff.me.uk
|{{compliance-root-email-address}}|Email address for the compliance account|jason+compliance@goff.me.uk|
|{{orgbuild-root-email-address}}|Email address for the org build account|jason+orgbuild@goff.me.uk|

Search and replace in the instructions isn't perfect.  Particularly emails did not get replaced correctly.

I had to search for `email` in the code and replace with a relevant email address.

## Onto Step 5 - executing org-formation

Continue at step 5.2 [here](https://github.com/org-formation/org-formation-reference)








  


