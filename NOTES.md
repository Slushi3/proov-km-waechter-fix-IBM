# What I checked, and what the agent got wrong

The agent fixed the wear bug (`//` floor division made every car under the service
interval show 0% wear), but I found problems in how it handled the edge cases:
- Cars with no `last_service_km` now default to the odometer reading, which makes
  km-since-service 0. A car with an unknown reading is treated as "just serviced"
  and is never flagged. For a safety check I think unknown should be flagged or
  surfaced, not assumed fine.
- Its audit flagged the shared module-level `LOG_LINES` list as a test-isolation
  hazard, but the fix only changed `del LOG_LINES[:]` to `LOG_LINES.clear()`. The
  global state is still there.
- It called `get_setting` a "dead wrapper" while also keeping it so callers don't
  break, which is contradictory. 
- It declared several functions "never called" without showing a search.

## What the agent got wrong
(Every agent gets something wrong on a job this size. What did you catch? How did you notice?)

## What I checked before I accepted its work
- - I ran the tests: 4/4 pass, including the almost-due-car and missing-reading cases.
- I ran `python verify.py`: 9/11 before this file, with the two remaining failures
  being `analyze.py` and `NOTES.md`, which were out of scope for that step.
- I grepped for `WARN_AT_PERCENT` and `SERVICE_INTERVAL_KM` in `km_wachter.py` and
  confirmed they are still 80 and 15000, and that `git diff` shows no change to them.
  Only write this if you ran it.
- I grepped for `chunk_list`, `is_due`, `parse_service_date` and `debug(` and found
  no callers before accepting the deletions. Only write this if you ran it.


## What the data actually said
km_since_service dominated: it was the strongest predictor of breakdown (r = +0.40),
followed by avg_daily_km (r = +0.25) and load_factor (r = +0.22). Total odometer
mileage (r = +0.002) and age (r = -0.001) were completely flat, so the intuition that
older, higher-mileage cars break down more is not supported by this data. The risk
score built from the three real signals put 8 of the top 10 cars in the broken-down
group and separated the groups by about 21 points on average (63.1 vs 41.6). That
result is in-sample, since the weights came from the same 120 cars, so it shows the
score ranks this fleet well, not that it would predict breakdowns on new cars.
