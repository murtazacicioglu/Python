#!/usr/bin/env python3
#
#       Ferit Yiğit BALABAN <fybalaban@fybx.dev>
#
#       expressions.py
#       proje boyunca çeşitli yerlerde kullanılan tüm reg. expresionlar


exp_regaddr_rv32i = "^x(0|[1-2][0-9]|3[0-1])$"
exp_preproc_space = "[\t ]+"
exp_preproc_comment = "\s*;.*"
exp_preproc_newline = "^(?:[\t ]*(?:\r?\n|\r))+"
