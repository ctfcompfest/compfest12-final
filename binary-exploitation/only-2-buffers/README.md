# Only 2 buffers

by Zafirr 

---

## Flag

```
COMPFEST12{I_wanted_to_name_this_ROP_King_but_that_kind_of_name_is_overused_already_cc102f}
```

## Description
I'm nice so I'll give you 2 buffers, only 2 buffers. Btw, you MUST get RCE!

## Attachment

* share/
* Dockerfile
* docker-compose
* xinetd

Ini semua dizip. Upload ke google docs dan CTFd.

## Deployment
How to compile:

`gcc -o only-2-buffers -fno-stack-protector -fno-builtin-printf -no-pie only-2-buffers.c`<br>

Workdir di /home/compfest12

Jalanin:<br>
`./only-2-buffers`

Gunakan libc 2.31. Alias Ubuntu 20.04.

## Note
* Penting! Jangan compile ulang di dockerfile, ntar bisa rusak exploit. Pake yang udah dicompile aja.
* Penting! Port di docker-compose belum pasti. Jangan lupa check ulang