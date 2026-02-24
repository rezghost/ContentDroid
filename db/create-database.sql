CREATE EXTENSION IF NOT EXISTS pgcrypto;

DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'video_status') THEN
    CREATE TYPE video_status AS ENUM (
      'PENDING',
      'PROCESSING',
      'COMPLETE',
      'FAILED',
      'CANCELED'
    );
  END IF;
END
$$;

CREATE TABLE IF NOT EXISTS videos (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

  storage_key TEXT,
  file_name TEXT,
  file_size_bytes BIGINT CHECK (file_size_bytes >= 0),
  mime_type TEXT DEFAULT 'video/mp4',

  status video_status NOT NULL DEFAULT 'PENDING',
  progress SMALLINT CHECK (progress BETWEEN 0 AND 100),

  error_code TEXT,
  error_message TEXT,

  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  started_at TIMESTAMPTZ,
  completed_at TIMESTAMPTZ,
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
