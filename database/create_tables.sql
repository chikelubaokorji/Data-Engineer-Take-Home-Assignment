CREATE TABLE IF NOT EXISTS "Position" (
  "position_id" varchar(50) PRIMARY KEY,
  "position_title" varchar(100) NOT NULL,
  "position_uri" varchar(200) UNIQUE,
  "timestamp" timestamp NOT NULL
);

CREATE TABLE IF NOT EXISTS "PositionLocation" (
  "location_name" varchar(100) NOT NULL,
  "country_code" char(15) NOT NULL,
  "country_subdivision_code" varchar(50) NOT NULL,
  "city_name" varchar(100) NOT NULL,
  "longitude" float NOT NULL,
  "latitude" float NOT NULL,
  "position_id" varchar(50)
);

CREATE TABLE IF NOT EXISTS "PositionRemuneration" (
  "minimum_range" varchar(10) NOT NULL,
  "maximum_range" varchar(10) NOT NULL,
  "rate_interval_code" varchar(5) NOT NULL,
  "description" varchar(20) NOT NULL,
  "position_id" varchar(50)
);

ALTER TABLE "PositionLocation" ADD FOREIGN KEY ("position_id") REFERENCES "Position" ("position_id");

ALTER TABLE "PositionRemuneration" ADD FOREIGN KEY ("position_id") REFERENCES "Position" ("position_id");