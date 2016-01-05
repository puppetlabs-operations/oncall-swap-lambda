# oncall-swap-lambda
An AWS lambda function to override the SysOps PagerDuty oncall schedule if the current oncall person has been paged for N consecutive nights.

# Configuration
The lambda function handler is configured with a JSON file that gets baked in to the zip file during the build process.
To create a new configuration for the lambda copy config.example.json to config.json and edit the file with the appropriate data.
```
cp config.example.json config.json
```

# Building
Create a virtualenv in the project directory and run the build script. It will produce as zip file that you will then upload to AWS.
```
virtualenv .
mkdir build
./build.sh
```

# Upload to AWS
This step assumes you have the aws cli configured and you have the correct access policy in place to use the AWS lambda service.
Run the following command to upload the lambda function to AWS.
```
aws lambda update-function-code --zip-file fileb://$PWD/oncall-swap-lambda.zip --function-name PagerDutyOncallSwap
```

# Basic Testing
You can test through the AWS console using the API gateway workflow editor.
