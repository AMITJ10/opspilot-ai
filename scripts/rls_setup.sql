BEGIN;

ALTER TABLE business_orders
    ENABLE ROW LEVEL SECURITY;

ALTER TABLE business_orders
    FORCE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS tenant_orders_policy
    ON business_orders;

CREATE POLICY tenant_orders_policy
ON business_orders
FOR ALL
TO opspilot_app
USING (
    tenant_id = NULLIF(
        current_setting('app.tenant_id', true), ''
    )::integer
)
WITH CHECK (
    tenant_id = NULLIF(
        current_setting('app.tenant_id', true), ''
    )::integer
);

COMMIT;
