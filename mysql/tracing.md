## Scenario: High threads running (>50)

```bash
SHOW GLOBAL STATUS LIKE 'Threads_running';

SELECT state, count(*) as count FROM information_schema.processlist WHERE command != "Sleep" GROUP BY state ORDER BY count DESC;
```

Example output: if `waiting for handler commit` > 40 --> it is fucking issue.
```bash
mysql> SELECT state, count(*) as count FROM information_schema.processlist WHERE command != "Sleep" GROUP BY state ORDER BY count DESC;
+-----------------------------------------------------------------+-------+
| state                                                           | count |
+-----------------------------------------------------------------+-------+
| executing                                                       |     3 |
| waiting for handler commit                                      |     3 |
| Waiting on empty queue                                          |     1 |
| Source has sent all binlog to replica; waiting for more updates |     1 |
+-----------------------------------------------------------------+-------+
4 rows in set (0.00 sec)

mysql> SHOW GLOBAL STATUS LIKE 'Threads_running';
+-----------------+-------+
| Variable_name   | Value |
+-----------------+-------+
| Threads_running | 4     |
+-----------------+-------+
1 row in set (0.00 sec)
```
