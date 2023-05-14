# PaperFives

---

# 1. Introduction

BUAA 2023 Software Engineering Project.

---

# 2. Tech

Django + uWSGI + NginX

---

# 3. Git Guide

To make commit more consistent, you **MUST** follow the commit convention. There should better be fewer change in one commit.

Generally, commit should be lower-case, and not final period punctuation. 

## 3.1 feat

To introduce a new feature.

```
feat: add User model
```

## 3.2 update

Not to introduce a new feature, but only made updates to an old one.

```
update: add extra-check for username
```

This can also be used when new files are added or removed. The 'add' or 'remove' action must be included.

```
update: add website favicon
update: remove register.py
```

## 3.3 fix

Indicate a bug is fixed.

```
fix: invalid login password ignored
```

## 3.4 refactor

Indicate that changes are made, but no affect to the function.

```
refactor: divide views.py to multiple files
```

## 3.5 trivial

Indicate this is a trivial change. Such commit should not include any change to the code.

```
trivial: correct spelling error
```
