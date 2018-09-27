

# [AWS Credentials] and updating them in .boto file
export AWS_ACCESS_KEY_ID=XXXX
export AWS_SECRET_ACCESS_KEY=XXXX
export AWS_DEFAULT_REGION=us-east-1
export REM_USER=ubuntu


# Generating .boto file in Google cloud platform and
# it with the below credentials
export GOOGLE_ACCESS_KEY_ID= xxxxxxxxxxxxxxx
export GOOGLE_SECRET_ACCESS_KEY_ID= xxxxxxxxxxxxxxx

# command to migrate data from google cloud platform to amazon s3
gsutil rsync -d -r gs://bucketname  s3://bucketname
