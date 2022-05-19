drop table audios;
create table audios (
  audio_id SERIAL PRIMARY KEY,
  person_id text,
  timecreate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  filename text,
  data bytea,
  description text,
  search tsvector,
  publicity INT NOT NULL DEFAULT 0,
  likes INT NOT NULL DEFAULT 0
);
