# PaperFives

Copyright &copy; Fives 2023

---

# 1. Introduction

## 1.1 Purpose

BUAA 2023 Software Engineering Project.

## 1.2 Tech

Django + uWSGI + NginX

---

# 2. Git Guide

## 2.1 Branch Description

### 2.1.1 Branch List

There are four types of branch.

> `master`: Current stable version of the project.
>
> `release`: Next version in development.
>
> `dev`: Workspace for the next version.
>
> `{name}`: Each developer has his/her own branch.

### 2.1.2 Push Order

1. Developers should be on his/her own branch for daily development. You should remember to **pull** from `dev` regularly.

2. Once a change is done, **push** from `{name}` to `dev` branch.

3. When `dev` branch passed test, the **leader** of the team should **push** it to `release` branch.

4. Finally, when `release` branch is ready to go, the **leader** should then **push** it to `master` branch.

> All push and pull should follow the convention mentioned in the following section.

## 2.2 Commit Convention

To make commit more consistent, you **MUST** follow the commit convention. There should better be fewer changes in one commit.

> 'Fewer' doesn't mean fewer lines of code, but fewer functions.

Generally, commit should be lower-case, and no final period punctuation. 

### 2.2.1 `feat`

To introduce a new feature.

```
feat: add User model
```

### 2.2.2 `update`

Not to introduce a new feature, but only made updates to an old one.

```
update: add extra-check for username
```

This can also be used when new files are added or removed. The 'add' or 'remove' action must be included.

```
update: add website favicon
update: remove register.py
```

### 2.2.3 `fix`

It indicates a bug is fixed.

```
fix: invalid login password ignored
```

### 2.2.4 `refactor`

It indicates that changes are made, but no affect to the function.

```
refactor: divide views.py to multiple files
```

### 2.2.5 `trivial`

It indicates this is a trivial change. Such commit should not include any change to the code.

```
trivial: correct spelling error
```

---

# 3. Environment

## 3.1 Basic Environment

Environment is based on `Python 3.8` using `conda`.

> Environment should be created on Linux. Otherwise, fatal conflicts will occur between `mysqlclient` and `uwsgi`. For detailed information, please refer to this post:
> - [Configure Remote Interpreter in PyCharm](http://www.tonys-studio.top/2023/05/14/Configure-Remote-Interpreter-in-PyCharm/)

## 3.2 Troubleshoot

Some packages may not be easy to install, here are some hints.

### 3.2.1 `django-cors-headers`

```bash
conda install -c conda-forge django-cors-headers
```

### 3.2.2 `uwsgi`

```bash
conda install -c conda-forge uwsgi
```

---

# 4. Project Structure

## 4.1 Applications

There are three main applications corresponding to the three sub-systems. They are `users`, `papers` and `msgs`. In addition, for test purpose, there is a `zeta` application.

> We use `msgs` because there is a package `messages` in Django.

## 4.2 Shared Packages

This package contains some shared components of the whole project.

### 4.2.1 Utility Package

All utility scripts are placed under `/shared/utils/`. Each util Python Script deals with a specific function.

### 4.2.2 DTO package

DTO, a.k.a. Data Transfer Object, is used to carry data between frontend and backend. Things will be much easier if they can be mapped to actual Python object, instead of raw JSON data.
