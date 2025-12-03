### Kill all connections sleep > 600 seconds
- Requirements: need config for `.my.cnf`
- Script
```bash
mysql -e "SELECT CONCAT('KILL ', id, ';') 
FROM information_schema.processlist 
WHERE Command = 'Sleep' 
AND Time > 600 
AND id != CONNECTION_ID();" \
| grep -v CONCAT | mysql
```

### Description:
- First: `mysql -e "SELECT CONCAT('KILL ', id, ';') ..."` Output will be printed...:
```
   CONCAT('KILL ', id, ';')
   KILL 123;
   KILL 456;
   KILL 789;
```

- Second: pipe through `grep -v CONCAT` to remove header
- Third: Execute the command `kill processId`

 
