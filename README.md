# Search a function
###Business Problem and the solution
-Now-a-days there are millions of code repositories and finding a function to decode errors or changing the existing functionality  in that huge codebase is a difficult task.
-Search a function application is designed to reduce the complexity and increase the accessibility to the code with a few clicks.
###Data Extraction for the project
-Google Big Query contains a full snapshot of more than 2.8 million open source GitHub repositories with an estimate of over 500 GB of data.
-Data is extracted from the Google Big Query tables by querying (with the help of Big Query and standard SQL) the required fields and saving it in the Google Cloud Platform.
-Data is then migrated from GCP to Amazon S3 bucket and is processed with the help of spark job.
