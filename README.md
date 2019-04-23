# photoshare
Simple app for sharing photos with friends

## Prerequisites to use with GAE

- Create a project no Google Cloud Platform and an app in APP Engine.
- Install the [Google Cloud SDK](https://cloud.google.com/sdk/install) on the local machine and enable the sdk to your project.
- Create a service account and set roles and permissions for APIs. Download the json file with credentials.
- Enable APIs (Cloud SQL, Datastore, Storage).
- Create an instance and database in Cloud SQL. Then perform the flask migration.
- Create a bucket on the Storage and make it public.
- Create a Datastore and execute the command ```sh gcloud app deploy index.yaml``` to create indexes.
- In your local machine, create the docker container for this project. Then perform for sql proxy:
-- ```sh./cloud_sql_proxy --dir=/cloudsql -instances='[INSTANCE_CONNECTION_NAME]'=tcp:0.0.0.0:3306 -credential_file=./cloudsql/credentials.json```


