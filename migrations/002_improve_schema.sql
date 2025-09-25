-- Fix schema types and constraints
-- Create tables with proper types

-- Drop existing tables
DROP TABLE IF EXISTS "login_log";
DROP TABLE IF EXISTS "vault";
DROP TABLE IF EXISTS "user";

-- Create user table with UUID
CREATE TABLE "user" (
  "id" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  "email" VARCHAR(255) UNIQUE NOT NULL,
  "password" VARCHAR(255) NOT NULL,
  "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create vault table
CREATE TABLE "vault" (
  "id" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  "user_id" UUID NOT NULL REFERENCES "user"("id") ON DELETE CASCADE,
  "password" VARCHAR(255) NOT NULL,
  "passphrase" VARCHAR(255) NOT NULL,
  "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  "last_accessed_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create login_log table
CREATE TABLE "login_log" (
  "id" SERIAL PRIMARY KEY,
  "user_id" UUID NOT NULL REFERENCES "user"("id") ON DELETE CASCADE,
  "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
