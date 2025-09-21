SET SQL_SAFE_UPDATES = 0;

DELETE FROM u430613007_StudySpot.availabilities
WHERE end_time >= start_time
  AND TIME_TO_SEC(TIMEDIFF(end_time, start_time)) <= 600;

SET SQL_SAFE_UPDATES = 1;