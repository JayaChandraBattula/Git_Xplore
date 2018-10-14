### PostgreSQL table schemas:

// table for inserting details for each repos
  javarepos(

     repo_id text PRIMARY KEY,
     repo_name text,
     repo_path text,
     repo_size text,
     class_name text,
     method_names text,
     method_dependencies text    )
