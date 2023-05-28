# PaperFives

Copyright &copy; Fives 2023

---

# Briefing on Deployment

Copyright &copy; Fives 2023

---

To run the project, run the following commands in project directory, with `paper` env activated.

## Step 1. Run Django Backend

Use `django` bash script to start Django backend.

```bash
./django serv
```

If it is your first time to run the project, you need to run `makemigrations` first, or simply add `-a` option.

```bash
./django mak
./django serv -a
```

## Step 2. Run Redis Service

Some services depends on Redis, so you have to run Redis service first. Make sure you've installed this feature.

```bash
redis-server
```

## Step 3. Run Celery Service

There are some asynchronous and periodic tasks in this project, and `celery` is used. You should launch them with your project. If you want more info logged, use info option.

```bash
./celery [info]       # asyc tasks
./celery beat [info]  # periodic tasks
```

You may need to restart them if you modified some of your configurations.

---

Except for `redis-server`, which will run background, the others will take up the session. So you may need `tmux`. 😋



