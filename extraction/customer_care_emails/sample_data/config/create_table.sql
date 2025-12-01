CREATE TABLE IF NOT EXISTS public.customer_care_emails (
  subject TEXT NULL,
  sender TEXT NULL,
  receiver TEXT NULL,
  timestamp TIMESTAMP NULL,
  message_body TEXT NULL,
  thread_id TEXT NULL,
  email_types TEXT NULL,
  email_status TEXT NULL,
  email_criticality TEXT NULL,
  product_types TEXT NULL,
  agent_effectivity TEXT NULL,
  agent_efficiency TEXT NULL,
  customer_satisfaction FLOAT NULL
);
