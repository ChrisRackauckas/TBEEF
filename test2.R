args<-commandArgs(TRUE)
print(args[1])
misc = args[1]
exists(misc)
print(misc)
is.na(misc)