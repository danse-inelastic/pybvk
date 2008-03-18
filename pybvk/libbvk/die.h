#ifndef DIE_H
#define DIE_H

#include <stdio.h>
#include <stdlib.h>

#define DIE(c,m) if(c) { perror(m); abort(); }

#endif // DIE_H
