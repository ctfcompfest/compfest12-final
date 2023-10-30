# Secret Sharing v2.32

by Zafirr 

---

## Flag

```
COMPFEST12{New_Fastbin_Protection_POOOOOOOG_e34f53}
```

## Description
Share you secrets, now with glibc 2.32!


## Attachment

* share/
* Dockerfile
* docker-compose
* nsjail (kalo pake)

Ini semua dizip. Upload ke google docs dan CTFd.

## Deployment
How to compile:

`gcc secrets.c -o secrets -Wl,--rpath=. -Wl,--dynamic-linker=ld-2.32.so -O2 -D\_FORTIFY\_SOURCE=2 -fstack-protector-all -Wl,-z,now,-z,relro -fPIE -s`<br>

Gausah compile ulang di docker, takut beda gcc

Workdir di /home/compfest12

Jalanin:<br>
`./secrets`

Gunakan libc 2.32. Filenya sudah ada di repo

## Note
* Penting! Gunakan ubuntu 20.04, tapi libcnya yang ada di repo.