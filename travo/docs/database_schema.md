| table_name             | column_name         | data_type                | is_nullable |
| ---------------------- | ------------------- | ------------------------ | ----------- |
| daily_summaries        | id                  | uuid                     | NO          |
| daily_summaries        | user_id             | uuid                     | NO          |
| daily_summaries        | date                | date                     | NO          |
| daily_summaries        | summary_text        | text                     | YES         |
| daily_summaries        | created_at          | timestamp with time zone | YES         |
| favorites              | id                  | uuid                     | NO          |
| favorites              | user_id             | uuid                     | NO          |
| favorites              | monument_id         | text                     | NO          |
| favorites              | created_at          | timestamp with time zone | YES         |
| label_corrections      | id                  | uuid                     | NO          |
| label_corrections      | user_id             | uuid                     | NO          |
| label_corrections      | photo_id            | uuid                     | NO          |
| label_corrections      | original_label      | text                     | YES         |
| label_corrections      | corrected_label     | text                     | NO          |
| label_corrections      | original_confidence | double precision         | YES         |
| label_corrections      | gps_lat             | double precision         | YES         |
| label_corrections      | gps_lon             | double precision         | YES         |
| label_corrections      | created_at          | timestamp with time zone | YES         |
| photo_processing_queue | id                  | uuid                     | NO          |
| photo_processing_queue | photo_id            | uuid                     | NO          |
| photo_processing_queue | status              | text                     | YES         |
| photo_processing_queue | attempts            | integer                  | YES         |
| photo_processing_queue | created_at          | timestamp with time zone | YES         |
| photo_processing_queue | updated_at          | timestamp with time zone | YES         |
| photos                 | id                  | uuid                     | NO          |
| photos                 | user_id             | uuid                     | NO          |
| photos                 | local_uri           | text                     | YES         |
| photos                 | remote_url          | text                     | YES         |
| photos                 | timestamp           | timestamp with time zone | YES         |
| photos                 | gps_lat             | double precision         | YES         |
| photos                 | gps_lon             | double precision         | YES         |
| photos                 | status              | text                     | YES         |
| photos                 | ai_label            | text                     | YES         |
| photos                 | confidence          | double precision         | YES         |
| photos                 | created_at          | timestamp with time zone | YES         |
| photos                 | is_shared           | boolean                  | YES         |
| profiles               | id                  | uuid                     | NO          |
| profiles               | username            | text                     | YES         |
| profiles               | full_name           | text                     | YES         |
| profiles               | avatar_url          | text                     | YES         |
| profiles               | created_at          | timestamp with time zone | YES         |
| profiles               | updated_at          | timestamp with time zone | YES         |
| trip_members           | id                  | uuid                     | NO          |
| trip_members           | trip_id             | uuid                     | NO          |
| trip_members           | user_id             | uuid                     | NO          |
| trip_members           | role                | text                     | YES         |
| trip_members           | invited_by          | uuid                     | YES         |
| trip_members           | joined_at           | timestamp with time zone | YES         |
| trip_photos            | id                  | uuid                     | NO          |
| trip_photos            | trip_place_id       | uuid                     | NO          |
| trip_photos            | photo_url           | text                     | NO          |
| trip_photos            | caption             | text                     | YES         |
| trip_photos            | created_at          | timestamp with time zone | YES         |
| trip_places            | id                  | uuid                     | NO          |
| trip_places            | trip_id             | uuid                     | NO          |
| trip_places            | place_name          | text                     | NO          |
| trip_places            | gps_lat             | double precision         | YES         |
| trip_places            | gps_lon             | double precision         | YES         |
| trip_places            | address             | text                     | YES         |
| trip_places            | created_at          | timestamp with time zone | YES         |
| trip_places            | is_home_location    | boolean                  | YES         |
| trips                  | id                  | uuid                     | NO          |
| trips                  | user_id             | uuid                     | NO          |
| trips                  | title               | text                     | YES         |
| trips                  | start_time          | timestamp with time zone | YES         |
| trips                  | end_time            | timestamp with time zone | YES         |
| trips                  | status              | text                     | YES         |
| trips                  | created_at          | timestamp with time zone | YES         |
| trips                  | auto_detected       | boolean                  | YES         |
| user_embeddings        | id                  | uuid                     | NO          |
| user_embeddings        | user_id             | uuid                     | NO          |
| user_embeddings        | location_name       | text                     | NO          |
| user_embeddings        | embedding           | USER-DEFINED             | YES         |
| user_embeddings        | frequency           | integer                  | YES         |
| user_embeddings        | last_visited        | timestamp with time zone | YES         |
| user_embeddings        | created_at          | timestamp with time zone | YES         |
| user_subscriptions     | id                  | uuid                     | NO          |
| user_subscriptions     | user_id             | uuid                     | NO          |
| user_subscriptions     | tier                | text                     | YES         |
| user_subscriptions     | status              | text                     | YES         |
| user_subscriptions     | started_at          | timestamp with time zone | YES         |
| user_subscriptions     | expires_at          | timestamp with time zone | YES         |
| user_subscriptions     | created_at          | timestamp with time zone | YES         |
| user_subscriptions     | updated_at          | timestamp with time zone | YES         |
-------------------------------------------------------------------------------------


| table_name             | column_name   | foreign_table_name | foreign_column_name |
| ---------------------- | ------------- | ------------------ | ------------------- |
| trip_places            | trip_id       | trips              | id                  |
| trip_photos            | trip_place_id | trip_places        | id                  |
| photo_processing_queue | photo_id      | photos             | id                  |
| trip_members           | trip_id       | trips              | id                  |
| label_corrections      | photo_id      | photos             | id                  |



in storage i have one bucket called trip_photos 