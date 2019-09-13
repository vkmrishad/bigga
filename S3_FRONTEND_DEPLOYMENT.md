# Deploy your angular/react based front-end code on AWS

1. Go to your S3 console
1. Create a new bucket. Lets assume the bucket name is `myappfrontend`
1. On thhe "Configure options" select your relevant options
1. On the "Set persmissions" page, UNCHECK "block all public access"
1. Review and hit "Create Bucket"
1. Click on the bucket that you just created and select "permissions" (You will be taken to the "Permissions" tab on bucket settings page)
1. Go to "Access Control List" tab
1. I the "Public access" section of this page, select the "Everyone" radio option
1. And CHECK the "Read bucked permissions" & "List Objects" options and hit "Save"
1. Go the "Properties" tab in the bucket setting page.
1. Select "static website hosting"
1. Select "Use this bucket to host a website" option
1. Enter "index.html" in both Index and Error document inputs
1. Bucket settings are configures. We should configure ACM options
1. Go to ACM console (Amazon Certificate Manager) & Make sure you are in `US East (N. Virginia)` region (Other regions are NOT SUPPORTED by CloudFront)
1. Hit on "Get Started" button in the "Provision certificates" Section
1. Select "Request a public certificate" and hit "Request a certificate" button.
1. In the domain names, add all your domain names (For example `myapp.com`. You can add more subdomains here including wildcard subdomains `*.myapp.com`)
1. Hit "Next" button
1. Select "DNS Validation" radio option and hit "Review" button
1. Confirm your domain name(s) abd click "Confirm and request"
1. You will be taken to validation page
1. Copy the CNAME settings from the validation page into your DNS settings (typically from someone like GoDaddy or name.com. Whereever you have registed your `myapp.com` from)
1. Once you are preety sure that you have added the right CNAME to tight domain, click "Continue"
1. YOu should see a "Pending Validation" message no the certificate you requested (If you are lucky you will see the validation successful immedietly)
1. If validation is still pending, wait for sometime for DNS changes to propagate and hit the refresh button to check the validation status.
1. After 5-10 mins, if you still seeing "Pending Validation", you can be pretty sure that you did something wrong. Check the settings once again or delete the old certificate, and try requesting new one from ACM console.
1. Everything worked well if you see a Green "Issued" in the status of your certificate
1. ACM is configured. We should configure CloudFront options
1. Go to the Cloudfront confole.
1. Hit "Create Distribution" button
1. Select "Get started" option in the "Web" Section.
1. In the "Origin Domain Name", selct the s3 bucket that you just created above (for eg. `myappfrontend`)
1. In the "Viewer Protocol Policy" select "Redirect HTTP to HTTPS"
1. In the "Compress Object Aautomatically", select "Yes" option (This will enable gzip)
1. In the alternate domain names, input the domain you want (For example, `myapp.com`)
1. Select "Custom SSL CErtificate" radio option and select the `myapp.com` certificate that you created in the ACM
1. THE DOMAIN NAME IN CLOUDFRONT AND THE DOMAIN NAME IN ACM MUST MATCH
1. In the "Default root object" input, enter "index.html"
1. Hit "Create Distribution"
1. It will take about 10 minutes for the Distribution to be deployed
1. Meanwhile, click on the Distribution and open the distribution settings
1. Click on "Error Pages" and hit create custom response
1. Select 404 not found in HTTP error code
1. In the "customize error response", select "Yes"
1. In the "Response Page Path", enter "/index.html"
1. In the HTTP Response Code select "200: OK"
1. Hit "Create" button
1. This custom error response MUST be make to support SPA so your SPAs routing will still work after refresh

## Enable gzip
1. Go to the "behaviors" tab
1. CLick on "Create Behavior"
1. In pattern path selct "*"
1. Selct the "Compress Objects by default" option and save it.


## Advantages
