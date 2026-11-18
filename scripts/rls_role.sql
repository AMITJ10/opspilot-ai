DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_roles
        WHERE rolname = 'opspilot_app'
    ) THEN
        CREATE ROLE opspilot_app LOGIN PASSWORD 'replace_local_app_password';
    END IF;
END
$$;

GRANT CONNECT ON DATABASE opspilot_db TO opspilot_app;
GRANT USAGE ON SCHEMA public TO opspilot_app;
GRANT SELECT, INSERT, UPDATE, DELETE
ON business_orders TO opspilot_app;
GRANT USAGE, SELECT ON ALL SEQUENCES
IN SCHEMA public TO opspilot_app;
