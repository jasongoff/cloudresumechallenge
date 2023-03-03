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

---
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
 OK then.  Google-Fu drew a blank on how to create SSO Groups and Users with CFTs, so back to the console for those.

---
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

---
## Onto Step 5 - executing org-formation

Once the [organization.yml](org-formation/organization.yml) was done, I executed the org-formation command to apply it.
```
npx org-formation update src\organization.yml --verbose
```
Unfortunately this didn't work, and generated an error:
```
WARN: ======================================
WARN: Hi there!
WARN: You just ran into an error when assuming the role OrganizationFormationBuildAccessRole in account 284148388796.
WARN: Possibly, this is due a breaking change in org-formation v0.9.15.
WARN: From v0.9.15 onwards the org-formation cli will assume a role in every account it deploys tasks to.
WARN: This will make permission management and SCPs to deny / allow org-formation tasks easier.
WARN: More information: https://github.com/org-formation/org-formation-cli/tree/master/docs/0.9.15-permission-change.md
WARN: Thanks!
WARN: ======================================
ERROR: error: AccessDenied, aws-request-id: 5ba51416-abf0-4b31-90cc-324280e18b86
ERROR: User: arn:aws:iam::284148388796:user/jasongoff is not authorized to perform: sts:AssumeRole on resource: arn:aws:iam::284148388796:role/OrganizationFormationBuildAccessRole
```
Looking further at the instructions, step 3 seems to create this role, so I executed that (some of the filenames had changed so I updated the command accordingly.)
```
aws cloudformation create-stack --stack-name org-formation-role --template-body file://src/templates/000-org-build/role.yml --capabilities CAPABILITY_NAMED_IAM
```
That managed to create the role!  Now to try the org-formation command again.
```
npx org-formation update src\organization.yml --verbose
```
This time it worked, and I have a new org structure with AWS accounts created for the shared OU.
```
DEBG: account with email jason@goff.me.uk was already part of the organization (accountId: 284148388796).
OC::ORG::MasterAccount        | ManagementAccount             | Create (284148388796)
DEBG: start executing task: CommitHash OC::ORG::MasterAccount ManagementAccount
OC::ORG::MasterAccount        | ManagementAccount             | CommitHash
DEBG: start executing task: Create OC::ORG::OrganizationRoot OrganizationRoot
OC::ORG::OrganizationRoot     | OrganizationRoot              | Create (r-d229)
DEBG: start executing task: CommitHash OC::ORG::OrganizationRoot OrganizationRoot
OC::ORG::OrganizationRoot     | OrganizationRoot              | CommitHash
INFO: done
DEBG: putting object to S3:
{
  "Bucket": "organization-formation-state-284148388796-prd",
  "Key": "{{state-object}}"
}
```
The `zip` command does not work on Windows, so had to use Winzip from Explorer.  I zipped up all the folders and then copied the zip file to the required folder.

Then, I ran the deploy stacks step to set up the OrgBuild account build pipeline.
```
npx org-formation perform-tasks ./src/templates/000-org-build/_tasks.yml --organization-file ./src/organization.yml --max-concurrent-stacks 50 --max-concurrent-tasks 1 --print-stack --verbose
```
That ran to success.

---
## Step 6. Setting up the org-formation repo and Build pipeline
First, I gathered the info needed to complete this step.

|Parameter|Description|Example|
|--|--|--|
|SSO start URL|The landing page URL to be found in the AWS SSO of the management account|https://d-9067ada9ca.awsapps.com/start|
|SSO region|The default region|us-east-1|
|SSO account id|Select the OrgBuild account from the drop-down	|061050625979|
|SSO role name|Select a role with write permission the drop-down|Administrator|
|CLI default client Region|The default region|us-east-1|
|CLI default output format|Whatever format you prefer|yaml|
|CLI profile name|Name of the profile, choose wisely|jg-orgbuild-admin|

Once I had the info, I followed [this guide](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-sso.html#sso-configure-profile-auto) to set up the CLI to use SSO.  I then installed git-codecommit and cloned the repo from the orgbuild account.

Example aws config for CLI SSO
```
[profile jasongoff-mgt]
sso_start_url = https://example.awsapps.com/start#/
sso_region = us-east-1
sso_account_id = 1234567890
sso_role_name = AdministratorAccess
region = us-east-1
output = json

[profile jasongoff-log]
sso_start_url = https://example.awsapps.com/start#/
sso_region = us-east-1
sso_account_id = 0987654321
sso_role_name = AdministratorAccess
region = us-east-1
output = json
```

By setting e.g. `AWS_PROFILE=jasongoff_mgt` on the command line, any AWS CLI commands would use that profile to connect to a signed in SSO session.








  


