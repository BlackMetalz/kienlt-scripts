### Self Monitoring

This solution can monitor whether the agent push metric is dead or alive, which could be useful as well for monitoring the server up/down.
```
(
  count_over_time(cpu_usage_system{host=~"host-.*",cpu="cpu-total"}[2m])
)
or on(host)
(
  0 * count_over_time(cpu_usage_system{host=~"host-.*",cpu="cpu-total"}[1h])
)
```
