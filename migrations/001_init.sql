-- Database Iteration 1
-- PostgreSQL syntax
-- Tables: user, vault, login_log

CREATE TABLE "user" (
  "id" integer PRIMARY KEY,
  "email" varchar,
  "password" text,
  "created_at" timestamp
);

CREATE TABLE "vault" (
  "id" integer PRIMARY KEY,
  "user_id" integer,
  "password" varchar,
  "passphrase" text,
  "created_at" timestamptz,
  "last_accessed_at" timestamptz,
  "metadata" jsonb
);

CREATE TABLE "login_log" (
  "id" integer PRIMARY KEY,
  "user_id" integer,
  "created_at" timestamptz
);

ALTER TABLE "vault" ADD FOREIGN KEY ("user_id") REFERENCES "user" ("id");

ALTER TABLE "login_log" ADD FOREIGN KEY ("user_id") REFERENCES "user" ("id");
