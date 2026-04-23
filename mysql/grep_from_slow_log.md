# Common grep
- Need to know time before grep: `2026-04-22T18:50:00Z`. Z stands for Zulu time = UCT

### Grep with specific time range and query time > 2s
```bash
awk '
BEGIN { RS="\n# Time: "; ORS="" }
NR > 1 {
    ts = substr($0, 1, 19)
    if (ts >= "2026-04-22T18:50:00" && ts <= "2026-04-22T19:05:59") {
        if (match($0, /Query_time: [0-9]+\.[0-9]+/)) {
            qt = substr($0, RSTART+12, RLENGTH-12) + 0
            if (qt >= 2000) print "# Time: " $0 "\n"
        }
    }
}' slow-queries.log-20260217 > /tmp/slow_1.txt
```

### Find query with time range without query time.
```bash
awk '
BEGIN { RS="\n# Time: "; ORS="" }
NR > 1 {
    ts = substr($0, 1, 19)
    if (ts >= "2026-04-22T18:50:00" && ts <= "2026-04-22T19:05:59") {
        print "# Time: " $0 "\n"
    }
}' slow-queries.log-20260217 > /tmp/slow_window.log
```

### Double check 
```bash
# Regex
grep -c "^# Time: 2026-04-22T18:[0-2][0-9]" slow-queries.log-20260217
# More regex
grep -cE "^# Time: 2026-04-22T(18:5[0-9]|19:0[0-5])" slow-queries.log-20260217
```