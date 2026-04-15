### Example to prevent Claude code read secret file

This would block access to the `.env` and `.data_new` files
```json
{
  "permissions": {
    "allow": [],
    "deny": [
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(**/.env)",
      "Bash(cat *.env*)",
      "Bash(grep *.env*)",
      "Bash(head *.env*)",
      "Bash(tail *.env*)",
      "Bash(less *.env*)",
      "Bash(more *.env*)",
      "Read(./.data_new)",
      "Read(./.data_new.*)",
      "Read(**/.data_new)",
      "Bash(cat *.data_new*)",
      "Bash(grep *.data_new*)",
      "Bash(head *.data_new*)",
      "Bash(tail *.data_new*)",
      "Bash(less *.data_new*)",
      "Bash(more *.data_new*)"
    ]
  }
}
```
