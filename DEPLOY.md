# PaperFives

Copyright &copy; Fives 2023

---

# Briefing on Deployment

To run the project, run the following commands in project directory, with `paper` env activated.

```bash
./django serv # 1
./celery      # 2
redis-server  # 3
```

You should run #1 and #2 on different sessions. #3 will run background.
